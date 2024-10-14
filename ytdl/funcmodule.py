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


def download_thumbnail(thumbnail_url, thumbnail_filename):
    data = requests.get(thumbnail_url).content
    with open(thumbnail_filename, 'wb') as f:
        f.write(data)


def download(link, mode, force=False):
    yt = YouTube(link)
    filename = fix_filename(yt.title)
    if (
            (
                    (mode == '-av' and
                     (filename + ' (audio only).mp4' in glob.glob("*.mp4") or
                      filename + ' (video only).mp4' in glob.glob("*.mp4"))) or
                    (mode != '-av' and filename + '.mp4' in glob.glob("*.mp4"))
            ) and
            (not force)
    ):
        print(f"{yt.title} is already downloaded")
        return
    yt.check_availability()

    thumbnail_filename = f'{filename}.jpg'
    download_thumbnail(yt.thumbnail_url, thumbnail_filename)

    if mode == '-a' or mode == '-v':
        download_single_stream(yt, filename, thumbnail_filename, mode)
    elif mode == '-av' or mode == '-d':
        download_double_stream(yt, filename, thumbnail_filename, mode)


def convert_add_metadata(input1, input2, output, yt, m1=1, m2=0):
    artist, album, title = yt.vid_info['videoDetails']['keywords']
    command = [
        'ffmpeg',
        '-i', input1,
        '-i', input2,
        '-map', f'{m1}',
        '-map', f'{m2}',
        '-c', 'copy',
        f'-disposition:v:{m2}', 'attached_pic',
        '-metadata', f'title={title}',
        '-metadata', f'artist={artist}',
        '-metadata', f'comment={big_num_format(yt.views) + " views"}',
        '-metadata', f'date={yt.publish_date}',
        '-metadata', f'album={album}',
        output + ".mp4",
        '-y'
    ]
    subprocess.run(command)


def download_single_stream(yt, filename, thumbnail_filename, mode):
    print(f"Fetching stream for {yt.title}")
    stream = None
    if mode == "-a":
        assert len(yt.streams.filter(only_audio=True)) > 0, "No available audio streams"
        stream = yt.streams.filter(only_audio=True).order_by("abr").last()
    if mode == "-v":
        assert len(yt.streams.filter(only_video=True)) > 0, "No available video streams"
        stream = yt.streams.filter(only_video=True).order_by("resolution").last()

    assert stream is not None, "mode is not valid"
    print(f"Downloading stream for {yt.title}")
    default_filename = "default " + fix_filename(stream.default_filename)
    stream.download(filename=default_filename, skip_existing=True)

    print(f"Adding metadata to {yt.title}")
    convert_add_metadata(default_filename, thumbnail_filename, filename, yt)

    print("Removing temporary files")
    os.remove(thumbnail_filename)
    os.remove(default_filename)


def download_double_stream(yt, filename, thumbnail_filename, mode):
    print(f"Fetching streams for {yt.title}")
    assert len(yt.streams.filter(only_audio=True)) > 0, "No available audio streams"
    audio_stream = yt.streams.filter(only_audio=True).order_by("abr").last()
    assert len(yt.streams.filter(only_video=True)) > 0, "No available video streams"
    video_stream = yt.streams.filter(only_video=True).order_by("resolution").last()

    print(f"Downloading streams for {yt.title}")
    audio_default_filename = "default audio " + fix_filename(audio_stream.default_filename)
    video_default_filename = "default video " + fix_filename(video_stream.default_filename)

    audio_stream.download(filename=audio_default_filename, skip_existing=True)
    video_stream.download(filename=video_default_filename, skip_existing=True)

    print(f"Adding metadata to {yt.title}")
    if mode == '-av':
        for suffix, stream in [(" (audio only)", audio_default_filename), (" (video only)", video_default_filename)]:
            convert_add_metadata(stream, thumbnail_filename, filename + suffix, yt)
    elif mode == '-d':
        convert_add_metadata(audio_default_filename, video_default_filename, filename + "tmp", yt, m1=0, m2=1)
        convert_add_metadata(filename + "tmp.mp4", thumbnail_filename, filename, yt)

    print("Removing temporary files")
    os.remove(thumbnail_filename)
    os.remove(audio_default_filename)
    os.remove(video_default_filename)
    if mode == '-d':
        os.remove(filename + "tmp" + ".mp4")
