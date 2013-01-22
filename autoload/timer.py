# coding: utf-8
from Tkinter import *
from threading import Thread
from tkMessageBox import showinfo
import tkMessageBox
import time
import datetime
import os
import getopt
# import ConfigParser, os
import logging
import logging.config

soundFile = 'C:/Program Files/CONEXANT/SAII/BlueStream.wav'
flagFile = os.path.expandvars('$temp') + '/pypomo'
vimDoneFlag = 'vimDone'

task_file = ''
task_name = ''

task_lineno = ''
countdown_interval = '25'
stopwatch_mode = False
run_now = False



def playSound():
    if sys.platform[:5] == 'linux':
        import os
        os.popen2('aplay -q' + soundFile)
    else:
        import winsound
        winsound.PlaySound(soundFile, winsound.SND_FILENAME)


def ctDone():
    lh = LogHandler(task_file)
    lh.log_out(str(countdown_interval))

    playSound()
    showinfo('Oh!','Time is over!')


class LogHandler():
    def __init__(self, filename):
        now = datetime.datetime.now()
        week_no = now.strftime("%U")
        week_no = str(int(week_no) + 1)
        week_day = now.strftime("%w")
        if week_day == "1" or week_day == "0":
            #get last week log
            week_no = '%02d' % (int(week_no) - 1)
        else:
            #get this week log
            week_no = '%02d' % (int(week_no))

        self.log_file = filename + '.' + now.strftime("%Y-%m_") + week_no + '.csv'
        #self.log_file = filename + '.' + now.strftime("%Y-%m_") + (week_no if now.strftime("%w") != "0" else str(int(week_no) - 1)) + '.csv'

    def log_in(self, taskname):
        f = file(self.log_file, 'a')
        f.write(datetime.datetime.now().strftime("%Y-%m-%d") + "," + datetime.datetime.now().strftime("%H:%M") + "," + taskname + ",")
        f.close()

    def log_out(self, taskinterval):
        f = file(self.log_file, 'a')
        f.write(taskinterval + "\n")
        f.close()

class checkflagfile(Thread):
    # def __init__(self,func):
    #     Thread.__init__(self)
    #     self.func=func
    over=False
    def __init__(self):
        Thread.__init__(self)

    def vimDone(self):
        str = open(flagFile).read()
        logger.debug('flag file:' + str)
        str.rstrip()
        str.rstrip('\n')
        str.rstrip('\r')

        if str == vimDoneFlag:
            # print 'vim done'
            # return True
            if t:
                if tkMessageBox.askokcancel("Stop", "Task in vim was marked DONE, Stop the timer?"):
                    t.st()
                    return True
            else:
                return True

        return False

    def kill(self): self.over=True

    def run(self):
        while not self.over:
            #logger.debug('self.over:' + str(self.over))
            time.sleep(2)
            vimStop = self.vimDone()
            if vimStop:
                return

        global cff
        cff = None

class Timer(Thread):
    over=False
    pause=False
    def __init__(self, func):
        Thread.__init__(self)
        self.func=func
        #self.setDaemon(True)
    def run(self):
        global t, root
        time.sleep(1)
        finish = False
        while not self.over and not finish:
            if not self.pause:
                finish = self.func()
            time.sleep(1)
        if finish:
            #root.focus_force()
            root.event_generate('<<pop>>', when='tail')
        t = None

    def kill(self): self.over=True
    def paus(self): self.pause=True
    def cont(self): self.pause=False

def usage():
    print ('python Timer.py -f [task file with full path] -t [task name] -l [line number]'
    '\n -h help'
    '\n -i [countdown interval],25 by defauly'
    '\n -s stopwatch mode, timer by default'
    '\n -r start right now, wait by default')


def show():
    global e1,e2,sec
    e1.set('%.2d'%(sec/60))
    e2.set('%.2d'%(sec%60))
def down():
    global timer_mode
    timer_mode = "ct"

    global sec
    if sec:
        sec-=1;show()
        return False
    else: return True
def up():
    global timer_mode
    timer_mode = "st"

    global sec
    sec+=1;show()
    return False

def st():
    global sec,t
    if t:t.cont();return
    sec=0;show()
    t=Timer(up)

    lh = LogHandler(task_file)
    lh.log_in(task_name)

    t.start()

