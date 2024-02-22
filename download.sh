#!/bin/bash

deactivate

python3 -m venv yt_venv
. yt_venv/bin/activate

#/volume2/Storage/Music/Youtube/yt_venv/bin/python3 -m pip install --upgrade pip
#pip install moviepy
#pip install pytube
#pip install eyed3

/volume2/Storage/Music/Youtube/yt_venv/bin/python3 /volume2/Storage/Music/Youtube/youtube.py | tee /volume2/Storage/Music/Youtube/log.txt

deactivate
