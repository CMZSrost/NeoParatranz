import os.path
from pathlib import Path
from lxml import etree
import csv
import tqdm

import loguru

from data_model import data_types, translation_name

logging = loguru.logger

def warning_write(msg: str):
    logging.warning(msg)
    tqdm.tqdm.write(f'warning: {msg}')

def get_xpath(id: str, data_type: str, field: str, id_field: str):
    return f'//table[@name="{data_type}"]/column[@name="{id_field}"][text()={id}]/../column[@name="{field}"]'

def clean_xpath(xpath: str):
    xpath = xpath.strip()
    xpath = xpath.replace('""', '"')
    spl = xpath.split('//', 1)
    xpath = f'//{spl[1]}'
    if xpath.startswith('"'):
        xpath = xpath[1:]
    if xpath.endswith('"'):
        xpath = xpath[:-1]
    return xpath

def convert_xml(xml_path: Path, csv_path: Path, turn_to_dst: bool = False):
    """
    Load an XML file from a given path.

    Args:
        xml_path: The path to the XML file.

    Returns:
        An ElementTree object representing the XML file.
    """
    tree = etree.parse(str(xml_path))

    rows = {}
    if csv_path.exists():
        with csv_path.open('r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for row in tqdm.tqdm(csv_reader, desc=f"loading existed csv {os.path.join(csv_path.parent.name, csv_path.name)}", unit='row', colour='blue',leave=False,position=1):
                xpath, value, dst = "", "", ""
                if len(row) == 2:
                    xpath, dst = row
                elif len(row) == 3:
                    xpath, value, dst = row
                else:
                    warning_write(f"invalid row: {row}")
                if len(row) in [2, 3]:
                    xpath = clean_xpath(xpath)
                    rows[xpath] = (xpath, value, dst)

    with csv_path.open('w', encoding='utf-8') as f:
        csv_writer = csv.writer(f, lineterminator='\n')
        for data_type in tqdm.tqdm(data_types, desc=f"converting {os.path.join(xml_path.parent.name, xml_path.name)} -> {os.path.join(csv_path.parent.name, csv_path.name)}", unit='table', colour='blue',leave=False,position=1):
            for element in tree.xpath(f'//table[@name="{data_type}"]'):
                attrib = {}
                id = None
                id_field = "id"
                for child in element.getchildren():
                    try:
                        key = child.attrib['name']
                        if key == 'id':
                            id = child.text
                        elif key == "nID":
                            id = child.text
                            id_field = "nID"
                        elif key not in translation_name:
                            continue
                        elif key == "strName" and data_type == "maps":
                            continue
                        elif key == "strType" and data_type == "gamevars":
                            continue
                        else:
                            attrib[child.attrib['name']] = child.text
                    except KeyError:
                        continue
                for field, value in attrib.items():
                    xpath = get_xpath(id, data_type, field, id_field)
                    if turn_to_dst:
                        row = (xpath, "", value)
                        if xpath in rows:
                            row = (xpath, rows[xpath][1], value)
                    else:
                        row = (xpath, value, "")
                        if xpath in rows:
                            row = (xpath, value, rows[xpath][2])
                    rows[xpath] = row
        # 对rows的[xpath, value, ""]中的xpath进行去重，取出最后一个值
        csv_writer.writerows(list(rows.values()))

def deconvert_xml(xml_path: Path, csv_path: Path):
    tree = etree.parse(str(xml_path))
    with csv_path.open('r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in tqdm.tqdm(csv_reader, desc=f"deconvert_xml {os.path.join(csv_path.parent.name, csv_path.name)} -> {os.path.join(xml_path.parent.name, xml_path.name)}", unit='row', colour="blue",position=1,leave=False):
            if len(row) == 2:
                xpath, dst = row
            elif len(row) == 3:
                xpath, _, dst = row
            else:
                warning_write(f"invalid row: {row}")
            xpath = clean_xpath(xpath)
            node = tree.xpath(xpath)
            if len(node) == 1:
                element = tree.xpath(xpath)[0]
                element.text = dst
            elif len(node) > 1:
                warning_write(f"xpath not unique: {xpath} {dst}")
                element = node[-1]
                element.text = dst
            else:
                warning_write(f"xpath not found: {xpath} {dst}")

    tree.write(str(xml_path), pretty_print=True, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    xml_path = Path(r"D:\software\Steam\steamapps\common\Neo Scavenger\Mods\NeoScavExtended\NSExtended\neogame.xml")
    csv_path = Path(r"NeoScavExtended_机翻\NSExtended\neogame.csv")
    deconvert_xml(xml_path, csv_path)
