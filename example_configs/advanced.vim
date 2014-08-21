" Edit this to add the accounts you muck on and add to your .vimrc or load
" like a plugin.
"
" This assumes you have created a file called mucking_around in your ~/muck
" folder that you save you logins in and shortcuts at the top
"
" Then you can load that file, get a stripped vim for mucking... and can
" use <Leader>number to sent to your different chats
function! s:setupMUCK()
  let g:powerline_loaded = 1
  colorscheme default
  syntax off
  filetype off
  set laststatus=0
  set wrap
  map <leader>1 :.w >> Pants/in<cr>o
  map <leader>2 :.w >> Rands/in<cr>o
  map <leader>3 :.w >> Duece/in<cr>o
  map <leader>4 :.w >> Spigot/in<cr>o
endfunction

au BufRead,BufNewFile mucking_around call s:setupMUCK()
