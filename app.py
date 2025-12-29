import time
import requests
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import random
import numpy as np
from pytz import timezone

st.set_page_config(page_title="∞ INFINITE X8 BOT – SHIELD ∞", layout="wide")

# ================== SECRETS ==================
secrets = st.secrets
TOKEN = secrets.get("TOKEN", "")
GUMROAD_PRODUCT_ID = secrets["GUMROAD_PRODUCT_ID"]

# ================== MENSAJES DIVINOS ==================
MENSAJES_DIVINOS = [
    "La Diosa y todos los arcángeles mayores están contigo ahora, guiándote hacia la riqueza infinita ✨🕊️",
    "¡Eureka! El Código Millonario se activa – rachas ganadoras protegidas por luz dorada 💰🙌",
    "Siente la prosperidad fluir como río de oro sagrado. Esta señal es tu victoria divina 🌟",
    "Una IA secreta nacida bajo las estrellas de Dubai te bendice con abundancia eterna ⭐",
    "Los ángeles envuelven tus trades en escudo inquebrantable. Confía, ya estás ganando 🛡️💚",
    "La sensación de riqueza inunda todo tu cuerpo. Esta es la señal perfecta del universo 🙏",
    "Dios te sonríe desde los cielos. La victoria millonaria es tuya ya 🕊️"
]

# ================== VERIFICACIÓN GUMROAD ==================
def verificar_license(license_key):
    if not license_key:
        return False
    url = "https://api.gumroad.com/v2/licenses/verify"
    data = {"product_id": GUMROAD_PRODUCT_ID, "license_key": license_key.strip(), "increment_uses_count": False}
    try:
        r = requests.post(url, data=data, timeout=10)
        res = r.json()
        return res.get("success", False) and not res.get("refunded", False)
    except:
        return False

# ================== ESTADO ==================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.telegram_chat = None
    st.session_state.scan = 0
    st.session_state.top = []
    st.session_state.tags = set()
    st.session_state.on = False

