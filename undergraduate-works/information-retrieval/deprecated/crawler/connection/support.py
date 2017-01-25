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

import socket, select, time, re
from crawler.http import HttpResponse
from crawler.http.requests import HttpRequestGet

class Connection(object):
    def __init__(self, socket, host, url):
        self.socket = socket
        self.host = host
        self.url = url
        self.__data = None

    def __get_data(self):
        return self.__data

    def __pull_data(self, data):
        if not self.__data or len(self.__data) == 0:
            self.__data = data
        else:
            self.__data += data
    data = property(__get_data, __pull_data)

def send_request(request_writable, host, port):
    try:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((host,port))
    except (socket.gaierror, socket.error):
        # TODO Should I return HttpResponse() ?
        return None
    connection.send(request_writable)
    data = connection.recv(16834)
    connection.close
    del connection
    response = HttpResponse(data)
    return response

def normalize_url(url, context=None):
    uri_scheme = authority = path = None
    if not context:
        authority = url.replace(' ', '') # remove white-spaces
        if authority.startswith('https://'):
            uri_scheme = 'https://'
            authority = authority.replace('https://','') # remove https://
        if authority.startswith('http://'):
            uri_scheme = 'http://'
            authority = authority.replace('http://','') # remove http://
        url_pieces = authority.split('/')
        authority = url_pieces.pop(0)
        path = '{0}{1}'.format('/','/'.join(url_pieces))
    else:
        # TODO Check how to make the context a valid url before it
        authority = context
        if not url.startswith('/'):
            path = "{0}{1}".format('/', url)
        else:
            path = url
    try:
        index = authority.rindex(':')
        port = authority[index+1:]
        authority = authority[:index]
        port = int(port)
        port = (port or (uri_scheme == 'https://' and 443) or ((uri_scheme == 'http://' or uri_scheme == None) and 80))
    except:
        port = (uri_scheme == 'https://' and 443) or ((uri_scheme == 'http://' or uri_scheme == None) and 80)
    return (uri_scheme,authority,port,path)

class NotAddressable(Exception):
    pass

class Unusable(Exception):
    pass

class Host(object):
    def __init__(self, url, ip=None):
        self.ip_list = list()
        self.url = url
        try:
            host_info = socket.gethostbyname_ex(url)
        # TODO EXCEPTION HERE: gaierror: [Errno -5] No address associated with hostname
        # TODO Raise a NotAddressable exception for this problem above
        except (socket.gaierror):
            import sys
            sys.stderr.write("Is {0} addressable?\n".format(url))
            raise NotAddressable("There's no address associated with hostname")
        for local_ip in host_info[2]:
            self.ip_list.append(local_ip)
        if ip:
            ip = str(ip)
            self.ip_list.append(ip)
        self.path = None
        self.crawl_delay = 10.0

    def __eq__(self, obj):
        if self.url == obj or self.ip_list == obj or obj in self.ip_list:
            return True
        return False

    def __ne__(self, obj):
        if self.url != obj and self.ip_list != obj and obj not in self.ip_list:
            return True
        return False

    def another_ip(self, actual_ip):
        try:
            if len(self.ip_list) > 1 and len(actual_ip) > 1:
                for local_ip in self.ip_list:
                    if local_ip not in actual_ip: return local_ip
        except TypeError:
            if len(self.ip_list) > 1:
                for local_ip in self.ip_list:
                    if local_ip != actual_ip: return local_ip
        return None

    def lock(self):
        if hasattr(self, "locked") and getattr(self, "locked", False):
            raise Unusable("Already locked")
        elif hasattr(self, "last_lock"):
            if (time.time() - self.last_lock) < self.crawl_delay:
                raise Unusable("You'll have to wait")
        self.last_lock = time.time()
        self.locked = True

    def unlock(self):
        self.locked = False

class Robot(Host):
    def __init__(self, url, ip=None):
        super(Robot, self).__init__(url, ip)
        from crawler.connection import USER_AGENT, send_request
        request = HttpRequestGet(host=self.url, path='/robots.txt')
        request.set("User-Agent", USER_AGENT)
        request.set("Accept", "text/plain")
        response = send_request(request.writable(), self.ip_list[0], 80)
        if response:
            self.robots_txt = response.content
            self.__process()
        del request, response

    def __process(self):
        if not getattr(self, "robots_txt", False):
            return
        pattern_user_agent = re.compile("[Uu]?ser-[Aa]?gent:[ ]?[A-Za-z0-9_.\/// ]+")
        pattern_exact = re.compile("[Uu]?ser-[Aa]?gent:[ ]?[*]+")
        final_robots_txt = str()
        user_agent = False
        for line in self.robots_txt.splitlines(True):
            if pattern_exact.match(line) and not user_agent:
                user_agent = True
            elif pattern_user_agent.match(line) and not pattern_exact.match(line) and user_agent:
                user_agent = False
                continue
            if user_agent:
                final_robots_txt = final_robots_txt + line
        self.robots_txt = final_robots_txt
        del pattern_user_agent, pattern_exact, user_agent, final_robots_txt
        disallow = list()
        pattern_disallow = re.compile("[Dd]?isallow:[ ]?(?P<path>.+)")
        for line in self.robots_txt.splitlines():
            result = pattern_disallow.match(line)
            if result:
                disallow.append(result.group('path'))
        self.disallow = disallow
        del pattern_disallow, disallow

    def can_access(self, path):
        pass

def can_access(url):
    from crawler.connection import normalize_url
    uri_scheme, authority, port, path = normalize_url(url)
    del uri_scheme, port
    robot = Robot(authority)
    value = robot.can_access(path)
    del robot
    return value

def receive_data(socket):
    message = ''
    while not False: # Why do I have do write True, instead?
        select.select((socket,), (), (), 20)
        data = socket.recv(16384)
        if not data:
            break
        message += data
    return message

