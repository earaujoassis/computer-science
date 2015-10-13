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

import time
from threading import Timer, Thread
from crbc import CRBCData, CRBCEstablishment, CRBCCommunication, generate_id
from crbc.exceptions import *
from crbc.support import *
from crbc.net.lsocket import UDPServer, UDPClient, UDPTwoWay


class CRBCRegistry(UDPTwoWay):

    def __init__(self, host, port):
        self.__registry_meta = (host, port)
        self.__mapping = {}
        super(CRBCRegistry, self).__init__(host, port)

    def __remove_entry(self, entry_name):
        if entry_name in self.__mapping:
            client_address, ttl = self.__mapping.pop(entry_name)
            response = CRBCNameRevocation(name=entry_name)
            self.socket.sendto(response.writable(), client_address)
            print("Entry removed \"{0}\" for {1}".format(
                entry_name, client_address))

    def finish_request(self, request, client_address):
        data, socket = request
        print("{0} wrote: {1}".format(client_address, repr(data)))
        datagram = CRBCData(complete=data)
        datagram.name = datagram.get('Name')
        response = None
        if datagram.method == CRBCEstablishment.Register:
            if datagram.name in self.__mapping.keys():
                response = CRBCNameAlreadyInUse(name=datagram.name)
            else:
                ttl = float(datagram.get('Time-to-live'))
                self.__mapping[datagram.name] = (client_address, ttl)
                if not ttl == 0:
                    Timer(
                        ttl, self.__remove_entry, [datagram.name], {}).start()
                response = CRBCNameAccepted(name=datagram.name)
        elif datagram.method == CRBCCommunication.Send or CRBCCommunication.Received == datagram.method:
            if datagram.name in self.__mapping.keys():
                destination = self.__mapping[datagram.name][0]
                received = super(CRBCRegistry, self).send_message(
                    datagram.writable(), *destination)
                response = CRBCCommunication(complete=received)
            else:
                response = CRBCDestinationUnknown(name=datagram.name)
        else:
            response = CRBCWhatThaHeck()
        socket.sendto(response.writable(), client_address)

    def handle_error(self, request, client_address):
        super(CRBCRegistry, self).handle_error(request, client_address)
        socket = request[1]
        response = CRBCTheBadMessage(name='reserved-for-errors')
        socket.sendto(response.writable(), client_address)


class CRBCDummyNode(UDPTwoWay):

    ttl = 10

    def __init__(self, host, port, name, check_revoke=True):
        self.__node_meta = (host, port)
        self.__name = name
        self.__main_register = None
        self.check_revoke = check_revoke
        super(CRBCDummyNode, self).__init__(host, port)

    def registration_process(self, host, port, edict={}):
        ttl = edict.pop('Time-to-live', None) or self.ttl
        establishment = CRBCEstablishment()
        establishment.set_method(CRBCEstablishment.Register)
        establishment.set_name(self.__name)
        establishment.set('Time-to-live', ttl)
        received = super(CRBCDummyNode, self).send_message(
            establishment.writable(), "localhost", 9999)
        response = CRBCEstablishment(complete=received)
        if response.method != CRBCEstablishment.Accept:
            raise NonEstablished(
                "Couldn't establish registration for {}".format(self.__name))
        else:
            self.__main_register = (host, port)

    def send_message(self, name, message):
        communication = CRBCCommunication(header={})  # Strangely necessary
        communication.set_method(CRBCCommunication.Send)
        communication.set_name(name)
        communication.set('Body-size', len(message))
        communication.set('Flow-Id', generate_id(message))
        communication.body = message
        received = super(CRBCDummyNode, self).send_message(
            communication.writable(), *self.__main_register)
        return CRBCCommunication(complete=received)

    def finish_request(self, request, client_address):
        data, socket = request
        print("{0} wrote: {1}".format(client_address, repr(data)))
        datagram = CRBCData(complete=data)
        if self.check_revoke:
            if self.process_crbc_revocation(datagram):
                return
        datagram.name = datagram.get('Name')
        response = self.process_crbc_datagram(datagram)
        socket.sendto(response.writable(), client_address)

    def process_crbc_datagram(self, datagram):
        pass

    def process_crbc_revocation(self, datagram):
        if datagram.method == CRBCEstablishment.Reject and datagram.get('Status-code') == '102':
            Thread(target=lambda: self.shutdown()).start()
            return True
        return False

    def reset_name(self, name):
        if not self.__main_register:
            self.__name = name
        else:
            raise NameChangingPostEstablishment(
                "Can't change it post-establishment")
