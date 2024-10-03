"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ...api import channel_pb2 as api_dot_channel__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fapi/nodes/electrical_stim.proto\x12\x07synapse\x1a\x11api/channel.proto"^\n\x15ElectricalStimOptions\x12\x10\n\x08ch_count\x18\x01 \x01(\r\x12\x13\n\x0bsample_rate\x18\x02 \x03(\r\x12\x11\n\tbit_width\x18\x03 \x03(\r\x12\x0b\n\x03lsb\x18\x04 \x03(\r"\x86\x01\n\x14ElectricalStimConfig\x12\x15\n\rperipheral_id\x18\x01 \x01(\r\x12"\n\x08channels\x18\x02 \x03(\x0b2\x10.synapse.Channel\x12\x13\n\x0bsample_rate\x18\x03 \x01(\r\x12\x11\n\tbit_width\x18\x04 \x01(\r\x12\x0b\n\x03lsb\x18\x05 \x01(\rb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.nodes.electrical_stim_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_ELECTRICALSTIMOPTIONS']._serialized_start = 63
    _globals['_ELECTRICALSTIMOPTIONS']._serialized_end = 157
    _globals['_ELECTRICALSTIMCONFIG']._serialized_start = 160
    _globals['_ELECTRICALSTIMCONFIG']._serialized_end = 294