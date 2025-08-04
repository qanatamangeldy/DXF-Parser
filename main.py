# Press the green button in the gutter to run the script.
import os
from dxf_parser import parse_dxf_file
from excel_writer import write_to_excel
import pandas as pd

def main():
    dxf_directory = "./"  # Указывем путь к папке с чертежами
    all_data = []

    # Проверяем, существует ли директория
    if not os.path.isdir(dxf_directory):
        print(f"Ошибка: Директория '{dxf_directory}' не найдена.")
        return

    # Получаем список всех DXF файлов
    dxf_files = [f for f in os.listdir(dxf_directory) if f.endswith('.dxf')]
    total_files = len(dxf_files)
    print(f"Найдено {total_files} DXF файлов для обработки.")

    # Обрабатываем каждый файл
    for i, filename in enumerate(dxf_files):
        file_path = os.path.join(dxf_directory, filename)
        print(f"Обработка файла {i + 1}/{total_files}: {filename}")
        data = parse_dxf_file(file_path)
        if data:
            all_data.append(data)

    # Записываем результаты в Excel
    if all_data:
        write_to_excel(all_data, "pipeline_specifications.xlsx")
    else:
        print("Не удалось извлечь данные ни из одного файла.")

if __name__ == '__main__':
    main()

    # Define the path to your Excel file
    file_path = 'pipeline_specifications.xlsx'
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(file_path)

        # Print the first 5 rows of the DataFrame
        # print(df.head())

        # You can now work with your data, for example, iterate over rows
        # for index, row in df.iterrows():
        #     print(f"Row {index}: {row['ColumnName']}")

    except FileNotFoundError:
        print(f"Error: The file was not found at {file_path}")

