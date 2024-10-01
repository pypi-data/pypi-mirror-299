#cython: language_level=3
include "utils.pxi"
from cpython.buffer cimport PyObject_GetBuffer, PyBuffer_Release, PyBUF_ANY_CONTIGUOUS, PyBUF_SIMPLE
import inspect
#import traceback

wire_types = {
    'int32': 0,
    'int64': 0,
    'sint32': 0,
    'sint64': 0,
    'uint32': 0,
    'uint64': 0,
    'bool': 0,
    'enum': 0,
    'fixed64': 1,
    'sfixed64': 1,
    'double': 1,
    'string': 2,
    'bytes': 2,
    'fixed32': 5,
    'sfixed32': 5,
    'float': 5,
}

default_objects = {
    'int32': 0,
    'int64': 0,
    'sint32': 0,
    'sint64': 0,
    'uint32': 0,
    'uint64': 0,
    'bool': False,
    'enum': 0,
    'fixed64': 0,
    'sfixed64': 0,
    'double': 0.0,
    'string': '',
    'bytes': b'',
    'fixed32': 0,
    'sfixed32': 0,
    'float': 0.0,
}

cdef class RepeatedContainer(list):
    cdef object klass

    def __init__(self, cls):
        self.klass = cls

    def add(self, **kwargs):
        obj = self.klass(**kwargs)
        self.append(obj)
        return obj

cdef class Field(object):

    cdef public str name
    cdef object type
    cdef public int index
    cdef public bint packed
    cdef public bint required
    cdef public bint repeated
    cdef object klass
    cdef object default

    cdef public unsigned char wire_type
    cdef Encoder encoder
    cdef Decoder decoder

    def __init__(self, type, index, required=True, repeated=False, packed=False, default=None):
        assert type in wire_types or isinstance(type, (str, unicode)) or issubclass(type, ProtoEntity), 'invalid type %s' % type

        self.type = type
        self.index = index
        self.required = required
        self.repeated = repeated
        self.packed = packed

        if inspect.isclass(self.type) and issubclass(self.type, ProtoEntity):
            self.klass = self.type
        elif self.type not in default_objects:
            # sub message specified as name
            self.klass = self.type
        else:
            self.klass = None

        self.default = default or default_objects.get(self.type)

        self.wire_type = self.get_wire_type()
        self.encoder = self.get_encoder()
        self.decoder = self.get_decoder()

        if self.packed:
            assert self.repeated, 'packed must be used with repeated'

    cdef resolve_klass(self):
        if self.klass and isinstance(self.klass, (str, unicode)):
            self.klass = get_proto(self.klass)

    def __get__(self, instance, type):
        if not instance:
            return self
        value = None

        if self.repeated:
            if self.klass:
                self.resolve_klass()
                value = RepeatedContainer(self.klass)
            else:
                value = []
            setattr(instance, self.name, value)
        elif self.klass:
            self.resolve_klass()
            value = self.klass()
            setattr(instance, self.name, value)
        else:
            value = self.default
        return value

    cdef unsigned char get_wire_type(self):
        if self.packed:
            return 2
        try:
            return wire_types[self.type]
        except KeyError:
            return 2

    cdef Encoder get_encoder(self):
        cdef Encoder e = get_encoder(self.type)
        if e == NULL:
            return encode_subobject
        return e

    cdef Decoder get_decoder(self):
        return get_decoder(self.type)

cdef dict _proto_classes = {}
cpdef get_proto(name):
    return _proto_classes[name]

def register_proto(name, cls):
    _proto_classes[name] = cls

class MetaProtoEntity(type):
    def __new__(cls, clsname, bases, attrs):
        if clsname == 'ProtoEntity':
            return super(MetaProtoEntity, cls).__new__(cls, clsname, bases, attrs)
        # _fields for encode
        # _fieldsmap for decode
        _fields = []
        _fieldsmap = {}
        _fieldsmap_by_name = {}
        cdef Field f
        for name, v in attrs.items():
            if name.startswith('__'):
                continue
            if not isinstance(v, Field):
                continue
            f = v
            f.name = name
            assert f.index not in _fieldsmap, 'duplicate field index %s' % f.index
            _fieldsmap[f.index] = f
            _fields.append(f)
            _fieldsmap_by_name[name] = f
        newcls = super(MetaProtoEntity, cls).__new__(cls, clsname, bases, attrs)
        _fields.sort(key=lambda f:f.index)
        newcls._fields = _fields
        newcls._fieldsmap = _fieldsmap
        newcls._fieldsmap_by_name = _fieldsmap_by_name
        register_proto(clsname, newcls)
        return newcls

