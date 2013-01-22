#-*- coding: utf-8 -*-

import chardet
import codecs
import StringIO
import time
import datetime
import os
import vim
import re
import subprocess
from threading import Thread

#flagFile = os.path.expanduser("~") + '/pypomo'

class CodecUtil:
    def convert_encoding(self, filename, target_encoding):
        source_encoding = self.getFileCodec(filename)
        f = codecs.open(filename, 'r', source_encoding)
        content = f.read().encode(target_encoding, 'ignore')
        f.close()
        return StringIO.StringIO(content)

    def getFileCodec(self, filename):
        content = codecs.open(filename, 'r').read()
        file_encoding = chardet.detect(content)['encoding']
        return file_encoding

    def convert_to_file(self, buf, target_encoding, filename):
        codecs.open(filename, 'w', encoding=target_encoding).write(buf)

class surveillant(Thread):
    over=False
    def __init__(self,func):
        Thread.__init__(self)
        self.func=func
    def run(self):
        finish=False
        while not finish:
            if self.over:
                print 'killed'
                break
            finish=self.func()
            time.sleep(1)
            if finish:
                print 'PyPomo surveilant gone'
                pass

        global s
        s = None

    def kill(self): self.over=True

class sur(Thread):
    over=False
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        i = 0
        while True:
            i += 1
            vim.current.buffer[1] = "if self.over: print killed break finish=self.func() time.sleep(1) if finish:" + str(i)
            #vim.command('call setline(1, "if self.over: print killed break finish=self.funffinish:' + str(i) + '")')
            if i > 10:
                break
            time.sleep(1)
            #vim.command("redraw")



def logit(con):
    flagFile = os.path.expandvars('$temp') + '/pypomo'
    f = file(flagFile, 'a')
    f.write(con + '\n')
    #f.write(con + '#' + str(len(line_log.split(','))) + '\n')
    f.close()

def DoneMonitor():
    global task_row, task_buf
    line = task_buf[task_row]

    #timer closed so do I
    flagFile = os.path.expandvars('$temp') + '/pypomo'
    if not os.path.exists(flagFile):
        # print 'stop:flag file' # + flagFile
        return True
    # tmep
    # else:
    #     return True

    #check vim
    vimDone = False
    if line.find('@done') > -1:
        # lg('vim @done found')
        vimDone = True

    #check timer
    timerDone = False
    now = datetime.datetime.now()
    week_no = now.strftime("%U")
    log_file = task_buf.name + '.' + now.strftime("%Y-%m_") + (week_no if now.strftime("%w") != "0" else str(int(week_no) - 1)) + '.csv'
    # lg(CodecUtil().getFileCodec(log_file))
    for line_log in file(log_file, 'r').readlines():
        if not line_log.split():
            continue
        else:
            # lg('log line:'+line_log)
            # lg('vim line:'+line.lstrip('\t'))
            # lg(str(line_log.find(line.lstrip('\t'))))
            # lg(str(len(line_log.rstrip().rstrip(',').split(','))))
            if line_log.find(line.lstrip('\t')) > -1 and len(line_log.rstrip().rstrip(',').split(',')) > 3:
                timerDone = True
            else:
                timerDone = False

    # lg('vimDone:'+str(vimDone)+' timerDone:'+str(timerDone))
    if vimDone and not timerDone:
        # lg('stop:vimDone but not timerDone')
        f = file(flagFile, 'w')
        f.write('vimDone')
        f.close()
        return True

    if not vimDone and timerDone:
        # lg('stop:not vimDone but timerDone')
        vim.command(str(task_row + 1) + "GtDone")
        return True

    return False

def logGTD(run_surveillant=True,run_now=False, ct_interval=25, stopwatch_mode=False):
    # 获取光标所在的位置
    (row, col) = vim.current.window.cursor

    global task_row, task_buf
    task_row = row - 1
    task_buf = vim.current.buffer

    # 获取当前行
    cur_line = re.sub('\t', '', vim.current.line)
    #cur_line = re.sub('\t', '', vim.current.line[col:])

    #now = datetime.datetime.now()
    #week_no = now.strftime("%U")
    buffername = vim.current.buffer.name
    #subprocess.call('timer.py')

    # INTERPRETER = "c:\Python27\python.exe"
    INTERPRETER = "c:\Python27\pythonw.exe"
    if not os.path.exists(INTERPRETER):
        print ("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER)

    processor = "e:/Backup/My Dropbox/Apps/Vim/bundle_vundle/Vim-vGTDSidebar/Timer.v2.0.py"

    pargs = [INTERPRETER, processor]
    #pargs.extend([buffername, str(cur_line), str(row), "ct", "start", "25"])
    pargs.extend(['-f',buffername])
    pargs.extend(['-t',cur_line])
    pargs.extend(['-l',str(row)])
    pargs.extend(['-i',str(ct_interval)])
    if stopwatch_mode:
        pargs.extend(['-s'])
    if run_now:
        pargs.extend(['-r'])

    # f = file('logvim.txt', 'w')
    # for p in pargs:
    #     f.write(p + ' ')
    # f.close()
    subprocess.Popen(pargs)

    if run_surveillant:
        #print surveillant
        time.sleep(2)
        global s
        s = surveillant(DoneMonitor)
        s.start()
