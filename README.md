# Synology Youtube Downloader
Python download script to get mp3 from YouTube playlists

Place this script on any volume and share on your Synology NAS

In my case, my car mp3 player only understands a certain mp3 bitrate so I had to come up with this script

Text file playlists_to_download.txt contains YouTube playlists. One per line.
When the script runs, it creates a folder structure per playlist as follows:

Folder Temp
--PlaylistName mp4 files
Folder Output
--PlaylistName

The script downloads stream 140 from YouTube, converts mp4 to mp3 and places them into an Output folder. There is an option to add a sequential number to the file and mp3 title for older mp3 players (like mine)

This python script is scheduled to run every midnight in my case with this command:
python3 /volume2/Storage/Music/Youtube/youtube.py

You would need to adjust the path of course to your own.

I have also installed a free app for Synology called 'USB Copy'
This app allows to create a task to assist with exporting data to your USB drive once it is plugged in.

So once the USB disk is plugged into synology, a full copy from the 'Output' folder will be copied to the USB drive automatically. All I need to do is wait for Synology to beep at me twice: once the copy is started and another time when it's finished and the USB is ejected.

