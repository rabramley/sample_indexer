from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Footer, Markdown, Header


UNSORTED_PATH = 'd:\My Drive\Data\Music\Patches\Samples\Computer Music'

class MarkdownApp(App):
    BINDINGS = [
        ("n", "show_next_folder", "Next Folder"),
    ]

    @property
    def markdown(self) -> Markdown:
        """Get the Markdown widget."""
        return self.query_one(Markdown)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield Markdown()

    async def on_mount(self) -> None:
        self.folders = self.listdirs(UNSORTED_PATH)
        self.markdown.focus()
        self.markdown.update("# Hello")

    async def action_show_next_folder(self) -> None:
        next_folder = next(self.folders)
        self.markdown.update(f"# {next_folder}")

    def listdirs(self, rootdir):
        for path in Path(rootdir).iterdir():
            if path.is_dir():
                yield path
                self.listdirs(path)


if __name__ == "__main__":
    app = MarkdownApp()
    app.run()