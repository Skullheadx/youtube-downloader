import glob
import os
import subprocess

import requests
from pytubefix import YouTube, Playlist


def check_playlist(links):
    for link in links:
        if "playlist" in link:
            p = Playlist(link)
            for url in p.video_urls:
                links.append(url)
            links.remove(link)
    return links


def big_num_format(num):  # https://stackoverflow.com/a/579376
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '%.1f%s' % (num, ['', 'K', 'M', 'B'][magnitude])


def fix_filename(filename):
    for i in ['/', ':', '*', '?', '"', '<', '>', '|']:
        filename = filename.replace(i, '')
    return filename


def get_and_download(link):
    yt = YouTube(link)
    # if fix_filename(yt.title) + '.mp4' in glob.glob("*.mp4"):
    #     print(f"{yt.title} is already downloaded")
    #     return

    yt.check_availability()
    print(f"Fetching stream for {yt.title}")

    assert len(yt.streams.filter(only_audio=True)) > 0, "No available audio streams"
    audio_stream = yt.streams.filter(only_audio=True).order_by("abr").last()


    # hierarchy:
    caption_hierarchy = ["ko", "ja", "zh", "en", "a.ko", "a.en"]
    caption_exists = False
    lang = None
    if len(yt.captions) > 0:
        for c in caption_hierarchy:
            if c in yt.captions.keys():
                yt.captions[c].download(title=fix_filename(yt.title))
                lang = c
                caption_exists = True
                break
    print(f"Downloading audio stream for {yt.title}")
    audio_stream.download(filename=fix_filename(audio_stream.default_filename), skip_existing=True)

    # create thumbnail file
    data = requests.get(yt.thumbnail_url).content
    thumbnail_filename = f'{fix_filename(audio_stream.title)}.jpg'
    with open(thumbnail_filename, 'wb') as f:
        f.write(data)

    if caption_exists:
        command = [
            'ffmpeg',
            '-loop', '1',
            '-i', thumbnail_filename,
            '-i', fix_filename(audio_stream.default_filename),
            '-vf', f'subtitles={fix_filename(yt.title) + f" ({lang}).srt"}',
            '-metadata', f'title={fix_filename(audio_stream.title)}',
            '-metadata', f'artist={yt.author}',
            '-metadata', f'date={yt.publish_date}',
            '-metadata', f'comment={big_num_format(yt.views) + " views"}',
            '-shortest',
            fix_filename(audio_stream.title) + ".mp4",
            '-y'
        ]
    else:
        command = [
            'ffmpeg',
            '-i', fix_filename(audio_stream.default_filename),
            '-i', thumbnail_filename,
            '-map', '0',
            '-map', '1',
            '-metadata', f'title={fix_filename(audio_stream.title)}',
            '-metadata', f'artist={yt.author}',
            '-metadata', f'date={yt.publish_date}',
            '-metadata', f'comment={big_num_format(yt.views) + " views"}',
            fix_filename(audio_stream.title) + ".mp4",
            '-y'
        ]
    subprocess.run(command)

    # clean up tmp files
    os.remove(thumbnail_filename)
    os.remove(fix_filename(audio_stream.default_filename))
    os.remove(fix_filename(yt.title) + f" ({lang}).srt")
