# -*- coding: utf-8 -*-

# Copyright 2011 Éwerton Assis
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
from abc import ABCMeta, abstractmethod

class NoContentError(Exception):
    pass

class Provider(object):
    __metaclass__ = ABCMeta

    def __init__(self, host, port=80):
        self.host, self.port = host, port
        self.ip = socket.gethostbyname(host)

    @abstractmethod
    def close(self):
        raise NotImplemented

    def __del__(self):
        return self.close()

