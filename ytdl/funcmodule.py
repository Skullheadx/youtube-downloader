from pytubefix import YouTube, Playlist, extract
import requests
import subprocess
import os


def check_playlist(links):
    for link in links:
        if "playlist" in link:
            p = Playlist(link)
            for url in p.video_urls:
                links.append(url)
            links.remove(link)
    return links


def get_audio_metadata_streams(links):
    audio_streams = []
    metadata = []

    for link in links:
        yt = YouTube(link)
        yt.check_availability()
        print(f"Fetching stream for {yt.title}")
        assert len(yt.streams.filter(only_audio=True)) > 0, "No available audio streams"
        audio_streams.append(yt.streams.filter(only_audio=True).order_by("abr").last())
        metadata.append(
            {
                "title": yt.title,
                "artist": yt.author,
                "thumbnail_url": yt.thumbnail_url,
                "publish_date": yt.publish_date,
                "views": yt.views
            }
        )
    return audio_streams, metadata

def big_num_format(num):  # https://stackoverflow.com/a/579376
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.1f%s' % (num, ['', 'K', 'M', 'B'][magnitude])


def download_audio_streams(audio_streams, metadata):
    for audio_stream, md in zip(audio_streams, metadata):
        print(f"Downloading audio stream for {audio_stream.title}")
        audio_stream.download()
        data = requests.get(md["thumbnail_url"]).content
        f = open('thumbnail.jpg', 'wb')
        f.write(data)
        f.close()

        command = [
            'ffmpeg',
            '-i', audio_stream.default_filename,
            '-i', "thumbnail.jpg",
            '-map', '0',
            '-map', '1',
            '-metadata', f'title={audio_stream.title}',
            '-metadata', f'artist={md["artist"]}',
            '-metadata', f'date={md["publish_date"]}',
            '-metadata', f'comment={big_num_format(md["views"]) + " views"}',
            audio_stream.title + ".mp4",
            '-y'
        ]

        subprocess.run(command)
        os.remove("thumbnail.jpg")
        os.remove(audio_stream.default_filename)
