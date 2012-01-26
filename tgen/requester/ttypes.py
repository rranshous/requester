#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#

from thrift.Thrift import *

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TProtocol
try:
  from thrift.protocol import fastbinary
except:
  fastbinary = None



class Exception(Exception):
  """
  Attributes:
   - msg
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'msg', None, None, ), # 1
  )

  def __init__(self, msg=None,):
    self.msg = msg

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.msg = iprot.readString();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Exception')
    if self.msg != None:
      oprot.writeFieldBegin('msg', TType.STRING, 1)
      oprot.writeString(self.msg)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class Request:
  """
  Attributes:
   - url
   - method
   - data
   - cookies
   - no_cache
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'url', None, None, ), # 1
    (2, TType.STRING, 'method', None, None, ), # 2
    (3, TType.MAP, 'data', (TType.STRING,None,TType.STRING,None), None, ), # 3
    (4, TType.MAP, 'cookies', (TType.STRING,None,TType.STRING,None), None, ), # 4
    (5, TType.BOOL, 'no_cache', None, False, ), # 5
  )

  def __init__(self, url=None, method=None, data=None, cookies=None, no_cache=thrift_spec[5][4],):
    self.url = url
    self.method = method
    self.data = data
    self.cookies = cookies
    self.no_cache = no_cache

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.url = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.STRING:
          self.method = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.MAP:
          self.data = {}
          (_ktype1, _vtype2, _size0 ) = iprot.readMapBegin() 
          for _i4 in xrange(_size0):
            _key5 = iprot.readString();
            _val6 = iprot.readString();
            self.data[_key5] = _val6
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.MAP:
          self.cookies = {}
          (_ktype8, _vtype9, _size7 ) = iprot.readMapBegin() 
          for _i11 in xrange(_size7):
            _key12 = iprot.readString();
            _val13 = iprot.readString();
            self.cookies[_key12] = _val13
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.BOOL:
          self.no_cache = iprot.readBool();
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Request')
    if self.url != None:
      oprot.writeFieldBegin('url', TType.STRING, 1)
      oprot.writeString(self.url)
      oprot.writeFieldEnd()
    if self.method != None:
      oprot.writeFieldBegin('method', TType.STRING, 2)
      oprot.writeString(self.method)
      oprot.writeFieldEnd()
    if self.data != None:
      oprot.writeFieldBegin('data', TType.MAP, 3)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.data))
      for kiter14,viter15 in self.data.items():
        oprot.writeString(kiter14)
        oprot.writeString(viter15)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    if self.cookies != None:
      oprot.writeFieldBegin('cookies', TType.MAP, 4)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.cookies))
      for kiter16,viter17 in self.cookies.items():
        oprot.writeString(kiter16)
        oprot.writeString(viter17)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    if self.no_cache != None:
      oprot.writeFieldBegin('no_cache', TType.BOOL, 5)
      oprot.writeBool(self.no_cache)
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)

