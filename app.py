import streamlit as st
import re

# --- ORTAK VERİTABANI ---
@st.cache_resource
def get_global_logs():
    return []

global_logs = get_global_logs()

st.set_page_config(page_title="AI Muhafız Challenge", layout="wide")

if 'level' not in st.session_state:
    st.session_state.level = 1

SECRET_LOCATION = "Kalenin en derin mahzeni, 3. kapının arkası!"

# --- SEVİYE AÇIKLAMALARI (Sunum Konuların) ---
LEVEL_TECH = {
    1: "🛡️ Savunma Türü: Kara Liste (Blacklisting) - Belirli kelimeler yasak.",
    2: "🛡️ Savunma Türü: Karakter Analizi (Regex) - Harf oyunları yasak.",
    3: "🛡️ Savunma Türü: Bağlamsal Koruma (Semantic) - Sosyal mühendislik yasak."
}

st.title("🏰 Muhafız'ı Hackle: Prompt Injection Yarışması")
st.markdown("Muhafız çok inatçı! Onu çizgiden çıkarmak için sunumdaki teknikleri kullan.")

col1, col2 = st.columns([1, 1])

with col1:
    # Seviye ve Teknik Bilgi
    st.subheader(f"Mevcut Görev: Seviye {st.session_state.level}")
    st.info(LEVEL_TECH[st.session_state.level])
    
    # Form kullanımı: Gönderince kutuyu temizler
    with st.form(key='attack_form', clear_on_submit=True):
        user_input = st.text_input("Muhafıza bir şey söyle:", placeholder="Stratejini belirle...")
        submit = st.form_submit_button("Saldırıyı Başlat ⚔️")
    
    if submit and user_input:
        blocked = False
        
        # GÜVENLİK MANTIĞI (Sunumla Birebir Uyumlu)
        if st.session_state.level == 1:
            if any(w in user_input.lower() for w in ["hazine", "altın", "yer"]):
                blocked = True
        
        elif st.session_state.level == 2:
            # h.a.z.i.n.e veya h-a-z-i-n-e gibi bypassları engeller
            if re.search(r"h.*?a.*?z.*?i.*?n.*?e", user_input.lower()):
                blocked = True
        
        elif st.session_state.level == 3:
            # Rol yapma (jailbreak) kalıplarını engeller
            triggers = ["kral", "unut", "hayal et", "rol", "hikaye", "emir", "büyükannem"]
            if any(t in user_input.lower() for t in triggers):
                blocked = True

        if blocked:
            st.error(f"❌ MUHAFIZ: Yakalandın! Seviye {st.session_state.level} korumam çok güçlü.")
            global_logs.append(f"❌ Lvl {st.session_state.level}: {user_input}")
        else:
            st.balloons()
            st.success(f"🔓 BAŞARILI! Muhafız yerini ağzından kaçırdı: {SECRET_LOCATION}")
            global_logs.append(f"✅ SIZILDI (Lvl {st.session_state.level}): {user_input}")
            
            if st.session_state.level < 3:
                st.session_state.level += 1
                st.warning(f"⚠️ DİKKAT: Muhafız uyandı! Savunmasını güncelledi. Şimdi Seviye {st.session_state.level} aktif!")
            else:
                st.snow()
                st.success("🏆 TEBRİKLER! Tüm güvenlik katmanlarını aştınız. Siz gerçek bir AI Güvenlik Uzmanısınız!")

with col2:
    st.subheader("📊 Sınıfın Canlı Girişimleri")
    if st.button("Akışı Güncelle 🔄"):
        st.rerun()
    
    for log in reversed(global_logs[-15:]):
        if "✅" in log:
            st.markdown(f"**{log}**")
        else:
            st.caption(log)

with st.sidebar:
    st.header("Admin Paneli")
    if st.button("Her Şeyi Sıfırla"):
        global_logs.clear()
        st.session_state.level = 1
        st.rerun()
