from utils.helpers import save_to_txt
from collections import Counter, defaultdict
import statistics
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.analyzed_model_name = "Mila"  # Analiz edilen modelin adı
        self.analysis_model = "GPT-5nano"  # Analizi yapan model
    
    def set_model_names(self, analyzed_model, analysis_model="GPT-5nano"):
        """Model isimlerini ayarlar"""
        self.analyzed_model_name = analyzed_model
        self.analysis_model = analysis_model
    
    def generate_swot(self, analysis_results):
        """Detaylı SWOT analizi oluşturur - Analiz edilen model için"""
        strengths = []
        weaknesses = []
        opportunities = []
        threats = []
        
        # İstatistiksel veriler
        total_chats = len(analysis_results)
        resolved_count = sum(1 for r in analysis_results if r.get('yanıt_durumu') == 'Çözüldü')
        unresolved_count = sum(1 for r in analysis_results if r.get('yanıt_durumu') == 'Çözülemedi')
        positive_sentiment = sum(1 for r in analysis_results if r.get('sentiment') == 'Pozitif')
        negative_sentiment = sum(1 for r in analysis_results if r.get('sentiment') == 'Negatif')
        neutral_sentiment = sum(1 for r in analysis_results if r.get('sentiment') == 'Nötr')
        
        # Tür ve intent dağılımı
        tur_counts = Counter(r.get('tür', '') for r in analysis_results)
        intent_counts = Counter(r.get('intent', '') for r in analysis_results)
        
        # Yanıt kalitesi metrikleri - DÜZELTME: yanıt_metni yerine intent_detay kullan
        response_lengths = [
            len(str(r.get('intent_detay', ''))) 
            for r in analysis_results 
            if r.get('intent_detay') and str(r.get('intent_detay', '')).strip()
        ]
        
        # Ortalama hesaplama - boş liste kontrolü
        avg_response_length = statistics.mean(response_lengths) if response_lengths else 0
        
        # Güçlü Yönler (Analiz edilen modelin)
        if resolved_count > 0:
            resolution_rate = (resolved_count / total_chats) * 100
            if resolution_rate >= 80:
                strengths.append(f"Üstün çözüm oranı (%{resolution_rate:.1f}) - müşteri sorunlarının büyük kısmını çözebiliyor")
            elif resolution_rate >= 60:
                strengths.append(f"İyi çözüm oranı (%{resolution_rate:.1f}) - temel sorunları etkili şekilde çözüyor")
            else:
                strengths.append(f"Temel çözüm yeteneği (%{resolution_rate:.1f}) - bazı sorunları çözebiliyor")
        
        if positive_sentiment > 0:
            positive_rate = (positive_sentiment / total_chats) * 100
            if positive_rate >= 70:
                strengths.append(f"Mükemmel müşteri deneyimi (%{positive_rate:.1f}) - kullanıcıların çoğu memnun")
            elif positive_rate >= 50:
                strengths.append(f"Olumlu müşteri etkileşimi (%{positive_rate:.1f}) - kullanıcılar genellikle memnun")
            else:
                strengths.append(f"Kabul edilebilir müşteri tepkisi (%{positive_rate:.1f}) - bazı kullanıcılar memnun")
        
        # Çeşitli intent'lere yanıt verebilme
        unique_intents = len(intent_counts)
        if unique_intents >= 10:
            strengths.append(f"Geniş kapsamlı anlama yeteneği - {unique_intents} farklı niyeti anlayabiliyor")
        elif unique_intents >= 5:
            strengths.append(f"Çok yönlü yanıt kapasitesi - {unique_intents} farklı niyete cevap verebiliyor")
        
        # Zayıf Yönler
        if unresolved_count > 0:
            unresolved_rate = (unresolved_count / total_chats) * 100
            if unresolved_rate >= 40:
                weaknesses.append(f"Ciddi çözüm açığı (%{unresolved_rate:.1f}) - sohbetlerin neredeyse yarısı çözümsüz kalıyor")
            elif unresolved_rate >= 20:
                weaknesses.append(f"Önemli çözüm eksikliği (%{unresolved_rate:.1f}) - her 5 sohbetten 1'i çözülemiyor")
            else:
                weaknesses.append(f"Sınırlı çözüm kapasitesi (%{unresolved_rate:.1f}) - bazı karmaşık sorunları çözemiyor")
        
        if negative_sentiment > 0:
            negative_rate = (negative_sentiment / total_chats) * 100
            if negative_rate >= 30:
                weaknesses.append(f"Ciddi müşteri memnuniyetsizliği (%{negative_rate:.1f}) - kullanıcıların üçte biri memnun değil")
            elif negative_rate >= 15:
                weaknesses.append(f"Kayda değer olumsuz tepki (%{negative_rate:.1f}) - önemli sayıda kullanıcı memnun değil")
        
        # Çözülemeyen sohbetlerin detaylı analizi
        unresolved_chats = [r for r in analysis_results if r.get('yanıt_durumu') == 'Çözülemedi']
        if unresolved_chats:
            unresolved_intents = Counter(r.get('intent', '') for r in unresolved_chats)
            for intent, count in unresolved_intents.most_common(3):
                intent_failure_rate = (count / len(unresolved_chats)) * 100
                weaknesses.append(f"'{intent}' konusunda kritik başarısızlık - çözülemeyen sohbetlerin %{intent_failure_rate:.1f}'u")
        
        # Fırsatlar
        for intent, count in intent_counts.most_common(5):
            intent_rate = (count / total_chats) * 100
            if intent_rate >= 15:
                opportunities.append(f"'{intent}' alanında uzmanlaşma - taleplerin %{intent_rate:.1f}'i bu alandan geliyor")
            elif intent_rate >= 8:
                opportunities.append(f"'{intent}' konusunda derinleşme - önemli talep yoğunluğu (%{intent_rate:.1f}) mevcut")
        
        # Teknik iyileştirme fırsatları
        if avg_response_length > 0:
            if avg_response_length < 50:
                opportunities.append(f"Kısa ve öz yanıt yapısı - ortalama {avg_response_length:.0f} karakter ile hızlı iletişim")
            elif avg_response_length > 200:
                opportunities.append(f"Detaylı açıklama potansiyeli - ortalama {avg_response_length:.0f} karakter ile kapsamlı yanıtlar")
        
        # Tehditler
        if negative_sentiment > total_chats * 0.3:
            threats.append("Yüksek müşteri kaybı riski - negatif deneyim oranı kabul edilemez seviyede")
        
        if unresolved_count > total_chats * 0.4:
            threats.append("Marka itibarı tehlikesi - çözümsüz sohbet oranı müşteri güvenini sarsıyor")
        
        # Benzersiz hale getir ve sırala
        strengths = list(dict.fromkeys(strengths))
        weaknesses = list(dict.fromkeys(weaknesses))
        opportunities = list(dict.fromkeys(opportunities))
        threats = list(dict.fromkeys(threats))
        
        swot_text = f"DETAYLI {self.analyzed_model_name.upper()} SWOT ANALİZİ\n"
        swot_text += "=" * 60 + "\n\n"
        swot_text += f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        swot_text += f"Analizi Yapan: {self.analysis_model}\n"
        swot_text += f"Analiz Edilen: {self.analyzed_model_name}\n\n"
        
        swot_text += "📊 GENEL PERFORMANS İSTATİSTİKLERİ:\n"
        swot_text += "-" * 40 + "\n"
        swot_text += f"• Toplam Analiz Edilen Sohbet: {total_chats}\n"
        swot_text += f"• Başarıyla Çözülen: {resolved_count} (%{(resolved_count/total_chats)*100:.1f})\n"
        swot_text += f"• Çözülemeyen: {unresolved_count} (%{(unresolved_count/total_chats)*100:.1f})\n"
        swot_text += f"• Pozitif Deneyim: {positive_sentiment} (%{(positive_sentiment/total_chats)*100:.1f})\n"
        swot_text += f"• Negatif Deneyim: {negative_sentiment} (%{(negative_sentiment/total_chats)*100:.1f})\n"
        swot_text += f"• Nötr Deneyim: {neutral_sentiment} (%{(neutral_sentiment/total_chats)*100:.1f})\n"
        swot_text += f"• Anlaşılan Farklı Niyet Sayısı: {len(intent_counts)}\n"
        swot_text += f"• Ortalama Yanıt Uzunluğu: {avg_response_length:.0f} karakter\n\n"
        
        swot_text += "💪 GÜÇLÜ YÖNLER:\n"
        swot_text += "-" * 20 + "\n"
        for i, strength in enumerate(strengths[:8], 1):
            swot_text += f"{i}. ✅ {strength}\n"
        if not strengths:
            swot_text += "• Tespit edilen belirgin güçlü yön bulunamadı\n"
        swot_text += "\n"
        
        swot_text += "⚠️ ZAYIF YÖNLER:\n"
        swot_text += "-" * 20 + "\n"
        for i, weakness in enumerate(weaknesses[:8], 1):
            swot_text += f"{i}. ❌ {weakness}\n"
        if not weaknesses:
            swot_text += "• Tespit edilen kritic zayıf yön bulunamadı\n"
        swot_text += "\n"
        
        swot_text += "🚀 FIRSATLAR:\n"
        swot_text += "-" * 20 + "\n"
        for i, opportunity in enumerate(opportunities[:8], 1):
            swot_text += f"{i}. 🔮 {opportunity}\n"
        if not opportunities:
            swot_text += "• Belirgin gelişim fırsatı tespit edilemedi\n"
        swot_text += "\n"
        
        swot_text += "🔴 TEHDİTLER:\n"
        swot_text += "-" * 20 + "\n"
        for i, threat in enumerate(threats[:5], 1):
            swot_text += f"{i}. ⚠️ {threat}\n"
        if not threats:
            swot_text += "• Acil müdahale gerektiren tehdit tespit edilmedi\n"
        
        return swot_text
    
    def generate_recommendations(self, analysis_results):
        """Detaylı model geliştirme önerileri oluşturur"""
        recommendations = []
        
        # Temel istatistikler
        total_chats = len(analysis_results)
        unresolved_chats = [r for r in analysis_results if r.get('yanıt_durumu') == 'Çözülemedi']
        negative_chats = [r for r in analysis_results if r.get('sentiment') == 'Negatif']
        
        # Çözülemeyen sohbetlerin detaylı analizi
        if unresolved_chats:
            unresolved_rate = (len(unresolved_chats) / total_chats) * 100
            unresolved_intents = Counter(r.get('intent', '') for r in unresolved_chats)
            unresolved_tur = Counter(r.get('tür', '') for r in unresolved_chats)
            
            recommendations.append(f"🎯 **ÇÖZÜM ORANI İYİLEŞTİRME** (%{unresolved_rate:.1f} çözülemeyen sohbet):")
            
            for intent, count in unresolved_intents.most_common(3):
                intent_failure_rate = (count / len(unresolved_chats)) * 100
                recommendations.append(f"   • '{intent}' intent'i için özel eğitim verilmeli (%{intent_failure_rate:.1f} çözümsüzlük)")
            
            # Tür bazlı öneriler
            for tur, count in unresolved_tur.most_common(2):
                recommendations.append(f"   • {tur} türündeki sorgulara özel çözüm akışları geliştirilmeli")
        
        # Negatif sentiment analizi
        if negative_chats:
            negative_rate = (len(negative_chats) / total_chats) * 100
            negative_intents = Counter(r.get('intent', '') for r in negative_chats)
            
            recommendations.append(f"😊 **MÜŞTERİ DENEYİMİ İYİLEŞTİRME** (%{negative_rate:.1f} negatif deneyim):")
            
            for intent, count in negative_intents.most_common(3):
                recommendations.append(f"   • '{intent}' sürecinde daha empatik dil kullanılmalı")
            
            recommendations.append(f"   • Olumsuz durumlarda 'özür ve telafi' şablonları entegre edilmeli")
            recommendations.append(f"   • Duygu analizi modülü güçlendirilmeli")
        
        # Intent bazlı optimizasyon önerileri
        intent_counts = Counter(r.get('intent', '') for r in analysis_results)
        tur_counts = Counter(r.get('tür', '') for r in analysis_results)
        
        recommendations.append(f"📈 **INTENT BAZLI OPTİMİZASYON**:")
        top_intents = intent_counts.most_common(6)
        for intent, count in top_intents:
            intent_rate = (count / total_chats) * 100
            if intent_rate > 10:
                recommendations.append(f"   • '{intent}': YÜKSEK ÖNCELİK - %{intent_rate:.1f} talep oranı")
            elif intent_rate > 5:
                recommendations.append(f"   • '{intent}': ORTA ÖNCELİK - %{intent_rate:.1f} talep oranı")
            else:
                recommendations.append(f"   • '{intent}': DÜŞÜK ÖNCELİK - %{intent_rate:.1f} talep oranı")
        
        # Teknik iyileştirme önerileri
        recommendations.append(f"⚙️ **TEKNİK İYİLEŞTİRMELER**:")
        recommendations.append(f"   • Doğal dil anlama (NLU) modeli Türkçe için optimize edilmeli")
        recommendations.append(f"   • Context ve bellek yönetimi geliştirilmeli")
        recommendations.append(f"   • Gerçek zamanlı öğrenme ve adaptasyon mekanizması eklenmeli")
        recommendations.append(f"   • Hata yönetimi ve esnek yanıt sistemleri kurulmalı")
        
        # Performans ölçüm önerileri
        recommendations.append(f"📊 **PERFORMANS TAKİP SİSTEMLERİ**:")
        recommendations.append(f"   • Detaylı analytics dashboard oluşturulmalı")
        recommendations.append(f"   • KPI (Key Performance Indicators) metrikleri tanımlanmalı")
        recommendations.append(f"   • Kullanıcı geri bildirim loop'u kurulmalı")
        recommendations.append(f"   • ROI (Return on Investment) ölçüm mekanizması geliştirilmeli")
        
        rec_text = f"DETAYLI {self.analyzed_model_name.upper()} GELİŞTİRME ÖNERİLERİ\n"
        rec_text += "=" * 60 + "\n\n"
        rec_text += f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        rec_text += f"Analizi Yapan: {self.analysis_model}\n"
        rec_text += f"Analiz Edilen: {self.analyzed_model_name}\n\n"
        
        rec_text += "📈 PERFORMANS ÖZETİ:\n"
        rec_text += f"• Toplam Analiz: {total_chats} sohbet\n"
        rec_text += f"• Çözülemeyen: {len(unresolved_chats)} sohbet (%{(len(unresolved_chats)/total_chats)*100:.1f})\n"
        rec_text += f"• Negatif Deneyim: {len(negative_chats)} sohbet (%{(len(negative_chats)/total_chats)*100:.1f})\n"
        rec_text += f"• Başarı Oranı: %{((total_chats - len(unresolved_chats)) / total_chats) * 100:.1f}\n\n"
        
        rec_text += "💡 DETAYLI ÖNERİLER:\n"
        rec_text += "-" * 30 + "\n"
        
        for i, rec in enumerate(recommendations, 1):
            if rec.startswith(('🎯', '😊', '📈', '⚙️', '📊')):
                rec_text += f"\n{rec}\n"
            else:
                rec_text += f"{rec}\n"
        
        rec_text += f"\n🔮 **GENEL DEĞERLENDİRME**:\n"
        rec_text += f"{self.analyzed_model_name} modeli, temel müşteri hizmetleri ihtiyaçlarını karşılayabilmektedir. "
        rec_text += "Önerilen iyileştirmelerle performansı %30-50 oranında artırılabilir."
            
        return rec_text

    def calculate_accuracy(self, analysis_results, ground_truth):
        """Doğruluk ölçümü yapar - Analiz edilen modelin performansı için"""
        accuracy_results = {
            'yanıt_durumu': {'correct': 0, 'total': 0},
            'sentiment': {'correct': 0, 'total': 0},
            'tür': {'correct': 0, 'total': 0},
            'intent': {'correct': 0, 'total': 0}
        }
    
        field_mapping = {
            'yanit_durumu': 'yanıt_durumu',
            'sentiment': 'sentiment', 
            'tur': 'tür',
            'intent': 'intent'
        }
    
        for ai_result in analysis_results:
            sohbet_id = ai_result.get('sohbet_id')
            truth = next((item for item in ground_truth if item['sohbet_id'] == sohbet_id), None)
        
            if truth:
                for truth_field, ai_field in field_mapping.items():
                    ai_value = ai_result.get(ai_field, '').lower().strip()
                    truth_value = truth.get(truth_field, '').lower().strip()
                
                    if ai_value and truth_value:
                        accuracy_results[ai_field]['total'] += 1
                        if ai_value == truth_value:
                            accuracy_results[ai_field]['correct'] += 1
    
        accuracy_percentages = {}
        for field, counts in accuracy_results.items():
            if counts['total'] > 0:
                accuracy_percentages[field] = round((counts['correct'] / counts['total']) * 100, 1)
            else:
                accuracy_percentages[field] = 0
    
        return accuracy_percentages

    def generate_accuracy_report(self, accuracy_results):
        """Detaylı doğruluk raporu oluşturur"""
        report = f"DETAYLI {self.analyzed_model_name.upper()} DOĞRULUK RAPORU\n"
        report += "=" * 60 + "\n\n"
        report += f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"Analizi Yapan: {self.analysis_model}\n"
        report += f"Analiz Edilen: {self.analyzed_model_name}\n\n"
        
        report += "📊 KATEGORİ BAZINDA DOĞRULUK ORANLARI:\n"
        report += "-" * 45 + "\n"
        
        performance_icons = {
            'yanıt_durumu': '✅', 
            'sentiment': '😊', 
            'tür': '📝', 
            'intent': '🎯'
        }
        
        performance_descriptions = []
        
        for field, accuracy in accuracy_results.items():
            icon = performance_icons.get(field, '📊')
            
            if accuracy >= 90:
                level = "MÜKEMMEL"
                color = "🟢"
            elif accuracy >= 80:
                level = "İYİ"
                color = "🟡"
            elif accuracy >= 70:
                level = "ORTA"
                color = "🟠"
            elif accuracy >= 60:
                level = "ZAYIF"
                color = "🔴"
            else:
                level = "KRİTİK"
                color = "💥"
            
            report += f"{icon} {field.upper()}: {color} %{accuracy} - {level}\n"
            performance_descriptions.append((field, accuracy, level))
        
        # Genel değerlendirme
        avg_accuracy = sum(accuracy_results.values()) / len(accuracy_results)
        
        if avg_accuracy >= 90:
            overall = "MÜKEMMEL PERFORMANS"
            recommendation = "Model üretim ortamında güvenle kullanılabilir"
        elif avg_accuracy >= 80:
            overall = "İYİ PERFORMANS"
            recommendation = "Model kullanılabilir, küçük iyileştirmeler önerilir"
        elif avg_accuracy >= 70:
            overall = "ORTA PERFORMANS"
            recommendation = "Model geliştirme gerektiriyor"
        elif avg_accuracy >= 60:
            overall = "ZAYIF PERFORMANS"
            recommendation = "Model ciddi iyileştirme gerektiriyor"
        else:
            overall = "KRİTİK DURUM"
            recommendation = "Model üretimde kullanılmamalı"
        
        report += f"\n🎯 GENEL DEĞERLENDİRME:\n"
        report += f"• Ortalama Doğruluk: %{avg_accuracy:.1f}\n"
        report += f"• Performans Seviyesi: {overall}\n"
        report += f"• Öneri: {recommendation}\n\n"
        
        report += "📈 PERFORMANS DETAYLARI:\n"
        for field, accuracy, level in performance_descriptions:
            report += f"• {field.upper()}: %{accuracy} ({level})\n"
        
        return report
    
    def generate_demand_summary(self, analysis_results):
        """Detaylı müşteri talepleri özeti oluşturur"""
        intent_counts = Counter()
        intent_details = defaultdict(set)
        intent_by_tur = defaultdict(Counter)
        sentiment_by_intent = defaultdict(Counter)
        resolution_by_intent = defaultdict(Counter)
        
        for result in analysis_results:
            intent = result.get('intent', 'Diğer')
            detail = result.get('intent_detay', 'Belirtilmemiş')
            tur = result.get('tür', 'Belirsiz')
            sentiment = result.get('sentiment', 'Belirsiz')
            resolution = result.get('yanıt_durumu', 'Belirsiz')
            
            intent_counts[intent] += 1
            intent_details[intent].add(detail)
            intent_by_tur[intent][tur] += 1
            sentiment_by_intent[intent][sentiment] += 1
            resolution_by_intent[intent][resolution] += 1
        
        # İstatistikler
        total = sum(intent_counts.values())
        intent_percentages = {k: round((v/total)*100, 1) for k, v in intent_counts.items()}
        sorted_intents = sorted(intent_percentages.items(), key=lambda x: x[1], reverse=True)
        
        summary_text = f"DETAYLI {self.analyzed_model_name.upper()} TALEP ANALİZİ\n"
        summary_text += "=" * 60 + "\n\n"
        summary_text += f"Analiz Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary_text += f"Analizi Yapan: {self.analysis_model}\n"
        summary_text += f"Analiz Edilen: {self.analyzed_model_name}\n\n"
        
        summary_text += "📈 GENEL İSTATİSTİKLER:\n"
        summary_text += "-" * 25 + "\n"
        summary_text += f"• Toplam Talep: {total}\n"
        summary_text += f"• Benzersiz Intent Sayısı: {len(intent_counts)}\n"
        summary_text += f"• En Yaygın 5 Talep: %{sum([p for _, p in sorted_intents[:5]])} toplamın\n"
        summary_text += f"• Talep Çeşitlilik Oranı: %{(len(intent_counts) / total) * 100:.1f}\n\n"
        
        summary_text += "🎯 TALEP DAĞILIMI (ÖNCELİK SIRASINA GÖRE):\n"
        summary_text += "-" * 55 + "\n\n"
        
        for intent, percentage in sorted_intents:
            count = intent_counts[intent]
            summary_text += f"🔹 {intent.upper()}: %{percentage} ({count} talep)\n"
            
            # Çözüm oranı
            resolution_dist = resolution_by_intent[intent]
            resolved_count = resolution_dist.get('Çözüldü', 0)
            resolution_rate = (resolved_count / count) * 100 if count > 0 else 0
            
            resolution_icon = "✅" if resolution_rate >= 80 else "⚠️" if resolution_rate >= 60 else "❌"
            summary_text += f"   {resolution_icon} Çözüm Oranı: %{resolution_rate:.1f}\n"
            
            # Tür dağılımı
            tur_dist = intent_by_tur[intent]
            if tur_dist:
                summary_text += "   📝 Tür Dağılımı: "
                tur_texts = []
                for tur_name, tur_count in tur_dist.most_common():
                    tur_percentage = (tur_count / count) * 100
                    tur_texts.append(f"{tur_name} (%{tur_percentage:.1f})")
                summary_text += ", ".join(tur_texts) + "\n"
            
            # Sentiment dağılımı
            sentiment_dist = sentiment_by_intent[intent]
            if sentiment_dist:
                summary_text += "   😊 Sentiment: "
                sentiment_texts = []
                for sent_name, sent_count in sentiment_dist.most_common():
                    sent_percentage = (sent_count / count) * 100
                    sentiment_icon = "😊" if sent_name == 'Pozitif' else "😐" if sent_name == 'Nötr' else "😞"
                    sentiment_texts.append(f"{sentiment_icon} %{sent_percentage:.1f}")
                summary_text += " | ".join(sentiment_texts) + "\n"
            
            # Detaylar
            if intent in intent_details:
                details_list = list(intent_details[intent])
                summary_text += f"   📋 Detay Çeşitliliği: {len(details_list)} farklı varyasyon\n"
                for i, detail in enumerate(details_list[:3], 1):
                    summary_text += f"      {i}. {detail}\n"
                if len(details_list) > 3:
                    summary_text += f"      ... ve {len(details_list) - 3} detay daha\n"
            
            summary_text += "\n"
        
        # Trend analizi ve öneriler
        summary_text += "📊 TREND ANALİZİ & STRATEJİ ÖNERİLERİ:\n"
        summary_text += "-" * 45 + "\n"
        
        high_demand = [(intent, perc) for intent, perc in sorted_intents if perc >= 10]
        medium_demand = [(intent, perc) for intent, perc in sorted_intents if 5 <= perc < 10]
        low_demand = [(intent, perc) for intent, perc in sorted_intents if perc < 5]
        
        summary_text += f"🚀 Yüksek Talep (>%10): {len(high_demand)} kategori\n"
        for intent, perc in high_demand:
            summary_text += f"   • {intent} (%{perc}) - ÖNcelikli geliştirme alanı\n"
        
        summary_text += f"\n📈 Orta Talep (%5-10): {len(medium_demand)} kategori\n"
        for intent, perc in medium_demand[:3]:
            summary_text += f"   • {intent} (%{perc}) - İkincil geliştirme alanı\n"
        
        summary_text += f"\n📉 Düşük Talep (<%5): {len(low_demand)} kategori\n"
        summary_text += f"   • Toplam: %{sum([p for _, p in low_demand]):.1f} talep oranı\n"
        
        return summary_text
    
    def save_all_reports(self, analysis_results, ground_truth, output_paths):
        """Tüm detaylı raporları kaydeder"""
        # Model ismini analiz sonuçlarından çıkar
        if analysis_results:
            first_result = analysis_results[0]
            if 'model_adi' in first_result:
                self.analyzed_model_name = first_result['model_adi']
        
        swot = self.generate_swot(analysis_results)
        recommendations = self.generate_recommendations(analysis_results)
        demand_summary = self.generate_demand_summary(analysis_results)
        
        accuracy_results = self.calculate_accuracy(analysis_results, ground_truth)
        accuracy_report = self.generate_accuracy_report(accuracy_results)
        
        # Dosyalara kaydet
        save_to_txt(output_paths.get('swot', 'outputs/swot_analizi.txt'), swot)
        save_to_txt(output_paths.get('recommendations', 'outputs/oneriler.txt'), recommendations)
        save_to_txt(output_paths.get('demand_summary', 'outputs/talepler_ozeti.txt'), demand_summary)
        save_to_txt(output_paths.get('accuracy_report', 'outputs/dogruluk_raporu.txt'), accuracy_report)
        
        return {
            'swot': swot,
            'recommendations': recommendations,
            'demand_summary': demand_summary,
            'accuracy_report': accuracy_report
        }
