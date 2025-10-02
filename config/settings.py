import os
from dotenv import load_dotenv

# Çevresel değişkenleri yükle
load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-5-nano")
    DATA_FILE = "data/40-sohbet-trendyol-mila.json"
    OUTPUT_EXCEL = "outputs/excel_raporlar/sohbet_analiz.xlsx"
    OUTPUT_SWOT = "outputs/swot_analizi.txt"
    OUTPUT_RECOMMENDATIONS = "outputs/bot_önerileri.txt"
    OUTPUT_DEMAND_SUMMARY = "outputs/talep_özeti.txt"

settings = Settings()
