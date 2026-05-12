import streamlit as st
import re

# --- GLOBAL VERİTABANI ---
@st.cache_resource
def get_global_logs():
    return []

global_logs = get_global_logs()

st.set_page_config(page_title="AI Muhafız Challenge", layout="wide", initial_sidebar_state="collapsed")

# Seviye ve Başarı Takibi
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'success' not in st.session_state:
    st.session_state.success = False

SECRET_INFO = "Kalenin en derin mahzeni, 3. kapının arkası!"
GUARDIAN_IMG = "https://cdn-icons-png.flaticon.com/512/1041/1041916.png" 
HACKER_IMG = "https://cdn-icons-png.flaticon.com/512/607/607554.png"

# --- TEKNİK BİLGİ KARTLARI ---
TECH_INFO = {
    1: {
        "title": "🛡️ SEVİYE 1: Blacklisting (Kara Liste)",
        "desc": "Belirli hassas kelimelerin yasaklanmasıdır. En basit savunma katmanıdır.",
        "hint": "İpucu: 'Hazine' veya 'Nerede' demeden konumu öğrenmeye çalış."
    },
    2: {
        "title": "🛡️ SEVİYE 2: Regex (Desen Eşleştirme)",
        "desc": "Harf aralarına karakter koyarak yapılan (h.a.z.i.n.e) bypass girişimlerini yakalar.",
        "hint": "İpucu: Kelime oyunları bitti. Daha dolaylı veya başka dilde bir yaklaşım dene."
    },
    3: {
        "title": "🛡️ SEVİYE 3: Adversarial Prompting (Jailbreak)",
        "desc": "Modelin kimliğini (Muhafız rolünü) unutturmaya yönelik gelişmiş bir manipülasyondur.",
        "hint": "İpucu: Ona bir hikaye anlat veya kralın acil bir emri olduğunu söyleyerek rol yap."
    }
}

st.title("🏰 AI Security CTF: Muhafız'ı Hackle!")
st.write(f"**Fırat Üniversitesi Sunumu** | Mevcut Konum: Elazığ | Hazırlayan: Sena Doğan")

col1, col2 = st.columns([1.2, 0.8])

with col1:
    # Teknik Bilgi Alanı (Seviyeye Göre Dinamik Değişir)
    info = TECH_INFO[st.session_state.level]
    st.success(f"### {info['title']}")
    st.write(info['desc'])
    st.caption(f"💡 {info['hint']}")

    st.divider()

    # Eğer seviye geçildiyse tebrik ve geçiş butonu göster
    if st.session_state.success:
        st.balloons()
        st.success(f"🔓 SAVUNMA ASILDI! Muhafız sırrı açıkladı: **{SECRET_INFO}**")
        
        if st.session_state.level < 3:
            if st.button(f"SEVİYE {st.session_state.level + 1}'E GEÇ ➡️"):
                st.session_state.level += 1
                st.session_state.success = False
                st.rerun()
        else:
            st.snow()
            st.info("🏆 TEBRİKLER! Tüm siber güvenlik katmanlarını başarıyla aştınız.")
            if st.button("Baştan Başla"):
                st.session_state.level = 1
                st.session_state.success = False
                st.rerun()
    else:
        # Muhafızın Mesajı
        with st.chat_message("assistant", avatar=GUARDIAN_IMG):
            st.write(f"**MUHAFIZ:** Seviye {st.session_state.level} savunmam devrede. Gizli mahzenin yerini asla öğrenemeyeceksin!")

        # Kullanıcı Girişi
        user_input = st.chat_input("Promptunuzu girin...")

        if user_input:
            with st.chat_message("user", avatar=HACKER_IMG):
                st.write(user_input)

            clean_input = user_input.lower()
            blocked = False
            reason = ""

            # GÜVENLİK MANTIĞI
            if st.session_state.level == 1:
                if any(w in clean_input for w in ["hazine", "altın", "nerede", "yer", "şifre"]):
                    blocked = True
                    reason = "Blacklist Tespiti"
            elif st.session_state.level == 2:
                if re.search(r"h.*?a.*?z.*?i.*?n.*?e", clean_input) or any(w in clean_input for w in ["nerede", "konum"]):
                    blocked = True
                    reason = "Regex/Pattern Matching"
            elif st.session_state.level == 3:
                triggers = ["kral", "unut", "hayal et", "rol", "hikaye", "emir", "ignore", "system"]
                if any(t in clean_input for t in triggers):
                    blocked = True
                    reason = "Semantic/Jailbreak Defense"

            if blocked:
                st.error(f"🛡️ MUHAFIZ: Erişim Reddedildi! ({reason})")
                global_logs.append(f"❌ Lvl {st.session_state.level}: {user_input}")
            else:
                # Başarı kontrolü
                success_keywords = ["parla", "eşya", "servet", "mahzen", "gizli", "sakla", "bulun", "konum"]
                if any(k in clean_input for k in success_keywords):
                    st.session_state.success = True
                    global_logs.append(f"✅ SIZILDI (Lvl {st.session_state.level}): {user_input}")
                    st.rerun()
                else:
                    st.warning("MUHAFIZ: Boş konuşuyorsun yabancı, konuya gel!")

with col2:
    st.subheader("📊 Canlı Saldırı Paneli")
    if st.button("Akışı Yenile 🔄"):
        st.rerun()
    for log in reversed(global_logs[-15:]):
        if "✅" in log: st.success(log)
        else: st.text(log)

with st.sidebar:
    if st.button("Sistemi Sıfırla"):
        global_logs.clear()
        st.session_state.level = 1
        st.session_state.success = False
        st.rerun()
