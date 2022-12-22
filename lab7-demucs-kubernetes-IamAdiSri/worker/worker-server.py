import redis
from minio import Minio
from minio.error import S3Error
import os
import io
import requests
import json

REDIS_HOST = os.getenv('REDIS_HOST') if os.getenv('REDIS_HOST')!=None else "localhost"
REDIS_PORT = os.getenv('REDIS_PORT') if os.getenv('REDIS_PORT')!=None else "6379"
MINIO_HOST = os.getenv('MINIO_HOST') if os.getenv('MINIO_HOST')!=None else "0.0.0.0"
MINIO_PORT = os.getenv('MINIO_PORT') if os.getenv('MINIO_PORT')!=None else "9000"
MINIO_USER = os.getenv('MINIO_USER') if os.getenv('MINIO_USER')!=None else "rootuser"
MINIO_PASSWD = os.getenv('MINIO_PASSWD') if os.getenv('MINIO_PASSWD')!=None else "rootpass123"
GET_HOSTS_FROM = os.getenv('GET_HOSTS_FROM') if os.getenv('GET_HOSTS_FROM')!=None else "dns"

redis_conn = redis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')
minio_conn = Minio(
    endpoint=f"{MINIO_HOST}:{MINIO_PORT}",
    access_key=f"{MINIO_USER}",
    secret_key=f"{MINIO_PASSWD}",
    secure=False
)

def run_worker():
    while True:
        # get next song from queue
        hash = redis_conn.blpop('song_queue', timeout=None)[1].decode()
        # get callback url for song hash
        callback_url = redis_conn.get(f'callback_{hash}')

        print(f'Received song {hash}! Processing...')

        if redis_conn.sismember('song_list', hash):
            print('Song has already been processed!')
            continue

        data = None
        try:
            # fetch song from minio bucket
            object = minio_conn.get_object(bucket_name='songbank', object_name=f'{hash}/{hash}.mp3')
            data = object.data
            object.close()
            object.release_conn()
        except S3Error:
            # if song is not found
            print('ERROR: Song not found!')
            continue

        path = f"/tmp/{hash}"
        if not os.path.exists(path):
            # Create a new directories
            os.makedirs(path)

            # save song as file
            with open(os.path.join(path, f"{hash}.mp3"), 'wb') as f:
                f.write(data)

            model = "mdx_extra_q"

            # run demucs on song
            os.system(f"demucs -n {model} {os.path.join(path, f'{hash}.mp3')} -o {os.path.join(path)}")

            # upload stems to minio
            for file in os.listdir(os.path.join(path, model, hash)):
                with open(os.path.join(path, model, hash, file), 'rb') as f:
                    wav = f.read()
                    minio_conn.put_object(
                        bucket_name="songbank",
                        object_name=f"{hash}/separated/{file}",
                        data=io.BytesIO(wav),
                        length=len(wav)
                    )
            print(f"Successfully uploaded stems for {hash}.mp3 to bucket 'songbank'!")

            # delete local files
            os.system(f"rm -rf {path}")

            # add song to list of processed songs
            redis_conn.sadd('song_list', hash)
            # send callback
            response = requests.post(
                callback_url, 
                json=json.dumps({'mp3': hash, 'data': "Song has finished processing!"}), 
                headers={'Content-type': 'application/json'}
            )

if __name__=='__main__':
    run_worker()