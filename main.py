# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "loguru>=0.7.3",
#     "lxml",
#     "pydantic>=2.11.7",
#     "python-dotenv>=1.1.1",
#     "requests>=2.32.4",
#     "tqdm>=4.67.1",
#     "typer",
# ]
# ///

import datetime
import functools
import os
import zipfile
from pathlib import Path
from glob import glob
from typing import Annotated
from contextlib import contextmanager

import typer
import tqdm
from dotenv import load_dotenv
import loguru
import requests

from loader import convert_xml, deconvert_xml
from paratranz_model import File

logging = loguru.logger
logging.remove(0)

load_dotenv()
paratranz_url = "https://paratranz.cn/api"
post = functools.partial(requests.post, headers={"Authorization": f"Bearer {os.getenv('TOKEN')}"})
get = functools.partial(requests.get, headers={"Authorization": f"Bearer {os.getenv('TOKEN')}"})

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


@app.command(help="从mod文件导出csv文件")
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
        save_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
                help="导出文件存放目录",
            )
        ] = Path.cwd(),
        todst: Annotated[
            bool,
            typer.Option("--todst", "-t", help="导出到译文位置")
        ] = False,
):
    logging.add(f"logs/convert/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    # 从mod_dir中遍历所有xml文件
    query = str(mod_dir/"**"/"*.xml")
    info_write(f"Mod Dir: {mod_dir}")
    info_write(f"Save Dir: {save_dir}")

    with timer(f"Convert {mod_dir.name}"):
        for xml_file in tqdm.tqdm(glob(query, recursive=True, root_dir=mod_dir), desc=f"Converting {mod_dir.name}...", unit="file", colour="green",leave=False,position=0):
            info_write(f"Converting {xml_file}")
            
            # 读取xml文件然后从mod_dir转移到save_dir
            csv_file = save_dir / Path(mod_dir.name) / Path(xml_file).relative_to(mod_dir).with_suffix(".csv")
            csv_file.parent.mkdir(parents=True, exist_ok=True)
            convert_xml(Path(xml_file), csv_file, todst)



@app.command(help="从csv文件更新mod文件")
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
                help="翻译文件存放目录",
            )
        ]
):
    logging.add(f"logs/deconvert/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
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



@app.command(help="列出paratranz上该项目的文件")
def files():
    logging.add(f"logs/files/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    resp = get(f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/files")
    resp.raise_for_status()
    files = [File(**file) for file in resp.json()]
    for file in files:
        file_path = Path(file.name)
        if file_path.exists():
            info_write(f"{file.name} ({file.total} words, {file.translated} translated, {file.disputed} disputed, {file.checked} checked, {file.reviewed} reviewed, {file.hidden} hidden, {file.locked} locked)")
        else:
            info_write(f"{file.name} ({file.total} words, {file.translated} translated, {file.disputed} disputed, {file.checked} checked, {file.reviewed} reviewed, {file.hidden} hidden, {file.locked} locked) [NOT FOUND]")

@app.command(help="将本地的翻译文件上传到paratranz")
def upload(
        csv_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
                help="翻译文件存放目录",
            )
        ],
        create: bool = typer.Option(False, "--create", "-c", help="文件不存在时创建新文件，否则跳过"),
        original: bool = typer.Option(False, "--original", "-o", help="文件存在时更新原文"),
        translated: bool = typer.Option(False, "--translated", "-t", help="文件存在时更新译文，仅更新未翻译的词条"),
        force_translated: bool = typer.Option(False, "--force-translated", "-f", help="更新译文时对涉及的所有词条进行覆盖"),
):
    logging.add(f"logs/upload/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    info_write(f"Upload mode: c:{create} o:{original} t:{translated} f:{force_translated}")
    info_write(f"Project ID: {os.getenv('PROJECT_ID')}")

    info_write(f"get files from paratranz")
    resp = get(f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/files")
    resp.raise_for_status()
    files = [File(**file) for file in resp.json()]
    file_paths = [Path(file.name) for file in files]
    info_write(f"found {len(files)} files in paratranz")

    info_write(f"get files from csv_dir")
    query_csv_dir = str(csv_dir / "**" / "*.csv")
    csv_files = [Path(os.path.join(Path(csv_dir).name,Path(csv_file).relative_to(csv_dir))) for csv_file in glob(query_csv_dir, recursive=True, root_dir=csv_dir)]
    info_write(f"found {len(csv_files)} files in csv_dir")

    info_write(f"upload files to paratranz")
    c_url = f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/files"
    o_url = f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/files/{{file_id}}"
    t_url = f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/files/{{file_id}}/translation"

    for csv_file in csv_files:
        if csv_file not in file_paths and create:
            file_payload = {"file": (str(csv_file.name), open(csv_file, "rb")), "path": (None, str(csv_file.parent.as_posix()))}
            info_write(f"upload file_payload {file_payload} to {c_url}")
            resp = post(c_url, files=file_payload)
            resp.raise_for_status()
            info_write(f"create new file {csv_file} -> {File(**(resp.json()['file'])).name}")
        elif csv_file in file_paths:
            file_id = files[file_paths.index(csv_file)].id
            if original:
                resp = post(o_url.format(file_id=file_id), files={"file": (str(csv_file.name), open(csv_file, "rb"))})
                resp.raise_for_status()
                resp_json = resp.json()
                if 'status' in resp_json:
                    info_write(f"file {csv_file} is the same as paratranz, skip updating")
                else:
                    info_write(f"update original of file {csv_file} -> {File(**(resp_json['file'])).name}")
            if translated:
                resp = post(t_url.format(file_id=file_id), files={"file": (str(csv_file.name), open(csv_file, "rb")), "force": (None, force_translated)})
                resp.raise_for_status()
                if 'status' in resp_json:
                    info_write(f"file {csv_file} is the same as paratranz, skip updating")
                else:
                    info_write(f"update translated of file {csv_file} -> {File(**(resp_json['file'])).name}")

    # if update == UploadMode.create:
    #     resp = get(f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/files")

@app.command(help="从paratranz下载翻译文件")
def download(
        save_dir: Annotated[
            Path,
            typer.Argument(
                exists=True,
                dir_okay=True,
                file_okay=False,
                resolve_path=True,
                help="下载文件存放目录",
            )
        ] = Path.cwd(),
        renew: Annotated[bool, typer.Option("--renew", "-r", help="触发导出最新翻译文件再下载")] = False,
        unzip_delete: Annotated[bool, typer.Option("--unzip-delete", "-z", help="解压并删除zip文件")] = False,
):
    logging.add(f"logs/download/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")
    info_write(f"Download mode: r:{renew}")
    info_write(f"Project ID: {os.getenv('PROJECT_ID')}")
    info_write(f"Save Dir: {save_dir}")

    if renew:
        info_write(f"trigger export latest translation files")
        resp = post(f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/artifacts")
        resp.raise_for_status()
        info_write(f"export latest translation files -> {resp.json()}")

    info_write(f"download files from paratranz")
    resp = get(f"{paratranz_url}/projects/{os.getenv('PROJECT_ID')}/artifacts/download")
    resp.raise_for_status()

    with open(save_dir / "translations.zip", "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    info_write(f"download translations.zip to {save_dir / 'translations.zip'}")
    if unzip_delete:
        with zipfile.ZipFile(save_dir / "translations.zip", "r") as zip_ref:
            zip_ref.extractall(save_dir)
        info_write(f"extract translations.zip to {save_dir}")


if __name__ == "__main__":
    app()
