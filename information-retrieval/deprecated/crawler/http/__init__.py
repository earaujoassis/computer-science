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

from abc import ABCMeta, abstractmethod

class BadRequestError(ValueError):
    pass

class InvalidField(ValueError):
    pass

class Http(object):
    __metaclass__ = ABCMeta
    def __init__(self, complete=None, header={}, content=''):
        self._complete, self._header, self._content = complete, header, content
        return self.process()

    @abstractmethod
    def writable(self):
        raise NotImplemented

    @abstractmethod
    def process(self):
        raise NotImplemented

    def __str__(self):
        return self.writable()

    def __setitem__(self, key, value):
        self._header[key] = value

    def _get_header(self):
        return self._header
    header = property(_get_header)

    def _get_content(self):
        return self._content

    def _set_content(self, content):
        self._content = content
    content = property(_get_content, _set_content)

    def _get_complete(self):
        return self._complete

    def _set_complete(self, complete):
        self._complete = complete
        self.process()
    complete = property(_get_complete, _set_complete)

class HttpRequest(Http):
    def __init__(self, complete=None, header={}, content=''):        
        self._method = str()
        super(HttpRequest, self).__init__(complete, header, content)

    def writable(self):
        if self._complete and not self._header and not self._content:
            return self._complete
        fields = list()
        header = self._header.copy()
        request_line = "{0} {1} {2}".format(header.pop('Method'), header.pop('Request-URI'), header.pop('HTTP-Version'))
        for key, value in header.items():
            try:
                if len(value) > 1 and isinstance(value, list):
                    value = "; ".join(value)
            except TypeError:
                pass
            field = '{0}: {1}'.format(key, value)
            fields.append(field)
        if len(fields) < 0:
            return "{0}\r\n\r\n{1}".format(request_line, self._content)
        header = "\r\n".join(fields)
        return "{0}\r\n{1}\r\n\r\n{2}".format(request_line, header, self._content)

    def process(self):
        if not self._complete:
            return
        header, self._content = self._complete.split('\r\n\r\n', 1)
        header = header.split('\r\n')
        header_dict = {}
        header_dict['Method'], header_dict['Request-URI'], header_dict['HTTP-Version'] = header.pop(0).split(' ')
        self._method = header_dict['Method']
        for field in header:
            index = field.index(':')
            key = field[0:index]
            field = field.replace(field[:index+2], '')
            if ';' in field:
                fields = field.split('; ')
                value = fields
            else:
                value = field
            header_dict[key] = value
        self._header = header_dict

    def _get_method(self):
        return self._method
    method = property(_get_method)

    def _get_get(self):
        if not hasattr(self, '_get'):
            uri = self._header.get('Request-URI', '')
            try:
                index_up = uri.index('?')
                try:
                    index_down = uri.index('#')
                    uri = uri[index_up+1:index_down]
                except ValueError:
                    uri = uri[index_up+1:]
                uri = uri.split('&')
                if not isinstance(uri, list):
                    uri = uri.split(';')
                if isinstance(uri, list):
                    queries = list()
                    for query in uri:
                        queries.append(query.split('='))
                    self._get = dict(queries)
                else:
                    self._get = {}
            except ValueError:
                self._get = {}
        return self._get
    GET = property(_get_get)

    def _get_post(self):
        if not hasattr(self, '_post'):
            if (self._method == 'GET' or self._method == 'POST') and len(self._content) > 0:
                content = self._content
                content = content.split('&')
                if not isinstance(content, list):
                    content = content.split(';')
                if isinstance(content, list):
                    queries = list()
                    for query in content:
                        queries.append(query.split('='))
                    self._post = dict(queries)
                else:
                    self._post = {}
            else:
                self._post = {}
        return self._post
    POST = property(_get_get)

class HttpResponse(Http):
    def __init__(self, complete=None, header={}, content=''):        
        self._status_code = int()
        super(HttpResponse, self).__init__(complete, header, content)

    def writable(self):
        if self._complete and not self._header and not self._content:
            return self._complete
        fields = list()
        header = self._header.copy()
        status_line = "{0} {1} {2}".format(header.pop('HTTP-Version'), header.pop('Status-Code'), header.pop('Reason-Phrase'))
        for key, value in header.items():
            try:
                if len(value) > 1 and isinstance(value, list):
                    value = "; ".join(value)
            except TypeError:
                pass
            field = '{0}: {1}'.format(key, value)
            fields.append(field)
        if len(fields) < 0:
            return "{0}\r\n\r\n{1}".format(request_line, self._content)
        header = "\r\n".join(fields)
        return "{0}\r\n{1}\r\n\r\n{2}".format(status_line, header, self._content)

    def process(self):
        if not self._complete:
            return
        header, self._content = self._complete.split('\r\n\r\n', 1)
        header = header.split('\r\n')
        header_dict = {}
        status_line = header.pop(0).split(' ', 2)
        if len(status_line) > 3:
            status_line[2] = ' '.join(status_line[2:])
            del status_line[3:]
        header_dict['HTTP-Version'], header_dict['Status-Code'], header_dict['Reason-Phrase'] = status_line
        self._status_code = int(status_line[1])
        for field in header:
            index = field.index(':')
            key = field[0:index]
            field = field.replace(field[:index+2], '')
            if ';' in field:
                fields = field.split('; ')
                value = fields
            else:
                value = field
            header_dict[key] = value
        self._header = header_dict

    def _get_status_code(self):
        return self._status_code
    status_code = property(_get_status_code)

