from __future__ import print_function
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from mm.logger import SessionLogger
from mm.utils import get_timestamp


class MuckSession(StatefulTelnetProtocol):
    def __init__(self):
        self.logger = None

    def connectionMade(self):
        self.logger = SessionLogger(open(self.transport.factory.filename, 'a'))
        self.logger.log("~Connected at {}".format(get_timestamp()))

    def lineReceived(self, line):
        self.logger.log(line)

    def write(self, line):
        return self.sendLine(line)

    def close(self):
        self.logger.log("~Connection lost at {}".format(get_timestamp()))
        self.factory.transport.loseConnection()
        self.logger.close()
        return True


class MuckFactory(ClientFactory):
    protocol = StatefulTelnetProtocol

    def __init__(self, outfile):
        self.filename = outfile
        self.transport = None

    def buildProtocol(self, addr):
        self.transport = TelnetTransport(MuckSession)
        self.transport.factory = self
        return self.transport

    def clientConnectionFailed(self, connector, reason):
        print("!Connection Failed: {}".format(reason))
        ClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print("!Disconnected: {}".format(reason))
        ClientFactory.clientConnectionLost(self, connector, reason)

