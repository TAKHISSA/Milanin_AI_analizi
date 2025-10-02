import json
import pandas as pd
from datetime import datetime

def load_json_file(file_path):
    """JSON dosyasını yükler"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"JSON yükleme hatası: {e}")
        return None

def save_to_txt(file_path, content):
    """Metin dosyasına kaydeder"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Dosya kaydedildi: {file_path}")
    except Exception as e:
        print(f"Dosya kaydetme hatası: {e}")

def format_duration(minutes):
    """Dakikayı 'X dk Y sn' formatına çevirir"""
    if isinstance(minutes, (int, float)):
        mins = int(minutes)
        secs = int((minutes - mins) * 60)
        return f"{mins} dk {secs} sn"
    return "0 dk 0 sn"

def parse_timestamp(timestamp_str, format="%d.%m.%Y %H:%M"):
    """Zaman damgasını parse eder"""
    try:
        return datetime.strptime(timestamp_str, format)
    except:
        return None
