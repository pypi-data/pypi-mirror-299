"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...api import datatype_pb2 as api_dot_datatype__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x19api/nodes/stream_in.proto\x12\x07synapse\x1a\x12api/datatype.proto"6\n\x0eStreamInConfig\x12$\n\tdata_type\x18\x01 \x01(\x0e2\x11.synapse.DataTypeb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.nodes.stream_in_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_STREAMINCONFIG']._serialized_start = 58
    _globals['_STREAMINCONFIG']._serialized_end = 112