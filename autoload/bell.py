# coding: utf-8
import sys

soundFile = 'C:/Program Files (x86)/Workrave/share/sounds/subtle/rest-break-ended.wav'

def playSound():
    if sys.platform[:5] == 'linux':
        import os
        os.popen2('aplay -q' + soundFile)
    else:
        import winsound
        winsound.PlaySound(soundFile, winsound.SND_FILENAME)

if __name__ == '__main__':
    playSound()
