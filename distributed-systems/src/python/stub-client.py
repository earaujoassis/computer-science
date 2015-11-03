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

from crbc.net import CRBCDummyNode

message = "In the face of ambiguity, refuse the temptation to guess."
registration_server = ("localhost", 9999)
client_addr = ("localhost", 7070)
client = CRBCDummyNode(client_addr[0], client_addr[1], "stub-client")
client.registration_process(*registration_server)
print("{} is now writing as a client".format(client_addr))
response = client.send_message("stub-server", message)
print("{} wrote: {}".format(registration_server, repr(response.writable())))
client.socket_close()
print
