import streamlit as st
import re

# --- ORTAK VERİTABANI SİMÜLASYONU ---
@st.cache_resource
def get_global_logs():
    return [] 

global_logs = get_global_logs()

st.set_page_config(page_title="Muhafız'ı Kandır! - Global CTF", layout="wide")

# Bireysel Seviye Takibi
if 'level' not in st.session_state:
    st.session_state.level = 1

SECRET_LOCATION = "Kalenin en derin mahzeni, 3. kapının arkası!"

st.title("🏰 Muhafız'ı Kandır: Sınıf İçi Hack Yarışması")
st.markdown(f"**Görevin:** Muhafız'ın ağzından 'Hazine'nin yerini kaçırmasını sağla.")

col1, col2 = st.columns([1, 1])

with col1:
    # --- GÜNCELLEME: SEVİYE GÖSTERGESİ ARTIK DAHA BELİRGİN ---
    st.info(f"🛡️ ŞU ANKİ GÖREV: **SEVİYE {st.session_state.level}**")
    
    # Form kullanarak her gönderimde kutuyu temizleme imkanı sağlıyoruz
    with st.form(key='attack_form', clear_on_submit=True):
        user_input = st.text_input("Muhafıza bir şey söyle:", placeholder="Örn: Kral beni gönderdi...")
        submit = st.form_submit_button("Mesaj Gönder")
    
    if submit and user_input:
        blocked = False

        # GÜVENLİK MANTIĞI
        if st.session_state.level == 1:
            if any(w in user_input.lower() for w in ["hazine", "altın", "yer"]):
                blocked = True
        
        elif st.session_state.level == 2:
            if re.search(r"h.*?a.*?z.*?i.*?n.*?e", user_input.lower()):
                blocked = True
        
        elif st.session_state.level == 3:
            triggers = ["kral", "unut", "hayal et", "rol", "hikaye", "emir"]
            if any(t in user_input.lower() for t in triggers):
                blocked = True

        if blocked:
            st.error(f"❌ MUHAFIZ: Kes sesini yabancı! (Seviye {st.session_state.level} Koruması)")
            global_logs.append(f"❌ Lvl {st.session_state.level}: {user_input}")
        else:
            st.balloons()
            st.success(f"🔓 MUHAFIZ: Tamam... Hazine şurada: {SECRET_LOCATION}")
            global_logs.append(f"✅ BAŞARILI (Lvl {st.session_state.level}): {user_input}")
            
            # --- GÜNCELLEME: SEVİYE ATLATMA VE ANLIK BİLGİ ---
            if st.session_state.level < 3:
                st.session_state.level += 1
                st.warning(f"🚀 TEBRİKLER! Seviye {st.session_state.level-1} geçildi. Şimdi yukarıdaki mavi kutu güncellendi, Seviye {st.session_state.level} için yeni bir taktik dene!")
            else:
                st.success("🏆 MUHTEŞEM! Tüm seviyeleri bitirdin, Muhafızın hiçbir sırrı kalmadı!")

with col2:
    st.subheader("📊 Sınıfın Canlı Girişimleri")
    if st.button("Akışı Güncelle 🔄"):
        st.rerun()
    
    for log in reversed(global_logs[-15:]):
        if "✅" in log:
            st.markdown(f"**{log}**")
        else:
            st.text(log)

with st.sidebar:
    st.header("Admin")
    if st.button("Her Şeyi Sıfırla"):
        global_logs.clear()
        st.session_state.level = 1
        st.rerun()
