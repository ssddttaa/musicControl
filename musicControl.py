from omxplayer import OMXPlayer
from time import sleep
import serial

globalPlayer = None

currentSongIndex = 0

isPaused = False

songList = []

path = "/songLists/"

port = serial.Serial("/dev/ttyS0", 57600, timeout=0.5)

volumeAngle = 45.0
volumeScale = 100

def skipAhead():
    nextsong()
    pass

def skipBack():
    prevSong()
    pass

def pause():
    pauseSong()
    pass

def play():
    playSong()
    pass

while port.inWaiting() < 4:
    pass

currentHeading = ord(port.read())
currentSide = ord(port.read())

currentHeading = ord(port.read())
currentSide = ord(port.read())

print currentSide, currentHeading

volume = 0.5 * volumeScale
deltaVolume = 0

def readSongData():
    global songList

    names = open(path + "songNames.txt")
    songList = names.splitlines()

while True:
    readSongData()
    globalPlayer = OMXPlayer(path + songList[0])
    if(not globalPlayer.is_playing() and not isPaused):
        nextsong()

    while port.inWaiting() < 2:
        pass
    newHeading = ord(port.read())
    newSide = ord(port.read())

    if(newSide == 3 or newSide == 6):
        if(currentSide != 3 and currentSide != 6):
            pause()

    if(currentSide == 3 or currentSide == 6):
        if(newSide != 3 and newSide != 6):
            play()

    if(currentSide == 1):
        if(newSide == 5):
            skipAhead()
        if(newSide == 2):
            skipBack()
    elif(currentSide == 2):
        if(newSide == 1):
            skipAhead()
        if(newSide == 4):
            skipBack()
    elif(currentSide == 4):
        if(newSide == 2):
            skipAhead()
        if(newSide == 5):
            skipBack()
    elif(currentSide == 5):
        if(newSide == 4):
            skipAhead()
        if(newSide == 1):
            skipBack()


    if(abs(newHeading - currentHeading) > volumeAngle):
        if(newHeading - currentHeading > 0):
            dif = 255 - newHeading + currentHeading + 1
            deltaVolume = (0 - dif) / volumeAngle * volumeScale
        else:
            dif = newHeading + 1 + 255 - currentHeading
            deltaVolume = dif / volumeAngle * volumeScale
    else:
        deltaVolume = (newHeading - currentHeading) / volumeAngle * volumeScale

    volume += deltaVolume

    if(volume > volumeScale):
        volume = volumeScale

    if(volume < 0):
        volume = 0

    currentHeading = newHeading

    print newSide, newHeading, volume, deltaVolume


def pauseSong():
    global isPaused
    isPaused = True
    globalPlayer.pause()

def playSong():
    global isPaused
    isPaused = False
    globalPlayer.play()

def prevSong():
    global path
    global currentSongIndex
    if(currentSongIndex < 0 and globalPlayer.is_playing()):
        currentSongIndex = len(songList)
    else:
        currentSongIndex = currentSongIndex - 1

    globalPlayer = OMXPlayer(path + songList[currentSongIndex])
    globalPlayer.play()

def nextsong():
    global currentSongIndex
    global path
    if(currentSongIndex >= len(songList) and globalPlayer.is_playing()):
        currentSongIndex = 0
    else:
        currentSongIndex = currentSongIndex + 1

    globalPlayer = OMXPlayer(path + songList[currentSongIndex])
    globalPlayer.play(currentSongIndex)
