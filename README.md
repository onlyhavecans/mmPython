# mm

mm is the muck/mush/mud/MU* equivalent of [ii](http://tools.suckless.org/ii/), the FIFO and filesystem based irc client.

It relies on a fairly recent version of Twisted (>=13.0.0) and Python 2.7. Because of it's reliance on Twisted it does not work with Python 3

# Usage
When run it creates the ~/muck directory and a subdirectory based on the name of the connection specified on the command line

In this directory it creates an out file which has the output, and a FIFO in

write to in, get muck from out.