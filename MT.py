import os
import csv
import argparse
from googletrans import Translator

CSV_DIR = 'csv'
translator = Translator()

def translate_csv(csv_path, overwrite=True):
    rows = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if overwrite or not row['ZH'].strip():
                try:
                    zh = translator.translate(row['EN'], src='en', dest='zh-cn').text
                    row['ZH'] = zh
                    print(f"🌍 {row['EN']} → {zh}")
                except Exception as e:
                    print(f"❌ 翻译失败: {row['EN']} | 错误: {e}")
            rows.append(row)
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Key', 'EN', 'ZH'])
        writer.writeheader()
        writer.writerows(rows)
    print(f'✅ 翻译完成 {csv_path}')

def batch_translate():
    for fname in os.listdir(CSV_DIR):
        if fname.endswith('.csv'):
            translate_csv(os.path.join(CSV_DIR, fname), overwrite=True)

def main():
    parser = argparse.ArgumentParser(description='批量英译中')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已有翻译')
    args = parser.parse_args()
    batch_translate()

if __name__ == '__main__':
    main()