class ProtoEntity(object, metaclass=MetaProtoEntity):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def SerializeToString(self):
        return encode_data(type(self), self.__dict__)

    def ParseFromString(self, s, int offset=0, int count=-1):
        cdef char *buff
        cdef char *start
        cdef char *end
        cdef Py_ssize_t size
        cdef Py_buffer buffer
        PyObject_GetBuffer(s, &buffer, PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)
        try:
            buff = <char *>buffer.buf
            size = buffer.len

            assert (size == 0 and offset == 0 and count <= 0) or offset < size, "Offset out of bound."
            assert offset + count < size, "Count out of bound."

            start = buff + offset
            if count < 0:
                end = buff + size
            else:
                end = start + count

            try:
                decode_object(self, &buff, end)
            except InternalDecodeError as e:
                #traceback.print_exc()
                raise DecodeError(e.args[0] - <uint64_t>start, e.args[1])
        finally:
            PyBuffer_Release(&buffer)

    def __unicode__(self):
        return str(self).decode('utf-8')

    def __str__(self):
        return str(self.todict())

    def todict(self):
        cdef Field f
        data = {}
        d = self.__dict__
        for f in self._fields:
            value = d.get(f.name)
            if value == None:
                continue
            if f.repeated:
                if len(value) < 1:
                    continue
                if isinstance(value[0], ProtoEntity):
                    data[f.name] = [v.todict() for v in value]
                else:
                    data[f.name] = value
            else:
                if isinstance(value, ProtoEntity):
                    data[f.name] = value.todict()
                else:
                    data[f.name] = value
        return data

def encode_data(cls, dict d):
    cdef bytearray buf = bytearray()
    cdef bytearray buf1
    cdef Field f
    for f in <list>cls._fields:
        value = d.get(f.name)
        if value is None:
            continue
        if f.packed:
            encode_type(buf, f.wire_type, f.index)
            buf1 = bytearray()
            for item in value:
                f.encoder(f, buf1, item)
            encode_bytes(f, buf, buf1)
        else:
            if f.repeated:
                for item in value:
                    encode_type(buf, f.wire_type, f.index)
                    f.encoder(f, buf, item)
            else:
                encode_type(buf, f.wire_type, f.index)
                f.encoder(f, buf, value)
    return buf

cdef inline encode_subobject(Field f, bytearray array, value):
    cdef object sub_buf
    f.resolve_klass()
    cdef object cls = f.klass
    if isinstance(value, dict):
        sub_buf = encode_data(cls, value)
    else:
        sub_buf = encode_data(cls, value.__dict__)
    encode_bytes(f, array, sub_buf)

cdef inline int decode_object(object self, char **pointer, char *end) except -1:
    cdef dict fieldsmap = self._fieldsmap
    cdef uint32_t tag, wtype, findex

    cdef char *sub_buff
    cdef char *sub_end
    cdef uint64_t sub_size

    cdef Field f
    cdef dict d = self.__dict__
    cdef list l

    while pointer[0] < end:
        if raw_decode_uint32(pointer, end, &tag):
            raise makeDecodeError(pointer[0], "Can't deserialize type tag at [{0}] for value")
        findex = tag >> 3
        f = fieldsmap.get(findex)
        if f is None:
            wtype= tag & 0x07
            if skip_unknown_field(pointer, end, wtype):
                raise makeDecodeError(pointer[0], "Can't skip enough bytes for wire_type %s at [{0}] for value" % wtype)
        else:
            if f.packed:
                if raw_decode_delimited(pointer, end, &sub_buff, &sub_size):
                    raise makeDecodeError(pointer[0], "Can't decode value of type `packed` at [{0}]")
                sub_end = sub_buff + sub_size
                l = d.setdefault(f.name, [])
                while sub_buff < sub_end:
                    l.append(f.decoder(&sub_buff, sub_end))
            else:
                if f.klass is None:
                    value = f.decoder(pointer, end)
                else:
                    if raw_decode_delimited(pointer, end, &sub_buff, &sub_size):
                        raise makeDecodeError(pointer[0], "Can't decode value of sub message at [{0}]")
                    f.resolve_klass()
                    value = f.klass()
                    decode_object(value, &sub_buff, sub_buff+sub_size)
                if f.repeated:
                    l = d.setdefault(f.name, [])
                    l.append(value)
                else:
                    d[f.name] = value

    return 0


def encode_primitive(tp, v):
    cdef bytearray buf = bytearray()
    cdef Encoder encoder = get_encoder(tp)
    encoder(None, buf, v)
    return buf


def decode_primitive(s, tp):
    cdef char* buf 
    cdef char *end 
    cdef char *cur 
    cdef Field f
    cdef Decoder d
    cdef Py_buffer buffer
    PyObject_GetBuffer(s, &buffer, PyBUF_SIMPLE | PyBUF_ANY_CONTIGUOUS)
    try:
        buf = <char *>buffer.buf
        end = buf + buffer.len
        cur = buf
        d = get_decoder(tp)
        v = d(&cur, end)
        return v, cur - buf
    finally:
        PyBuffer_Release(&buffer)
