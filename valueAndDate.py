import re
from datetime import datetime

def extract_date_amount(ocr_text):
    patterns = {
        'date_patterns': [
            {'pattern': r'\d{4}年\d{1,2}月\d{1,2}日', 'format': '%Y年%m月%d日'},
            {'pattern': r'\d{4}/\d{1,2}/\d{1,2}', 'format': '%Y/%m/%d'},
            {'pattern': r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}', 'format': '%Y/%m/%d %H:%M:%S'},
            # 可以根据需要添加更多日期格式
        ],
        'amount': r'¥[\d,]+'
    }

    def is_valid_date(date_str, date_format):
        try:
            datetime.strptime(date_str, date_format)
            return True
        except ValueError:
            return False

    def format_date(date_str, date_format):
        date_obj = datetime.strptime(date_str, date_format)
        return date_obj.strftime('%Y%m%d')

    # 尝试不同的日期格式
    formatted_dates = []
    for date_pattern in patterns['date_patterns']:
        date_matches = re.findall(date_pattern['pattern'], ocr_text)
        for date_str in date_matches:
            if is_valid_date(date_str, date_pattern['format']):
                formatted_dates.append(format_date(date_str, date_pattern['format']))
                break  # 一旦找到有效日期，跳出循环

    # 提取并排序金额
    amount_matches = re.findall(patterns['amount'], ocr_text)
    amounts = [int(a.replace('¥', '').replace(',', '')) for a in amount_matches]
    unique_amounts = sorted(set(amounts), reverse=True)  # 对金额进行去重并降序排序

    max_amount = unique_amounts[0] if unique_amounts else None
    second_max_amount = unique_amounts[1] if len(unique_amounts) > 1 else None

    return formatted_dates, max_amount, second_max_amount
