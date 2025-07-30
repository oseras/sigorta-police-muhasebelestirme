from datetime import datetime, timedelta
import pandas as pd

# Girdi
baslangic_tarihi = datetime(2025, 7, 4)
toplam_tutar = 31592.62
kkeg_orani = 0.30
gider_orani = 1 - kkeg_orani
gunluk_tutar = toplam_tutar * gider_orani / 365

# Vergi dönemleri
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
    return "Bilinmiyor"

# Tablonun oluşturulması
rows = []
kalan_tutar = toplam_tutar * gider_orani
tarih = baslangic_tarihi
toplam_gun = 0

while kalan_tutar > 0 and toplam_gun < 365:
    ay_sonu = datetime(tarih.year, tarih.month % 12 + 1, 1) - timedelta(days=1)
    gun_sayisi = (ay_sonu - tarih).days + 1
    if toplam_gun + gun_sayisi > 365:
        gun_sayisi = 365 - toplam_gun
    
    tutar = round(gun_sayisi * gunluk_tutar, 2)
    vergi_donemi = get_donem(tarih.month)
    muhasebe_hesabi = "770" if tarih.year == baslangic_tarihi.year else "280"

    rows.append({
        "Tarih": tarih.strftime("%d.%m.%Y"),
        "Gün Sayısı": gun_sayisi,
        "Tutar": tutar,
        "Geçici Vergi Dönemi": vergi_donemi,
        "Muhasebe Hesabı": muhasebe_hesabi
    })

    toplam_gun += gun_sayisi
    kalan_tutar -= tutar
    tarih = ay_sonu + timedelta(days=1)

# KKEG satırı
rows.append({
    "Tarih": baslangic_tarihi.strftime("%d.%m.%Y"),
    "Gün Sayısı": "-",
    "Tutar": round(toplam_tutar * kkeg_orani, 2),
    "Geçici Vergi Dönemi": "KKEG",
    "Muhasebe Hesabı": "689"
})

df = pd.DataFrame(rows)
print(df)
