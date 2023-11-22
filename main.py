from pytube import YouTube

SAVE_PATH = "D:/Youtube/"

with open('links_file.txt', 'r') as f:
    links = f.read().split('\n')
    if links[-1] == "":
        links = links[:-1]

VIDEO = False

def download_video(link):
    yt = YouTube(link)
    mp4_files = yt.streams.filter(file_extension="mp4")
    mp4_files = mp4_files.get_highest_resolution()
    mp4_files.download(output_path=SAVE_PATH)
    print("Download is completed successfully")
def download_audio(link):
    yt = YouTube(link)
    audio = yt.streams.filter(only_audio=True).get_audio_only()
    audio.download(output_path=SAVE_PATH)
    print("Download is completed successfully")


for i in links:
    if VIDEO:
        download_video(i)
    else:
        download_audio(i)

print('Items Downloaded!')
