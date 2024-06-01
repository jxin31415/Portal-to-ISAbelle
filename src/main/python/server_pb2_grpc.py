# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import server_pb2 as server__pb2


class ServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InitialiseIsabelle = channel.unary_unary(
                '/server.Server/InitialiseIsabelle',
                request_serializer=server__pb2.IsaPath.SerializeToString,
                response_deserializer=server__pb2.IsaMessage.FromString,
                )
        self.IsabelleContext = channel.unary_unary(
                '/server.Server/IsabelleContext',
                request_serializer=server__pb2.IsaContext.SerializeToString,
                response_deserializer=server__pb2.IsaMessage.FromString,
                )
        self.IsabelleWorkingDirectory = channel.unary_unary(
                '/server.Server/IsabelleWorkingDirectory',
                request_serializer=server__pb2.IsaPath.SerializeToString,
                response_deserializer=server__pb2.IsaMessage.FromString,
                )
        self.IsabelleCommand = channel.unary_unary(
                '/server.Server/IsabelleCommand',
                request_serializer=server__pb2.IsaCommand.SerializeToString,
                response_deserializer=server__pb2.IsaState.FromString,
                )
        self.IsabelleSetSearchWidth = channel.unary_unary(
                '/server.Server/IsabelleSetSearchWidth',
                request_serializer=server__pb2.IsaSearchWidth.SerializeToString,
                response_deserializer=server__pb2.IsaMessage.FromString,
                )
        self.IsabelleSearchIndexCommand = channel.unary_unary(
                '/server.Server/IsabelleSearchIndexCommand',
                request_serializer=server__pb2.IsaSearchIndexCommand.SerializeToString,
                response_deserializer=server__pb2.IsaState.FromString,
                )


class ServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InitialiseIsabelle(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsabelleContext(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsabelleWorkingDirectory(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsabelleCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsabelleSetSearchWidth(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def IsabelleSearchIndexCommand(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InitialiseIsabelle': grpc.unary_unary_rpc_method_handler(
                    servicer.InitialiseIsabelle,
                    request_deserializer=server__pb2.IsaPath.FromString,
                    response_serializer=server__pb2.IsaMessage.SerializeToString,
            ),
            'IsabelleContext': grpc.unary_unary_rpc_method_handler(
                    servicer.IsabelleContext,
                    request_deserializer=server__pb2.IsaContext.FromString,
                    response_serializer=server__pb2.IsaMessage.SerializeToString,
            ),
            'IsabelleWorkingDirectory': grpc.unary_unary_rpc_method_handler(
                    servicer.IsabelleWorkingDirectory,
                    request_deserializer=server__pb2.IsaPath.FromString,
                    response_serializer=server__pb2.IsaMessage.SerializeToString,
            ),
            'IsabelleCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.IsabelleCommand,
                    request_deserializer=server__pb2.IsaCommand.FromString,
                    response_serializer=server__pb2.IsaState.SerializeToString,
            ),
            'IsabelleSetSearchWidth': grpc.unary_unary_rpc_method_handler(
                    servicer.IsabelleSetSearchWidth,
                    request_deserializer=server__pb2.IsaSearchWidth.FromString,
                    response_serializer=server__pb2.IsaMessage.SerializeToString,
            ),
            'IsabelleSearchIndexCommand': grpc.unary_unary_rpc_method_handler(
                    servicer.IsabelleSearchIndexCommand,
                    request_deserializer=server__pb2.IsaSearchIndexCommand.FromString,
                    response_serializer=server__pb2.IsaState.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'server.Server', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Server(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InitialiseIsabelle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/server.Server/InitialiseIsabelle',
            server__pb2.IsaPath.SerializeToString,
            server__pb2.IsaMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsabelleContext(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/server.Server/IsabelleContext',
            server__pb2.IsaContext.SerializeToString,
            server__pb2.IsaMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsabelleWorkingDirectory(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/server.Server/IsabelleWorkingDirectory',
            server__pb2.IsaPath.SerializeToString,
            server__pb2.IsaMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsabelleCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/server.Server/IsabelleCommand',
            server__pb2.IsaCommand.SerializeToString,
            server__pb2.IsaState.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsabelleSetSearchWidth(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/server.Server/IsabelleSetSearchWidth',
            server__pb2.IsaSearchWidth.SerializeToString,
            server__pb2.IsaMessage.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def IsabelleSearchIndexCommand(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/server.Server/IsabelleSearchIndexCommand',
            server__pb2.IsaSearchIndexCommand.SerializeToString,
            server__pb2.IsaState.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
