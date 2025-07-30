import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Poliçe Gider Dağılımı", layout="centered")
st.title("📆 Poliçe Gider Dağılım Hesaplayıcı")
st.markdown("Başlangıç tarihini ve tutarı gir, sistem yıl ve aya göre dağıtım yapsın. %30 KKEG içerir.")

# Girdi
tarih_input = st.date_input("📅 Poliçe Başlangıç Tarihi", datetime.today())
tutar_input = st.number_input("💰 Toplam Poliçe Tutarı (TL)", min_value=0.0, value=10000.0)

kkeg_orani = 0.30
gider_orani = 1 - kkeg_orani

if st.button("📊 Hesapla"):
    gunluk_tutar = tutar_input * gider_orani / 365
    kalan_tutar = tutar_input * gider_orani
    tarih = tarih_input
    topla
