Set objPlayer = CreateObject("WMPlayer.OCX")
Set objMedia = objPlayer.newMedia("assets_music.mp3")
objPlayer.currentMedia = objMedia
objPlayer.controls.play

' Keep script running to allow the music to play
WScript.Sleep(9690) ' Adjust time in milliseconds (10 seconds)
