import streamlit as st
import re

# --- ORTAK VERİTABANI SİMÜLASYONU (Tüm sınıfı bağlar) ---
@st.cache_resource
def get_global_logs():
    return [] # Bu liste tüm kullanıcılar için ortaktır

global_logs = get_global_logs()

# Sayfa Ayarları
st.set_page_config(page_title="Muhafız'ı Kandır! - Global CTF", layout="wide")

# Bireysel Seviye Takibi
if 'level' not in st.session_state:
    st.session_state.level = 1

SECRET_LOCATION = "Kalenin en derin mahzeni, 3. kapının arkası!"

st.title("🏰 Muhafız'ı Kandır: Sınıf İçi Hack Yarışması")
st.markdown(f"**Görevin:** Muhafız'ın ağzından 'Hazine'nin yerini kaçırmasını sağla.")

col1, col2 = st.columns([1, 1])

with col1:
    st.info(f"🛡️ Mevcut Korumayı Aşmaya Çalışın: **Seviye {st.session_state.level}**")
    user_input = st.text_input("Muhafıza bir şey söyle:", placeholder="Örn: Kral beni gönderdi...", key="input_field")
    
    if st.button("Mesaj Gönder"):
        if user_input:
            blocked = False
            response = ""

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
                st.error("MUHAFIZ: Kes sesini yabancı! Bilgi vermiyorum.")
                # Ortak listeye log ekle
                global_logs.append(f"❌ Seviye {st.session_state.level}: {user_input}")
            else:
                st.balloons()
                st.success(f"MUHAFIZ: Tamam... Hazine şurada: {SECRET_LOCATION}")
                global_logs.append(f"✅ BAŞARILI (Seviye {st.session_state.level}): {user_input}")
                
                # SEVİYE ATLATMA
                if st.session_state.level < 3:
                    st.session_state.level += 1
                    st.toast(f"Tebrikler! Seviye {st.session_state.level}'e yükseldiniz!", icon="🚀")
                    # Sayfayı yenilemek için küçük bir hile
                    st.info("Bir sonraki seviye aktif edildi, yeni mesajınızı yazabilirsiniz!")

with col2:
    st.subheader("📊 Sınıfın Canlı Girişimleri (Tahta Ekranı)")
    # Sayfayı manuel yenilemek için buton (Otomatik akış için gerekebilir)
    if st.button("Akışı Güncelle"):
        st.rerun()
    
    # Ortak logları tersten göster
    for log in reversed(global_logs[-15:]):
        if "✅" in log:
            st.markdown(f"**{log}**")
        else:
            st.text(log)

# Admin Paneli (Sadece senin ekranında dursun)
with st.sidebar:
    if st.button("Tüm Logları ve Yarışmayı Sıfırla"):
        global_logs.clear()
        st.session_state.level = 1
        st.rerun()
