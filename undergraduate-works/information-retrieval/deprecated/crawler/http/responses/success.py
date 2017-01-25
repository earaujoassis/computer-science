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

from crawler.http import HttpResponse

# Client errors

class HttpResponseOK(HttpResponse):
    def __init__(self, content=''):
        super(HttpResponseOK, self).__init__(content=content)
        self._status_code = 200
        self.__setitem__('Reason-Phrase', 'OK')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse200 = HttpResponseOK

class HttpResponseCreated(HttpResponse):
    def __init__(self, content=''):
        super(HttpResponseCreated, self).__init__(content=content)
        self._status_code = 201
        self.__setitem__('Reason-Phrase', 'Created')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse201 = HttpResponseCreated

