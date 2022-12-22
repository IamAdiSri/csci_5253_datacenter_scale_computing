from concurrent import futures
from PIL import Image
import io
import json
import base64

import grpc
import lab6_pb2
import lab6_pb2_grpc

class lab6Servicer(lab6_pb2_grpc.lab6Servicer):
    def doAdd(self, request, context):
        return lab6_pb2.addReply(sum=request.a+request.b)

    def doRawImage(self, request, context):
        data = request.img
        # convert the data to a PIL image type so we can extract dimensions
        try:
            ioBuffer = io.BytesIO(data)
            img = Image.open(ioBuffer)
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except:
            return lab6_pb2.imageReply(width=0, height=0)

    def doDotProduct(self, request, context):
        if len(request.a) != len(request.b):
            raise RuntimeError('Input vectors have different lengths!')
        dp = sum([request.a[i]*request.b[i] for i in range(len(request.a))])
        return lab6_pb2.dotProductReply(dotproduct=dp)

    def doJsonImage(self, request, context):
        data = request.img
        query = json.loads(data)
        jpg = base64.b64decode(query['img'])
        # convert the data to a PIL image type so we can extract dimensions
        try:
            ioBuffer = io.BytesIO(jpg)
            img = Image.open(ioBuffer)
            return lab6_pb2.imageReply(width=img.size[0], height=img.size[1])
        except:
            return lab6_pb2.imageReply(width=0, height=0)
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    lab6_pb2_grpc.add_lab6Servicer_to_server(lab6Servicer(), server)
    server.add_insecure_port('0.0.0.0:5001')
    server.start()
    server.wait_for_termination()
    
if __name__ == '__main__':
    serve()
