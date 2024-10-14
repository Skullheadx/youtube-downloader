import sys
from .funcmodule import check_playlist, get_audio_metadata_stream, download_audio_stream, get_and_download
import concurrent.futures


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

    audio_streams = []
    metadata_list = []

    for link in links:
        stream, metadata = get_audio_metadata_stream(link)
        assert stream is not None, "was not able to get audio stream"
        assert metadata is not None, "no metadata found"
        audio_streams.append(stream)
        metadata_list.append(metadata)

    assert len(audio_streams) > 0, "no audio streams found"
    assert len(metadata_list) > 0, "no metadata found"

    if mode == "-d":
        pass
    elif mode == "-a":
        # Use ThreadPoolExecutor to run downloads concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Schedule the download_audio_stream function for each audio stream
            futures = {executor.submit(get_and_download, link): link for link in links}

    elif mode == "-v":
        pass
    elif mode == "-av":
        pass


if __name__ == '__main__':
    main()
