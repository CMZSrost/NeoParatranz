# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "loguru>=0.7.3",
#     "lxml",
#     "tqdm>=4.67.1",
#     "typer",
# ]
# ///

import datetime
from pathlib import Path
from glob import glob
from typing import Annotated
from contextlib import contextmanager

import typer
from loader import convert_xml, deconvert_xml
import tqdm
import loguru


logging = loguru.logger
logging.remove(0)
logging.add(f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

app = typer.Typer()

def info_write(msg: str):
    logging.info(msg)
    tqdm.tqdm.write(msg)

@contextmanager
def timer(name: str):
    start_time = datetime.datetime.now()
    yield
    end_time = datetime.datetime.now()
    logging.info(f"{name} took {end_time - start_time}, {(end_time - start_time).seconds}s")


@app.command()
def convert(
        mod_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
                help="需要导出翻译文件的mod目录"
            )
        ],
        todst: Annotated[
            bool,
            typer.Option("--todst", "-t", help="导出到译文位置")
        ] = False,
):
    # 从mod_dir中遍历所有xml文件
    query = str(mod_dir/"**"/"*.xml")
    info_write(f"Mod Dir: {mod_dir}")

    with timer(f"Convert {mod_dir.name}"):
        for xml_file in tqdm.tqdm(glob(query, recursive=True, root_dir=mod_dir), desc=f"Converting {mod_dir.name}...", unit="file", colour="green",leave=False,position=0):
            info_write(f"Converting {xml_file}")
            
            # 读取xml文件然后从mod_dir转移到save_dir
            csv_file = Path(mod_dir.name) / Path(xml_file).relative_to(mod_dir).with_suffix(".csv")
            csv_file.parent.mkdir(parents=True, exist_ok=True)
            convert_xml(Path(xml_file), csv_file, todst)



@app.command()
def deconvert(
        mod_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
                help="更新翻译的mod目录"
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
                help="翻译文件存放目录",
            )
        ]
):
    query_mod_dir = str(mod_dir/"**"/"*.xml")
    info_write(f"Mod Dir: {mod_dir}")
    info_write(f"CSV Dir: {csv_dir}")
    with timer(f"Deconvert {mod_dir.name} from {csv_dir.name}"):
        for xml_file in tqdm.tqdm(glob(query_mod_dir, recursive=True, root_dir=mod_dir), desc=f"Deconverting {mod_dir.name} from {csv_dir.name}...", unit="file", colour="green",leave=False,position=0):
            csv_file = Path(csv_dir) / Path(xml_file).relative_to(mod_dir).with_suffix(".csv")
            if csv_file.exists():
                info_write(f"Deconverting {xml_file} from {csv_file}")
                deconvert_xml(Path(xml_file), csv_file)
            else:
                logging.warning(f"CSV file {csv_file} not found for {xml_file}")


if __name__ == "__main__":
    app()
