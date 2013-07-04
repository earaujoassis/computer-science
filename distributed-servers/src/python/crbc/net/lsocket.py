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

import socket
import select
import sys
import os
import errno
import time
try:
  import threading
except ImportError:
  import dummy_threading as threading

__all__ = ("UDPServer", "UDPClient", "UDPTwoWay")

def _eintr_retry(func, *args):
  while True:
    try:
      return func(*args)
    except (OSError, select.error) as e:
      if e.args[0] != errno.EINTR:
        raise

class UDPServer(object):

  timeout = None
  allow_reuse_address = False
  max_packet_size = 8192

  def __init__(self, host, port):
    self.__meta_server = (host, port)
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.socket.bind(self.__meta_server)
    self.socket.setblocking(False)
    self.server_address = self.socket.getsockname()
    self.__is_shut_down = threading.Event()
    self.__shutdown_request = False

  def serve_forever(self, poll_interval=0.5):
    self.__is_shut_down.clear()
    try:
      while not self.__shutdown_request:
        r, w, e = _eintr_retry(select.select, [self], [], [], poll_interval)
        if self in r:
          self.__handle_request_noblock()
    finally:
      self.__shutdown_request = False
      self.__is_shut_down.set()

  def serve_forever_safe(self, poll_interval=0.5):
    try:
      self.serve_forever(poll_interval=poll_interval)
    except KeyboardInterrupt:
      threading.Thread(target=lambda: self.shutdown()).start()

  def socket_close(self):
    self.socket.close()

  def shutdown(self):
    self.__shutdown_request = True
    self.__is_shut_down.wait()

  def handle_request(self):
    timeout = self.socket.gettimeout()
    if timeout is None:
      timeout = self.timeout
    elif self.timeout is not None:
      timeout = min(timeout, self.timeout)
    fd_sets = _eintr_retry(select.select, [self], [], [], timeout)
    if not fd_sets[0]:
      self.handle_timeout()
      return
    self.__handle_request_noblock()

  def __handle_request_noblock(self):
    try:
      request, client_address = self.get_request()
    except socket.error:
      return
    if self.verify_request(request, client_address):
      try:
        self.process_request(request, client_address)
      except:
        self.handle_error(request, client_address)

  def handle_timeout(self):
    # a timeout handler
    pass

  def verify_request(self, request, client_address):
    # request verification
    return True

  def process_request(self, request, client_address):
    self.finish_request(request, client_address)
    self.shutdown_request(request)

  def finish_request(self, request, client_address):
    # process the request
    pass

  def shutdown_request(self, request):
    self.close_request(request)

  def close_request(self, request):
    # close the request
    pass

  def handle_error(self, request, client_address):
    print('-' * 40)
    print("Exception happened during processing of request from {0}".format(client_address))
    import traceback
    traceback.print_exc()
    print('-' * 40)

  def get_request(self):
    data, client_addr = self.socket.recvfrom(self.max_packet_size)
    return (data, self.socket), client_addr

  def fileno(self):
    return self.socket.fileno()

class UDPClient(object):

  max_packet_size = 8192

  def __init__(self):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

  def send_message(self, data, host, port):
    received = ""
    self.socket.sendto(data, (host, port))
    r, w, e = _eintr_retry(select.select, [self], [], [], 0.5)
    if self in r:
      received = self.socket.recv(self.max_packet_size)
    return received

  def fileno(self):
    return self.socket.fileno()

class UDPTwoWay(UDPServer):
  def __init__(self, host, port):
    self.__meta_server = (host, port)
    super(UDPTwoWay, self).__init__(host, port)

  def send_message(self, data, host, port):
    received = ""
    self.socket.sendto(data, (host, port))
    r, w, e = _eintr_retry(select.select, [self], [], [], 0.5)
    if self in r:
      received = self.socket.recv(self.max_packet_size)
    return received

  def fileno(self):
    return self.socket.fileno()
