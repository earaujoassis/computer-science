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
from crawler.connection.support import Connection, send_request, normalize_url, receive_data
from crawler.connection.support import Robot as Host
from crawler.connection.support import Unusable, NotAddressable
from crawler.utils.limited import List
from crawler.http.requests import HttpRequestGetHtml

USER_AGENT = 'Diaburu/0.1'

class Unreachable(Exception):
    pass

class FullOfWork(Exception):
    pass

class NotSupported(Exception):
    pass

class FetchingContext(object):
    def __init__(self, host_buffer_size=70, max_connected_ips=150,
            max_working_urls=100, max_pending_pages=100):
        # Data strucutes used for setup_host method
        self.__host_buffer = List(host_buffer_size)
        # Data strucutes used for setup_connection method
        self.__connected_ips = List(max_connected_ips)
        # Data strucutes used for fetch_page method
        self.__pending_pages = List(max_pending_pages)
        self.__working_urls = List(max_working_urls)
        self.__pending_connections = list()

    def __setup_host(self, host_url):
        # TODO This code should provide some verifiable requirements from its clients
        # TODO Check it's whether a valid URL
        for work_host in self.__host_buffer:
            if work_host == host_url:
                return work_host
        try:
            new_host = Host(host_url)
        except NotAddressable:
            return None
        self.__host_buffer.force_append(new_host)
        return new_host

    def __setup_connection(self, message, host, port=80):
        try:
            host.lock()
        except Unusable:
            return None
        free_ip = list(set(host.ip_list) - set(self.__connected_ips))
        if self.__connected_ips.is_full() or not free_ip:
            return None
        free_ip = free_ip.pop(0)
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.connect((free_ip, port))
        except Exception as error:
            import sys
            sys.stderr.write("{0}\n".format(error))
            return None
        connection.setblocking(0)
        connection.send(message)
        self.__connected_ips.append(free_ip)
        return connection

    def __teardown_connection(self, connection):
        self.__connected_ips.remove(connection.getpeername()[0])
        connection.close()

    def __del__(self):
        while len(self.__pending_connections) > 0:
            connection, url = self.__pending_connections.pop()
            try:
                self.__teardown_connection(connection)
                self.__working_urls.remove(url)
            except socket.error:
                pass
            del connection, url

    def fetch_page(self, url, context=None):
        if url in self.__working_urls or not url:
            return False
        if self.__working_urls.is_full():
            # FIXME Client classes are not handling this exception
            raise FullOfWork("All the fetching context workers are occupied right now")
        import sys
        sys.stdout.write("Fetch for: {0}\n".format(url))
        uri_scheme, authority, port, path = normalize_url(url, context)
        if uri_scheme == 'mailto':
            raise NotSupported("There's no support for mailto scheme")
        if port == 443:
            # FIXME TODO There's no support for HTTPS/port 443 yet
            # FIXME Client classes are not handling this exception
            raise NotSupported("There's no support for HTTPS yet")
        host = self.__setup_host(authority)
        if host is None:
            raise Unreachable("There's no host associated")
        request = HttpRequestGetHtml(USER_AGENT, host=host.url, path=path)
        connection = self.__setup_connection(request.writable(), host, port)
        if connection:
            self.__pending_connections.append(Connection(connection, host, url))
        else:
            pending_dict = {'message':request.writable(),'host':host,'port':port}
            self.__pending_pages.append_or_loose(pending_dict)
        self.__working_urls.append(url)

    def received_data(self):
        data_list = list()
        while len(self.__pending_connections) > 0:
            connection = self.__pending_connections.pop()
            connection.data = receive_data(connection.socket)
            data_list.append((connection.url, connection.data))
            self.__teardown_connection(connection.socket)
            self.__working_urls.remove(connection.url)
            connection.host.unlock()
            del connection
        if len(self.__pending_pages) > 0 and not self.__connected_ips.is_full():
            while not self.__connected_ips.is_full() and self.__pending_pages:
                self.__setup_connection(**self.__pending_pages.pop())
        return data_list

    def has_data(self):
        return (len(self.__pending_connections) > 0)

    def teardown(self):
        return self.__del__()

