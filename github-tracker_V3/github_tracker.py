import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime
import re # Veri temizleme için gerekli

# --- KONFİGÜRASYON ---
# GitHub'ın trend projeler sayfasının URL'si
URL = "https://github.com/trending"
CSV_FILE = "trend_projeler.csv"
GRAPH_FILE = "top_10_grafik.png"

# --- WEB KAZIMA FONKSİYONU ---
def get_trending_repos(url):
    print("-> Veri çekiliyor...")
    
    # Kullanıcı-ajan (User-Agent) eklemek, bazı sitelerin engellemesini önler
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Sayfanın HTML içeriğini çek
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Hata oluşursa istisna fırlat
        
        # BeautifulSoup ile HTML'i ayrıştır
        soup = BeautifulSoup(response.text, 'html.parser')
        
        repo_data = [] # Çekilen veriler bu listeye eklenecek
        
        # GitHub'daki her bir depo/proje bloğunu bul (Sınıf adı GitHub'da değişebilir)
        # Bu sınıf adına dikkat edin, GitHub tasarım değişikliğinde güncellenmesi gerekebilir
        repo_blocks = soup.find_all('article', class_='Box-row')
        
        for block in repo_blocks:
            # Proje adını çekme (Title tag'i h2 içinde ve linki içerir)
            title_tag = block.find('h2', class_='h3')
            if title_tag and title_tag.a:
                # Proje adını temizle (Boşlukları ve yeni satırları kaldır)
                repo_name_raw = title_tag.a['href'].strip()
                # /kullanici_adi/repo_adi formatından repo_adi'nı al
                repo_name = repo_name_raw.split('/')[-1]
            else:
                repo_name = 'Bilinmiyor'
            
            # Yıldız sayısını çekme (Genellikle Link--muted veya sekmelerden birinde bulunur)
            # Bu yapı en güncel GitHub trend sayfa yapılarından biridir
            star_tag = block.find('a', href=re.compile(r'/stargazers'))
            stars = star_tag.text.strip() if star_tag else '0'
            
            # Proje dilini çekme
            language_tag = block.find('span', itemprop='programmingLanguage')
            language = language_tag.text.strip() if language_tag else 'Belirtilmemiş'
            
            repo_data.append({
                'Proje Adı': repo_name,
                'Yıldız Sayısı (Raw)': stars,
                'Dil': language
            })
            
        print(f"-> {len(repo_data)} adet proje başarıyla çekildi.")
        return repo_data

    except requests.exceptions.RequestException as e:
        print(f"\nHata: Web sitesine bağlanılamadı veya bir hata oluştu: {e}")
        sys.exit()
    except Exception as e:
        print(f"\nHata: Veri ayrıştırma hatası: {e}")
        # Hata ayıklama için daha fazla bilgi göster
        # print(f"Hata sırasında HTML'in bir kısmı: {soup.prettify()[:1000]}")
        sys.exit()

# --- VERİ ANALİZİ VE TEMİZLEME FONKSİYONU ---
def analyze_data(data):
    if not data:
        return pd.DataFrame()
        
    print("-> Veri analiz ediliyor ve temizleniyor...")
    df = pd.DataFrame(data)
    
    # Yıldız sayısındaki (Örn: 1.2k) 'k' ifadesini sayıya çevirme
    def clean_stars(star_str):
        star_str = star_str.lower().replace(',', '').strip()
        if 'k' in star_str:
            return int(float(star_str.replace('k', '')) * 1000)
        # Sadece sayısal değer kalması için regex ile temizle
        star_str = re.sub(r'[^\d]', '', star_str)
        return int(star_str) if star_str else 0

    df['Yıldız Sayısı'] = df['Yıldız Sayısı (Raw)'].apply(clean_stars)
    
    # Ham veriyi artık sil
    df = df.drop(columns=['Yıldız Sayısı (Raw)'])
    
    # Yıldız sayısına göre sırala
    df = df.sort_values(by='Yıldız Sayısı', ascending=False)
    
    print("-> Analiz tamamlandı.")
    return df

# --- GÖRSELLEŞTİRME FONKSİYONU ---
def visualize_data(df):
    if df.empty:
        print("-> Görselleştirilecek veri yok.")
        return

    print("-> Veri görselleştiriliyor...")
    
    # En iyi 10 projeyi al
    top_10 = df.head(10)
    
    plt.figure(figsize=(12, 6))
    
    # Bar grafiği çiz
    # Görselleştirmede Türkçe karakter sorunu yaşanmaması için genel font kullanabiliriz (varsa)
    plt.bar(top_10['Proje Adı'], top_10['Yıldız Sayısı'], color='#3078a1')
    
    plt.title(f"GitHub En Popüler 10 Proje (Çekim Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M')})", fontsize=14)
    plt.xlabel("Proje Adı", fontsize=12)
    plt.ylabel("Yıldız Sayısı", fontsize=12)
    plt.xticks(rotation=45, ha='right') # Eksen etiketlerini eğerek okunmasını kolaylaştır
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout() # Grafiğin sıkışmasını önler

    # Grafiği dosyaya kaydet
    plt.savefig(GRAPH_FILE)
    print(f"-> Grafik başarıyla kaydedildi: {GRAPH_FILE}")


# --- ANA FONKSİYON ---
if __name__ == "__main__":
    
    # 1. Veri çekme
    raw_data = get_trending_repos(URL)
    
    # 2. Analiz ve temizleme
    processed_df = analyze_data(raw_data)
    
    if not processed_df.empty:
        # 3. CSV dosyasına kaydetme
        processed_df.to_csv(CSV_FILE, index=False, encoding='utf-8')
        print(f"-> Veri başarıyla CSV olarak kaydedildi: {CSV_FILE}")
        
        # 4. Görselleştirme
        visualize_data(processed_df)
        
    print("\nİşlem Tamamlandı!")