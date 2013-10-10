from __future__ import print_function
import sys
from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from twisted.internet.protocol import ReconnectingClientFactory, ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol


class ConnectionError(Exception):
    pass


class MuckSession(StatefulTelnetProtocol):
    def __init__(self):
        self.outfile = sys.stdout

    def connectionMade(self):
        print("~Connected!", file=self.outfile)

    def lineReceived(self, line):
        print(line, file=self.outfile)

    def write(self, line):
        return self.sendLine(line)

    def close(self):
        self.write("QUIT")
        self.factory.transport.loseConnection()
        return True


class MuckFactory(ClientFactory):
    def __init__(self, outfile):
        self.outfile = outfile

    def startedConnecting(self, connector):
        print("~Connecting", file=self.outfile)

    def clientConnectionFailed(self, connector, reason):
        print("!Connection Failed: {}".format(reason), file=self.outfile)

    def clientConnectionLost(self, connector, reason):
        print("!Disconnected: {}".format(reason), file=self.outfile)

