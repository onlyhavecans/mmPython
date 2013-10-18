from __future__ import print_function
import os
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.protocols.basic import LineReceiver
import errno
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from twisted.internet import main
from mm.fifo import FIFOReader
from mm.logger import SessionLogger
from mm.utils import get_timestamp


class MuckSession(StatefulTelnetProtocol):
    def __init__(self):
        self.setLineMode()
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


class HackFIFO(FIFOReader):
    def doRead(self):
        """
        Don't die till I tell you to
        """
        while True:
            try:
                output = os.read(self.fileno(), self.chunk_size)
            except (OSError, IOError), err:
                if err.args[0] in (errno.EAGAIN, errno.EINTR):
                    return
                else:
                    return main.CONNECTION_LOST
            self.protocol.dataReceived(output)


class FIFOProtocol(Protocol):
    def __init__(self, factory):
        self.delimiter = "\n"
        self.factory = factory

    def dataReceived(self, data):
        self.factory.transport.write(data)


class MuckFactory(ClientFactory):
    def __init__(self, outfile, infile):
        self.filename = outfile
        self.fifo = HackFIFO(infile)
        self.transport = None

    def buildProtocol(self, addr):
        self.transport = TelnetTransport(MuckSession)
        self.transport.factory = self
        self.fifo.protocol = FIFOProtocol(self)
        self.fifo.protocol.makeConnection(self.fifo)
        self.fifo.startReading()
        return self.transport

    def clientConnectionFailed(self, connector, reason):
        print("!Connection Failed: {}".format(reason))
        ClientFactory.clientConnectionFailed(self, connector, reason)

    def clientConnectionLost(self, connector, reason):
        print("!Disconnected: {}".format(reason))
        ClientFactory.clientConnectionLost(self, connector, reason)

