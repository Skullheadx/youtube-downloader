import sys
from .funcmodule import check_playlist, download
import concurrent.futures


def main():
    args = sys.argv[1:]
    modes = ["-d", "-a", "-v", "-av"]

    links = []
    mode = "-d"
    force = False
    assert len(args) > 0, "no args :("
    for arg in args:
        if arg in modes:
            mode = arg
        if arg == '-f': # force
            force = True
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

    # Use ThreadPoolExecutor to run downloads concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Schedule the download_audio_stream function for each audio stream
        futures = {executor.submit(download, link, mode, force): link for link in links}


if __name__ == '__main__':
    main()
