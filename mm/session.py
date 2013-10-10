from __future__ import print_function
from twisted.internet.protocol import ClientFactory
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol


class ConnectionError(Exception):
    pass


class MuckSession(StatefulTelnetProtocol):
    def __init__(self, outfile):
        self.outfile = outfile

    def connectionMade(self):
        print("~Connected!", file=self.outfile)

    def lineReceived(self, line):
        print(line, file=self.outfile)
        self.outfile.flush()

    def write(self, line):
        return self.sendLine(line)

    def close(self):
        self.factory.transport.loseConnection()
        return True


class MuckFactory(ClientFactory):
    def __init__(self, outfile):
        self.outfile = outfile
        self.transport = None

    def buildProtocol(self, addr):
        self.transport = TelnetTransport(MuckSession, self.outfile)
        self.transport.factory = self
        return self.transport

    def startedConnecting(self, connector):
        print("~Connecting", file=self.outfile)

    def clientConnectionFailed(self, connector, reason):
        print("!Connection Failed: {}".format(reason), file=self.outfile)
        self.outfile.flush()
        ClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print("!Disconnected: {}".format(reason), file=self.outfile)
        self.outfile.flush()
        ClientFactory.clientConnectionLost(self, connector, reason)

