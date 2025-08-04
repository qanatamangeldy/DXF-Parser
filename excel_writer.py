# excel_writer.py

from openpyxl import Workbook

def write_to_excel(data_list, output_file="output.xlsx"):
    """
    Записывает собранные данные в файл Excel.

    Args:
        data_list (list): Список словарей с данными по каждому чертежу.
        output_file (str): Имя выходного файла Excel.
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Спецификация трубопроводов"

    # Создаем заголовок
    headers = ["File name", "Unit", "Line", "ID", "Quantity", "Steel", "Diameter", "Thk. (mm)"]
    ws.append(headers)

    # Записываем данные
    for data in data_list:
        if not data:
            continue
        # Если спецификация пуста, все равно записываем имя файла и номер линии
        if not data["specification"]:
            ws.append([data["file_name"], data["unit"], data["line_number"], "N/A", 0, "N/A", "N/A", "N/A"])
        else:
            # Для каждой позиции в спецификации создаем новую строку
            for item in data["specification"]:
                row = [
                    data["file_name"],
                    data["unit"],
                    data["line_number"],
                    item.get("ID", "N/A"),
                    item.get("Quantity", 0),
                    item.get("Steel", "N/A"),
                    item.get("Diameter", "N/A"),
                    item.get("Thickness", "N/A")
                ]
                ws.append(row)

    wb.save(output_file)
    print(f"Данные успешно сохранены в файл: {output_file}")