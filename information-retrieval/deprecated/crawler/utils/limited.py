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

class LimitedResourceIsFull(Exception):
    pass

class List(list):
    def __init__(self, buffer_size=20, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.__buffer_size = buffer_size

    def force_append(self,obj):
        if len(self) == self.__buffer_size:
            super(List, self).pop()
            super(List, self).append(obj)
        elif len(self) < self.__buffer_size:
            super(List, self).append(obj)
        else:
            raise LimitedResourceIsFull("list max size, {0}, reached".format(self.__buffer_size))

    def append(self,obj):
        if len(self) < self.__buffer_size:
            super(List, self).append(obj)
        else:
            raise LimitedResourceIsFull("list max size, {0}, reached".format(self.__buffer_size))

    def append_or_loose(self, obj):
        if len(self) < self.__buffer_size:
            super(List, self).append(obj)

    def is_full(self):
        return (len(self) == self.__buffer_size)

    def remaining_space(self):
        return (self.__buffer_size - len(self))

