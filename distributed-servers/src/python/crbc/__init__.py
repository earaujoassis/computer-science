# -*- coding: utf-8 -*-

# Copyright 2013 Ewerton Assis
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sha

from abc import ABCMeta, abstractmethod
from crbc.exceptions import *

def generate_id(message):
  return sha.new(message).hexdigest()

class CRBCData(object):

  ProtocolVersion = "CRBC/1.0"
  General = "General"
  Methods = (General, )

  def __init__(self, complete=None, header={}, body=''):
    self.__complete, self.__header, self.__body = complete, header, body
    self.__method = None
    return self.process()

  def _get_header(self):
    return self.__header
  header = property(_get_header)

  def writable(self):
    if self.__complete and not self.__header and not self.__body:
      return self.__complete
    fields = []
    header = self.__header.copy()
    protocol = header.pop('Protocol', None) or self.ProtocolVersion
    presentation_line = "{0} {1} {2}".format(protocol, header.pop('Method'), header.pop('Name'))
    for key, value in header.items():
      field = "{0}: {1}".format(key, value)
      fields.append(field)
    if len(fields) < 0:
      return "{0}\r\n\r\n{1}".format(presentation_line, self.__body)
    header = "\r\n".join(fields)
    return "{0}\r\n{1}\r\n\r\n{2}".format(presentation_line, header, self.__body)

  def process(self):
    if not self.__complete:
      return
    header, self.__body = self.__complete.split('\r\n\r\n', 1)
    header = header.split('\r\n')
    header_dict = {}
    header_dict['Protocol'], header_dict['Method'], header_dict['Name'] = header.pop(0).split(' ')
    self.__method = header_dict['Method']
    for field in header:
      index = field.index(':')
      if (index < 0):
        raise InvalidField("Invalid line in CRBC message")
      key = field[0:index]
      field = field.replace(field[:index+2], '')
      value = field
      header_dict[key] = value
    self.__header = header_dict

  def __str__(self):
    return self.writable()

  def __get_method(self):
    return self.__method
  method = property(__get_method)

  def set_method(self, method):
    if (method in self.Methods):
      self.header['Method'] = method

  def set_name(self, name):
    self.header['Name'] = name

  def set(self, key, value):
    if self.__header:
      self.__header[key] = value

  def get(self, key):
    if self.__header and key in self.__header.keys():
      return self.__header[key]
    return None

  def __set_body(self, message):
    self.__body = message

  def __get_body(self):
    return self.__body
  body = property(__get_body, __set_body)

class CRBCEstablishment(CRBCData):

  Register = "Register"
  Alias = "Alias"
  Accept = "Accept"
  Reject = "Reject"
  Methods = (Register, Alias, Accept, Reject)

class CRBCCommunication(CRBCData):

  Send = "Send"
  Received = "Received"
  Unknown = "Unknown"
  Methods = (Send, Received, Unknown)
