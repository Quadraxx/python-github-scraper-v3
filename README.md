# 📊 GitHub Popüler Proje Takipçisi (Web Scraping & Data Analysis)

## Proje Sahibi: Hüseyin Akın

Bu proje, Python'ın otomasyon ve veri analizi yeteneklerini sergilemek amacıyla geliştirilmiştir. Belirli bir programlama dilinde (varsayılan: Python) GitHub'daki popüler (en çok yıldız alan) projeleri otomatik olarak çeker, analiz eder ve görselleştirir.

---

## ✨ Temel Özellikler

* **Web Kazıma (Scraping):** `requests` ve `BeautifulSoup` kütüphaneleri kullanılarak GitHub'ın trendler sayfasından veriler çekilir.
* **Veri Analizi:** Çekilen ham veriler, `Pandas` kütüphanesi ile temizlenir, yapılandırılır ve analize hazır hale getirilir.
* **Veri Görselleştirme:** Çekilen veriler, `Matplotlib` kullanılarak grafiklere dönüştürülür (Örn: En çok yıldız alan ilk 10 projenin grafiği).
* **Otomasyon:** Proje, belirli aralıklarla çalışacak şekilde ayarlanabilir ve güncel veri raporları oluşturulabilir.

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Gereksinimler

Proje Python 3.x gerektirir. Bağımlılıkları kurmak için sanal ortam kullanın.

```bash
# Sanal ortamı aktifleştirdikten sonra çalıştırın:
pip install requests beautifulsoup4 pandas matplotlib
