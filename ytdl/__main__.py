import sys
from .funcmodule import check_playlist, links_work, get_audio_streams, download_audio_streams, \
    get_metadata



def main():
    args = sys.argv[1:]
    modes = ["-d", "-a", "-v", "-av"]

    links = []
    mode = "-d"
    for arg in args:
        if arg in modes:
            mode = arg

        if "youtube.com" in arg:
            links.extend(arg.split(" "))

    assert len(links) > 0, "Should pass at least one link as arg"
    assert mode in modes, f"Mode should be one of {modes}"

    # remove empty strings
    links = list(filter(None, links))
    assert len(links) > 0, "Should not remove all links"

    links = check_playlist(links)
    assert len(links) > 0, "Should be at least one song in playlist"

    assert links_work(links), "Links don't work :("

    streams = get_audio_streams(links)
    assert len(streams) > 0, "was not able to get audio streams"

    metadata = get_metadata(links)
    assert len(metadata) == len(streams), "make sure metadata for every stream"

    if arg == "-d":
        pass
    elif arg == "-a":
        download_audio_streams(streams, metadata)
    elif arg == "-v":
        pass
    elif arg == "-av":
        pass


if __name__ == '__main__':
    main()
