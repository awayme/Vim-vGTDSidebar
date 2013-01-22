# coding: utf-8
from Tkinter import *
from threading import Thread
from tkMessageBox import showinfo
import time,tkMessageBox
import datetime
import chardet
import os

soundFile = 'C:/Program Files/CONEXANT/SAII/BlueStream.wav'
flagFile = os.path.expandvars('$temp') + '/pypomo'
vimDoneFlag = 'vimDone'

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
        self.log_file = filename + '.' + now.strftime("%Y-%m_") + (week_no if now.strftime("%w") != "0" else str(int(week_no) - 1)) + '.csv'
        #print self.log_file

    def log_in(self, taskname): 
        f = file(self.log_file, 'a')
        #print taskname
        #print task_id
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
    def __init__(self):
        Thread.__init__(self)

    def vimDone(self):
        str = open(flagFile).read()
        str.rstrip()
        str.rstrip('\n')
        str.rstrip('\r')
        
        if str == vimDoneFlag:
            # print 'vim done'
            # return True
            root = Tk()
            root.mainloop()
            if t:
                if tkMessageBox.askokcancel("Stop", "Task in vim was marked DONE, Stop the timer?"):
                    t.st()
                    return True
            else:
                return True

        return False


    def run(self):
        while True:
            time.sleep(2)
            vimStop = self.vimDone()
            if vimStop:
                return

class Timer(Thread):
    over=False
    pause=False
    def __init__(self,func):
        Thread.__init__(self)
        self.func=func
        #self.setDaemon(True)
    def run(self):
        global t,root
        time.sleep(1)
        finish=False
        while not self.over and not finish:
            if not self.pause:
                finish=self.func()
            time.sleep(1)
        if finish:
            #root.focus_force()
            root.event_generate('<<pop>>',when='tail')
        t=None

    def kill(self): self.over=True
    def paus(self): self.pause=True
    def cont(self): self.pause=False
 
task_file=None
task_name = None
task_mode = None
task_start = None
countdown_interval = None

timer_mode = None

t=None
sec=None
root=Tk()
root.bind('<<pop>>',lambda event=None: ctDone())
e1=StringVar()
e2=StringVar()
einfo=StringVar()
 
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

def closew():
    if t:
        if tkMessageBox.askokcancel("Quit", "Timer is running,Do you want to stop it then quit?"):
            st()
        else:
            return

    os.remove(flagFile)
    root.destroy()



task_file = sys.argv[1]
task_name = sys.argv[2]
task_lineno = sys.argv[3] 
task_mode = sys.argv[4]
task_start = sys.argv[5]
countdown_interval = int(sys.argv[6])

print task_file
print task_name
print task_lineno
print task_mode
print task_start
print countdown_interval

 
en1 = Entry (root, textvariable = e1 ,width=10 ,justify=RIGHT)
en2 = Entry (root, textvariable = e2 ,width=10)
#en3 = Text (root, width=20, state = "disable", height = 3)
en3 = Text (root, width=20,  height = 3)
#en3 = Entry (root, textvariable = einfo , width=24, state = "readonly")
lb = Label (root, text = ':' )
stbtn = Button(root ,width=10,text= 'start',command =st)
cdbtn = Button(root ,width=10,text= 'countdown',command =cd)
pusbtn = Button(root ,width=10,text= 'pause',command =pus)
stpbtn = Button(root ,width=10,text= 'stop',command =stp)
 
en1.grid(row = 0 ,column = 0,)
lb .grid(row = 0 ,column = 1)
en2.grid(row = 0 ,column = 2)
stbtn.grid(row = 1 ,column = 0)
cdbtn.grid(row = 1 ,column = 2)
pusbtn.grid(row = 2 ,column = 0)
stpbtn.grid(row = 2 ,column = 2)
en3.grid(row = 3 ,column = 0,columnspan = 3, rowspan = 3)

task_name_without_id = task_name.split('@')[0].decode('gbk')
#print chardet.detect(task_name)['encoding']
#print chardet.detect(task_name_without_id)['encoding']
#task_name_without_id = task_name_without_id.decode('gbk')
#print chardet.detect( temp  )['encoding']
#print temp
#task_name_without_id = temp

en3.insert(INSERT, task_name_without_id + "\n" + str(countdown_interval) + "\n" + task_lineno + "\n" + task_mode + "\n" + task_start + "\n" + task_file)
 
root.geometry('+500+400')

# import tkMessageBox
print flagFile
f = file(flagFile, 'w')
f.write('dersu')
f.close()

checkflagfile().start()

root.protocol("WM_DELETE_WINDOW", closew)
root.mainloop ()
