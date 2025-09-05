import os
import re
import csv
import argparse

ZH_DIR = 'ZH'
EN_DIR = 'EN'
CSV_DIR = 'csv'
ENTRY_PATTERN = r'<entry name="(.*?)">(.*?)</entry>'

os.makedirs(CSV_DIR, exist_ok=True)

def txt_to_csv(zh_path, en_path, csv_path):
    with open(en_path, 'r', encoding='utf-8') as f:
        en_content = f.read()
    en_entries = dict(re.findall(ENTRY_PATTERN, en_content, flags=re.DOTALL))
    zh_entries = {}
    if os.path.exists(zh_path):
        with open(zh_path, 'r', encoding='utf-8') as f:
            zh_entries = dict(re.findall(ENTRY_PATTERN, f.read(), flags=re.DOTALL))
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Key', 'EN', 'ZH'])
        for key, en_val in en_entries.items():
            zh_val = zh_entries.get(key, '')
            writer.writerow([key, en_val.strip(), zh_val.strip()])
    print(f'✅ 导出 {csv_path}')

def csv_to_txt(csv_path, en_path, zh_path):
    translations = {}
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            translations[row['Key']] = row['ZH'].strip() or row['EN'].strip()
    with open(en_path, 'r', encoding='utf-8') as f:
        content = f.read()
    def replace_entry(match):
        key, _ = match.groups()
        return f'<entry name="{key}">{translations.get(key, "")}</entry>'
    new_content = re.sub(ENTRY_PATTERN, replace_entry, content, flags=re.DOTALL)
    with open(zh_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'✅ 生成 {zh_path}')

def batch_export():
    for fname in os.listdir(ZH_DIR):
        if fname.startswith('ZH_') and fname.endswith('.txt'):
            base = fname[3:-4]
            zh_path = os.path.join(ZH_DIR, f'ZH_{base}.txt')
            en_path = os.path.join(EN_DIR, f'EN_{base}.txt')
            csv_path = os.path.join(CSV_DIR, f'{base}.csv')
            if os.path.exists(en_path):
                txt_to_csv(zh_path, en_path, csv_path)

def batch_import():
    for fname in os.listdir(CSV_DIR):
        if fname.endswith('.csv'):
            base = fname[:-4]
            csv_path = os.path.join(CSV_DIR, fname)
            en_path = os.path.join(EN_DIR, f'EN_{base}.txt')
            zh_path = os.path.join(ZH_DIR, f'ZH_{base}.txt')
            if os.path.exists(en_path):
                csv_to_txt(csv_path, en_path, zh_path)

def main():
    parser = argparse.ArgumentParser(description='ZH<->CSV 批量转换工具')
    parser.add_argument('mode', choices=['export', 'import'], help='export: 导出csv, import: 生成ZH')
    args = parser.parse_args()
    if args.mode == 'export':
        batch_export()
    elif args.mode == 'import':
        batch_import()

if __name__ == '__main__':
    main()
