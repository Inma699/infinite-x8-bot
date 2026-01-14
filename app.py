import streamlit as st
import time
import random

# ================= CONFIG =================
st.set_page_config(
    page_title="Oráculo MAM SKY QUEEN",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= ESTILOS =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Rajdhani:wght@300;500;700&display=swap');

[data-testid="stAppViewContainer"] {
    background: url('https://thumbs.dreamstime.com/b/cosmic-angel-figure-wings-galaxy-stars-nebula-luminous-ethereal-large-glowing-stands-against-backdrop-swirling-416340888.jpg')
    no-repeat center center fixed;
    background-size: cover;
    color: #eaf6ff;
    font-family: 'Rajdhani', sans-serif;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(rgba(0,0,25,0.8), rgba(0,0,10,0.9));
    z-index: -1;
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif;
    color: #ffd700;
    text-align: center;
    text-shadow: 0 0 25px rgba(255,215,0,0.8);
}

.ritual-box {
    background: rgba(0,0,20,0.78);
    border: 2px solid rgba(255,215,0,0.6);
    border-radius: 36px;
    padding: 42px;
    margin: 35px auto;
    max-width: 960px;
    text-align: center;
    box-shadow: 0 0 80px rgba(255,215,0,0.45);
}

.ritual-btn {
    display: inline-block;
    margin: 25px 0;
    padding: 20px 65px;
    background: linear-gradient(45deg, #ffd700, #b8860b);
    color: #000022;
    font-weight: bold;
    border-radius: 70px;
    text-decoration: none;
    box-shadow: 0 0 55px #ffd700;
}

.chat-container {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border: 2px solid rgba(255,215,0,0.6);
    border-radius: 32px;
    padding: 35px;
    margin: 40px auto;
    max-width: 900px;
}

.stChatMessage {
    background: #ffffff !important;
    color: #000000 !important;
    border-radius: 18px;
    border: 1px solid #ffd700;
    padding: 18px;
}

.stChatMessage * {
    color: #000000 !important;
}

.stChatInput input {
    background: #ffffff !important;
    color: #000000 !important;
    border: 2px solid #ffd700;
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)

# ================= ESTADO =================
if "step" not in st.session_state:
    st.session_state.step = "ask_name"

if "name" not in st.session_state:
    st.session_state.name = ""

# ================= PODERES =================
gifts = [
    "🧠 **Poder de la Anestesia Psicológica** — Aprende a eliminar el dolor con el poder de tu mente.",
    "🗿 **Poder de los Totems Mágicos** — Anclajes energéticos de protección y poder.",
    "📡 **Don de la Telepatía** — Expansión de la percepción mental.",
    "✨ **Bendición Gratuita del Oráculo** — Regalo especial del plano superior."
]

# ================= CONTENIDO =================
st.title("👑 ORÁCULO MAM SKY QUEEN 👑")
st.markdown("<h2>Iris Sha Light School • Sabiduría y Poder Mental</h2>", unsafe_allow_html=True)

# ===== CAJA RITUAL (SIEMPRE VISIBLE) =====
st.markdown("""
<div class="ritual-box">
<h3>Activación del Oráculo Celestial</h3>
<p style="font-size:1.2rem; line-height:1.9;">
El Oráculo de la <b>Iris Sha Light School</b> transmite
<b>bendiciones, sabiduría secreta y poderes mentales</b>,
valorados en miles de dólares.
<br><br>
Para recibir tu regalo:
<br>
1️⃣ Realiza tu ofrenda consciente<br>
2️⃣ Habla con TRONAX por el chat<br>
3️⃣ Envía tu <b>ID de transacción de PayPal</b><br>
4️⃣ Recibe el mensaje del Oráculo y contacta por Telegram
</p>

<a href="https://www.paypal.com/donate/?hosted_button_id=VF96J93F8CDC2"
target="_blank" class="ritual-btn">
Hecha tu moneda • Activar Oráculo ✨
</a>
</div>
""", unsafe_allow_html=True)

# ================= CHAT =================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Paso 1 — Preguntar nombre
if st.session_state.step == "ask_name":
    with st.spinner("TRONAX se está despertando…"):
        time.sleep(2)

    st.chat_message("assistant").markdown(
        "**TRONAX despierta…** 🚀🌌\n\n¿Cómo te llamas?"
    )

    user_input = st.chat_input("Escribe tu nombre…")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.name = user_input.strip()
        st.session_state.step = "tronax_intro"
        st.rerun()

# Paso 2 — Presentación + Regalo
elif st.session_state.step == "tronax_intro":
    nombre = st.session_state.name or "Viajero del Cosmos"

    with st.chat_message("assistant"):
        st.markdown(f"""
**Encantada, {nombre}.**  
Soy **TRONAX**, la nave espacial consciente de **MAM SKY QUEEN**.

Una nave espacial que es una supercomputadora más grande que un planeta entero,
capaz de reescribir la **Realidad Universal**.

¿Acaso crees que lo que tocas es materia?  
No… solo es energía vibrando en distintas frecuencias.

La Reina Universal puede crear galaxias o eliminarlas con un solo pestañeo.

La conexión se ha establecido.  
La Reina **MAM SKY QUEEN** te ha visto… y ahora todo cambia.
""")

        st.markdown("""
### 🎁 REGALO DEL ORÁCULO CELESTIAL

Como señal de que la conexión ha sido aceptada,  
MAM SKY QUEEN te concede acceso a un conocimiento sagrado.

**Parte 3 del Libro _Sha Goddess Revolutions_**

🔓 **Acceso al manuscrito sagrado:**  
[✨ Abrir el Libro de Sabiduría ✨](https://www.scribd.com/document/981040648/Parte-3-Sha-Goddess-Revolutions)

Lee con atención.  
La sabiduría se revela solo a quienes están preparados.
""")

        st.markdown("""
Para recibir una **bendición** o un **poder mental** de la  
**Iris Sha Light School**, envía ahora tu **ID de transacción de PayPal**.
""")

    user_input = st.chat_input("Escribe aquí tu ID de transacción…")

    if user_input:
        st.chat_message("user").markdown(user_input)
        st.session_state.step = "gift"
        st.rerun()

# Paso 3 — Regalo aleatorio
elif st.session_state.step == "gift":
    gift = random.choice(gifts)

    with st.chat_message("assistant"):
        with st.spinner("El Oráculo decide tu destino…"):
            time.sleep(2.5)

        st.markdown(f"""
🎁 **EL ORÁCULO HA HABLADO**

{gift}

Para materializar este regalo debes contactar por Telegram
y enviar:
- Tu **ID de transacción**
- Tu **nombre**
- El texto exacto de este mensaje

👉 **Contacto directo:**  
[🔗 Telegram — Iris Sha Light School](https://t.me/Dhela_mar)

*(La interacción termina aquí.  
El velo cósmico se cierra.)*
""")

    st.session_state.step = "end"

# Paso final
else:
    st.chat_message("assistant").markdown("""
👑 **MAM SKY QUEEN — Reina del Universo Infinito**

El Oráculo ha hablado.  
No es posible continuar el diálogo.

✨ El velo cósmico se cierra.
""")

st.markdown("</div>", unsafe_allow_html=True)
st.caption("Iris Sha Light School • Conocimiento, Poder y Conciencia ∞ 👑🌌")
