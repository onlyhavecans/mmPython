# mm 

mm stands for MU*Me

mm is the muck/mush/mud/MU* equivalent of [ii](http://tools.suckless.org/ii/), the FIFO and filesystem based irc client.

It relies on a fairly recent version of Twisted and Python 2.7. Because of it's reliance on Twisted it does not work with Python 3

## Usage
When run it creates the ~/muck directory and a subdirectory based on the name of the connection specified on the command line

In this directory it creates an `out` file which has the output, and a FIFO `in`

write to in, get muck from out.

## Advanced usage tips
- Use screen or tmux to split your screen and then multitail to read out with all the coloring you need.
- In vim you can use key mappings like `map w1 :.w >> in<cr>`
- simple shell or perl scripts can be used to read from out and automate tasks
- A simple shell script wrapper could set up your env and auto log you in
