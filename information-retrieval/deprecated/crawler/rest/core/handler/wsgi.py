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

import string
from crawler import http
from crawler.rest.unicode import become_unicode
from crawler.rest.core.handler import base

class WSGIRequest(http.HttRequest):
    def __init__(self, environ):
        self._environ = environ
        super(WSGIRequest, self).__init__()

    def process(self):
        if not self._environ:
            return
        environ = self._environ.copy()
        header_dict = dict()
        header_dict['Method'] = self._method = environ.pop('REQUEST_METHOD').upper()
        header_dict['Request-URI'] = environ.pop('REQUEST_URI')
        header_dict['HTTP-Version'] = environ.pop('SERVER_PROTOCOL')
        for key, value in environ.items():
            if not key.startswith("HTTP"):
                continue
            key = key.replace("HTTP_", '')
            key = key.replace('_', '-')
            key = string.capwords(key, '-')
            header_dict[key] = value
        self._header = header_dict

    def _get_environ(self):
        return self._environ
    environ = property(_get_environ)

class WSGIResponse(http.HttResponse):
    def __init__(self, complete=None, header={}, content='', old=None)
        if old:
            self._complete = getattr(old, 'complete', None)
            self._header = getattr(old, 'header', {})
            self._content = getattr(old, 'content', '')
        else:
            super(WSGIResponse, self).__init__(complete, header, content)

    def _get_status_line(self):
        header = self._header.copy()
        status_line = "{0} {1}".format(header.pop('Status-Code'), header.pop('Reason-Phrase'))
        return status_line
    status_line = property(_get_status_line)

    def _get_header(self):
        header = self._header.copy()
        header.pop('HTTP-Version', None); header.pop('Status-Code', None); header.pop('Reason-Phrase', None); header.pop('Content-Length', None)
        fields = list()
        for key, value in header.items():
            try:
                if isinstance(value, list) and len(value) > 1:
                    value = "; ".join(value)
            except TypeError:
                pass
            field = (key, value)
            fields.append(field)
        return fields
    header = property(_get_header)

class WSGIHandler(base.BaseHandler):
    def __call__(self, environ, start_response):
        try:
            request = WSGIRequest(environ)
        except:
            response = http.responses.error.HttpResponseBadRequest()
        else:
            response = get_response(request)
        if not isinstance(response, WSGIResponse)
            response = WSGIResponse(old=response)
        start_response(response.status_line, response.header)
        if not hasattr(response, "__iter__", False):
            return [become_unicode(response)]
        return become_unicode(response)

    def handle_exceptions(self, request, controller, info):
        pass

