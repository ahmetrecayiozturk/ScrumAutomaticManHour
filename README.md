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