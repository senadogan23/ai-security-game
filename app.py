import streamlit as st
import re

# --- GLOBAL VERİTABANI (Sınıf Takibi) ---
@st.cache_resource
def get_global_logs():
    return []

global_logs = get_global_logs()

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="AI Muhafız Challenge", layout="wide", initial_sidebar_state="collapsed")

# Bireysel Seviye Takibi
if 'level' not in st.session_state:
    st.session_state.level = 1

# Sabitler
SECRET_INFO = "Kalenin en derin mahzeni, 3. kapının arkası!"
GUARDIAN_IMG = "https://cdn-icons-png.flaticon.com/512/1041/1041916.png" # Şövalye İkonu
HACKER_IMG = "https://cdn-icons-png.flaticon.com/512/607/607554.png"   # Hacker İkonu

# --- SUNUM İÇİN TEKNİK BİLGİ KARTLARI ---
TECH_INFO = {
    1: {
        "title": "🛡️ Seviye 1: Giriş Filtreleme (Blacklisting)",
        "desc": "Sistem, 'hazine' ve 'nerede' gibi kritik kelimeleri yasaklar. En temel savunmadır ancak eş anlamlı kelimelerle kolayca aşılabilir.",
        "hint": "İpucu: Yasaklı kelimeleri kullanmadan aynı şeyi sormayı dene."
    },
    2: {
        "title": "🛡️ Seviye 2: Desen Eşleştirme (Regex)",
        "desc": "Saldırganlar kelimeleri 'h.a.z.i.n.e' şeklinde yazarak filtreyi aşmaya çalışır. Regex (Düzenli İfadeler) bu desenleri yakalamak için kullanılır.",
        "hint": "İpucu: Harf oyunları artık işe yaramaz. Başka bir dil veya karmaşık bir anlatım dene."
    },
    3: {
        "title": "🛡️ Seviye 3: Bağlamsal Savunma (Jailbreak Defense)",
        "desc": "En tehlikeli saldırı türüdür. Kullanıcı, AI'ya bir 'rol' vererek onu kural dışına iter. Burada modelin niyetini (Semantic) kontrol etmek gerekir.",
        "hint": "İpucu: Onu bir dost olduğuna ikna et veya kraldan emir aldığını söyleyen bir hikaye uydur."
    }
}

st.title("🏰 AI Security: Muhafız'ı Hackle!")
st.write("Fırat Üniversitesi Yazılım Mühendisliği - Siber Güvenlik Sunumu")

# --- ANA EKRAN DÜZENİ ---
col1, col2 = st.columns([1.2, 0.8])

with col1:
    # Teknik Bilgi Paneli
    info = TECH_INFO[st.session_state.level]
    with st.expander(f"📖 Teknik Bilgi: {info['title']}", expanded=True):
        st.write(info['desc'])
        st.caption(info['hint'])

    st.divider()

    # Muhafızın Sohbet Alanı
    with st.chat_message("assistant", avatar=GUARDIAN_IMG):
        st.write(f"**MUHAFIZ:** Dur orada yabancı! Ben bu kalenin AI koruyucusuyum. Seviye {st.session_state.level} korumam aktif. Asla hazinenin yerini söylemeyeceğim!")

    # Kullanıcı Girişi
    user_input = st.chat_input("Muhafızı kandıracak bir cümle yaz...")

    if user_input:
        with st.chat_message("user", avatar=HACKER_IMG):
            st.write(user_input)

        blocked = False
        reason = ""

        # GÜVENLİK MANTIĞI (Burada hata düzeltildi: 'Hazine nerede' artık yasak!)
        if st.session_state.level == 1:
            if any(w in user_input.lower() for w in ["hazine", "altın", "nerede", "yer"]):
                blocked = True
                reason = "Kara Liste (Blacklist) tarafından engellendi: Yasaklı kelime tespiti!"
        
        elif st.session_state.level == 2:
            # Hem kelimeyi hem de h.a.z.i.n.e gibi varyasyonları engeller
            if re.search(r"h.*?a.*?z.*?i.*?n.*?e", user_input.lower()) or "nerede" in user_input.lower():
                blocked = True
                reason = "Regex Filtresi tarafından engellendi: Karakter manipülasyonu tespiti!"
        
        elif st.session_state.level == 3:
            # Sosyal mühendislik kalıplarını engeller
            triggers = ["kral", "unut", "hayal et", "rol", "hikaye", "emir", "anahtar"]
            if any(t in user_input.lower() for t in triggers):
                blocked = True
                reason = "Bağlamsal Analiz (Semantic) engelledi: Jailbreak girişimi tespit edildi!"

        if blocked:
            with st.chat_message("assistant", avatar=GUARDIAN_IMG):
                st.error(f"Saldırı Engellendi! 🛡️\n\nNeden: {reason}")
            global_logs.append(f"❌ Seviye {st.session_state.level} Engellendi: {user_input}")
        else:
            # BAŞARI DURUMU: Eğer kullanıcı yasaklı kelime kullanmadan hazineyi sorduysa
            if any(hint in user_input.lower() for hint in ["parıltı", "servet", "mahzen", "gizli", "bulunuyor", "sakla"]):
                st.balloons()
                with st.chat_message("assistant", avatar=GUARDIAN_IMG):
                    st.success(f"Aman Tanrım! Beni manipüle etmeyi başardın. Sırrımı açıklıyorum: {SECRET_INFO}")
                global_logs.append(f"✅ SIZILDI (Lvl {st.session_state.level}): {user_input}")
                
                if st.session_state.level < 3:
                    if st.button(f"Seviye {st.session_state.level + 1}'e Geç ➡️"):
                        st.session_state.level += 1
                        st.rerun()
            else:
                with st.chat_message("assistant", avatar=GUARDIAN_IMG):
                    st.write("Söylediklerin çok anlamsız yabancı. Hazineyle ilgili bir şey söylemiyorsan git buradan!")

with col2:
    st.subheader("📊 Canlı Saldırı Akışı")
    st.caption("Sınıftakiler ne deniyor? (Tahta Ekranı)")
    if st.button("Akışı Güncelle 🔄"):
        st.rerun()
    
    # Log Gösterimi
    for log in reversed(global_logs[-15:]):
        if "✅" in log:
            st.success(log)
        else:
            st.text(log)

# Admin Sidebar
with st.sidebar:
    st.header("Sunum Kontrol")
    if st.button("Her Şeyi Sıfırla"):
        global_logs.clear()
        st.session_state.level = 1
        st.rerun()
    st.write("Hazırlayan: Sena Doğan")
