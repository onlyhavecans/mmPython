" Edit this to add the accounts you muck on and add to your .vimrc or load
" like a plugin.
"
" This assumes you have created a file called mucking_around in your ~/muck
" folder that you save you logins in and shortcuts at the top
"
" Then you can load that file, get a stripped vim for mucking... and can
" use <Leader>number to sent to your different chats

function! SetMuck(user)
  let w:muck = a:user.'/in'
  echo 'Outfile set to: '.w:muck
endfunction

function! SendToMuck()
  if exists("w:muck")
    execute ".w >> ".w:muck
    normal o
    startinsert
  else
    echohl ErrorMsg | echo "No muck set! Use <leader># to set" | echohl None
  endif
endfunction

map <leader>m :call SendToMuck()<CR>
imap <leader>m <ESC>:call SendToMuck()<CR>

function! s:SetupMUCK()
  let g:powerline_loaded = 1
  colorscheme default
  syntax off
  filetype off
  set laststatus=0
  set wrap
  map <leader>1 :call SetMuck("Pants")<CR>
  map <leader>2 :call SetMuck("Rands")<CR>
  map <leader>3 :call SetMuck("Duece")<CR>
  map <leader>4 :call SetMuck("Spigot")<CR>
endfunction

au BufRead,BufNewFile mucking_around call s:SetupMUCK()
