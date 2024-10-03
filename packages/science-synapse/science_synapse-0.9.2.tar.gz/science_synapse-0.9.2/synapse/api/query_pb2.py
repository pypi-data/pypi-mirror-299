"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_sym_db = _symbol_database.Default()
from ..api import channel_pb2 as api_dot_channel__pb2
from ..api import status_pb2 as api_dot_status__pb2
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fapi/query.proto\x12\x07synapse\x1a\x11api/channel.proto\x1a\x10api/status.proto"G\n\x0bSampleQuery\x12"\n\x08channels\x18\x01 \x03(\x0b2\x10.synapse.Channel\x12\x14\n\x0csample_count\x18\x02 \x01(\r"\'\n\x0eImpedanceQuery\x12\x15\n\relectrode_ids\x18\x01 \x03(\r"N\n\x14ImpedanceMeasurement\x12\x14\n\x0celectrode_id\x18\x01 \x01(\r\x12\x11\n\tmagnitude\x18\x02 \x01(\x02\x12\r\n\x05phase\x18\x03 \x01(\x02"H\n\x11ImpedanceResponse\x123\n\x0cmeasurements\x18\x01 \x03(\x0b2\x1d.synapse.ImpedanceMeasurement"\xe3\x01\n\x0cQueryRequest\x123\n\nquery_type\x18\x01 \x01(\x0e2\x1f.synapse.QueryRequest.QueryType\x122\n\x0fimpedance_query\x18\x02 \x01(\x0b2\x17.synapse.ImpedanceQueryH\x00\x12,\n\x0csample_query\x18\x03 \x01(\x0b2\x14.synapse.SampleQueryH\x00"3\n\tQueryType\x12\t\n\x05kNone\x10\x00\x12\x0e\n\nkImpedance\x10\x01\x12\x0b\n\x07kSample\x10\x02B\x07\n\x05query"\x84\x01\n\rQueryResponse\x12\x1f\n\x06status\x18\x01 \x01(\x0b2\x0f.synapse.Status\x12\x0c\n\x04data\x18\x02 \x03(\r\x128\n\x12impedance_response\x18\x03 \x01(\x0b2\x1a.synapse.ImpedanceResponseH\x00B\n\n\x08responseb\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api.query_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    DESCRIPTOR._options = None
    _globals['_SAMPLEQUERY']._serialized_start = 65
    _globals['_SAMPLEQUERY']._serialized_end = 136
    _globals['_IMPEDANCEQUERY']._serialized_start = 138
    _globals['_IMPEDANCEQUERY']._serialized_end = 177
    _globals['_IMPEDANCEMEASUREMENT']._serialized_start = 179
    _globals['_IMPEDANCEMEASUREMENT']._serialized_end = 257
    _globals['_IMPEDANCERESPONSE']._serialized_start = 259
    _globals['_IMPEDANCERESPONSE']._serialized_end = 331
    _globals['_QUERYREQUEST']._serialized_start = 334
    _globals['_QUERYREQUEST']._serialized_end = 561
    _globals['_QUERYREQUEST_QUERYTYPE']._serialized_start = 501
    _globals['_QUERYREQUEST_QUERYTYPE']._serialized_end = 552
    _globals['_QUERYRESPONSE']._serialized_start = 564
    _globals['_QUERYRESPONSE']._serialized_end = 696