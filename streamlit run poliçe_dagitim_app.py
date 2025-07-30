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
    toplam_gun = 0
    rows = []

    # Vergi dönemi
    donemler = {
        1: [1, 2, 3],
        2: [4, 5, 6],
        3: [7, 8, 9],
        4: [10, 11, 12]
    }

    def get_donem(ay):
        for key, val in donemler.items():
            if ay in val:
                return f"{key}. Dönem"
        return "?"

    while kalan_tutar > 0 and toplam_gun < 365:
        next_month = tarih.month % 12 + 1
        year = tarih.year + (1 if tarih.month == 12 else 0)
        ay_sonu = datetime(year, next_month, 1) - timedelta(days=1)

        gun_sayisi = (ay_sonu - tarih).days + 1
        if toplam_gun + gun_sayisi > 365:
            gun_sayisi = 365 - toplam_gun

        tutar = round(gun_sayisi * gunluk_tutar, 2)
        vergi_donemi = get_donem(tarih.month)
        muhasebe_hesabi = "770" if tarih.year == tarih_input.year else "280"

        rows.append({
            "Yıl": tarih.year,
            "Ay": tarih.strftime("%B"),
            "Tarih (Ay Başlangıcı)": tarih.strftime("%d.%m.%Y"),
            "Gün Sayısı": gun_sayisi,
            "Tutar (TL)": f"{tutar:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "Geçici Vergi Dönemi": vergi_donemi,
            "Muhasebe Hesabı": muhasebe_hesabi
        })

        toplam_gun += gun_sayisi
        kalan_tutar -= tutar
        tarih = ay_sonu + timedelta(days=1)

    # %30 KKEG
    rows.append({
        "Yıl": tarih_input.year,
        "Ay": "-",
        "Tarih (Ay Başlangıcı)": tarih_input.strftime("%d.%m.%Y"),
        "Gün Sayısı": "-",
        "Tutar (TL)": f"{tutar_input * kkeg_orani:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "Geçici Vergi Dönemi": "KKEG",
        "Muhasebe Hesabı": "689"
    })

    df = pd.DataFrame(rows)
    st.success("✅ Gider dağılımı başarıyla oluşturuldu.")
    st.dataframe(df, use_container_width=True)

    # Excel çıktısı
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Dağılım")
    output.seek(0)

    st.download_button(
        label="⬇️ Excel Olarak İndir",
        data=output,
        file_name="police_gider_dagilimi.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
