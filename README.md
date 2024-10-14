# Youtube Downloader - ytdl

## Usage
```shell
ytdl "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
By default, downloads the audio and video and stitches it together in the current directory. Automatically detects playlists.

- `-a` - audio only
- `-v` - video only
- `-av` - audio + video separate
- `-f` - force replace if file exists

## Build From Source:
1. Clone the repo
2. In the directory, run the installation file
```shell
sh install.sh
```


## TODO:
- [ ] Figure out why -av takes so long compared to -a and -v
