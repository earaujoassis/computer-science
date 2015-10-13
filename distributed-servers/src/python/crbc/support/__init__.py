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

from crbc import CRBCData, CRBCEstablishment, CRBCCommunication

__all__ = ("CRBCNameAlreadyInUse", "CRBCNameRevocation", "CRBCNameAccepted",
           "CRBCReceived", "CRBCWhatThaHeck", "CRBCTheBadMessage",
           "CRBCDestinationUnknown")

REASON_PHRASE = {
    100: 'Undefined name error',
    101: 'Name already in use',
    102: 'Name revoked',
    103: 'Wrong name pattern',
    110: 'Undefined registry error',
    111: 'Registry is full',
    200: 'Name accepted gracefully',
    201: 'Name aliased gracefully',
    300: 'Message sent and received gracefully',
    400: 'Message fully understood, but doens\'t make any sense for me',
    401: 'Bad CRBC message',
    402: 'Unknown name destination',
    403: 'That\'s not me (name non-repudiation)'
}


class CRBCNameAlreadyInUse(CRBCEstablishment):

    status_code = 101

    def __init__(self, name='', complete=None, header={}, body=''):
        super(CRBCNameAlreadyInUse, self).__init__(
            complete=complete, header=header, body=body)
        self.set_method(CRBCEstablishment.Reject)
        if name:
            self.set_name(name)
        self.set('Status-code', self.status_code)
        self.set('Reason-Phrase', REASON_PHRASE[self.status_code])


class CRBCNameRevocation(CRBCEstablishment):

    status_code = 102

    def __init__(self, name='', complete=None, header={}, body=''):
        super(CRBCNameRevocation, self).__init__(
            complete=complete, header=header, body=body)
        self.set_method(CRBCEstablishment.Reject)
        if name:
            self.set_name(name)
        self.set('Status-code', self.status_code)
        self.set('Reason-Phrase', REASON_PHRASE[self.status_code])


class CRBCNameAccepted(CRBCEstablishment):

    status_code = 200

    def __init__(self, name='', complete=None, header={}, body=''):
        super(CRBCNameAccepted, self).__init__(
            complete=complete, header=header, body=body)
        self.set_method(CRBCEstablishment.Accept)
        if name:
            self.set_name(name)
        self.set('Status-code', self.status_code)
        self.set('Reason-Phrase', REASON_PHRASE[self.status_code])


class CRBCReceived(CRBCCommunication):

    status_code = 300

    def __init__(self, name='', complete=None, header={}, body=''):
        super(CRBCReceived, self).__init__(
            complete=complete, header=header, body=body)
        self.set_method(CRBCCommunication.Received)
        if name:
            self.set_name(name)
        self.set('Status-code', self.status_code)
        self.set('Reason-Phrase', REASON_PHRASE[self.status_code])


class CRBCWhatThaHeck(CRBCData):

    status_code = 400

    def __init__(self, name='', complete=None, header={}, body=''):
        super(CRBCWhatThaHeck, self).__init__(
            complete=complete, header=header, body=body)
        self.set_method(CRBCData.General)
        if name:
            self.set_name(name)
        self.set('Status-code', self.status_code)
        self.set('Reason-Phrase', REASON_PHRASE[self.status_code])


class CRBCTheBadMessage(CRBCData):

    status_code = 401

    def __init__(self, name='', complete=None, header={}, body=''):
        super(CRBCTheBadMessage, self).__init__(
            complete=complete, header=header, body=body)
        self.set_method(CRBCData.General)
        if name:
            self.set_name(name)
        self.set('Status-code', self.status_code)
        self.set('Reason-Phrase', REASON_PHRASE[self.status_code])


class CRBCDestinationUnknown(CRBCCommunication):

    status_code = 402

    def __init__(self, name='', complete=None, header={}, body=''):
        super(CRBCDestinationUnknown, self).__init__(
            complete=complete, header=header, body=body)
        self.set_method(CRBCCommunication.Unknown)
        if name:
            self.set_name(name)
        self.set('Status-code', self.status_code)
        self.set('Reason-Phrase', REASON_PHRASE[self.status_code])
