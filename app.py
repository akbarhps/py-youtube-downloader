import os
import re
import sys
import subprocess
from pytube import YouTube
from pytube import Playlist
from pytube.cli import on_progress
import moviepy.editor as moviepy


FOLDER_AUDIO = 'Audio'
FOLDER_VIDEO = 'Video'

file_type = ''


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def open_file_explorer(file_path):
    subprocess.Popen(
        r'explorer /select,"{}"'.format(file_path))


def convert_mp4_to_mp3(file_path):
    clear_terminal()
    print('Converting file...')
    mp4_path = os.path.join(file_path)
    mp3_path = os.path.join(os.path.splitext(file_path)[0]+'.mp3')
    new_file = moviepy.AudioFileClip(mp4_path)
    new_file.write_audiofile(mp3_path)
    os.remove(mp4_path)


def get_youtube_url():
    url = input('Insert youtube Url: ')
    download_video(url)


def get_file_type():
    global file_type

    clear_terminal()
    while True:
        file_type = input(
            f'Download as\n[0] Exit\n[1] MP4 (Video)\n[2] MP3 (Audio)\n\n(number) >>> ')

        if file_type == '1' or file_type == '2':
            break
        elif file_type == '0':
            exit()

    return file_type


def download_video(url):
    try:
        youtube = YouTube(url, on_progress_callback=on_progress,
                          on_complete_callback=on_complete).streams
    except:
        clear_terminal()
        print("url: {}\nError occured\n- Check your connection\n- Check your url\n\n".format(url))
        get_youtube_url()

    file_type = get_file_type()
    file_path = generate_folder_path(file_type)

    if file_type == '1':
        video_itag = get_video_itag(youtube)
        selected_vid = youtube.get_by_itag(video_itag)
    else:
        selected_vid = youtube.filter(only_audio=True).first()

    clear_terminal()
    print('Downloading {}'.format(selected_vid.title))

    try:
        selected_vid.download(file_path)
    except:
        print("Connection Error")


def generate_folder_path(file_type):
    folder_name = FOLDER_VIDEO if(file_type == '1') else FOLDER_AUDIO
    home = os.path.expanduser('~')
    return os.path.join(home, 'Downloads\\YoutubeDownloader\\{}'.format(folder_name))


def get_video_itag(youtube):
    selected = -1
    qualities = {}
    filtered_data = youtube.filter(
        progressive=True, file_extension='mp4').order_by('resolution').desc()

    clear_terminal()
    print('[0] [Exit]')

    for i, data in enumerate(filtered_data):
        qualities[i+1] = data
        res = data.resolution
        fps = data.fps
        print(f'[{i+1}] [Quality: {res} {fps}fps]')

    while selected not in qualities.keys():
        selected = int(
            input('Select video quality (number: 0 - {}):\n>>> '.format(len(qualities))))
        if selected in qualities.keys():
            break
        elif selected == 0:
            exit()

    return qualities[selected].itag


def on_complete(itag, file_path):
    global file_type

    if file_type == '2':
        convert_mp4_to_mp3(file_path)
        file_path = os.path.join(os.path.splitext(file_path)[0]+'.mp3')

    clear_terminal()
    print('Download Success\nFile location: {}'.format(file_path))

    is_open_file = input('Open file explorer? (y/n): ')
    if is_open_file == 'y' or is_open_file == 'Y':
        open_file_explorer(file_path)


###################################################################################################################

clear_terminal()
get_youtube_url()
