from pytubefix import YouTube, Playlist
from pytubefix.exceptions import VideoUnavailable
import ffmpeg


RES = ["1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
ABR = ["160kbps", "128kbps", "70kbps", "50kbps", "48kbps"]
target_res = 0
target_abr=0

failed_download = set()

if __name__ == "__main__":

    # get list of links from file
    links = []
    with open('links.txt', 'r') as f:
        links = f.read().split('\n')
        if links[-1] == "":
            links = links[:-1]

    for link in links:
        if "playlist" in link:
            p = Playlist(link)
            for url in p.video_urls:
                links.append(url)
            links.remove(link)


    # download links one by one
    for link in links:
        target_res = 0
        target_abr = 0
        video_success = True
        audio_success = True

        try:
            yt = YouTube(link)
            yt.streams

        except VideoUnavailable:
            print(f'Video {link} is unavaialable, skipping.')
            failed_download.add(((yt.title, link)))
        else:
            video_streams = []            
            while len(video_streams) == 0:
                video_streams = yt.streams.filter(file_extension='mp4', res=RES[target_res]) # find available streams
                if target_res + 1 < len(RES):
                    target_res = target_res + 1
                else:
                    video_success = False
                    break
            if not video_success:
                print(f"Unable to find video stream for {yt.title}")
                failed_download.add(((yt.title, link)))

                break
            vstream = video_streams[0]

            # audio
            audio_streams = []
            while len(audio_streams) == 0:
                audio_streams = yt.streams.filter(only_audio=True, abr=ABR[target_abr]) # find available streams

                if target_abr + 1 < len(RES):
                    target_abr = target_abr + 1
                else:
                    audio_success = False
                    break
            if not audio_success:
                print(f"Unable to find audio stream for {yt.title}")
                failed_download.add(((yt.title, link)))

                break
            astream = audio_streams[0]

            vstream.download(output_path="downloaded/video_only")
            astream.download(output_path="downloaded/audio_only")

            input_video = ffmpeg.input(f"downloaded/video_only/{vstream.default_filename}")
            input_audio = ffmpeg.input(f"downloaded/audio_only/{astream.default_filename}")

            ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'downloaded/{yt.title}.mp4').run()

print("Failed Downloading:")
print(failed_download)

