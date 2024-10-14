import pytubefix.extract

from .__init__ import *
from pytubefix import YouTube, Playlist, extract
import ffmpeg
import requests


def check_playlist(links):
    for link in links:
        if "playlist" in link:
            p = Playlist(link)
            for url in p.video_urls:
                links.append(url)
            links.remove(link)
    return links


def links_work(links):
    for link in links:
        YouTube(link).check_availability()
    return True


def get_audio_streams(links):
    audio_streams = []
    for link in links:
        yt = YouTube(link)
        assert len(yt.streams.filter(only_audio=True)) > 0, "No available audio streams"
        audio_streams.append(yt.streams.filter(only_audio=True).order_by("abr").last())
    return audio_streams


def get_metadata(links):
    metadata = []
    for link in links:
        yt = YouTube(link)
        metadata.append(
            {
                "title": yt.title,
                "author": yt.author,
                "thumbnail_url": yt.thumbnail_url,
                "description": yt.description,
                "publish_date": yt.publish_date,
                "rating": yt.rating,
                "views": yt.views
            }
        )
    return metadata


def download_audio_streams(audio_streams, metadata):
    for audio_stream, md in zip(audio_streams, metadata):
        audio_stream.download()
        data = requests.get(md["thumbnail_url"]).content
        f = open('thumbnail.jpg', 'wb')
        f.write(data)
        f.close()

        audio = ffmpeg.input(audio_stream.default_filename)
        thumb = ffmpeg.input("thumbnail.jpg")
        (
            ffmpeg
            .output(
                audio, thumb,
                audio_stream.title + ".mp4",
                author=md["author"], year=md["publish_date"], description=md["description"]
            )
            .overwrite_output()
            .run()
        )

# RES = ["1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
# ABR = ["160kbps", "128kbps", "70kbps", "50kbps", "48kbps"]
# target_res = 0
# target_abr=0

# get list of links from file
# links = []
# with open('links.txt', 'r') as f:
#     links = f.read().split('\n')
#     if links[-1] == "":
#         links = links[:-1]
# print(links)


#     # download links one by one
#     for link in links:
#         target_res = 0
#         target_abr = 0
#         video_success = True
#         audio_success = True

#         try:
#             yt = YouTube(link)
#             yt.streams

#         except VideoUnavailable:
#             print(f'Video {link} is unavaialable, skipping.')
#             failed_download.add(((yt.title, link)))
#         else:
#             video_streams = []            
#             while len(video_streams) == 0:
#                 video_streams = yt.streams.filter(file_extension='mp4', res=RES[target_res]) # find available streams
#                 if target_res + 1 < len(RES):
#                     target_res = target_res + 1
#                 else:
#                     video_success = False
#                     break
#             if not video_success:
#                 print(f"Unable to find video stream for {yt.title}")
#                 failed_download.add(((yt.title, link)))

#                 break
#             vstream = video_streams[0]

#             # audio
#             audio_streams = []
#             while len(audio_streams) == 0:
#                 audio_streams = yt.streams.filter(only_audio=True, abr=ABR[target_abr]) # find available streams

#                 if target_abr + 1 < len(RES):
#                     target_abr = target_abr + 1
#                 else:
#                     audio_success = False
#                     break
#             if not audio_success:
#                 print(f"Unable to find audio stream for {yt.title}")
#                 failed_download.add(((yt.title, link)))

#                 break
#             astream = audio_streams[0]

#             vstream.download(output_path="downloaded/video_only")
#             astream.download(output_path="downloaded/audio_only")

#             input_video = ffmpeg.input(f"downloaded/video_only/{vstream.default_filename}")
#             input_audio = ffmpeg.input(f"downloaded/audio_only/{astream.default_filename}")

#             ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'downloaded/{yt.title}.mp4').run()

# print("Failed Downloading:")
# print(failed_download)
