import json
from datetime import datetime
from utils.helpers import load_json_file, parse_timestamp, format_duration

class DataProcessor:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = self.load_data()
        
    def load_data(self):
        """JSON verisini yükler"""
        return load_json_file(self.json_file_path)
    
    def extract_chat_info(self, chat):
        """Sohbetten temel bilgileri çıkarır"""
        if not chat:
            return None
            
        # Zaman farkını hesapla
        start_time = chat.get('tarih_saat')
        end_time = None
        
        # Son mesajın zamanını al
        mesajlar = chat.get('mesajlar', [])
        if mesajlar:
            end_time = mesajlar[-1].get('timestamp')
        
        duration = self.calculate_duration(start_time, end_time)
        
        return {
            'sohbet_id': chat.get('sohbet_id', ''),
            'sohbet_baslangic': start_time,
            'sohbet_bitis': end_time,
            'toplam_sure': duration,
            'gercek_yanit_durumu': chat.get('yanit_durumu', ''),
            'gercek_sentiment': chat.get('sentiment', ''),
            'gercek_tur': chat.get('tur', ''),
            'gercek_intent': chat.get('intent', ''),
            'gercek_intent_detay': chat.get('intent_detay', '')
        }
    
    def calculate_duration(self, start, end):
        """İki zaman arasındaki farkı hesaplar"""
        if not start or not end:
            return format_duration(0)
            
        try:
            # Zaman formatını ayarla
            start_dt = parse_timestamp(start, "%d.%m.%Y %H:%M:%S")
            end_dt = parse_timestamp(end, "%d.%m.%Y %H:%M:%S")
            
            if start_dt and end_dt:
                diff = end_dt - start_dt
                minutes = diff.total_seconds() / 60
                return format_duration(minutes)
        except Exception as e:
            print(f"Zaman hesaplama hatası: {e}")
            
        return format_duration(0)
    
    def get_all_chats(self):
        """Tüm sohbetleri ve bilgilerini getirir"""
        chat_infos = []
        for chat in self.data:
            chat_info = self.extract_chat_info(chat)
            if chat_info:
                chat_info['raw_chat'] = chat  # Orijinal sohbet verisini de sakla
                chat_infos.append(chat_info)
                
        return chat_infos
    
    def get_ground_truth_labels(self):
        """Önceden hazırlanmış etiketleri getirir"""
        ground_truth = []
        for chat in self.data:
            ground_truth.append({
                'sohbet_id': chat.get('sohbet_id'),
                'yanit_durumu': chat.get('yanit_durumu'),
                'sentiment': chat.get('sentiment'),
                'tur': chat.get('tur'),
                'intent': chat.get('intent'),
                'intent_detay': chat.get('intent_detay')
            })
        return ground_truth
