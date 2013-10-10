__author__ = 'bitm'

import logging

from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol


class ConnectionError(Exception):
    pass


class MuckSession(StatefulTelnetProtocol):
    def connectionMade(self):
        pass

    def lineReceived(self, line):
        print(line)

    def write(self, line):
        return self.sendLine(line)

    def close(self):
        self.sendLine(self.factory.logout_command)
        self.factory.transport.loseConnection()


class MuckFactory(ReconnectingClientFactory):
    logout_command = "QUIT"

    def setLogoutCommand(self, cmd):
        self.logout_command(cmd)

    def clientConnectionLost(self, connector, reason):
        print("connection lost. Reason {}".format(reason))
        super(self).clientConnectionLost(self, connector, reason)
