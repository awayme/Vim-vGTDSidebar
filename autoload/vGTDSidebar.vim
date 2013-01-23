"init{{{
if exists("g:loaded_autoload_vgtdsidebar")
    " requires nocompatible and clientserver
    " also, don't double load
    finish
endif

let s:script_dir = substitute(expand("<sfile>:p:h"),'\','/','g')
let g:loaded_autoload_vgtdsidebar = 1.0
let t:vGTDSidebar_SidebarBufName = 'VGTD sidebar'
let t:vGTDSidebar_ConcealMatchGroupName = "concealMatch"
"}}}

"global setting {{{

if !exists("g:vGTDSidebar_Width")
    let g:vGTDSidebar_Width = 20
endif
if !exists("g:vGTDSidebar_WinPos")
    let g:vGTDSidebar_WinPos = "left" 
endif
"}}}

"default mapping{{{
" noremap <silent><buffer> <leader>n :call vGTDSidebar#VGTD_toggleSidebar()<CR>
function! vGTDSidebar#VGTD_patch()
    return '^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$'
endfunction
noremap <silent><buffer> <leader>n :execute 'Bsgrep!' . vGTDSidebar#VGTD_patch()<CR>
"}}}

"internal functions{{{
"date calculating functions{{{
function! s:getChineseWeekDayNo()
    let eng_wdn = strftime("%w", localtime())
    return eng_wdn == 0 ? 7 : eng_wdn
endfunction

function! s:getChineseWeekNo()
    let eng_wn = strftime("%U", localtime())
    return printf("%02d", (s:getChineseWeekDayNo() == 7 ? eng_wn - 1 : eng_wn))
endfunction

function! s:getChineseYear()
    return strftime("%y", localtime())
endfunction

function! s:getMyWeekNoStr(...)
    if a:0 > 0
        return s:getChineseYear() . 'W' . s:getChineseWeekNo() . '+'. a:1
        "strftime("%yW%U".'+'. a:1 , localtime())
    else
        return s:getChineseYear() . 'W' . s:getChineseWeekNo()
        "return strftime("%yW%U", localtime())
    endif
endfunction

function! s:getWeekPatternBefToday()
     let i = 1
     let td = s:getChineseWeekDayNo()
     let wn = s:getChineseYear() . 'W' . s:getChineseWeekNo() . '+'
     "strftime("%yW%U".'+', localtime())
     let exp = wn

    while i < td
        let exp = exp . i . '\|' . wn
        let i = i + 1
    endwhile

    let exp = exp . i

    return exp
endfunction
"}}}
"function! s:defaultMapping(){{{
function! s:defaultMapping()
    command! -range GtDone :<line1>,<line2>call taskpaper#toggle_tag('done', taskpaper#date()) | call s:calDone(FindRootParent(line(".")))
    "command! -range GtDone :<line1>,<line2>call taskpaper#toggle_tag('done', taskpaper#date())
    nnoremap <unique> <buffer> <localleader>td :GtDone<CR>

    " command! -range GtDue :<line1>,<line2>call taskpaper#toggle_tag('due', s:getMyWeekNoStr())
    " nnoremap <unique> <buffer> <localleader>tn :GtDue<CR>

    " command! -range GtStart :<line1>,<line2>call taskpaper#add_tag('stt','')
    command! -range GtStartt :call vGTDSidebar#VGTD_startLog('tm')
    command! -range GtStartc :call vGTDSidebar#VGTD_startLog('ct', 25)
    command! -range GtPause :<line1>,<line2>call taskpaper#add_tag('pse','')
    command! -range GtResume :<line1>,<line2>call taskpaper#add_tag('rsm','')
    command! -range GtStop :<line1>,<line2>call taskpaper#add_tag('stp','')

    command! -range GtDueToday :<line1>,<line2>call taskpaper#toggle_tag('due', s:getMyWeekNoStr() . '+' . s:getChineseWeekDayNo())
    nnoremap <unique> <buffer> <localleader>tn :GtDueToday<CR>

    command! -range GtDueTomorrow :<line1>,<line2>call taskpaper#toggle_tag('due', s:getMyWeekNoStr() . '+' . (s:getChineseWeekDayNo() + 1))
    nnoremap <unique> <buffer> <localleader>to :GtDueTomorrow<CR>

    command! -range GtDueDay :<line1>,<line2>call taskpaper#toggle_tag('due', s:getMyWeekNoStr(input('Value: ')))
    nnoremap <unique> <buffer> <localleader>tnd :GtDueDay<CR>

    " command! -range GtPriority :<line1>,<line2>call taskpaper#add_tag('priority')
    " nnoremap <unique> <buffer> <localleader>tpp :GtPriority<CR>
    " command! -range GtPriority1 :<line1>,<line2>call taskpaper#add_tag('priority','1')
    " command! -range GtPriority2 :<line1>,<line2>call taskpaper#add_tag('priority','2')
    " command! -range GtPriority3 :<line1>,<line2>call taskpaper#add_tag('priority','3')
    " command! -range GtPriority4 :<line1>,<line2>call taskpaper#add_tag('priority','4')
    " command! -range GtPriority5 :<line1>,<line2>call taskpaper#add_tag('priority','5')

    " command! -range GtEtiny :<line1>,<line2>call taskpaper#toggle_tag('estimates', 'tiny')
    " nnoremap <unique> <buffer> <localleader>tt :GtEtiny<CR>

    " command! -range GtEmedium :<line1>,<line2>call taskpaper#toggle_tag('estimates', 'medium')
    " nnoremap <unique> <buffer> <localleader>tm :GtEmedium<CR>

    " command! -range GtEhuge :<line1>,<line2>call taskpaper#toggle_tag('estimates', 'huge')
    " nnoremap <unique> <buffer> <localleader>th :GtEhuge<CR>

    " command! -range GtStar :<line1>,<line2>call taskpaper#toggle_tag('~', '')
    " nnoremap <unique> <buffer> <localleader>ts :GtStar<CR>

    " command! GfAll              :execute "BstermPri! NextAll"
    " nnoremap <unique> <buffer> <localleader>fl :GfAll<CR>
    " command! GfStar             :execute "BstermPri! NextAll"    | Bsfilter @\~
    " nnoremap <unique> <buffer> <localleader>fs :GfStar<CR>
    " command! GfAllToday         :execute "BstermPri! NextAToday"
    " nnoremap <unique> <buffer> <localleader>ft  :GfAllToday<CR>
    " command! GfOnlineToday      :execute "BstermPri! NextAToday" | Bsfilter @status(online)
    " nnoremap <unique> <buffer> <localleader>fo :GfOnlineToday<CR>
    " command! GfHomeToday        :execute "BstermPri! NextAToday" | Bsfilter @status(home)
    " nnoremap <unique> <buffer> <localleader>fh :GfHomeToday<CR>
    " command! GfGooutToday       :execute "BstermPri! NextAToday" | Bsfilter @status(goout)
    " nnoremap <unique> <buffer> <localleader>fg :GfGooutToday<CR>
    " command! GfPcToday          :execute "BstermPri! NextAToday" | Bsfilter @status(pc)
    " nnoremap <unique> <buffer> <localleader>fp :GfPcToday<CR>
    " command! GfAnywhereToday    :execute "BstermPri! NextAToday" | Bsfilter @status(anywhere)
    " nnoremap <unique> <buffer> <localleader>fa :GfAnywhereToday<CR>
    " command! GfCallToday        :execute "BstermPri! NextAToday" | Bsfilter @status(call)
    " nnoremap <unique> <buffer> <localleader>fn :GfNone<CR>
    " command! GfContextNone      :execute "BstermPri! NextAToday" | Bsfilter ^\(.*@status\)\@!.*
    " command! GfPriorityNone     :execute "BstermPri! NextAToday" | Bsfilter ^\(.*@priority\)\@!.*
    " command! GfPriority123      :execute "BstermPri! NextAToday" | Bsfilter @priority(\(1\|2\|3\))

    command! GcConcealTask :call ConcealLine(".*@done.*")
    command! GcConcealClose :call ConcealLineClear()

    ""To delete a tag:
    "nnoremap <buffer> <silent> <Leader>tN
    "\    :<C-u>call Taskpaper_delete_tag('next', '')<CR>

    ""To delete the priority tag with any argument:
    "nnoremap <buffer> <silent> <Leader>tQ
    "\    :<C-u>call Taskpaper_delete_tag('priority', '')<CR>

    ""To delete only the level 1 of priority tag:
    "nnoremap <buffer> <silent> <Leader>tQ
    "\    :<C-u>call Taskpaper_delete_tag('priority', '1')<CR>

    ""To toggle a tag with an argument:
    "nnoremap <buffer> <silent> <Leader>tq
    "\    :<C-u>call Taskpaper_toggle_tag('priority')<CR>

    ""To update a tag (not delete if the tag exists):
    "nnoremap <buffer> <silent> <Leader>tq
    "\    :<C-u>call Taskpaper_update_tag('priority')<CR>
endfunction
"}}}
"function! s:renderFilterNames(){{{
function! s:renderFilterNames()
    setlocal modifiable
    "let filter_keys = sort(keys(g:v_GTD_filter))

    let i = 0
    let filter_group = keys(g:v_GTD_filter)
    for filter_group_key in filter_group
        "echo filter_group_key
        let filter_keys = sort(keys(g:v_GTD_filter[filter_group_key]))
        let i = i + 1
        call setline(i, filter_group_key)
        for filter in filter_keys
            call setline((i + index(filter_keys, filter) + 1), "\t" . filter)
        endfor
        let i = i + len(filter_keys)
    endfor

    setlocal nomodifiable
endfunction

"}}}
"function! s:applyFilter(filter_name){{{
function! s:applyFilter(filter_name)

    let filter_group = keys(g:v_GTD_filter)
    for filter_group_key in filter_group
        " let filter_keys = sort(keys())
        " for filter in filter_keys
        "     
        " endfor
        if has_key(g:v_GTD_filter[filter_group_key], a:filter_name)
            let dic_filter = g:v_GTD_filter[filter_group_key][a:filter_name]['filter']
            "echo g:v_GTD_filter[filter_group_key][a:filter_name]
            for key in dic_filter
                execute 'Bsfilter ' . key
            endfor
        "else
        "    echo a:filter_name . " can't be found"
        endif
    endfor
endfunction
"}}}
"function! s:getBsgrepPattern(filter_name){{{
function! s:getBsgrepPattern(filter_name)
    let filter_group = keys(g:v_GTD_filter)
    for filter_group_key in filter_group
        if has_key(g:v_GTD_filter[filter_group_key], a:filter_name)
            let dic_grep = g:v_GTD_filter[filter_group_key][a:filter_name]['grep']
            "echo g:v_GTD_filter[filter_group_key][a:filter_name]
            "echo dic_grep
            for key in dic_grep
                let pt = key
            endfor
            return pt
        " else
        "     echo a:filter_name . " can't be found"
        "     return ''
        endif
    endfor
endfunction
"}}}
"function! s:getSidebarWinNum(){{{
function! s:getSidebarWinNum()
    if exists("t:vGTDSidebar_SidebarBufName")
        return bufwinnr(t:vGTDSidebar_SidebarBufName)
    else
        return -1
    endif
endfunction
"}}}
"function! s:isSidebarOpen(){{{
function! s:isSidebarOpen()
    return s:getSidebarWinNum() != -1
endfunction
"}}}
"function! s:getFilterUnderCursor(){{{
function! s:getFilterUnderCursor()
    let str = getline(line("."))
    return substitute(str, "\t", "", "g")
endfunction
"}}}
"function! s:exec(cmd){{{
function! s:exec(cmd)
    let old_ei = &ei
    set ei=all
    exec a:cmd
    let &ei = old_ei
endfunction
"}}}
"function! s:closeSidebar(){{{
function! s:closeSidebar()
    if !s:isSidebarOpen()
        throw "vGTD Sidebar.FoundError: no sidebar is open"
    endif

    if winnr("$") != 1
        if winnr() == s:getSidebarWinNum()
            call s:exec("wincmd p")
            let bufnr = bufnr("")
            call s:exec("wincmd p")
        else
            let bufnr = bufnr("")
        endif

        call s:exec(s:getSidebarWinNum() . " wincmd w")
        close
        call s:exec(bufwinnr(bufnr) . " wincmd w")
    else
        close
    endif
endfunction
"}}}
"function! s:createSidebarWin(){{{
function! s:createSidebarWin()
    "create the nerd tree window
    let splitLocation = g:vGTDSidebar_WinPos ==# "left" ? "topleft " : "botright "
    let splitSize = g:vGTDSidebar_Width
    if !exists('t:SidebarOpened')
        let t:SidebarOpened = 1
        silent! exec splitLocation . 'vertical ' . splitSize . ' new'
        silent! exec "edit " . t:vGTDSidebar_SidebarBufName
    else
        silent! exec splitLocation . 'vertical ' . splitSize . ' split'
        silent! exec "buffer " . t:vGTDSidebar_SidebarBufName
    endif

    setlocal winfixwidth
    call s:setCommonBufOptions()
endfunction
"}}}
"function! s:setCommonBufOptions(){{{
function! s:setCommonBufOptions()
    "throwaway buffer options
    "setlocal filetype=vo_base

    setlocal noswapfile
    setlocal buftype=nofile
    setlocal bufhidden=hide
    setlocal nowrap
    setlocal foldcolumn=0
    setlocal foldmethod=manual
    setlocal nofoldenable
    setlocal nobuflisted
    setlocal nospell

    iabc <buffer>

    setlocal cursorline

    call s:bindMappings()
endfunction
"}}}
"function! s:bindMappings(){{{
function! s:bindMappings()
    noremap <silent><buffer> <Enter> :call vGTDSidebar#VGTD_RunPattern()<CR>
endfunction
"}}}
"function! s:calDone(line){{{
" Calculates proportion of already done work in the subtree
function! s:calDone(line)
    let l:done = 0
    let l:count = 0
    let l:i = 1
    while Ind(a:line) < Ind(a:line+l:i)
        if (Ind(a:line)+1) == (Ind(a:line+l:i))
            let l:childdoneness = s:calDone(a:line+l:i)
            if l:childdoneness >= 0
               let l:done = l:done + l:childdoneness
               let l:count = l:count+1
            endif
        endif
        let l:i = l:i+1
    endwhile
   let l:proportion=0
   "echo getline(a:line)
   if l:count>0
     let l:proportion = ((l:done * 100)/l:count)/100
   else
      if match(getline(a:line),"@done") != -1
      "if match(getline(a:line),"\\[X\\]") != -1 l
          let l:proportion = 100
      else
          let l:proportion = 0
      endif
   endif
   call setline(a:line,substitute(getline(a:line),"[0-9]*%",l:proportion."%",""))
   if l:proportion == 100
      "call setline(a:line,substitute(getline(a:line),"\\[.\\]","[X]",""))
      if getline(a:line) !~ "@done"
          call setline(a:line,substitute(getline(a:line),"$"," @done",""))
      endif
      return 100
   elseif l:proportion == 0 && l:count == 0
      if match(getline(a:line),"@done") != -1 
          return 100
      " elseif match(getline(a:line),"\\[_\\]") != -1
        " return 0
      else
          return 0 
          "return -1
      endif
   else
      "call setline(a:line,substitute(getline(a:line),"\\[.\\]","[_]",""))
      return l:proportion
   endif
endf
"}}}
"}}}

"functions exported{{{
"concealing done tasks by default{{{
function! vGTDSidebar#VGTD_ConcealInline(expr)
    "exe ":syntax match " . w:matchgroup . " \"" . a:expr . "\"" . " conceal containedin = ALL"
    exe ":syntax match " . t:vGTDSidebar_ConcealMatchGroupName . " \"" . a:expr . "\"" . " conceal cchar= containedin = ALL"
    set conceallevel=1
    set concealcursor=c
endfunction

function! vGTDSidebar#VGTD_ConcealLine(expr)
    "exe ":syntax match " . w:matchgroup . " \"" . a:expr . "\"" . " conceal containedin = ALL"
    exe ":syntax match " . t:vGTDSidebar_ConcealMatchGroupName . " \"" . a:expr . "\"" . " conceal cchar= containedin = ALL"
    set conceallevel=1
endfunction

function! vGTDSidebar#VGTD_ConcealLineClear()
    exe ":syntax clear " . t:vGTDSidebar_ConcealMatchGroupName
    set conceallevel=0
endfunction
"}}}
"function! vGTDSidebar#VGTD_RunPattern(){{{
function! vGTDSidebar#VGTD_RunPattern()
    let pt_str = s:getFilterUnderCursor()
    let expt = s:getBsgrepPattern(pt_str)
    if expt != ''
        wincmd w
        execute "Bsgrep! " . expt
        call s:applyFilter(pt_str)
    endif
endfunction
"}}}
"function! vGTDSidebar#VGTD_toggleSidebar(){{{
function! vGTDSidebar#VGTD_toggleSidebar()
    if !s:isSidebarOpen()
        call s:createSidebarWin()
        " if !&hidden
        "     call s:renderFilterNames()
        " endif
        call s:renderFilterNames()
    else
        call s:closeSidebar()
    endif
endfunction
"}}}
"function! vGTDSidebar#VGTD_initEnviron(){{{
function! vGTDSidebar#VGTD_initEnviron()
    call s:defaultMapping()
    call vGTDSidebar#VGTD_ConcealLine(".*@done.*")
    call vGTDSidebar#VGTD_ConcealInline("@id(.*)")
    set foldtext=vGTDSidebar#VGTD_MyFoldText()
endfunction
"}}}
"function! vGTDSidebar#VGTD_MyFoldText(){{{
function! vGTDSidebar#VGTD_MyFoldText()
    let l:foldtext = MyFoldText()
    let l:foldtext = substitute(l:foldtext,'@id(.\{-})','','g')
    "echo l:foldtext
    return l:foldtext
endfunction
"}}}
"function! vGTDSidebar#VGTD_startLog(){{{
function! vGTDSidebar#VGTD_startLog(mode, ...)
python << EOF
import sys, vim
if not vim.eval("s:script_dir") in sys.path:
    sys.path.append(vim.eval("s:script_dir"))

import vGTDTimer

mode = vim.eval("a:mode")
if mode == 'tm':
    vGTDTimer.VimTimerHelper().startTimerLog()
elif mode == 'ct':
    minutes = vim.eval("a:1") #or vim.eval("a:0")
    vGTDTimer.VimTimerHelper().startCountdownLog(int(minutes)*60)

#default is 10 scond
# setShowNewtimeInterval(itv):
#default is 2 second
# setSurveillantPace(pace):
EOF
endfunction

" "function! vGTDSidebar#VGTD_startTimerLog(){{{
" function! vGTDSidebar#VGTD_startTimerLog()
" python << EOF
" import vGTDTimer
" vGTDTimer.VimTimerHelper().startTimerLog()
" EOF
" endfunction
" "}}}
" "function! vGTDSidebar#VGTD_startCountdownLog(minutes){{{
" function! vGTDSidebar#VGTD_startCountdownLog(minutes)
" python << EOF
" import vim
" import vGTDTimer
" 
" minutes = vim.eval("a:minutes") #or vim.eval("a:0")
" vGTDTimer.VimTimerHelper().startCountdownLog(int(minutes)*60)
" EOF
" endfunction
"}}}
"}}}

