# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: embeddingservice.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x16\x65mbeddingservice.proto\x12\x10\x65mbeddingservice"\x96\x01\n\x10\x43hunk2VdbRequest\x12\x14\n\x0c\x63ontext_name\x18\x01 \x01(\t\x12\x12\n\ncontext_id\x18\x02 \x01(\t\x12\x12\n\nchunk_name\x18\x03 \x01(\t\x12\x10\n\x08\x63hunk_id\x18\x04 \x01(\t\x12\x0c\n\x04text\x18\x05 \x01(\t\x12\x10\n\x08open_url\x18\x06 \x01(\t\x12\x12\n\ntable_name\x18\x07 \x01(\t"$\n\x11\x43hunk2VdbResponse\x12\x0f\n\x07reponse\x18\x01 \x01(\x08"$\n\x14TextEmbeddingRequest\x12\x0c\n\x04text\x18\x01 \x01(\t"U\n\x15TextEmbeddingResponse\x12\x0e\n\x06vector\x18\x01 \x03(\x02\x12,\n\x08metadata\x18\x02 \x01(\x0b\x32\x1a.embeddingservice.Metadata"&\n\x08Metadata\x12\x0c\n\x04\x64im1\x18\x01 \x01(\x05\x12\x0c\n\x04\x64im2\x18\x02 \x01(\x05\x32\xca\x01\n\x10\x45mbeddingService\x12T\n\tChunk2Vdb\x12".embeddingservice.Chunk2VdbRequest\x1a#.embeddingservice.Chunk2VdbResponse\x12`\n\rTextEmbedding\x12&.embeddingservice.TextEmbeddingRequest\x1a\'.embeddingservice.TextEmbeddingResponseb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "embeddingservice_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_CHUNK2VDBREQUEST"]._serialized_start = 45
    _globals["_CHUNK2VDBREQUEST"]._serialized_end = 195
    _globals["_CHUNK2VDBRESPONSE"]._serialized_start = 197
    _globals["_CHUNK2VDBRESPONSE"]._serialized_end = 233
    _globals["_TEXTEMBEDDINGREQUEST"]._serialized_start = 235
    _globals["_TEXTEMBEDDINGREQUEST"]._serialized_end = 271
    _globals["_TEXTEMBEDDINGRESPONSE"]._serialized_start = 273
    _globals["_TEXTEMBEDDINGRESPONSE"]._serialized_end = 358
    _globals["_METADATA"]._serialized_start = 360
    _globals["_METADATA"]._serialized_end = 398
    _globals["_EMBEDDINGSERVICE"]._serialized_start = 401
    _globals["_EMBEDDINGSERVICE"]._serialized_end = 603
# @@protoc_insertion_point(module_scope)
