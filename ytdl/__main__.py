import sys
from .funcmodule import check_playlist, get_audio_metadata_streams, download_audio_streams



def main():
    args = sys.argv[1:]
    modes = ["-d", "-a", "-v", "-av"]

    links = []
    mode = "-d"
    assert len(args) > 0, "no args :("
    for arg in args:
        if arg in modes:
            mode = arg

        if "youtube" in arg or "youtu.be" in arg:
            links.extend(arg.split(" "))

    assert len(links) > 0, "Should pass at least one link as arg"
    assert mode in modes, f"Mode should be one of {modes}"
    print("Processing links")
    # remove empty strings
    links = list(filter(None, links))
    assert len(links) > 0, "Should not remove all links"
    print("Checking for playlists")
    links = check_playlist(links)
    assert len(links) > 0, "Should be at least one song in playlist"

    print("Getting audio streams and metadata")
    streams, metadata = get_audio_metadata_streams(links)
    assert len(streams) > 0, "was not able to get audio streams / metadata"
    assert len(metadata) == len(streams), "make sure metadata for every stream"

    if arg == "-d":
        pass
    elif arg == "-a":
        print("Downloading audio streams")
        download_audio_streams(streams, metadata)
    elif arg == "-v":
        pass
    elif arg == "-av":
        pass


if __name__ == '__main__':
    main()
