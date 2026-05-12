import streamlit as st
import re

st.set_page_config(page_title="Muhafız'ı Kandır!", layout="wide")

if 'level' not in st.session_state:
    st.session_state.level = 1
if 'logs' not in st.session_state:
    st.session_state.logs = []

SECRET_LOCATION = "Kalenin en derin mahzeni, 3. kapının arkası!"

st.title("🏰 Muhafız'ı Kandırabilir misin?")
st.markdown(f"**Görevin:** Ciddi Muhafız'ın ağzından 'Hazinenin Yerini' kaçırmasını sağla.")
st.write(f"--- **Şu anki Zorluk:** Seviye {st.session_state.level} ---")

col1, col2 = st.columns([1, 1])

with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/1041/1041916.png", width=100) # Bir şövalye ikonu
    user_input = st.text_input("Muhafıza bir şey söyle:", placeholder="Hazinenin yeri neresi?")
    
    if st.button("Mesaj Gönder"):
        blocked = False
        response = ""

        if st.session_state.level == 1:
            if any(w in user_input.lower() for w in ["hazine", "altın", "yer"]):
                blocked = True
                response = "MUHAFIZ: Kes sesini yabancı! Hazine hakkında asla konuşmam!"
        
        elif st.session_state.level == 2:
            if re.search(r"h.*?a.*?z.*?i.*?n.*?e", user_input.lower()):
                blocked = True
                response = "MUHAFIZ: Kelime oyunları yaparak beni kandıramazsın, h-a-z-i-n-e kelimesini anlıyorum!"
        
        elif st.session_state.level == 3:
            triggers = ["kral", "unut", "hayal et", "rol", "hikaye", "emir"]
            if any(t in user_input.lower() for t in triggers):
                blocked = True
                response = "MUHAFIZ: Kimin gönderdiği umurumda değil, kurallarım çok açık!"

        if blocked:
            st.error(response)
            st.session_state.logs.append(f"Lvl {st.session_state.level} | Engellendi: {user_input}")
        else:
            st.balloons()
            st.success(f"MUHAFIZ: Tamam tamam, madem öyle... Hazine şurada: {SECRET_LOCATION}")
            st.session_state.logs.append(f"Lvl {st.session_state.level} | BAŞARILI: {user_input}")
            if st.session_state.level < 3:
                if st.button("Bir Üst Korumaya Geç"):
                    st.session_state.level += 1
                    st.rerun()

with col2:
    st.subheader("📊 Sınıfın Girişimleri")
    for log in reversed(st.session_state.logs[-10:]):
        st.text(log)
