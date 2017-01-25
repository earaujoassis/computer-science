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

class HttpResponseBadRequest(HttpResponse):
    def __init__(self, content=''):
        super(HttpResponseBadRequest, self).__init__(content=content)
        self._status_code = 400
        self.__setitem__('Reason-Phrase', 'Bad Request')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse400 = HttpResponseBadRequest

class HttpResponseUnauthorized(HttpResponse):
    def __init__(self):
        super(HttpResponseUnauthorized, self).__init__()
        self._status_code = 401
        self.__setitem__('Reason-Phrase', 'Unauthorized')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse401 = HttpResponseUnauthorized

class HttpResponseForbidden(HttpResponse):
    def __init__(self):
        super(HttpResponseForbidden, self).__init__()
        self._status_code = 403
        self.__setitem__('Reason-Phrase', 'Forbidden')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse403 = HttpResponseForbidden

class HttpResponseNotFound(HttpResponse):
    def __init__(self):
        super(HttpResponseNotFound, self).__init__()
        self._status_code = 404
        self.__setitem__('Reason-Phrase', 'Not Found')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse404 = HttpResponseNotFound

class HttpResponseMethodNotAllowed(HttpResponse):
    def __init__(self):
        super(HttpResponseMethodNotAllowed, self).__init__()
        self._status_code = 405
        self.__setitem__('Reason-Phrase', 'Method Not Allowed')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse405 = HttpResponseMethodNotAllowed

class HttpResponseNotAcceptable(HttpResponse):
    def __init__(self):
        super(HttpResponseNotAcceptable, self).__init__()
        self._status_code = 406
        self.__setitem__('Reason-Phrase', 'Not Acceptable')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse406 = HttpResponseNotAcceptable

# Server errors

class HttpResponseInternalServerError(HttpResponse):
    def __init__(self):
        super(HttpResponseInternalServerError, self).__init__()
        self._status_code = 501
        self.__setitem__('Reason-Phrase', 'Internal Server Error')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse500 = HttpResponseInternalServerError

class HttpResponseNotImplemented(HttpResponse):
    def __init__(self):
        super(HttpResponseNotImplemented, self).__init__()
        self._status_code = 501
        self.__setitem__('Reason-Phrase', 'Not Implemented')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse501 = HttpResponseNotImplemented

class HttpResponseServiceUnavailable(HttpResponse):
    def __init__(self):
        super(HttpResponseServiceUnavailable, self).__init__()
        self._status_code = 503
        self.__setitem__('Reason-Phrase', 'Service Unavailable')
        self.__setitem__('HTTP-Version', 'HTTP/1.1')
        self.__setitem__('Status-Code', self._status_code)
HttpResponse503 = HttpResponseServiceUnavailable

