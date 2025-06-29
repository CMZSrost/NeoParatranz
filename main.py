# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "lxml",
#     "typer",
# ]
# ///

from pathlib import Path
from glob import glob
from typing import Annotated, Optional

import lxml
import typer
from loader import convert_xml, deconvert_xml

app = typer.Typer()


@app.command()
def convert(
        mod_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
            )
        ],
        todst: Annotated[
            bool,
            typer.Option()
        ] = False,
):
    # 从mod_dir中遍历所有xml文件
    query = str(mod_dir/"**"/"*.xml")
    print(query)
    for xml_file in glob(query, recursive=True, root_dir=mod_dir):
        # 读取xml文件然后从mod_dir转移到save_dir
        csv_file = Path(mod_dir.name) / Path(xml_file).relative_to(mod_dir).with_suffix(".csv")
        csv_file.parent.mkdir(parents=True, exist_ok=True)
        convert_xml(Path(xml_file), csv_file, todst)
        # print(f'Converting {xml_file} to {csv_file}')



@app.command()
def deconvert(
        mod_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
            )
        ],
        csv_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
                # autocompletion=current_dir_autocompletion
            )
        ],
        onlydst: Annotated[
            bool,
            typer.Option()
        ] = False,
):
    query_mod_dir = str(mod_dir/"**"/"*.xml")
    for xml_file in glob(query_mod_dir, recursive=True, root_dir=mod_dir):
        csv_file = Path(csv_dir) / Path(xml_file).relative_to(mod_dir).with_suffix(".csv")
        if csv_file.exists():
            deconvert_xml(Path(xml_file), csv_file, onlydst)
        else:
            print(f"CSV file {csv_file} not found for {xml_file}")


if __name__ == "__main__":
    app()
