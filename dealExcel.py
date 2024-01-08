from datetime import datetime
import os
import pandas as pd
import shutil
from PyQt5.QtWidgets import QMessageBox

def process_file(date, amount_str, purpose, supplemental_info, file_path):
    # 解析日期
    date_obj = datetime.strptime(date, "%Y%m%d")
    year = date_obj.year
    month = date_obj.month

    # 转换金额为整数，假设金额格式为 "¥1234" 或 "1234"
    amount = int(amount_str.replace('¥', ''))  # 去除货币符号并转换为整数

    # 确保输出目录和月份目录存在
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    month_dir = os.path.join(output_dir, f'{month}月')
    os.makedirs(month_dir, exist_ok=True)

    # 获取文件名（不含路径）
    file_name = os.path.basename(file_path)

    # 检查文件是否已存在于目标文件夹中
    new_file_path = os.path.join(month_dir, file_name)
    if os.path.exists(new_file_path):
        show_message(f"ファイル {file_name} すでに存在する，操作キャンセル。")
        return False

    # Excel文件路径
    excel_path = os.path.join(output_dir, f'{year}.xlsx')

    # 检查Excel文件是否存在，如果不存在则创建
    if not os.path.exists(excel_path):
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for m in range(1, 13):
                pd.DataFrame(columns=['No', 'Amount', 'Date', 'Purpose', 'Supplemental Info', 'File Name']).to_excel(writer, sheet_name=f'{m}月', index=False)

    # 追加数据到对应月份的sheet
    with pd.ExcelWriter(excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
        book = writer.book
        if f'{month}月' not in book.sheetnames:
            pd.DataFrame(columns=['No', 'Amount', 'Date', 'Purpose', 'Supplemental Info', 'File Name']).to_excel(writer, sheet_name=f'{month}月', index=False)
        sheet = book[f'{month}月']
        start_row = sheet.max_row + 1 if sheet.max_row > 1 else 2
        data = pd.DataFrame([[1, amount, date, purpose, supplemental_info, file_name]], columns=['No', 'Amount', 'Date', 'Purpose', 'Supplemental Info', 'File Name'])
        data.to_excel(writer, sheet_name=f'{month}月', startrow=sheet.max_row, header=False, index=False)

    # 移动文件到月份文件夹
    shutil.move(file_path, new_file_path)
    show_message(f"ファイル {file_name} 実施成功、Excelに書き込み成功成功！")
    return True

def show_message(message):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setText(message)
    msgBox.setWindowTitle("操作通知")
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec_()
