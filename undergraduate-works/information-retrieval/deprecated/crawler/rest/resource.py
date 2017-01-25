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

class MetaResource(type):
    def __new__(klass, name, bases, namespace):
        cls = super(MetaResource, klass).__new__(klass, name, bases, namespace)
        resources = set(key for key, value in namespace.items() if getattr(value, "__resource__", False))
        notimplemented = set(key for key, value in namespace.items() if getattr(value, "__isnotimplemented__", False))        
        for base in bases:
            for name in getattr(base, "__notimplementedmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isnotimplemented__", False):
                    notimplemented.add(name)
            for name in getattr(base, "__resources__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__resource__", False):
                    resources.add(name)
        for resource in resources:
            notimplemented.discard(getattr(namespace.get(resource, None), "__verb__", ''))
        if not resources and not hasattr(namespace, "__resourcename__") and len(notimplemented) < 4:
            cls.__resourcename__ = getattr(cls, "__name__").lower().replace('resource', '')
        cls.__notimplementedmethods__ = frozenset(notimplemented)
        cls.__resources__ = frozenset(resources)
        return cls

def notimplemented(method):
    method.__isnotimplemented__ = True
    return method

def setresource(urlregex, default_output='xml', verb=''):
    def wrapper(method):
        method.__isnotimplemented__ = False
        method.__resource__ = True
        method.__defaultoutput__ = default_output
        method.__urlregex__ = urlregex
        method.__verb__ = verb or method.__name__
        return method
    return wrapper

class BaseResource(object):
    __metaclass__ = MetaResource

    @notimplemented
    def create(self, request):
        pass

    @notimplemented
    def read(self, request):
        pass

    @notimplemented
    def update(self, request):
        pass

    @notimplemented
    def delete(self, request):
        pass

