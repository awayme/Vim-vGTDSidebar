#-*- coding: utf-8 -*-

import datetime
import sys
import vim
import timer2
import os
import subprocess

class RoTimer(object):

    def __init__(self):
        self.timer = None
        self.status_flag = {'stop':1, 'running':2, 'pause':3}
        self.mode_flag = {'timer':1, 'countdown':2}
        self.status = self.status_flag['stop']
        self.mode = self.mode_flag['timer']
        self.count_delta = 0
        self.timer_pace = 1000

    def getCountDelta(self):
        return self.count_delta

    def __timerCallback(self, func_callback):
        if self.status == self.status_flag['running']:
            if self.mode == self.mode_flag['timer']:
                self.count_delta += self.timer_pace
                func_callback()

            if self.mode == self.mode_flag['countdown']:
                self.count_delta -= self.timer_pace
                func_callback()
                if self.count_delta <= 0:
                    self.cmdStop()

    def getMode(self):
        return self.mode

    def getStatus(self):
        return self.status

    def cmdStartTimer(self, func_callback=None):
        if func_callback == None:
            func_callback = self.display_count
        self.mode = self.mode_flag['timer']
        self.cmdStart(func_callback)

    def display_count(self):
        sec = self.getCountDelta()/self.timer_pace
        sys.stdout.write("\r" + '%.2d'%(sec/(60)) + ':' + '%.2d'%(sec%(60)))

    def cmdStartCountdown(self, interval, func_callback=None):
        if func_callback == None:
            func_callback = self.display_count
        self.mode = self.mode_flag['countdown']
        self.countdown_interval = interval
        self.count_delta = self.countdown_interval
        self.cmdStart(func_callback)

    def cmdStart(self, func_callback):
        self.timer = timer2.Timer()
        self.timer.apply_interval(self.timer_pace, self.__timerCallback, [func_callback])
        self.status = self.status_flag['running']

    def cmdStop(self):
        self.status = self.status_flag['stop']
        self.count_delta = 0
        self.timer.stop() # stops the thread and joins it.

    def cmdPause(self):
        self.status = self.status_flag['pause']

    def cmdResume(self):
        self.status = self.status_flag['running']

class VimTimer(RoTimer):
    def __init__(self):
        RoTimer.__init__(self)
        (row, col) = vim.current.window.cursor
        self.task_row = row - 1
        self.cur_line = vim.current.line
        self.vim_buffer = vim.current.buffer
        self.start_date = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        self.vim_cmd_tag = {'stop':'@stp', 'pause':'@pse', 'resume':'@rsm'}
        self.show_newtime_interval = 10 #in second

    def setShowNewtimeInterval(self, itv):
        self.show_newtime_interval = itv

    def flush_line(self):
        p = self.cur_line.find('@id')
        t = self.start_date
        sec = self.count_delta/self.timer_pace
        tstr = '%.2d'%(sec/(60)) + ':' + '%.2d'%(sec%(60))

        if sec % self.show_newtime_interval == 0 or sec <= 1:
            if p >= 0:
                newline = self.cur_line[0:p] + '@log(' + t + '/' + tstr + ') ' + self.cur_line[p:len(self.cur_line)]
            else:
                newline = self.cur_line + ' @log(' + t + '/' + tstr + ')'

            self.vim_buffer[self.task_row] = newline

    def startCountdownLog(self, interval):
        RoTimer.cmdStartCountdown(self, interval, self.flush_line)

    def startTimerLog(self):
        RoTimer.cmdStartTimer(self, self.flush_line)

    def stopLog(self):
        if self.mode == self.mode_flag['timer']:
            self.cmdStop()
            # self.__removeTag('@stp')
            self.__removeTag(self.vim_cmd_tag['stop'])

        if self.mode == self.mode_flag['countdown']:
            p = self.cur_line.find('@id')
            t = self.start_date
            sec = (self.countdown_interval - self.count_delta)/self.timer_pace
            tstr = '%.2d'%(sec/(60)) + ':' + '%.2d'%(sec%(60))
            # print tstr

            if p >= 0:
                newline = self.cur_line[0:p] + '@log(' + t + '/' + tstr + ') ' + self.cur_line[p:len(self.cur_line)]
            else:
                newline = self.cur_line + ' @log(' + t + '/' + tstr + ')'

            self.vim_buffer[self.task_row] = newline
            self.__removeTag(self.vim_cmd_tag['stop'])

    def pauseLog(self):
        self.cmdPause()

    def resumeLog(self):
        self.__removeTag(self.vim_cmd_tag['pause'] + ' ')
        self.cmdResume()
        self.__removeTag(self.vim_cmd_tag['resume'] + ' ')

    def __removeTag(self, tag):
        newline = self.vim_buffer[self.task_row].replace(tag, '')
        self.vim_buffer[self.task_row] = newline

class VimTimerHelper(VimTimer):
    def __init__(self):
        VimTimer.__init__(self)
        self.over=False
        self.surveillant_pace = 2000

        (row, col) = vim.current.window.cursor
        self.task_row = row - 1
        self.vimbuf = vim.current.buffer

    #pace in second
    def setSurveillantPace(self, pace):
        self.surveillant_pace = pace * self.timer_pace

    def __aft_countdown(self):
        INTERPRETER = "c:\Python27\pythonw.exe"
        if not os.path.exists(INTERPRETER):
            print ("Cannot find INTERPRETER at path \"%s\"." % INTERPRETER)

        processor = "bell.py"
        pargs = [INTERPRETER, processor]
        subprocess.Popen(pargs)

    def startTimerLog(self):
        VimTimer.startTimerLog(self)
        self.__run()

    #intveral in second
    def startCountdownLog(self, interval):
        VimTimer.startCountdownLog(self, interval * self.timer_pace)
        self.__run()

    def __timerCallback(self):
        line = self.vimbuf[self.task_row]

        # print datetime.datetime.now().strftime("%M:%S ") + str(VimTimer.getStatus(self))
        if VimTimer.getStatus(self) == self.status_flag['stop']:
            # print 'timer stop'
            VimTimer.stopLog(self)
            self.__aft_countdown()
            self.sv_timer.stop() # stops the thread and joins it.

        if line.find(self.vim_cmd_tag['resume']) > -1:
            # print 'find rsm'
            VimTimer.resumeLog(self)
        elif line.find(self.vim_cmd_tag['pause']) > -1:
            # print 'find pse'
            VimTimer.pauseLog(self)
        elif line.find(self.vim_cmd_tag['stop']) > -1:
            # print 'find stp'
            VimTimer.stopLog(self)
            self.sv_timer.stop() # stops the thread and joins it.

    def __run(self):
        self.sv_timer = timer2.Timer()
        self.sv_timer.apply_interval(self.surveillant_pace, self.__timerCallback)
