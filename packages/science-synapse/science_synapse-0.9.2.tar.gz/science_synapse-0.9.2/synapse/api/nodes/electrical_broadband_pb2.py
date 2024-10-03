"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...api import channel_pb2 as api_dot_channel__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$api/nodes/electrical_broadband.proto\x12\x07synapse\x1a\x11api/channel.proto"\xbb\x01\n\x19ElectricalBroadbandConfig\x12\x15\n\rperipheral_id\x18\x01 \x01(\r\x12"\n\x08channels\x18\x02 \x03(\x0b2\x10.synapse.Channel\x12\x11\n\tbit_width\x18\x03 \x01(\r\x12\x13\n\x0bsample_rate\x18\x04 \x01(\r\x12\x0c\n\x04gain\x18\x05 \x01(\x02\x12\x15\n\rlow_cutoff_hz\x18\x06 \x01(\x02\x12\x16\n\x0ehigh_cutoff_hz\x18\x07 \x01(\x02b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.nodes.electrical_broadband_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_ELECTRICALBROADBANDCONFIG']._serialized_start = 69
    _globals['_ELECTRICALBROADBANDCONFIG']._serialized_end = 256