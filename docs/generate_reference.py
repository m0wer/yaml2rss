"""Script to automate the generation of the reference section."""

from pathlib import Path

import mkdocs_gen_files

src_root = Path("./yaml2rss")
for path in src_root.glob("**/*.py"):
    doc_path = Path("reference", path.relative_to(src_root)).with_suffix(".md")

    with mkdocs_gen_files.open(doc_path, "w") as f:
        ident = f"{src_root}." + ".".join(path.with_suffix("").parts[1:])
        print("::: " + ident, file=f)
