# Youtube Downloader - ytdl

## usage
```shell
ytdl "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
downloads the audio and video and stitches it together in the current directory. Automatically detects playlists.

- `-a` - audio only
- `-v` - video only
- `-av` - audio + video separate
- `-f` - force replace if file exists

# TODO:
- [ ] figure out why -av takes so long compared to -a and -v