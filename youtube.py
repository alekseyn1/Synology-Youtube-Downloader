#!/usr/bin/python
# coding=utf-8

#Pay attention to the permissions of the folder where this script is running from:
#if you get errors running this script from ssh (python3 tube.py) then run the below command in ssh terminal
#chmod ugo+rwx foldername 

#import subprocess
#from pathlib import Path
#import glob   

from moviepy.editor import * #to export the audio file from mp4

import re #for sanitising strings

import os #for folder check/create
import os.path
from os.path import exists

import pytube #main module for YouTube
from pytube import Playlist
from pytube import YouTube

import urllib.request #for retrieving URLs from playlists
 
import eyed3 #for manipulating id3 tags in mp3 files
from eyed3.id3.frames import ImageFrame  


#================= functions have to be defined first =================

#Function to sanitise strings
def sanitize_me(old_name):
    x = re.search(r"[^- A-Za-z0-9.]+", old_name)
    if x:
        #print('String for cleanup: ' + old_name)
        clean_name = re.sub(r"[^А-Яа-яЁёA-Za-z0-9 .-]+","",old_name)
        #print('first cleanup: ' + clean_name)
        
        #not required as REGEX takes care of this
        # return_name = ' '.join(clean_name.split())
        # print('second cleanup: ' + return_name)    
        
        return clean_name

#Function to check if the folder exists and create it if it does not
def check_folder(path):
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
      # Create a new directory because it does not exist 
      os.makedirs(path)
      print("New directory created: " + path)

#================= end of functions =================


#================= Settings ================================
#location of the script
PARENT_DIR = '/volume2/Storage/Music/Youtube'

#playlists text file that will be in the same folder as above
PLAYLISTS_FILE = 'playlists_to_download.txt'
PLAYLISTS_PATH = os.path.join(PARENT_DIR,PLAYLISTS_FILE)

#Directory with subfolders. One per playlist will be created.
OUTPUT_DIR = 'Output'

#Do you want to use sequence numbers for resulting mp3 files (001 - Song.mp3 as an example)
USE_SEQ_NUM = True

#Modify the value to download a different stream
YOUTUBE_STREAM_AUDIO = '140'
#================= End of Settings ================================

OUTPUT_FLD = os.path.join(PARENT_DIR,OUTPUT_DIR)
check_folder(OUTPUT_FLD)   

#Open the playlist file

playlists_file = open(PLAYLISTS_PATH, 'r')
pcount = 0

#Iterate lines in the playlist file. Indentation in the code is important
while True:
    pcount += 1
    # Get next line from file
    line = playlists_file.readline()
    # if line is empty - end of file is reached
    if not line:
        break
        
    print("==============================================================")
    print("Processing Playlist {}: {}".format(pcount, line.strip()))
    print("")
    
    playlist = Playlist(line.strip())
    playlist_title = playlist.title
    print("Playlist title: " + playlist_title)
        
    # this fixes the empty playlist.videos list
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    #print(len(playlist.video_urls))
    #for url in playlist.video_urls:
    #    print(url)
    
    #input("Press Enter to continue...")

    TEMP_DIR = os.path.join(PARENT_DIR,'Temp')
    check_folder(TEMP_DIR)

    DOWNLOAD_DIR = os.path.join(TEMP_DIR,playlist_title+' mp4 files')
    check_folder(DOWNLOAD_DIR)    
    
    THUMBS_DIR = os.path.join(DOWNLOAD_DIR,'Art')
    check_folder(THUMBS_DIR)
    
    SAVE_DIR = os.path.join(OUTPUT_FLD,playlist_title)
    check_folder(SAVE_DIR)

    # physically downloading the audio track
    count = 1
    for video in playlist.videos:
        print('=====> (' + str(count) + '/' + str(len(playlist)) + ') Downloading Title: '+video.title)
        count += 1        
        #pytube will not download the file if it exists. To make is faster, you can use the block below
        if os.path.exists(os.path.join(DOWNLOAD_DIR,str(video.title+'.mp4'))):
            print('MP4 File Exists')
            continue
            
        try: 
          audioStream = video.streams.get_by_itag(YOUTUBE_STREAM_AUDIO)
          audioStream.download(output_path=DOWNLOAD_DIR)
          #get thumbnail
          urllib.request.urlretrieve(video.thumbnail_url, os.path.join(THUMBS_DIR,sanitize_me(str(video.title))+'.jpg'))

        except:
             print("error "+str(IOError))
             pass
             continue

    #get a list of files
    files = filter( lambda x: os.path.isfile(os.path.join(DOWNLOAD_DIR, x)), os.listdir(DOWNLOAD_DIR) )

    #sort the files in the order they were downloaded, i.e. order they were added to the playlist
    files = sorted( files, key = lambda x: os.path.getmtime(os.path.join(DOWNLOAD_DIR, x)) )

    #Converting files to mp3
    print("")
    print("==============================================================")
    print("Starting the mp4 to mp3 conversions")
    print("")
    
    count2 = 1
    for file in files:

        if re.search('mp4', file):
            
            mp4_path = os.path.join(DOWNLOAD_DIR,file)
            print('')
            #print('Processing: '+mp4_path)
            print('=====> (' + str(count2) + '/' + str(len(os.listdir(DOWNLOAD_DIR))) + ') Converting Title: '+file)

            try:     
                file = sanitize_me(os.path.splitext(file)[0])
                
                if (USE_SEQ_NUM):
                  prefix = str(count2).zfill(3) + ' - '
                else:
                  prefix = ''
                
                
                mp3_path = os.path.join(SAVE_DIR,str(prefix + os.path.splitext(file)[0]+'.mp3'))
                count2 += 1

                #print(mp3_path)
                #print(os.path.exists(mp3_path))
                #print(mp4_path)
                #print(os.path.exists(mp4_path))

                if os.path.exists(mp3_path):
                  print('MP3 File Exists')
                  continue

                new_file = AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                
                #set mp3 cover art
                audiofile = eyed3.load(mp3_path)
                if (audiofile.tag == None):
                    audiofile.initTag()
                audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(os.path.join(THUMBS_DIR,str(os.path.splitext(file)[0]+'.jpg')),'rb').read(), 'image/jpeg')
                
                #set mp3 title tag to the video name
                #audiofile.tag.title = os.path.splitext(file)[0]
                
                #set mp3 title tag to the video name and add sequential number
                audiofile.tag.title = prefix + os.path.splitext(file)[0]
                
                #older tag standard below
                #audio.tag.save(version=eyed3.id3.ID3_V2_3)
                audiofile.tag.save()
                #os.remove(mp4_path)
            except:
                print("error "+str(IOError))
                pass
                continue
    #end WHILE loop
    

playlists_file.close()

#set the output folder time stamp to year 2000. The mp3 player in my car lists folders by date in acsending order (older folders first)
import time
import datetime
date = datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, second=0)
modTime = time.mktime(date.timetuple())
os.utime(SAVE_DIR, (modTime, modTime))