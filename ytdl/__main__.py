from .__init__ import *
import sys
from .classmodule import MyClass
from .funcmodule import check_playlist, links_work, download_audio

def main():
    args = sys.argv[1:]

    links = []
    mode = "-d"
    for arg in args:
        print('passed argument :: {}'.format(arg))
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
  
    #assert links_work(links), "Links don't work :("
    
    if arg == "-d":
        pass
    elif arg == "-a":
        download_audio(links)
    elif arg == "-v":
        pass
    elif arg == "-av":
        pass


if __name__ == '__main__':
    main()


