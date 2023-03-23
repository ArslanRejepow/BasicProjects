import html
import os

import requests
from django.utils.text import slugify
from pyyoutube import Api
from vtt_to_srt.vtt_to_srt import ConvertFile
from yt_dlp import YoutubeDL
import config
from functions.functions import get_duration, remove_emojis


class YT:
    def __init__(self, api_key):
        self.channel = None
        self.api = Api(api_key=api_key)

    def reset_channel(self):
        self.channel = None

    def get_channel(self, link, setup=True):
        if '@' in link:
            username = '@' + link.split('@')[1]
            channel = self.search_channel_by_username(username)
            if setup:
                self.channel = channel
                self.channel['videos'] = []
                self.channel['shorts'] = []
            return channel
        try:
            channel_id = link.split('/')[-1:]
            channel = self.api.get_channel_info(
                channel_id=channel_id).items[0].to_dict()
        except:
            print("[Can't find channel. Please check your channel ID]")
            return
        metadata = dict()
        metadata['id'] = channel['id']
        metadata['title'] = channel['snippet']['title']
        metadata['description'] = remove_emojis(
            channel['snippet']['description'])
        metadata['avatar_url'] = channel['snippet']['thumbnails']['high']['url']
        metadata['banner_url'] = channel['brandingSettings']['image']['bannerExternalUrl'] if \
            channel['brandingSettings']['image'] is not None else None
        metadata['keywords'] = channel['brandingSettings']['channel']['keywords']
        metadata['categories'] = channel['topicDetails']['topicIds'] if channel['topicDetails'] is not None else []
        if setup:
            self.channel = metadata
            self.channel['videos'] = []
            self.channel['shorts'] = []
        return metadata

    def get_video(self, video_id):
        video = self.api.get_video_by_id(video_id=video_id).items[0].to_dict()
        metadata = dict()
        metadata['id'] = video['id']
        metadata['title'] = remove_emojis(video['snippet']['title'])
        metadata['description'] = remove_emojis(
            video['snippet']['description'])
        metadata['duration'] = get_duration(
            video['contentDetails']['duration'])
        metadata['thumbnail_url'] = video['snippet']['thumbnails']['high']['url']
        metadata['playlist'] = None
        return metadata

    def get_playlists_from_channel(self, channel_id):
        playlists = self.api.get_playlists(
            channel_id=channel_id, count=None).items
        self.channel['playlists'] = []
        for playlist in playlists:
            playlist_data = playlist.to_dict()
            metadata = dict()
            metadata['id'] = playlist_data['id']
            metadata['title'] = playlist_data['snippet']['title']
            metadata['description'] = playlist_data['snippet']['description']
            metadata['thumbnail_url'] = playlist_data['snippet']['thumbnails']['high']['url']
            self.channel['playlists'].append(metadata)
        return self.channel['playlists']

    def get_videos_from_playlist(self, playlist_id):
        videos = self.api.get_playlist_items(
            playlist_id=playlist_id, count=None).items
        for item in videos:
            video = item.to_dict()
            ids = [video['id'] for video in self.channel['videos']]
            ids.extend([shorts['id'] for shorts in self.channel['shorts']])
            metadata = self.get_video(
                video['snippet']['resourceId']['videoId'])
            metadata['playlist'] = playlist_id
            if metadata['id'] not in ids:
                if 'Shorts' in metadata['title'] or 'shorts' in metadata['title']:
                    self.channel['shorts'].append(metadata)
                else:
                    self.channel['videos'].append(metadata)

    def get_videos_without_playlist(self, channel_id):
        channel_id = channel_id[:1] + 'U' + channel_id[1 + 1:]
        playlist = self.api.get_playlist_items(
            playlist_id=channel_id, count=None).items
        # print(ids)
        for item in playlist:
            video = item.to_dict()
            ids = [video['id'] for video in self.channel['videos']]
            ids.extend([shorts['id'] for shorts in self.channel['shorts']])

            if video['snippet']['resourceId']['videoId'] not in ids:
                metadata = self.get_video(
                    video['snippet']['resourceId']['videoId'])
                if 'Shorts' in metadata['title'] or 'shorts' in metadata['title']:
                    self.channel['shorts'].append(metadata)
                else:
                    self.channel['videos'].append(metadata)

    def get_all_videos(self, playlists):
        for playlist in playlists:
            self.get_videos_from_playlist(playlist['id'])

        self.get_videos_without_playlist(self.channel['id'])
        return self.channel['videos']

    def search_channel_by_username(self, username):
        r = self.api.search_by_keywords(q=username, search_type=[
                                        'channel'], count=5, limit=5)
        for item in r.items:
            item = item.to_dict()
            channel = self.api.get_channel_info(
                channel_id=item['id']['channelId']).items[0].to_dict()
            if 'customUrl' in channel['snippet'] and channel['snippet']['customUrl'] == username:
                channel = self.get_channel(channel['id'])
                return channel

    @staticmethod
    def detect_language(captions):
        lang = [lang for lang in captions if
                'orig' in lang or len(lang.split('-')) > 1 and lang.split('-')[0] == lang.split('-')[1]]
        return lang[0]

    def format_selector(self, ctx):
    
        formats = ctx.get('formats')[::-1]

        best_video = next(f for f in formats
                        if f['vcodec'] != 'none' and f['acodec'] == 'none' and f['height']==1080)
        
        audio_ext = {'mp4': 'm4a', 'webm': 'webm'}[best_video['ext']]
        best_audio = next(f for f in formats if (
            f['acodec'] != 'none' and f['vcodec'] == 'none' and f['ext'] == audio_ext))

        yield {
            'format_id': f'{best_video["format_id"]}+{best_audio["format_id"]}',
            'ext': best_video['ext'],
            'requested_formats': [best_video, best_audio],
            'protocol': f'{best_video["protocol"]}+{best_audio["protocol"]}'
        }

    def download_video(self, video_id, path):
        link = "https://youtube.com/watch?v=" + video_id
        ydl_opts = {"format": self.format_selector,  # This will select the specific resolution typed here
                    "outtmpl": path + video_id}
        with YoutubeDL(ydl_opts) as (ydl):
            ydl.download(link)

        return path + video_id + '.webm'

    def download_subtitle(self, video_id, path):
        link = "https://youtube.com/watch?v=" + video_id

        ydl_opts = {'dump-json': True,
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'youtube_include_dash_manifest': False}

        with YoutubeDL(ydl_opts) as (ydl):
            # ydl.download(link, )
            info_dict = ydl.extract_info(link, download=False)
            if not info_dict['formats']:
                print(' Status : Something went wrong retry or video is unavailable')
                return
            automatic_captions = info_dict.get('automatic_captions')
            lang = self.detect_language(automatic_captions)
            url = [item['url']
                   for item in automatic_captions[lang] if item['ext'] == 'vtt'][0]
            # NOTE the stream=True parameter below
            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                with open(path + video_id + '.vtt', 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            convert_file = ConvertFile(video_id + '.vtt', "utf-8")
            convert_file.convert()
            os.remove(path + video_id + '.vtt')
            return path + video_id + '.srt'

    

yt = YT(config.YOUTUBE_KEY)
yt.download_video('1It1GhuRBKY', '')