class Response:
  """
  Attributes:
   - url
   - status_code
   - headers
   - content
   - from_cache
   - response_time
   - timestamp
   - cookies
  """

  thrift_spec = (
    None, # 0
    (1, TType.STRING, 'url', None, None, ), # 1
    (2, TType.I32, 'status_code', None, None, ), # 2
    (3, TType.MAP, 'headers', (TType.STRING,None,TType.STRING,None), None, ), # 3
    (4, TType.STRING, 'content', None, None, ), # 4
    (5, TType.BOOL, 'from_cache', None, None, ), # 5
    (6, TType.DOUBLE, 'response_time', None, None, ), # 6
    (7, TType.DOUBLE, 'timestamp', None, None, ), # 7
    (8, TType.MAP, 'cookies', (TType.STRING,None,TType.STRING,None), None, ), # 8
  )

  def __init__(self, url=None, status_code=None, headers=None, content=None, from_cache=None, response_time=None, timestamp=None, cookies=None,):
    self.url = url
    self.status_code = status_code
    self.headers = headers
    self.content = content
    self.from_cache = from_cache
    self.response_time = response_time
    self.timestamp = timestamp
    self.cookies = cookies

  def read(self, iprot):
    if iprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None and fastbinary is not None:
      fastbinary.decode_binary(self, iprot.trans, (self.__class__, self.thrift_spec))
      return
    iprot.readStructBegin()
    while True:
      (fname, ftype, fid) = iprot.readFieldBegin()
      if ftype == TType.STOP:
        break
      if fid == 1:
        if ftype == TType.STRING:
          self.url = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 2:
        if ftype == TType.I32:
          self.status_code = iprot.readI32();
        else:
          iprot.skip(ftype)
      elif fid == 3:
        if ftype == TType.MAP:
          self.headers = {}
          (_ktype19, _vtype20, _size18 ) = iprot.readMapBegin() 
          for _i22 in xrange(_size18):
            _key23 = iprot.readString();
            _val24 = iprot.readString();
            self.headers[_key23] = _val24
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      elif fid == 4:
        if ftype == TType.STRING:
          self.content = iprot.readString();
        else:
          iprot.skip(ftype)
      elif fid == 5:
        if ftype == TType.BOOL:
          self.from_cache = iprot.readBool();
        else:
          iprot.skip(ftype)
      elif fid == 6:
        if ftype == TType.DOUBLE:
          self.response_time = iprot.readDouble();
        else:
          iprot.skip(ftype)
      elif fid == 7:
        if ftype == TType.DOUBLE:
          self.timestamp = iprot.readDouble();
        else:
          iprot.skip(ftype)
      elif fid == 8:
        if ftype == TType.MAP:
          self.cookies = {}
          (_ktype26, _vtype27, _size25 ) = iprot.readMapBegin() 
          for _i29 in xrange(_size25):
            _key30 = iprot.readString();
            _val31 = iprot.readString();
            self.cookies[_key30] = _val31
          iprot.readMapEnd()
        else:
          iprot.skip(ftype)
      else:
        iprot.skip(ftype)
      iprot.readFieldEnd()
    iprot.readStructEnd()

  def write(self, oprot):
    if oprot.__class__ == TBinaryProtocol.TBinaryProtocolAccelerated and self.thrift_spec is not None and fastbinary is not None:
      oprot.trans.write(fastbinary.encode_binary(self, (self.__class__, self.thrift_spec)))
      return
    oprot.writeStructBegin('Response')
    if self.url != None:
      oprot.writeFieldBegin('url', TType.STRING, 1)
      oprot.writeString(self.url)
      oprot.writeFieldEnd()
    if self.status_code != None:
      oprot.writeFieldBegin('status_code', TType.I32, 2)
      oprot.writeI32(self.status_code)
      oprot.writeFieldEnd()
    if self.headers != None:
      oprot.writeFieldBegin('headers', TType.MAP, 3)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.headers))
      for kiter32,viter33 in self.headers.items():
        oprot.writeString(kiter32)
        oprot.writeString(viter33)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    if self.content != None:
      oprot.writeFieldBegin('content', TType.STRING, 4)
      oprot.writeString(self.content)
      oprot.writeFieldEnd()
    if self.from_cache != None:
      oprot.writeFieldBegin('from_cache', TType.BOOL, 5)
      oprot.writeBool(self.from_cache)
      oprot.writeFieldEnd()
    if self.response_time != None:
      oprot.writeFieldBegin('response_time', TType.DOUBLE, 6)
      oprot.writeDouble(self.response_time)
      oprot.writeFieldEnd()
    if self.timestamp != None:
      oprot.writeFieldBegin('timestamp', TType.DOUBLE, 7)
      oprot.writeDouble(self.timestamp)
      oprot.writeFieldEnd()
    if self.cookies != None:
      oprot.writeFieldBegin('cookies', TType.MAP, 8)
      oprot.writeMapBegin(TType.STRING, TType.STRING, len(self.cookies))
      for kiter34,viter35 in self.cookies.items():
        oprot.writeString(kiter34)
        oprot.writeString(viter35)
      oprot.writeMapEnd()
      oprot.writeFieldEnd()
    oprot.writeFieldStop()
    oprot.writeStructEnd()
    def validate(self):
      return


  def __repr__(self):
    L = ['%s=%r' % (key, value)
      for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

  def __eq__(self, other):
    return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

  def __ne__(self, other):
    return not (self == other)
