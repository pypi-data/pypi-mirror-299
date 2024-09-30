import pandas as pd

def traslate_excel_to_csv(excel_file_name, excel_sheet_name, scv_file_name):
    try:
        # Чтение данных из файла Excel в DataFrame
        df = pd.read_excel(excel_file_name, sheet_name=excel_sheet_name)

        # Объединение заголовков столбцов с разделением табуляцией
        headers_combined = '\t'.join(df.columns)

        # Объединение данных в один столбец с разделением табуляцией
        data_combined = df.apply(lambda x: '\t'.join([str(i) for i in x]), axis=1)

        # Запись заголовков и объединенных данных в CSV файл
        with open(scv_file_name, 'w', encoding='utf-8') as f:
            f.write(headers_combined + '\n')  # Записываем заголовки
            for row in data_combined:
                f.write(row + '\n')
    
        return True
    except:
        return False