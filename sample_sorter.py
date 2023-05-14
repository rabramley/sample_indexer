from pathlib import Path
import sounddevice as sd
import soundfile as sf
import curses

UNSORTED_PATH = 'd:\My Drive\Data\Music\Patches\Samples\Computer Music'

def walk(path):
    subdirs = [x for x in path.iterdir() if x.is_dir()]
    subfiles = [x for x in path.iterdir() if not x.is_dir() and not x.suffix in ('.txt')]

    if len(subfiles) > 0:
        for s in subfiles:
            data, samplerate = sf.read(s)
            sd.play(data, samplerate)
            sd.wait()
        exit()

    for s in subdirs:
        walk(s)

walk(Path(UNSORTED_PATH))
