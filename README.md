# mm 

mm stands for MU*Me

mm is the muck/mush/mud/MU* equivalent of [ii](http://tools.suckless.org/ii/), the FIFO and filesystem based irc client.

It relies on a fairly recent version of Twisted and Python 2.7. Because of it's reliance on Twisted it does not work with Python 3

## Usage
When run it creates the ~/muck directory and a subdirectory based on the name of the connection specified on the command line

In this directory it creates an `out` file which has the output, and a FIFO `in`

write to in, get muck from out.

when you disconnect the program quits and rotates out to a timestamped log. You can disable this with --nolog

## Advanced usage tips
- Use screen or tmux to split your screen and then multitail to read out with all the coloring you need.
- In vim you can use key mappings like `map <leader>m :.w >> in<cr>o` to shortcut write current line & open new line
- If you don't like history for some reason use `map <leader>m :w >> in<cr>ggdGi` to write all lines, wipe, & insert
- Also in vim use c-p and c-n to autocomplete names and words from your vimfile "history"
- simple shell or perl scripts can be used to read from out and automate tasks
- A simple shell script wrapper could set up your env and auto log you in
- in fact, most all tips and tricks for ii will work for mm including now to handle multiple sessions with one screen, ect
