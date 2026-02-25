<<<<<<< HEAD
# 🚀 Scrum Automatic Man Hour (Efor Tahminleme ve Kalibrasyon Aracı)

Scrum Automatic Man Hour, yazılım geliştirme takımlarının sprint planlama süreçlerini otomatize eden ve geçmiş sprint verilerinden öğrenerek **adam/saat tahminlerini optimize eden** makine öğrenmesi destekli bir masaüstü uygulamasıdır.

## 🌟 Neden Geliştirildi?
Çevik (Agile) takımlarda sprint planlamaları sırasında görev sürelerini tahmin etmek genellikle sezgiseldir ve hata payı yüksektir. Bu proje, görevlerin teknik karmaşıklığını (Entity sayısı, özel endpoint'ler, ekran sayıları vb.) analiz ederek **kural tabanlı algoritmalarla** bir baz (baseline) tahmin üretir. Daha sonra, sprint sonunda gerçekleşen süreleri **Doğrusal Regresyon (Linear Regression)** modeliyle analiz ederek takımın hızını öğrenir ve gelecekteki tahminlerini otomatik olarak kalibre eder.

## ✨ Temel Özellikler
* **🧠 Kendi Kendini Eğiten Model:** Sprint sonlarında "Tahmin Edilen" ve "Gerçekleşen" süreler arasındaki ilişkiyi analiz edip katsayılarını (multiplier) günceller.
* **📊 Otomatik Excel Ayrıştırma (Parsing):** Takımın kullandığı mevcut görev Excel'lerini, sütun adlarındaki ufak farklılıklara rağmen "Fuzzy Matching" ile otomatik tanır ve parse eder.
* **🖥️ Modern ve Kullanıcı Dostu Arayüz:** CustomTkinter ile geliştirilmiş, karanlık mod (dark mode) destekli şık bir masaüstü deneyimi sunar.
* **⚙️ Kapasite Kontrolü:** Takımdaki Backend ve Frontend geliştirici sayısına, günlük çalışma saatine ve sprint uzunluğuna göre kapasite aşım risklerini hesaplar.

## 🛠️ Kullanılan Teknolojiler
* **Dil:** Python 3
* **Arayüz (GUI):** CustomTkinter
* **Veri İşleme:** Pandas, Numpy, OpenPyXL
* **Makine Öğrenmesi:** Scikit-Learn (Linear Regression)
* **Paketleme:** PyInstaller

## 📂 Proje Mimarisi
Proje modüler bir yapıda kurgulanmıştır:
* `excel_parser.py`: Ham Excel verilerini normalize edip JSON formatına çevirir.
* `classifier.py`: Görevleri "Entity-Based" veya "Non-Entity-Based" olarak sınıflandırır.
* `estimator.py`: Belirlenen baz saatler ve karmaşıklık faktörleri üzerinden ilk efor hesaplamasını yapar.
* `fine_tuner.py`: Scikit-Learn kullanarak geçmiş veriler üzerinden Doğrusal Regresyon modelini eğitir ve katsayıları günceller.
* `main_app.py`: Tüm iş mantığını birleştiren ve GUI'yi başlatan ana modüldür.

## 🚀 Kurulum ve Çalıştırma

### Kaynak Koddan Çalıştırmak İçin
1. Repoyu klonlayın:
   ```bash
   git clone [https://github.com/ahmetrecayiozturk/ScrumAutomaticManHour.git](https://github.com/ahmetrecayiozturk/ScrumAutomaticManHour.git)
   cd ScrumAutomaticManHour
=======
###
======================================================
         SCRUM AUTOMATION APP - KULLANICI REHBERI
======================================================

Bu arac, yazilim takimimizin sprint planlama sureclerini 
otomatize etmek ve efor tahminlerini makine ogrenmesi 
kullanarak zamanla mukemmellestirmek icin gelistirilmistir.

Sistem iki temel amaca hizmet eder:
1. Planlama: Yeni bir sprint baslarken gorevlerin karmasikligina 
   gore otomatik adam/saat tahmini uretmek.
2. Ogrenme: Sprint bittiginde gerceklesen sureleri analiz ederek, 
   takimin hizini ogrenip bir sonraki sprint icin katsayilarini 
   duzeltmek.

------------------------------------------------------
1. KURULUM VE CALISTIRMA
------------------------------------------------------
Uygulama herhangi bir kurulum gerektirmez (Portable calisir).

- Klasoru bilgisayarinizda bir yere cikartin.
- Klasorun icindeki "main_app.exe" dosyasina cift tiklayin.
- Eger Windows "Kisisel bilgisayarinizi korudu" uyarisi verirse, 
  "Ek Bilgi" -> "Yine de Calistir" butonuna tiklayarak guvenle 
  giris yapabilirsiniz.

------------------------------------------------------
2. YENI SPRINT TAHMINI OLUSTURMA (Adim 1)
------------------------------------------------------
Yeni sprint planlamasinda eforlari hesaplamak icin kullanilir.

Gereksinimler: Icinde gorev detaylarinin (TaskKey, Modul, Ekran 
Sayisi vb.) bulundugu bir Sprint Excel dosyasi.

Nasıl Yapilir?
1. Uygulamada "Sprint Excel'i Sec" butonuna tiklayip dosyanizi secin.
2. "Tahminleri Calistir" butonuna basin.
3. Ciktilar ".exe" dosyasinin bulundugu klasorde "estimated_output.xlsx" 
   adiyla otomatik olarak olusturulacaktir.

------------------------------------------------------
3. SPRINT SONU MODELI EGITME / KALIBRASYON (Adim 2)
------------------------------------------------------
Sprint bittiginde, sistem gerceklesen surelerle tahminleri kiyaslayip 
kendini gunceller.

Gereksinimler: Sadece uc sutundan (TaskKey, Actual_BE, Actual_FE) 
olusan basit bir Gerceklesenler Excel dosyasi. O sprinte ait tahmin 
isleminin daha onceden ayni klasorde yapilmis olmasi gerekir.

Nasil Yapilir?
1. "Gerceklesen (Actuals) Excel'i Sec" butonuna tiklayip dosyanizi secin.
2. "Modeli Egit" butonuna basin.
3. Sistem yeni katsayilari hesaplar ve hafizasina kaydeder. Sonraki 
   tahminler bu yeni ve isabetli oranlara gore yapilacaktir.

------------------------------------------------------
ONEMLI UYARILAR
------------------------------------------------------
- ACIK DOSYALAR: Uygulamayi calistirirken okutacaginiz Excel 
  dosyalarinin arka planda ACIK OLMADIGINDAN emin olun.
- KLASOR BUTUNLUGU: ".exe" dosyasini klasorun icinden tek basina 
  alip baska yere kopyalamayin. Sistemin hafizasi ve gerekli 
  dosyalar (".json", ".csv" ve "_internal" klasoru) ayni dizinde 
  kalmalidir.
- GECMIS VERILER: Klasorde olusan "history.csv" dosyasi uygulamanin 
  egitim gecmisidir. Sistem bu dosya ile akillanir, lutfen silmeyin.

======================================================
###
# ScrumAutomaticManHour
ScrumAutomaticManHour
>>>>>>> 930fd4a3cfea80b129a01e0e862ba68d4753e655