"default filter setting{{{
if !exists("g:v_GTD_filter")
    let g:v_GTD_filter = {
                \ 'Status' : 
                \ {
                    \ 'Next(All)' :
                        \ {
                        \ 'filter': [],
                        \ 'grep': ['^.*@due\(.*@done\)\@!.*$']
                        \ },
                    \ '*Starred' : 
                        \ {
                        \ 'filter': ['\~'],
                        \ 'grep': ['^.*@due\(.*@done\)\@!.*$']
                        \ },
                    \ 'Today All' : 
                        \ {
                        \ 'filter': [],
                        \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                        \ }
                 \ }
             \ }
                " \ },
                " \ 'Context' : 
                " \ {
                "     \ 'Today @online' :
                "         \ {
                "         \ 'filter': ['@status(online)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @home' : 
                "         \ {
                "         \ 'filter': ['@status(home)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @goout' :
                "         \ {
                "         \ 'filter': ['@status(goout)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @pc' : 
                "         \ {
                "         \ 'filter': ['@status(pc)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @anywhere' : 
                "         \ {
                "         \ 'filter': ['@status(anywhere)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @call' :
                "         \ {
                "         \ 'filter': ['@status(call)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'no context' : 
                "         \ {
                "         \ 'filter': ['^\(.*@status\)\@!.*'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                " \ },
                " \ 'Context' : 
                " \ {
                "     \ 'Today @online' :
                "         \ {
                "         \ 'filter': ['@status(online)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @home' : 
                "         \ {
                "         \ 'filter': ['@status(home)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @goout' :
                "         \ {
                "         \ 'filter': ['@status(goout)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @pc' : 
                "         \ {
                "         \ 'filter': ['@status(pc)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @anywhere' : 
                "         \ {
                "         \ 'filter': ['@status(anywhere)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'Today @call' :
                "         \ {
                "         \ 'filter': ['@status(call)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                "     \ 'no context' : 
                "         \ {
                "         \ 'filter': ['^\(.*@status\)\@!.*'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "         \ },
                " \ },
                " \ 'Priority' :
                " \ {
                "     \ 'no priority' : 
                "     \ {
                "         \ 'filter': ['^\(.*@priority\)\@!.*'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "     \ },
                "     \ 'Today Pi=1' : 
                "     \ {
                "         \ 'filter': ['@priority(1)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "     \ },
                "     \ 'Today Pi=2' : 
                "     \ {
                "         \ 'filter': ['@priority(2)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "     \ },
                "     \ 'Today Pi=3' : 
                "     \ {
                "         \ 'filter': ['@priority(3)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "     \ },
                "     \ 'Today Pi=4' : 
                "     \ {
                "         \ 'filter': ['@priority(4)'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "     \ },
                "     \ 'Today Pi>=4' : 
                "     \ {
                "         \ 'filter': ['@priority(\(1\|2\|3\|4\))'],
                "         \ 'grep': ['^.*@due(\(' . s:getMyWeekNoStr() . '\|' . s:getWeekPatternBefToday() . '\))\(.*@done\)\@!.*$']
                "     \ }
            "     \ }
            " \ }
endif
"}}}
