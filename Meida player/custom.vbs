Set objPlayer = CreateObject("WMPlayer.OCX")
Set objMedia = objPlayer.newMedia("<choose your own directory>")
objPlayer.currentMedia = objMedia
objPlayer.controls.play

' Keep script running to allow the music to play
WScript.Sleep(9690) ' Adjust time in milliseconds (10 seconds)
