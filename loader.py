from pathlib import Path
from lxml import etree
import csv

from data_model import data_types, translation_name

def get_xpath(id: str, data_type: str, field: str, id_field: str):
    return f'//table[@name="{data_type}"]/column[@name="{id_field}"][text()={id}]/../column[@name="{field}"]'

def convert_xml(xml_path: Path, csv_path: Path, turn_to_dst: bool = False):
    """
    Load an XML file from a given path.

    Args:
        xml_path: The path to the XML file.

    Returns:
        An ElementTree object representing the XML file.
    """
    print(f"convert_xml: {xml_path} to {csv_path}")
    tree = etree.parse(str(xml_path))

    rows = {}
    if csv_path.exists():
        with csv_path.open('r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                xpath, value, dst = row
                rows[xpath] = (xpath, value, dst)

    with csv_path.open('w', encoding='utf-8') as f:
        csv_writer = csv.writer(f, lineterminator='\n')
        for data_type in data_types:
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
                        else:
                            attrib[child.attrib['name']] = child.text
                    except KeyError:
                        continue
                # print(attrib)
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
        print(len(rows))
        csv_writer.writerows(list(rows.values()))

def clean_xpath(xpath: str):
    new_xpath = xpath.strip().replace("﻿", "").replace('""', '"')
    if new_xpath.startswith('"'):
        new_xpath = new_xpath[1:]
    if new_xpath.endswith('"'):
        new_xpath = new_xpath[:-1]
    return new_xpath

def deconvert_xml(xml_path: Path, csv_path: Path, onlydst: bool = False):
    print(f"deconvert_xml: {csv_path} to {xml_path}")
    tree = etree.parse(str(xml_path))
    with csv_path.open('r', encoding='utf-8') as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if onlydst:
                xpath, dst = row
            else:
                xpath, _, dst = row
            xpath = clean_xpath(xpath)
            try:
                node = tree.xpath(xpath)
            except etree.XPathEvalError as e:
                print(f"xpath not found: {xpath}")
                raise e
            if len(node) == 1:
                element = tree.xpath(xpath)[0]
                element.text = dst
            elif len(node) > 1:
                print(f"xpath not unique: {xpath} {dst}")
                element = tree.xpath(xpath)[-1]
                element.text = dst
            else:
                print(f"xpath not found: {xpath} {dst}")

    tree.write(str(xml_path), pretty_print=True, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    xml_path = Path(r"D:\software\Steam\steamapps\common\Neo Scavenger\Mods\NeoScavExtended\NSExtended\neogame.xml")
    csv_path = Path(r"NeoScavExtended_机翻\NSExtended\neogame.csv")
    deconvert_xml(xml_path, csv_path)