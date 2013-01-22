#-*- coding: utf-8 -*-

import datetime
import sys
import vim
import timer2
import re

class RoTimer(object):

    def __init__(self):
        self.timer = None
        self.status_flag = {'stop':1, 'running':2, 'pause':3}
        self.mode_flag = {'timer':1, 'countdown':2}
        self.status = self.status_flag['stop']
        self.mode = self.mode_flag['timer']
        self.count_delta = 0
        self.timer_pace = 1000
        # self.countdown

    def getCountDelta(self):
        return self.count_delta

    def __timerCallback(self, func_callback):
        if self.status == self.status_flag['running']:
            if self.mode == self.mode_flag['timer']:
                self.count_delta += self.timer_pace
                #logger.debug(str(self.count_delta) + " passed")
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
        #self.timer.apply_interval(1000, self.timerCallback, None, None)
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

    def playSound(self):
        if sys.platform[:5] == 'linux':
            import os
            os.popen2('aplay -q' + soundFile)
        else:
            import winsound
            winsound.PlaySound(soundFile, winsound.SND_FILENAME)


    def flush_line(self):
        p = self.cur_line.find('@id')
        t = self.start_date
        sec = self.count_delta/self.timer_pace
        tstr = '%.2d'%(sec/(60)) + ':' + '%.2d'%(sec%(60))

        if sec % 10 == 0 or sec <= 1:
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
            newline = re.sub(r' @stp', '', self.vim_buffer[self.task_row])
            self.vim_buffer[self.task_row] = newline

        if self.mode == self.mode_flag['countdown']:
            p = self.cur_line.find('@id')
            t = self.start_date
            sec = (self.countdown_interval - self.count_delta)/self.timer_pace
            tstr = '%.2d'%(sec/(60)) + ':' + '%.2d'%(sec%(60))

            if p >= 0:
                newline = self.cur_line[0:p] + '@log(' + t + '/' + tstr + ') ' + self.cur_line[p:len(self.cur_line)]
            else:
                newline = self.cur_line + ' @log(' + t + '/' + tstr + ')'

            # line = self.vim_buffer[self.task_row]
            # newline = re.sub(r'\/.*?\)', '/' + tstr + ')', line)
            self.vim_buffer[self.task_row] = newline

    def pauseLog(self):
        self.cmdPause()

    def resumeLog(self):
        self.cmdResume()

class n_surveillant(object):
    # def __init__(self,func, vimtimer):
    def __init__(self, vimtimer):
        # Thread.__init__(self)
        self.soundFile = 'C:/Program Files/CONEXANT/SAII/BlueStream.wav'
        self.over=False
        # self.func=func
        self.vt = vimtimer
        self.status_flag = {'stop':1, 'running':2, 'pause':3}

        (row, col) = vim.current.window.cursor
        self.task_row = row - 1
        self.vimbuf = vim.current.buffer
        # self.cur_line = vim.current.line

    def aft_countdown(self):
        pass

    def __timerCallback(self):
        line = self.vimbuf[self.task_row]

        # print self.vt.getCountDelta()
        if self.vt.getStatus() == self.status_flag['stop']:
            print 'timer stop'
            self.vt.stopLog()
            self.timer.stop() # stops the thread and joins it.
            self.aft_countdown()

        if line.find('@stt') > -1:
            print 'find stt'
        elif line.find('@pse') > -1:
            print 'find pse'
            self.vt.pauseLog()
        elif line.find('@rsm') > -1:
            print 'find rsm'
            self.vt.resumeLog()
        elif line.find('@stp') > -1:
            print 'find stp'
            self.vt.stopLog()
            self.timer.stop() # stops the thread and joins it.

    def run(self):
        self.timer = timer2.Timer()
        self.timer.apply_interval(2000, self.__timerCallback)
