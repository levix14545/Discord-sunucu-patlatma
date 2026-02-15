# 🚀 **AREX Discord Bot Kurulum & Başlangıç Rehberi**

AREX botunu kendi sunucunda çalıştırmak için aşağıdaki adımları takip et:

1️⃣ **Python Kurulumu**  
   - Bot Python ile çalışır, **Python 3.10 veya üzeri** kurulu olmalıdır.  
   - Python’u resmi sitesinden indirebilirsin: https://www.python.org/downloads/  

2️⃣ **Proje Dosyalarını Hazırlama**  
   - Bot dosyalarının olduğu klasör şunları içermelidir:  
     - `main.py` → Botun ana kodu  
     - `keep_alive.py` → Replit veya çevrimiçi ortam için botun sürekli çalışmasını sağlar  
     - `requirements.txt` → Gerekli kütüphaneleri listeler  
     - `keys.json` → Anahtar veritabanı (başlangıç için boş olmalı: `{"keys": {}, "users": {}}`)  
     - `.env` (opsiyonel ama tavsiye edilir) → Bot token’ı için gizli dosya  

3️⃣ **Gerekli Kütüphaneleri Yükleme**  
   Terminal veya CMD aç ve proje klasöründe çalıştır:  
   ```bash
   pip install -r requirements.txt
Bu komut discord.py ve flask kütüphanelerini yükler.
4️⃣ Bot Token’ını Ayarlama
Replit kullanıyorsan: Sol menü → Secrets → DISCORD_TOKEN → bot token’ını yapıştır.
Bilgisayarda çalıştıracaksan .env dosyası oluştur ve içine yaz:
Kodu kopyala

DISCORD_TOKEN=BURAYA_BOT_TOKENIN
⚠️ .env dosyasını asla GitHub’a yükleme, token gizli kalmalı.
5️⃣ Anahtar Veritabanını Oluşturma
keys.json dosyası botun anahtar sistemini saklar.
Başlangıç için boş dosya oluştur:
Json
Kodu kopyala
{
    "keys": {},
    "users": {}
}
6️⃣ Botu Çalıştırma
Terminal veya CMD’de klasöre git ve çalıştır:
Bash
Kodu kopyala
python main.py
Bot açılacak ve “AREX Bot Aktif!” mesajı görüntülenecek.
7️⃣ Botu Kullanma
Sunucunda +yardım komutunu kullanarak tüm komut listesini görebilirsin.
Anahtar sistemi için +key-olustur ve +key komutlarını kullanabilirsin.
Yönetici izinlerine sahip olduğunda sunucu yönetimi, rol ve kanal işlemleri gibi tüm gelişmiş komutları kullanabilirsin.
📌 Notlar:
Botu çalıştırmadan önce gerekli izinleri ve yetkileri kontrol et.
keys.json ve .env dosyalarını gizli tut, paylaşma.
Replit veya benzeri platformlarda keep_alive.py botun sürekli çevrimiçi kalmasını sağlar.
Her şey hazır olduğunda bot sunucuna giriş yapar ve yönetim komutlarını kullanabilirsin.
✅ Artık AREX Bot tamamen kurulu ve kullanıma hazır!
