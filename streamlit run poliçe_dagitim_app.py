import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from io import BytesIO
import locale

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')  # Formatlama için

st.title("📆 Poliçe Muhasebe Dağılımı")
st.markdown("Başlangıç ve bitiş tarihi ile prim gir, sistem aylık ve dönemsel dağılımları hazırlar.")

# Girişler
bas_tarih = st.date_input("Başlangıç Tarihi", datetime.today())
bit_tarih = st.date_input("Bitiş Tarihi", bas_tarih + timedelta(days=364))
tutar = st.number_input("Toplam Poliçe Tutarı (TL)", min_value=0.0, value=31592.62)

if st.button("Hesapla"):
    gun_sayisi = (bit_tarih - bas_tarih).days + 1
    gunluk = tutar / gun_sayisi

    donemler = {
        1: [1,2,3], 2: [4,5,6],
        3: [7,8,9], 4: [10,11,12]
    }
    def donem_adi(ay):
        for d, ayl in donemler.items():
            if ay in ayl:
                return d

    rows = []
    dt = bas_tarih
    while dt <= bit_tarih:
        ay_son = datetime(dt.year, dt.month % 12 +1,1) - timedelta(days=1)
        ay_bit = min(ay_son, bit_tarih)
        gun = (ay_bit - dt).days +1
        aylik_tutar = round(gun * gunluk,2)
        d = donem_adi(dt.month)
        hesap = "740/760/770" if dt.month == bas_tarih.month and dt.year == bas_tarih.year else ("180" if dt.year == bas_tarih.year else "280")
        rows.append({
            "Hesap Adı": hesap,
            "Dönemler": f"{dt.year} / {d} Dönem",
            "Aylar": dt.strftime("%B"),
            "Gün Sayısı": gun,
            "Aylık Bedel": aylik_tutar,
            "Dönemsel Bedel": 0.00
        })
        dt = ay_bit + timedelta(days=1)

    # Şimdi dönemsel toplamları ayarla
    df = pd.DataFrame(rows)
    df["Dönemsel Bedel"] = df.groupby("Dönemler")["Aylık Bedel"].transform(lambda x: round(x.sum(),2))
    df.loc[df.groupby("Dönemler").head(1).index, "Dönemsel Bedel"] = df.groupby("Dönemler")["Dönemsel Bedel"].first()
    df["Aylık Bedel"] = df["Aylık Bedel"].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    df["Dönemsel Bedel"] = df["Dönemsel Bedel"].map(lambda x: f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    rows_list = df.to_dict('records')

    # KKEG satırı
    kkeg = round(tutar * 0.30,2)
    rows_list.append({
        "Hesap Adı": "689",
        "Dönemler": "K.K.E.G.",
        "Aylar": "-",
        "Gün Sayısı": "-",
        "Aylık Bedel": f"{kkeg:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "Dönemsel Bedel": ""
    })
    rows_list.append({
        "Hesap Adı": "Sigorta Acentesi",
        "Dönemler": "",
        "Aylar": "",
        "Gün Sayısı": "",
        "Aylık Bedel": f"{tutar:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        "Dönemsel Bedel": ""
    })

    df2 = pd.DataFrame(rows_list)
    st.dataframe(df2, use_container_width=True)

    # Excel indirme
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df2.to_excel(writer, index=False, sheet_name="Dağılım")
    output.seek(0)
    st.download_button("⬇️ Excel İndir", data=output,
                       file_name="police_dagitimi.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
