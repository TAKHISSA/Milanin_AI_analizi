import openai
import os
import json
import re
import time
from typing import Literal
from pydantic import BaseModel, Field
from config.settings import settings

# Structured output model for our analysis
class ChatAnalysis(BaseModel):
    """Sohbet analizi için yapılandırılmış çıktı modeli"""
    
    yanıt_durumu: Literal["Çözüldü", "Çözülemedi"] = Field(
        description="Sohbetin sonuç durumu"
    )
    
    sentiment: Literal["Negatif", "Pozitif", "Nötr"] = Field(
        description="Müşterinin duygu durumu"
    )
    
    tür: Literal["Soru", "Şikayet", "İstek", "Sorun", "Bilgi alma", "İade"] = Field(
        description="Sohbetin türü"
    )
    
    intent: Literal["Eksik ürün","Şifre sıfırlama","İade","Kupon","İptal","Defolu ürün","Hesap bilgisi","Fatura hatası","Stok","Ödeme","Kargo","Beden tablosu","Adres hatası","Yorum","Web sitesi","Ürün","Hasarlı ürün","Değişim","İndirim","Yanlış ürün","Hesap kapatma","Sipariş","Beden","Teknik sorun","Abonelik"] = Field(
        description="Müşterinin niyeti"
    )
    
    intent_detay: str = Field(
        description="Niyet detayı açıklaması",
        max_length=100
    )

class ChatAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.MODEL_NAME
        self.api_delay = 0.5  # API çağrıları arası bekleme süresi
        self.system_prompt = self._load_system_prompt()
        
    def _load_system_prompt(self):
        """Sistem promptunu dosyadan yükler"""
        try:
            prompt_path = os.path.join('prompts', 'system_prompt.txt')
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print("❌ Prompt dosyası bulunamadı, varsayılan prompt kullanılıyor...")
            return "Müşteri sohbetlerini analiz et: yanıt durumu, sentiment, tür, intent ve intent detayı."
        except Exception as e:
            print(f"❌ Prompt yükleme hatası: {e}")
            return "Müşteri sohbetlerini analiz et: yanıt durumu, sentiment, tür, intent ve intent detayı."
    
    def analyze_chat(self, chat_data):
        """
        Tek bir sohbeti analiz eder
        """
        prompt = self._create_analysis_prompt(chat_data)
        response = self._get_api_response(prompt)
        return self._parse_response(response)
    
    def _create_analysis_prompt(self, chat_data):
        """
        API için analiz promptu oluşturur - SADELEŞTİRİLMİŞ
        """
        # Sohbet metnini formatla
        chat_text = ""
        for message in chat_data.get('mesajlar', []):
            sender = "Müşteri" if message.get('sender') == 'Müşteri' else "Bot"
            chat_text += f"{sender}: {message.get('text', '')}\n"
    
        # Sadece sohbet metni - kurallar system prompt'ta zaten var
        return f"Aşağıdaki sohbeti analiz edin:\n\n{chat_text}"
    
    def _get_api_response(self, prompt):
        """
        API'den yanıt alır
        """
        try:
            # Konuşma metnini kısalt (token tasarrufu)
            if len(prompt) > 1000:
                prompt = prompt[:1000] + "..."
            
            completion = self.client.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                response_format=ChatAnalysis,
                max_completion_tokens=200,
                reasoning_effort="minimal",  # Token tasarrufu için
            )
            
            parsed = completion.choices[0].message.parsed
            
            if parsed is None:
                raise ValueError("Parsed result is None")
            
            # Pydantic modelini dict'e çevir
            result = parsed.model_dump()
            print(f"✅ API başarılı: {result}")
            return result
            
        except Exception as e:
            print(f"❌ API hatası: {str(e)[:200]}")
            # Hata durumunda fallback değerler
            return {
                "yanıt_durumu": "Çözülemedi",
                "sentiment": "Nötr", 
                "tür": "Sorun",
                "intent": "Diğer",
                "intent_detay": "Analiz hatası"
            }
    
    def _parse_response(self, response_data):
        """
        API yanıtını ayrıştırır
        """
        return response_data
    
    def analyze_all_chats(self, chats):
        """
        Tüm sohbetleri analiz eder
        """
        results = []
        success_count = 0
        
        for i, chat_info in enumerate(chats, 1):
            print(f"🔄 Analiz: {i}/{len(chats)} - Sohbet ID: {chat_info['sohbet_id']}")
            
            try:
                analysis_result = self.analyze_chat(chat_info['raw_chat'])
                
                # Temel bilgilerle birleştir
                combined_result = {**chat_info, **analysis_result}
                results.append(combined_result)
                success_count += 1
                
                # Her 3 analizde bir bekle (rate limiting)
                if i % 3 == 0:
                    time.sleep(self.api_delay)
                    
            except Exception as e:
                print(f"❌ Analiz hatası: {e}")
                # Hata durumunda fallback değerlerle devam et
                fallback_result = {
                    **chat_info,
                    "yanıt_durumu": "Çözülemedi",
                    "sentiment": "Nötr",
                    "tür": "Sorun",
                    "intent": "Diğer",
                    "intent_detay": "Analiz hatası"
                }
                results.append(fallback_result)
        
        print(f"📊 Analiz tamamlandı: {success_count}/{len(chats)} başarılı")
        return results
