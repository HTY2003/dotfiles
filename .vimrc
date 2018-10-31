call plug#begin('~/.vim/plugged')
Plug 'drewtempelmeyer/palenight.vim'
Plug 'itchyny/lightline.vim'
call plug#end()
set noshowmode
set background=dark
colorscheme palenight
set laststatus=2
let g:lightline = {
      \ 'colorscheme': 'palenight',
      \ }
