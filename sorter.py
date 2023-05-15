from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Static, ListView, ListItem, Label
import sounddevice as sd
import soundfile as sf


SAMPLE_FOLDER = Path('g:\My Drive\Data\Music\Patches\Samples')


class DirectoryHeader(Static):
    pass


class SampleDirectory(Static):
    def compose(self) -> ComposeResult:
        yield DirectoryHeader("")
        yield ListView()
    
    def set_path(self, path, files):
        relative = path.relative_to(SAMPLE_FOLDER)
        parts = ' > '.join(relative.parts)
        self.query_one(DirectoryHeader).update(parts)

        file_list = self.query_one(ListView)
        file_list.clear()

        for f in files:
            file_list.append(ListItem(Label(f.name)))
        
        file_list.focus()

class SampleIndexer(App):
    CSS_PATH = "sorter.css"
    BINDINGS = [
        ("n", "show_next_folder", "Next Folder"),
        ("p", "play_samples", "Play Samples"),
    ]

    def compose(self) -> ComposeResult:
        self.current_folder = None
        yield Header()
        yield Footer()
        yield SampleDirectory()

    async def on_mount(self) -> None:
        self.folders = self.listdirs(SAMPLE_FOLDER)

    async def action_show_next_folder(self) -> None:
        self.current_folder = next(self.folders)
        self.query_one(SampleDirectory).set_path(self.current_folder, self.potential_samples(self.current_folder))

    async def action_play_samples(self) -> None:
        for s in self.potential_samples(self.current_folder):
            data, samplerate = sf.read(s)
            sd.play(data, samplerate)
            sd.wait()

    def listdirs(self, rootdir):
        if len(self.potential_samples(rootdir)) > 0:
            yield rootdir
        else:
            print(f'skipping {rootdir}')

        for path in rootdir.iterdir():
            if path.is_dir():
                yield from self.listdirs(path)

    def potential_samples(self, dir):
        return [
            x for x in dir.iterdir()
            if not x.is_dir() and
            not x.suffix in ('.txt', '.zip', '.sf2', '.pdf', '.rx2', '.mid')
        ]

if __name__ == "__main__":
    app = SampleIndexer()
    app.run()