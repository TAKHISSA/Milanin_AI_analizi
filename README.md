# 📊 Mila'nın AI Analiz Aracı

Mila'nın AI Analiz Aracı, müşteri–bot sohbetlerini yapay zekâ ile analiz eden Python tabanlı bir sistemdir. Bu proje, Trendyol’un yapay zekâ destekli müşteri hizmetleri analiz aracının ilk prototipi olarak geliştirilmiştir.

## ✨ Özellikler

*   **✅ Sohbet Analizi & Etiketleme:** `yanıt_durumu`, `sentiment`, `tür`, `intent`, `intent_detay` gibi detaylı etiketler.
*   **📊 Doğruluk Ölçümü:** AI çıktılarının hazır etiketlerle kıyaslanması.
*   **📝 SWOT Analizi:** Botun Güçlü ve Zayıf Yönleri ile Fırsatlar ve Tehditlerin analizi.
*   **💡 Bot Geliştirme Önerileri:** Empati, yönlendirme, şablon iyileştirmeleri vb. konularda öneriler.
*   **📋 Müşteri Talepleri Özeti:** En sık karşılaşılan talep ve sorunların özeti.
*   **📂 Excel Çıktısı:** Sohbet bazlı etiketler ve zaman bilgilerini içeren rapor.
*   **📈 Doğruluk Raporu:** Alan bazlı doğruluk yüzdeleri.
*   **🤖 Akıllı Prompt Mimarisi:** Kural bazlı yaklaşımdan ziyade çok yönlü analiz ve yönlendirme kapasiteli prompt sistemi.

---

## 📂 Veri Seti

*   **Dosya:** `40-sohbet-trendyol-mila.json`
*   **İçerik:** 40 adet gerçek müşteri–bot sohbeti.
*   **Etiketler:** Sohbetler için önceden hazırlanmış (ground truth) etiketler mevcuttur.

---

## 📊 Doğruluk Ölçüm Raporu 

| Alan             | Doğruluk (%) |
|------------------|-------------|
| **yanıt_durumu** | 97.5%       |
| **sentiment**    | 100.0%       |
| **tür**          | 80.0%       |
| **intent**       | 90.0%       |

---

## 📈 Çıktılar

*   `📂 Excel Raporu` → Sohbet bazlı etiketleme ve zaman bilgileri.
*   `📊 Doğruluk Raporu` → Alan bazlı doğruluk yüzdeleri.
*   `📝 SWOT Analizi` → Botun performansına dair detaylı analiz.
*   `💡 Bot Geliştirme Önerileri` → Pratik iyileştirme tavsiyeleri.
*   `📋 Müşteri Talepleri Özeti` → İade, kargo takibi, kupon vb. taleplerin özeti.

---

## 🚀 Proje Yapısı
```
Milanin_AI_analizi/
├── README.md
├── config
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   └── settings.cpython-313.pyc
│   └── settings.py
├── data
│   └── 40-sohbet-trendyol-mila.json
├── outputs
│   ├── bot_önerileri.txt
│   ├── dogruluk_raporu.txt
│   ├── doğruluk_raporu.txt
│   ├── excel_raporlar
│   │   └── sohbet_analiz.xlsx
│   ├── swot_analizi.txt
│   └── talep_özeti.txt
├── prompts
│   └── system_prompt.txt
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-313.pyc
│   │   ├── chat_analyzer.cpython-313.pyc
│   │   ├── data_processor.cpython-313.pyc
│   │   ├── main.cpython-313.pyc
│   │   └── report_generator.cpython-313.pyc
│   ├── chat_analyzer.py
│   ├── data_processor.py
│   ├── main.py
│   └── report_generator.py
└── utils
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-313.pyc
    │   └── helpers.cpython-313.pyc
    └── helpers.py
```

---

## ⚙️ Kurulum

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/TAKHISSA/Milanin_AI_analizi.git
    cd Milanin_AI_analizi
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Programı Çalıştırın:**
    ```bash
    python -m src.main
    ```

---

## 📦 Kullanılan Teknolojiler

### 🔧 Programlama Dili
- 🐍 Python `3.10+`

### 📊 Veri İşleme ve Analiz
- 📊 Pandas `2.3.1` – Veri işleme ve analiz  
- 🔢 NumPy `2.2.6` – Sayısal hesaplama kütüphanesi  
- ⏱️ python-dateutil `2.9.0.post0` – Tarih ve zaman işlemleri  

### 📑 Dosya İşleme
- 📗 OpenPyXL `3.1.5` – Excel dosyaları oluşturma ve düzenleme  

### 📈 Görselleştirme
- 📉 Matplotlib `3.10.3` – Grafik çizimi  
- 🎨 Seaborn `0.13.2` – İstatistiksel veri görselleştirme  

### ⚙️ Ortam Yönetimi
- 🌍 python-dotenv `1.1.1` – `.env` dosyalarından ortam değişkenleri yönetimi  

### ✅ Veri Doğrulama
- 🛡️ Pydantic `2.11.7` – Veri modelleme ve doğrulama  

### 🤖 Yapay Zekâ
- 🤖 OpenAI (GPT-5 nano API) `1.99.1` – Sohbet analizi ve büyük dil modeli entegrasyonu  


---

## 📈 Kullanım Adımları

1.  **Sohbet Verisini Yükle:** `40-sohbet-trendyol-mila.json` dosyasını işle.
2.  **Sohbetleri Analiz Et:** Her sohbeti AI ile etiketle ve Excel çıktısını (`outputs/`) oluştur.
3.  **Doğruluğu Ölç:** AI etiketlerini hazır etiketlerle kıyasla ve raporu oluştur.
4.  **Stratejik Analiz Yap:** SWOT analizini ve bot geliştirme önerilerini otomatik üret.
5.  **Özet Çıkar:** Müşteri taleplerini özetle ve genel eğilimleri raporla.

---

## 👨‍💻 Geliştirici

**Emre Altundağ**  
[🌐 GitHub](https://github.com/TAKHISSA) • [💼 LinkedIn](https://www.linkedin.com/in/emre-altundag-830882271)









