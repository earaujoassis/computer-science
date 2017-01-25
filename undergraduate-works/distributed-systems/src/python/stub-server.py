# -*- coding: utf-8 -*-

# Copyright 2013 Ewerton Assis
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

from crbc import CRBCData, CRBCCommunication
from crbc.support import CRBCReceived, CRBCWhatThaHeck
from crbc.net import CRBCDummyNode


class UpperCaseMessage(CRBCDummyNode):

    def process_crbc_datagram(self, datagram):
        response = None
        if datagram.method == CRBCCommunication.Send:
            message = datagram.body.upper()
            response = CRBCReceived(name=datagram.name)
            response.set('Flow-Id', datagram.get('Flow-Id'))
            response.set('Body-size', len(message))
            response.body = message
        else:
            response = CRBCWhatThaHeck(name=datagram.name)
        return response

server_addr = ("localhost", 8080)
server = UpperCaseMessage(server_addr[0], server_addr[1], "stub-server")
server.registration_process("localhost", 9999, edict={'Time-to-live': 600})
print("{} is now listening as a server".format(server_addr))
server.serve_forever_safe()
server.socket_close()
print
