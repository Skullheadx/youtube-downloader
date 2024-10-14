from pytubefix import YouTube, Playlist
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


def get_audio_metadata_stream(link):
    yt = YouTube(link)
    yt.check_availability()
    print(f"Fetching stream for {yt.title}")
    assert len(yt.streams.filter(only_audio=True)) > 0, "No available audio streams"
    yield yt.streams.filter(only_audio=True).order_by("abr").last()
    yield {
            "title": yt.title,
            "artist": yt.author,
            "thumbnail_url": yt.thumbnail_url,
            "publish_date": yt.publish_date,
            "views": yt.views
        }

def big_num_format(num):  # https://stackoverflow.com/a/579376
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.1f%s' % (num, ['', 'K', 'M', 'B'][magnitude])


def download_audio_stream(audio_stream, metadata):
    print(f"Downloading audio stream for {audio_stream.title}")
    audio_stream.download()

    # create thumbnail file
    data = requests.get(metadata["thumbnail_url"]).content
    thumbnail_filename = f'{audio_stream.title}.jpg'
    with open(thumbnail_filename, 'wb') as f:
        f.write(data)

    command = [
        'ffmpeg',
        '-i', audio_stream.default_filename,
        '-i', thumbnail_filename,
        '-map', '0',
        '-map', '1',
        '-metadata', f'title={audio_stream.title}',
        '-metadata', f'artist={metadata["artist"]}',
        '-metadata', f'date={metadata["publish_date"]}',
        '-metadata', f'comment={big_num_format(metadata["views"]) + " views"}',
        audio_stream.title + ".mp4",
        '-y'
    ]
    subprocess.run(command)

    # clean up tmp files
    os.remove(thumbnail_filename)
    os.remove(audio_stream.default_filename)


def get_and_download(link):
    yt = YouTube(link)
    yt.check_availability()
    print(f"Fetching stream for {yt.title}")
    assert len(yt.streams.filter(only_audio=True)) > 0, "No available audio streams"
    audio_stream = yt.streams.filter(only_audio=True).order_by("abr").last()
    metadata = {
        "title": yt.title,
        "artist": yt.author,
        "thumbnail_url": yt.thumbnail_url,
        "publish_date": yt.publish_date,
        "views": yt.views
    }

    print(f"Downloading audio stream for {audio_stream.title}")
    audio_stream.download()

    # create thumbnail file
    data = requests.get(metadata["thumbnail_url"]).content
    thumbnail_filename = f'{audio_stream.title}.jpg'
    with open(thumbnail_filename, 'wb') as f:
        f.write(data)

    command = [
        'ffmpeg',
        '-i', audio_stream.default_filename,
        '-i', thumbnail_filename,
        '-map', '0',
        '-map', '1',
        '-metadata', f'title={audio_stream.title}',
        '-metadata', f'artist={metadata["artist"]}',
        '-metadata', f'date={metadata["publish_date"]}',
        '-metadata', f'comment={big_num_format(metadata["views"]) + " views"}',
        audio_stream.title + ".mp4",
        '-y'
    ]
    subprocess.run(command)

    # clean up tmp files
    os.remove(thumbnail_filename)
    os.remove(audio_stream.default_filename)