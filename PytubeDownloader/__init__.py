"""
Identification:
    @author: Elsio Lisboa De Almeida
    @location: Portugal
    @version: 1.0.0
Module Requirements:
    :arg = [
        native-modules: ( sys, urllib.requests, re )
        extern-modules: ( pytube )
    ]
Licenses:
"""

import sys
import urllib.request
import re
from time import sleep
from googletrans import Translator
from pytube import YouTube
from threading import Thread



class Downloader:
    def __init__(self):
        self._default_language = "en"

    def _animation_color(path_name, video_name):
        sleep(1)
        Thread(target=print(f'\033[34mDownloading \"{video_name}\" to {path_name}...'))

    def set_lang(self, new_lang):
        self._default_language = new_lang

    def get_lang(self):
        return self._default_language

    def _show_text(self, num_id, quantity, name_of_video):
        translator = Translator()
        txt = f'\n=> Video {num_id}: {name_of_video.upper()}\nExiste alguns videos parecidos, voce precisa escolher ' \
              f'apenas um, Eu recomendo o primeiro no index 0.\nPara isso voce precisa digitar um numero entr' \
              f'e 0 e {quantity}: '
        self._response_text = translator.translate(txt, dest=self._default_language).text
        return self._response_text

    """Criando uma lista de sons atraves do arquivo e colocando numa string"""

    def _file_video(self, name):

        self._songs_name = []
        try:
            with open(name, 'r') as file:
                text = file.read().split('\n')
                for id_name in range(len(text)):
                    if text[id_name] != "":
                        self._songs_name.append(text[id_name])
            return self._songs_name
        except:
            print(f'\n\033[31mERROR:Error on the file')

    """See if the name passed has space, if true join with a '+' string -> ex: gabriela morilo => gabriela+morilo """

    def _join_name(self, name):
        self._new_text = ""
        for letter in name:
            if letter == ' ':
                self._new_text += '+'
            else:
                self._new_text += letter
        return self._new_text

    """ Creating the videos urls by one file """

    def _create_urls_video_with_file(self, file_name):
        if file_name != "":
            new_url = []
            for video_list in range(len(self._file_video(file_name))):
                html = urllib.request.urlopen(
                    f'https://www.youtube.com/results?search_query={self._join_name(self._file_video(file_name)[video_list])}')
                video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                if len(video_id) > 1:
                    number_id = input(
                        f'\033[33m{self._show_text(video_list + 1, len(video_id) - 1, self._file_video(file_name)[video_list])}')
                    new_url.append(f'https://www.youtube.com/watch?v={video_id[int(number_id)]}')
                else:
                    new_url.append(f'https://www.youtube.com/watch?v={video_id[0]}')
            return new_url
        else:
            print(f'\n\033[31mERROR:It is not possible to find url videos')

    """ Creting only one url video """

    def _create_url_video(self, name):
        if name != "":
            new_url2 = None
            html = urllib.request.urlopen(f'https://www.youtube.com/results?search_query={self._join_name(name)}')
            video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            if len(video_id) > 1:
                number_id = input(f'\033[33m{self._show_text(1, len(video_id) - 1, name)}')
                new_url2 = f'https://www.youtube.com/watch?v={video_id[int(number_id)]}'
            else:
                new_url2 = f'https://www.youtube.com/watch?v={video_id[0]}'
            return new_url2
        else:
            print(f'\n\033[31mERROR:It is not possible to find url videos')

    def _create_more_url_videos(self, videos_name):
        if videos_name != "":
            new_url3 = []
            for video_list in range(len(videos_name)):
                html = urllib.request.urlopen(
                    f'https://www.youtube.com/results?search_query={self._join_name(videos_name[video_list])}')
                video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                if len(video_id) > 1:
                    number_id = input(
                        f'\033[33m{self._show_text(video_list + 1, len(video_id) - 1, videos_name[video_list])}')
                    new_url3.append(f'https://www.youtube.com/watch?v={video_id[int(number_id)]}')
                else:
                    new_url3.append(f'https://www.youtube.com/watch?v={video_id[0]}')
            return new_url3
        else:
            print(f'\n\033[31mERROR:It is not possible to find url videos')

    """Downloading many videos quickly with a file"""

    def download_videos_with_file(self, file_name, path):
        if file_name and path != "":
            if not file_name.endswith('.txt'):
                file_name = file_name + '.txt'
            urls = self._create_urls_video_with_file(file_name)
            for link in range(len(urls)):
                self._animation_color(path, self._file_video(file_name)[link])
                YouTube(urls[link]).streams.first().download(path)
                print(
                    f'\n\033[32mVideo {link + 1} downloaded with success\n\033[35mTitle: {YouTube(urls[link]).title}\nAuthor: {YouTube(urls[link]).author}\n')
        else:
            print(f'\033[31mERROR: File or Path not founded')

    """ Donwloading just one video """

    def download_one_video(self, video_name, path):
        if video_name and path != "":
            url = self._create_url_video(video_name)
            self._animation_color(path, video_name)
            YouTube(url).streams.first().download(path)
            print(
                f'\n\033[32mVideo 1 downloaded with success\n\033[35mTitle: {YouTube(url).title}\nAuthor: {YouTube(url).author}\n')
        else:
            print('\033[31mIs not possible download the video')

    def download_more_videos(self, array_video_names, path):
        if array_video_names and path != "":
            urls = self._create_more_url_videos(array_video_names)
            for link in range(len(urls)):
                self._animation_color(path, array_video_names[link])
                YouTube(urls[link]).streams.first().download(path)
                print(
                    f'\n\033[32mVideo {link + 1} downloaded with success\n\033[35mTitle: {YouTube(urls[link]).title}'
                    f'\nAuthor: {YouTube(urls[link]).author}\n')
        else:
            print(f'\033[31mIs not possible download the video')

    class download_with_command_line:
        def __init__(self):
            self.prototype = Downloader()

        def start_command_line(self):
            if len(sys.argv) == 3:
                if sys.argv[1].endswith('txt'):
                    self.prototype.download_videos_with_file(sys.argv[1], sys.argv[2])
                else:
                    self.prototype.download_one_video(sys.argv[1], sys.argv[2])
            elif len(sys.argv) > 3:
                videos = []
                v = 1
                while v < len(sys.argv) - 1:
                    videos.append(sys.argv[v])
                    v = v + 1
                self.prototype.download_more_videos(videos, sys.argv[len(sys.argv) - 1])