def cd():
    global sec,t
    global countdown_interval

    if t:t.cont();return
    #print sec
    #print e1.get()
    if e1.get() == "" and e2.get() == "":
        sec = countdown_interval*60
        show()
    elif int(e1.get()) == 0 and int(e2.get()) == 0:
        sec = countdown_interval*60
        show()
    else:
        sec=0
        try: sec=int(e1.get())*60
        except Exception:pass
        try: sec+=int(e2.get())
        except Exception:pass
        if not sec: return

    show()
    t=Timer(down)

    lh = LogHandler(task_file)
    lh.log_in(task_name)

    t.start()

    pass

def pus():
    global t
    t.paus()

def stp():
    global t,sec
    global timer_mode,countdown_interval

    if sec:
        lh = LogHandler(task_file)

        if timer_mode == "ct":
            lh.log_out(str(countdown_interval - sec/60))
        else:
            lh.log_out(str(sec/60))

    sec=0;show()
    if t: t.kill()
    t=None


def writeFlagFile(str):
    f = file(flagFile, 'w')
    f.write(str)
    f.close()

def closew():
    if t:
        if tkMessageBox.askokcancel("Quit", "Timer is running,Do you want to stop it then quit?"):
            st()
        else:
            return

    global cff
    cff.kill()
    time.sleep(2)
    os.remove(flagFile)
    root.destroy()

def initGUI():
    en1=Entry (root, textvariable=e1 ,width=10 ,justify=RIGHT)
    en2=Entry (root, textvariable=e2 ,width=10)
    en3=Text (root, width=20,  height=3)
    lb=Label (root, text=':' )
    stbtn=Button(root ,width=10,text='start',command =st)
    cdbtn=Button(root ,width=10,text='countdown',command =cd)
    pusbtn=Button(root ,width=10,text='pause',command =pus)
    stpbtn=Button(root ,width=10,text='stop',command =stp)

    en1.grid(row=0, column=0,)
    lb .grid(row=0, column=1)
    en2.grid(row=0, column=2)
    stbtn.grid(row=1, column=0)
    cdbtn.grid(row=1, column=2)
    pusbtn.grid(row=2, column=0)
    stpbtn.grid(row=2, column=2)
    en3.grid(row=3, column=0, columnspan=3, rowspan=3)

    task_name_without_id = task_name.split('@')[0].decode('gbk')
    en3.insert(INSERT, task_name_without_id + "\n" + str(countdown_interval) + "\n" + task_lineno + "\n" + 'stopwatch mode:' + str(stopwatch_mode) + "\n" + 'run now:' + str(run_now) + "\n" + task_file)

    root.protocol("WM_DELETE_WINDOW", closew)

    if run_now:
        if stopwatch_mode:
            cd()
        else:
            st()

    root.mainloop()


def parseOpts():
    # parse command line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hsrf:t:l:i:", ["help"])
    except getopt.error, msg:
        print msg
        usage()
        sys.exit(2)

    global task_file, task_name, task_lineno, countdown_interval, stopwatch_mode, run_now

      #Process options
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        if o in ("-f"):
            task_file = a
        elif o == "-t":
            task_name = a
        elif o == "-l":
            task_lineno = a
        elif o == "-i":
            countdown_interval = int(a)
        elif o == "-s":
            stopwatch_mode = True
        elif o == "-r":
            run_now = True

    if task_file == '' or task_name == '':
        print "task file or task name can't be empty"
        sys.exit(2)

    logger.debug('task file:' + task_file)
    logger.debug('task name:' + task_name)
    logger.debug('line number:' + task_lineno)
    logger.debug('countdown interval:' + str(countdown_interval))
    logger.debug('stopwatch mode:' + str(stopwatch_mode))
    logger.debug('run now:' + str(run_now))



t = None
cff = checkflagfile()
sec = None
root = Tk()
root.bind('<<pop>>', lambda event = None: ctDone())
e1 = StringVar()
e2 = StringVar()
einfo = StringVar()

if __name__ == '__main__':
    logging.config.fileConfig("e:/Backup/My Dropbox/Apps/Vim/bundle_vundle/Vim-vGTDSidebar/base.cfg")
    logger = logging.getLogger('root')

    parseOpts()
    writeFlagFile('start')

    cff.start()
    #cff = checkflagfile().start()

    initGUI()
