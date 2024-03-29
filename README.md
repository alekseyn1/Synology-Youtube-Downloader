# Youtube Playlist Downloader Python script. Great for Synology NAS
Python download script to get mp3 from YouTube playlists

Place this script and ```playlists_to_download.txt``` into the same folder on any volume / share on your Synology NAS

My car mp3 player only understands a certain mp3 bitrate so I had to come up with this script

When the script runs, it creates a folder structure per playlist as follows:
```
Temp
--PlaylistName mp4 files
Output
--PlaylistName
```
# What this script does:
- Input for the script is in a text file ```playlists_to_download.txt``` that contains links to YouTube playlists. One per line.
- Downloads [stream 140 from YouTube](https://github.com/alekseyn1/Synology-Youtube-Downloader/blob/main/youtube-stream-codes.md), 
- Converts mp4 to mp3 and places them into an Output folder. 
- Grabs a thumbnail from the YouTube video and writes it as cover art into every mp3 file.
- Optionally (default) adds a sequential number to the file and mp3 title for older mp3 players (like mine)

This Python script is scheduled to run every midnight in my case with this command:
```python3 /volume2/Storage/Music/Youtube/youtube.py```

Updated in Feb 2024 for Python 3.8 as the new DS has Python built in. now using download.sh script for the schedule
```bash download.sh```

You would need to adjust the path of course to your own and CHANGE THE SETTINGS SECTION in the youtube.py to match your path as well

I have also installed a free app for Synology called 'USB Copy'
This app allows to create a task to assist with exporting data to your USB drive once it is plugged in.

So once the USB disk is plugged into Synology, a full copy from the 'Output' folder will be copied to the USB drive automatically. All I need to do is wait for Synology to beep at me twice: once the copy is started and another time when it's finished and the USB is ejected.

This script is based on samples/projects related to pytube module, so if you see some of your code, please let me know and I'll credit your work.

# USB Copy Settings
![USB Copy](https://user-images.githubusercontent.com/1160500/190933704-86a9ee42-64bc-45fc-89fb-c883b2288f82.PNG)
![Capture2](https://user-images.githubusercontent.com/1160500/190933705-db67110c-d75d-4073-9f7a-e9bcc25aefb9.PNG)
![Capture3](https://user-images.githubusercontent.com/1160500/190933706-ef5cfffd-e490-48cc-b279-432bfce918b4.PNG)
![Capture4](https://user-images.githubusercontent.com/1160500/190933707-da1c0dc0-5b47-4c74-a0d6-4877f05a49cd.PNG)
![Capture5](https://user-images.githubusercontent.com/1160500/190933708-235b7c92-4d77-411c-ab2d-09b4a2efc9cb.PNG)

# Scheduled Task Settings
![Capture10](https://user-images.githubusercontent.com/1160500/190933709-cdd31694-97e6-4190-8542-73000fefbf9e.PNG)
![Capture11](https://user-images.githubusercontent.com/1160500/190933710-44ccd74b-f670-4447-ac34-f2038e3c3f4a.PNG)
![Capture12](https://user-images.githubusercontent.com/1160500/190933711-a1b353fa-520c-49e9-bd69-d12d551d9c4d.PNG)
![Capture13](https://user-images.githubusercontent.com/1160500/190933712-f12f1930-527e-4735-81ef-b9335cf2ca1e.PNG)
