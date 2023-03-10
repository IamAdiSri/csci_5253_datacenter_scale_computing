# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import lab6_pb2 as lab6__pb2


class lab6Stub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.doAdd = channel.unary_unary(
                '/lab6/doAdd',
                request_serializer=lab6__pb2.addMsg.SerializeToString,
                response_deserializer=lab6__pb2.addReply.FromString,
                )
        self.doRawImage = channel.unary_unary(
                '/lab6/doRawImage',
                request_serializer=lab6__pb2.rawImageMsg.SerializeToString,
                response_deserializer=lab6__pb2.imageReply.FromString,
                )
        self.doDotProduct = channel.unary_unary(
                '/lab6/doDotProduct',
                request_serializer=lab6__pb2.dotProductMsg.SerializeToString,
                response_deserializer=lab6__pb2.dotProductReply.FromString,
                )
        self.doJsonImage = channel.unary_unary(
                '/lab6/doJsonImage',
                request_serializer=lab6__pb2.jsonImageMsg.SerializeToString,
                response_deserializer=lab6__pb2.imageReply.FromString,
                )


class lab6Servicer(object):
    """Missing associated documentation comment in .proto file."""

    def doAdd(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doRawImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doDotProduct(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def doJsonImage(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_lab6Servicer_to_server(servicer, server):
    rpc_method_handlers = {
            'doAdd': grpc.unary_unary_rpc_method_handler(
                    servicer.doAdd,
                    request_deserializer=lab6__pb2.addMsg.FromString,
                    response_serializer=lab6__pb2.addReply.SerializeToString,
            ),
            'doRawImage': grpc.unary_unary_rpc_method_handler(
                    servicer.doRawImage,
                    request_deserializer=lab6__pb2.rawImageMsg.FromString,
                    response_serializer=lab6__pb2.imageReply.SerializeToString,
            ),
            'doDotProduct': grpc.unary_unary_rpc_method_handler(
                    servicer.doDotProduct,
                    request_deserializer=lab6__pb2.dotProductMsg.FromString,
                    response_serializer=lab6__pb2.dotProductReply.SerializeToString,
            ),
            'doJsonImage': grpc.unary_unary_rpc_method_handler(
                    servicer.doJsonImage,
                    request_deserializer=lab6__pb2.jsonImageMsg.FromString,
                    response_serializer=lab6__pb2.imageReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'lab6', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class lab6(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def doAdd(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lab6/doAdd',
            lab6__pb2.addMsg.SerializeToString,
            lab6__pb2.addReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def doRawImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lab6/doRawImage',
            lab6__pb2.rawImageMsg.SerializeToString,
            lab6__pb2.imageReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def doDotProduct(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lab6/doDotProduct',
            lab6__pb2.dotProductMsg.SerializeToString,
            lab6__pb2.dotProductReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def doJsonImage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/lab6/doJsonImage',
            lab6__pb2.jsonImageMsg.SerializeToString,
            lab6__pb2.imageReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
