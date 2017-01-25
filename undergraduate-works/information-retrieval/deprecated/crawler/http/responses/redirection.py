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

class HttpResponseFound(HttpResponse):
    def __init__(self, location, content=''):
        super(HttpResponseFound, self).__init__(content=content)
        self._status_code = 302
        self.__setitem__('Reason-Phrase', 'Found')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
        self.__setitem__('Location', location)
HttpResponse302 = HttpResponseFound

class HttpResponseSeeOther(HttpResponse):
    def __init__(self, location, content=''):
        super(HttpResponseSeeOther, self).__init__(content=content)
        self._status_code = 303
        self.__setitem__('Reason-Phrase', 'See Other')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
        self.__setitem__('Location', location)
HttpResponse303 = HttpResponseSeeOther

class HttpResponseNotModified(HttpResponse):
    def __init__(self, location, content=''):
        super(HttpResponseNotModified, self).__init__(content=content)
        self._status_code = 304
        self.__setitem__('Reason-Phrase', 'Not Modified')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
        self.__setitem__('Location', location)
HttpResponse304 = HttpResponseNotModified

class HttpResponseTemporaryRedirect(HttpResponse):
    def __init__(self, location, content=''):
        super(HttpResponseTemporaryRedirect, self).__init__(content=content)
        self._status_code = 307
        self.__setitem__('Reason-Phrase', 'Temporary Redirect')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
        self.__setitem__('Location', location)
HttpResponse307 = HttpResponseTemporaryRedirect

