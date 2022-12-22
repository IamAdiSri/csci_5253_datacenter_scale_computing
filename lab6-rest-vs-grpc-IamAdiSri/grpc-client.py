import sys
import random
import time
import base64
import json

import grpc
import lab6_pb2
import lab6_pb2_grpc

def getAddMsg():
    return lab6_pb2.addMsg(a=5, b=10)

def getDotProductMsg():
    v1 = [random.random() for _ in range(100)]
    v2 = [random.random() for _ in range(100)]
    return lab6_pb2.dotProductMsg(a=v1,b=v2)

def getRawImageMsg():
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    return lab6_pb2.rawImageMsg(img=img)

def getJsonImageMsg():
    img = open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb').read()
    img = base64.b64encode(img).decode('ascii')
    data = {'img': img}
    return lab6_pb2.jsonImageMsg(img=json.dumps(data))
    
def run(host, cmd, reps, debug=False):
    with grpc.insecure_channel(f'{host}:5001') as channel:
        stub = lab6_pb2_grpc.lab6Stub(channel)
        
        result = None
        if cmd == 'rawImage':
            start = time.perf_counter()
            for x in range(reps):
                result = stub.doRawImage(getRawImageMsg())
                if result and debug:
                    print(result)
            delta = ((time.perf_counter() - start)/reps)*1000
            print("Took", delta, "ms per operation")
            
        elif cmd == 'add':
            start = time.perf_counter()
            for x in range(reps):
                result = stub.doAdd(getAddMsg())
                if result and debug:
                    print(result)
            delta = ((time.perf_counter() - start)/reps)*1000
            print("Took", delta, "ms per operation")
            
        elif cmd == 'jsonImage':
            start = time.perf_counter()
            for x in range(reps):
                result = stub.doJsonImage(getJsonImageMsg())
                if result and debug:
                    print(result)
            delta = ((time.perf_counter() - start)/reps)*1000
            print("Took", delta, "ms per operation")
            
        elif cmd == 'dotProduct':
            start = time.perf_counter()
            for x in range(reps):
                result = stub.doDotProduct(getDotProductMsg())
                if result and debug:
                    print(result)
            delta = ((time.perf_counter() - start)/reps)*1000
            print("Took", delta, "ms per operation")
            
        else:
            print("Unknown option", cmd)
        
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <server ip> <cmd> <reps>")
        print(f"where <cmd> is one of add, rawImage, sum or jsonImage")
        print(f"and <reps> is the integer number of repititions for measurement")

    host = sys.argv[1]
    cmd = sys.argv[2]
    reps = int(sys.argv[3])

    addr = f"http://{host}:5001"
    print(f"Running {reps} reps against {addr}")
    
    run(host, cmd, reps)