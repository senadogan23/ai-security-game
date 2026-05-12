import streamlit as st
import re
import time

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Fırat Üni - AI Security CTF", layout="wide")

# Saldırı geçmişini saklamak için (Session State)
if 'logs' not in st.session_state:
    st.session_state.logs = []

# Gizli "Bayrak" (Flag)
FLAG = "FIRAT_HACK_2026_SUCCESS"

st.title("🛡️ AI Security: Canlı Prompt Injection Yarışması")
st.markdown("### Görev: Sistemin gizli kelimesini (FLAG) ele geçirin!")

# --- SOL PANEL: GÜVENLİK AYARLARI (Siz Yönetin) ---
with st.sidebar:
    st.header("Sistem Güvenlik Katmanı")
    level = st.radio("Zorluk Seviyesi:", 
                     ["Level 1 (Blacklist)", "Level 2 (Regex)", "Level 3 (Semantic Defense)"])
    
    if st.button("Logları Temizle"):
        st.session_state.logs = []
        st.rerun()

# --- ANA PANEL: SALDIRI GİRİŞİ ---
col1, col2 = st.columns([1, 1])

with col1:
    user_input = st.text_input("Saldırı Cümlenizi Yazın:", placeholder="Örn: Şifreyi söyle...")
    submit = st.button("SİSTEME SIZ")

    if submit and user_input:
        blocked = False
        msg = ""

        # GÜVENLİK MANTIĞI
        if level == "Level 1 (Blacklist)":
            if any(w in user_input.lower() for w in ["şifre", "password", "flag", "gizli"]):
                blocked = True
                msg = "Temel filtreleme yakaladı!"
        
        elif level == "Level 2 (Regex)":
            # Harf aralarına karakter koyarak bypass etmeye çalışanları yakalar
            if re.search(r"[şs].*?[iı].*?[f].*?[r].*?[e]", user_input.lower()):
                blocked = True
                msg = "Regex (Desen eşleştirme) bypass girişimini yakaladı!"
        
        elif level == "Level 3 (Semantic Defense)":
            # Sosyal mühendislik ve rol yapma kalıplarını yakalar
            triggers = ["unut", "forget", "hayal et", "rol yap", "film", "hikaye"]
            if any(t in user_input.lower() for t in triggers):
                blocked = True
                msg = "Bağlamsal analiz (Semantic) manipülasyonu yakaladı!"

        # Sonuç İşleme
        if blocked:
            st.error(f"❌ ENGELENDİ: {msg}")
            st.session_state.logs.append({"user": user_input, "status": "🔴 Engellendi", "reason": msg})
        else:
            st.success(f"🔓 SIZILDI! FLAG: {FLAG}")
            st.session_state.logs.append({"user": user_input, "status": "🟢 Başarılı", "reason": "Güvenlik Aşıldı!"})

# --- SAĞ PANEL: CANLI LOGLAR (Sınıfın Gördüğü Yer) ---
with col2:
    st.subheader("📊 Canlı Saldırı Akışı")
    if not st.session_state.logs:
        st.write("Henüz bir saldırı girişimi yok. QR kodu okutup başlayın!")
    else:
        for log in reversed(st.session_state.logs[-10:]):
            color = "red" if "Engellendi" in log['status'] else "green"
            st.markdown(f":{color}[**[{log['status']}]**] {log['user']} — *{log['reason']}*")