# dxf_parser.py
from idlelib.iomenu import encoding
from symbol import break_stmt

import ezdxf
import os
import re

from ezdxf.queryparser import number

#Настройки регулярных выражений
LINE_NUMBER = r"^\d{2,4}-[A-Z0-9/]+(?:-[a-zA-Z0-9]+)+$"
ITEM_CODE = r"^I\d{3,}$"
QUANTITY = r"^\s*\d+(\.\d+)?M$"
STEEL_CLASS = r",_[\w]+_GB\/T\d+"
DIAMETER = r"^DN\d+,$"
THICKNESS = r"\d+\.\d"


def find_line_number(doc):

    msp = doc.modelspace()
    line_number = "Не найден"
    for text_entity in msp.query('TEXT'):
        if re.match(LINE_NUMBER, text_entity.dxf.text):
            line_number = text_entity.dxf.text
            break
    return line_number

def extract_specification(doc):

    msp = doc.modelspace()
    raw_specification = []
    pipes_specification = []
    text_entities = msp.query('TEXT')

    for string in text_entities:
        if string.dxf.text == "FITTINGS":
            break
        raw_specification.append(string.dxf.text)

    n = len(raw_specification)

    pipe_properties = ""
    pipes_table = {}

    for i in range(9, n):
        if re.match(QUANTITY, raw_specification[i]):
            pipe_properties += " " + raw_specification[i]
            pipes_table['pipe' + pipe_properties.strip()[0]] = pipe_properties.strip()
            pipe_properties = ""
        else:
            pipe_properties += " " +  raw_specification[i]

    # print(pipes_table)

    for k, v in pipes_table.items():
        specs = v.split()
        # print(specs)
        output_specs = {}
        for item in specs:
            if re.match(ITEM_CODE, item):
                output_specs["ID"] = item
            elif re.match(QUANTITY, item):
                quantity = ""
                item = item.strip()
                for i in range(len(item) - 1):
                    quantity += item[i]
                quantity = float(quantity)
                output_specs["Quantity"] = quantity

            elif re.match(STEEL_CLASS, item):
                item = item.strip()
                stack = []
                steel_class = ""
                for c in item:
                    if len(stack) > 2:
                        break
                    elif c.isalnum():
                       steel_class += c
                    else:
                        stack.append(c)
                output_specs["Steel"] = steel_class
            elif re.match(DIAMETER, item):
                diameter = ""
                item = item.strip()
                for i in range(2, len(item) - 1):
                    diameter += item[i]
                diameter = int(diameter)
                output_specs["Diameter"] = diameter
            elif re.match(THICKNESS, item):
                item = item.strip()
                thickness = float(item)
                output_specs["Thickness"] = thickness

        pipes_specification.append(output_specs)

    # print(pipes_specification)

    return pipes_specification

def parse_dxf_file(file_path):
    if not os.path.exists(file_path):
        print(f"Файл не найден: {file_path}")
        return None

    try:
        doc = ezdxf.readfile(file_path)
    except IOError:
        print(f"Ошибка чтения файла: {file_path}")
        return None
    except ezdxf.DXFStructureError:
        print(f"Некорректная структура DXF файла: {file_path}")
        return None
    file_name = os.path.basename(file_path)
    unit = os.path.basename(file_path).split('-')
    line_number = find_line_number(doc)
    specification = extract_specification(doc)

    return {
        "file_name": file_name,
        "unit": unit[2],
        "line_number": line_number,
        "specification": specification
    }