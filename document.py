from datetime import datetime
from pathlib import Path

class DocumentEditor:
    def __init__(self, output_dir, filename="README.md"):
        self.file_path = output_dir.joinpath(filename)
        self.lines = []

    def add_h1(self, text):
        self.lines.append(f"# {text}")

    def add_h2(self, text):
        self.lines.append("")
        self.lines.append(f"## {text}")

    def add_h3(self, text):
        self.lines.append("")
        self.lines.append(f"### {text}")

    def add_content(self, text):
        self.lines.append(text)

    def write(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))

if __name__ == "__main__":
    output_dir = "output/"
    output_dir = Path(output_dir+datetime.now().strftime('%Y%m%d_%H%M%S'))
    output_dir.mkdir(exist_ok=True, parents=True)

    editor = DocumentEditor(output_dir)
    editor.add_h1("Python勉強会")
    editor.add_content("山梨県のPython勉強会です。")
    editor.add_h2("概要")
    editor.add_content("Hello, World!")
    editor.add_h3("詳細")
    editor.add_content("Hello, World を学びます")
    editor.add_content("- あれやって")
    editor.add_content("- これやって")
    editor.add_content("- こうする")
    editor.write()
