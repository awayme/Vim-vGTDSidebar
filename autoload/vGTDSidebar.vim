"init{{{
if exists("g:loaded_autoload_vgtdsidebar")
    " requires nocompatible and clientserver
    " also, don't double load
    finish
endif

let g:loaded_autoload_vgtdsidebar = 1

if !exists("g:v_GTD_filter")
    let g:v_GTD_filter = {
                \ 'Next(All)' : {
                    \ 'filter': [],
                    \ 'grep': ['^.*@due\(.*@done\)\@!.*$']},
                \ '*Starred' : {
                    \ 'filter': ['\~'],
                    \ 'grep': ['^.*@due\(.*@done\)\@!.*$']},
                \ 'Next All Today' : {
                    \ 'filter': [],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ '@online' : {
                    \ 'filter': ['@status(online)'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ '@home' : {
                    \ 'filter': ['@status(home)'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ '@goout' : {
                    \ 'filter': ['@status(goout)'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ '@pc' : {
                    \ 'filter': ['@status(pc)'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ '@anywhere' : {
                    \ 'filter': ['@status(anywhere)'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ '@call' : {
                    \ 'filter': ['@status(call)'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ '@none' : {
                    \ 'filter': ['^\(.*@status\)\@!.*'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ 'no priority' : {
                    \ 'filter': ['^\(.*@priority\)\@!.*'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']},
                \ 'This Week Pi>=3' : {
                    \ 'filter': ['@priority(\(1\|2\|3\))'],
                    \ 'grep': ['^.*@due(\(' . GetMyWeekNoStr() . '\|' . GetWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']}
                \ }
endif
if !exists("g:vGTDSidebar_width")
    let g:vGTDSidebar_width = 20
endif
"}}}

"autocmd {{{
" if !exists("g:vGTDSidebar_taskfile")
"     autocmd BufRead g:vGTDSidebar_taskfile :call vGTDSidebar#ConcealLine(".*@done.*")
"     autocmd BufRead g:vGTDSidebar_taskfile :call vGTDSidebar#VGTD_PrepSidebar()
" else
"     echo 'Plz set vGTDSidebar_taskfile'
"     finish
" endif
"}}}

"concealing done tasks by default{{{
if !exists("g:my_match_group")
    let g:my_match_group = "concealMatch"
endif

function! vGTDSidebar#ConcealLine(expr)
    "exe ":syntax match " . w:matchgroup . " \"" . a:expr . "\"" . " conceal containedin = ALL"
    exe ":syntax match " . g:my_match_group . " \"" . a:expr . "\"" . " conceal cchar= containedin = ALL"
    set conceallevel=1
endfunction

function! vGTDSidebar#ConcealLineClear()
    exe ":syntax clear " . g:my_match_group
    set conceallevel=0
endfunction
"}}}

"sidebar callback functions{{{
function vGTDSidebar#VGTD_PrepSidebar()
    "execute "vertical " . g:vGTDSidebar_width . " new"
    vertical 20 new
    file VGTD sidebar
    setlocal noswapfile
    "setlocal winfixwidth
    setlocal buftype=nofile
    setlocal bufhidden=hide
    setlocal nowrap
    setlocal nobuflisted
    call s:VGTD_RenderFilterNames()
    setlocal nomodifiable

    noremap <buffer> <Enter> :call vGTDSidebar#VGTD_RunPattern()<CR>
endfunction

function! s:VGTD_RenderFilterNames()
    let filter_keys = sort(keys(g:v_GTD_filter))
    for key in filter_keys
        call setline(index(filter_keys, key)+1, key)
        "call cursor(line(".")+1, col("."))
    endfor
endfunction

function! s:VGTD_GetCurPatternName()
    let str = getline(line("."))
    return substitute(str, "\t", "", "g")
endfunction

function! vGTDSidebar#VGTD_RunPattern()
    let pt_str = s:VGTD_GetCurPatternName()
    let expt = s:VGTD_GetBsgrepPattern(pt_str)
    if expt != ''
        wincmd w
        "echo getline(line("."))
        execute "Bsgrep! " . expt
        call s:FilterInclude(pt_str)
    endif
endfunction

function! s:FilterInclude(filter_name)
    if has_key(g:v_GTD_filter, a:filter_name)
        let dic_filter = g:v_GTD_filter[a:filter_name]['filter']
        for key in dic_filter
            "echo "Bsfilter " . key
            execute 'Bsfilter ' . key
        endfor
    else
        echo a:filter_name . " can't be found"
    endif
endfunction

function! s:VGTD_GetBsgrepPattern(filter_name)
    if has_key(g:v_GTD_filter, a:filter_name)
        let dic_grep = g:v_GTD_filter[a:filter_name]['grep']
        for key in dic_grep
            "let pt = '^\(.*@' . key . '\)\@!.*'
            let pt = key
        endfor
        return pt
    else
        echo a:filter_name . " can't be found"
        return ''
    endif
endfunction
"}}}
