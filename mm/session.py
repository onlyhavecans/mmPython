from __future__ import print_function
import os
from twisted.internet.protocol import ClientFactory, Protocol
import errno
from twisted.conch.telnet import TelnetTransport, StatefulTelnetProtocol
from twisted.internet import main, reactor
from mm.fifo import FIFOReader
from mm.logger import SessionLogger
from mm.utils import get_timestamp


DEBREKING THIS CODE    def __init__(self):
        self.setLineMode()
        self.logger = None

    def connectionMade(self):
        self.logger = SessionLogger(open(self.transport.factory.filename, 'a'))
        self.logger.log("~Connected at {}".format(get_timestamp()))

    def connectionLost(self, reason):
        self.logger.log("~Connection lost at {}".format(get_timestamp()))
        self.logger.close()
        StatefulTelnetProtocol.connectionLost(self, reason)

    def lineReceived(self, line):
        self.logger.log(line)

    def write(self, line):
        return self.sendLine(line)


class HackFIFO(FIFOReader):
    chunk_size = 3

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
            if not output:
                return
            self.protocol.dataReceived(output)


class FIFOProtocol(Protocol):
    def __init__(self, factory):
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

    def stopFactory(self):
        self.fifo.loseConnection()
        reactor.stop()