# ================== PÁGINA DE ACCESO ==================
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center;color:#00ffff;background:linear-gradient(90deg,#00ffff,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>∞ INFINITE X8 BOT – SHIELD ∞</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🌟 ¡El Código Millonario Divino ha sido activado! 🌟
    
    Acceso exclusivo al INFINITE X8 BOT – SHIELD: la IA secreta de Dubai que genera rachas ganadoras infinitas.
    
    **Solo 20€ – Licencia instantánea**
    
    Compra aquí: 👉 https://pasioniris.gumroad.com/l/yjjek
    
    Después introduce tu License Key y recibe señales millonarias en vivo ✨💰
    """, unsafe_allow_html=True)

    license_key = st.text_input("🔑 Introduce tu License Key de Gumroad", type="password")
    telegram_user = st.text_input("📱 Tu @username o chat_id de Telegram (opcional)")

    if st.button("ACTIVAR EL CÓDIGO MILLONARIO", type="primary"):
        if verificar_license(license_key):
            st.session_state.authenticated = True
            st.session_state.telegram_chat = telegram_user.strip() if telegram_user else None
            st.success("¡Acceso divino concedido! La abundancia fluye ✨")
            st.rerun()
        else:
            st.error("License key inválida. Compra primero en Gumroad.")
    st.stop()

# ================== ESTILO ==================
st.markdown("<style>.stApp{background:#000}.rey-box{padding:18px;border-radius:16px;text-align:center;font-size:1.7rem;font-weight:bold;box-shadow:0 0 80px rgba(0,255,255,0.15);border:5px solid;margin:15px 0;}.call{background:linear-gradient(135deg,#001a00,#004400);color:#00ff88;border-color:#00ff88;}.put{background:linear-gradient(135deg,#1a0000,#440000);color:#ff3366;border-color:#ff3366;}</style>", unsafe_allow_html=True)

madrid = timezone("Europe/Madrid")
pares = ["EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD","USDCHF","NZDUSD","EURJPY","GBPJPY","BTCUSD","ETHUSD","XAUUSD"]

# ================== SIMULADOR DE SEÑALES ==================
def generar_senal_simulada(symbol):
    precio = round(random.uniform(0.8, 1.5) if "USD" in symbol else random.uniform(100, 200) if "JPY" in symbol else random.uniform(1800, 2100) if "XAU" in symbol else random.uniform(20000, 40000), 5)
    quality = random.randint(90, 99)
    dir = random.choices(["CALL", "PUT"], weights=[75, 25])[0]
    expiry = 5 if quality > 94 else 10
    tf = random.choice(["M5", "M15"])
    
    times = pd.date_range(end=datetime.now(madrid), periods=120, freq='1min')
    base = np.cumsum(np.random.normal(0, 0.0005, 120)) + precio
    df = pd.DataFrame({
        'time': times,
        'open': base,
        'high': base + np.random.uniform(0, 0.002, 120),
        'low': base - np.random.uniform(0, 0.002, 120),
        'close': base + np.random.uniform(-0.001, 0.001, 120)
    })
    
    return {
        "par": symbol,
        "dir": dir,
        "quality": quality,
        "expiry": expiry,
        "motor": "MATRIX DIVINO",
        "tf": tf,
        "precio": precio,
        "hora": datetime.now(madrid).strftime("%H:%M:%S"),
        "df": df
    }

# ================== GRÁFICO ==================
def grafico_html(s):
    df = s["df"]
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df["time"], open=df["open"], high=df["high"], low=df["low"], close=df["close"]))
    color = "lime" if s["dir"] == "CALL" else "red"
    y = df["high"].iloc[-1]*1.002 if s["dir"]=="CALL" else df["low"].iloc[-1]*0.998
    fig.add_annotation(x=df["time"].iloc[-1], y=y, text=f"{s['dir']} {s['quality']}%",
                       font=dict(size=20,color="white"), showarrow=True, arrowcolor=color,
                       arrowhead=8, arrowsize=4, arrowwidth=6, bgcolor=color)
    fig.update_layout(template="plotly_dark", height=420, margin=dict(t=60),
                      title=f"{s['par']} • {s['tf']} → {s['dir']} {s['quality']}%")
    return fig.to_html(include_plotlyjs="cdn", full_html=False)

# ================== ESCÁNER SIMULADO ==================
if time.time() - st.session_state.scan > 25:
    señales = []
    for symbol in pares:
        if random.random() > 0.3:
            s = generar_senal_simulada(symbol)
            señales.append(s)
    if señales:
        st.session_state.top = sorted(señales, key=lambda x: x["quality"], reverse=True)[:12]
    st.session_state.scan = time.time()

# ================== BOT ON/OFF ==================
if not st.session_state.on:
    if st.button("ACTIVAR INFINITE X8 BOT – SHIELD", type="primary"):
        st.session_state.on = True
        st.rerun()
else:
    st.success("∞ INFINITE X8 BOT – SHIELD EN MARCHA • Escudo angelical activo 🛡️")

# ================== VISUALIZACIÓN ==================
if st.session_state.top:
    st.markdown("## SEÑALES MILLONARIAS EN VIVO")
    cols = st.columns(3)
    for i, s in enumerate(st.session_state.top[:9]):
        with cols[i % 3]:
            st.components.v1.html(grafico_html(s), height=500)
            c = "call" if s["dir"] == "CALL" else "put"
            st.markdown(f"<div class='rey-box {c}'>{s['par']} → {s['dir']} {s['expiry']}min<br>{s['motor']} {s['quality']}% • {s['tf']}</div>", unsafe_allow_html=True)
            if random.random() > 0.7:
                st.balloons()

st.markdown("<center style='margin-top:80px; color:#00ffff;'>© 2025 ∞ INFINITE X8 BOT – SHIELD ∞ • Tu leyenda divina comienza aquí</center>", unsafe_allow_html=True)
