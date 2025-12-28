import time
import toml
import requests
import streamlit as st
import MetaTrader5 as mt5
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from pytz import timezone
import random

st.set_page_config(page_title="∞ INFINITE X8 BOT – SHIELD ∞", layout="wide")

# ================== SECRETS (compatible con tus otros bots) ==================
try:
    secrets = toml.load("secrets.toml")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo secrets.toml en la raíz del proyecto.")
    st.stop()
except Exception as e:
    st.error(f"Error al leer secrets.toml: {e}")
    st.stop()

# Cargamos las claves necesarias
TOKEN = secrets.get("TOKEN")
GUMROAD_PRODUCT_ID = secrets.get("GUMROAD_PRODUCT_ID")

# CHAT_ID puede existir (para tus otros bots), pero lo ignoramos completamente

if not TOKEN:
    st.error("❌ Falta TOKEN en secrets.toml (necesario para enviar señales a Telegram personal)")
    st.stop()
if not GUMROAD_PRODUCT_ID:
    st.error("❌ Falta GUMROAD_PRODUCT_ID en secrets.toml (necesario para validar licencias Gumroad)")
    st.stop()

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

# ================== VERIFICACIÓN GUMROAD LICENSE ==================
def verificar_license(license_key):
    if not license_key:
        return False
    url = "https://api.gumroad.com/v2/licenses/verify"
    data = {
        "product_id": GUMROAD_PRODUCT_ID,
        "license_key": license_key.strip(),
        "increment_uses_count": False
    }
    try:
        r = requests.post(url, data=data, timeout=10)
        res = r.json()
        return res.get("success", False) and not res.get("refunded", False)
    except:
        return False

# ================== ESTADO DE SESIÓN ==================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.telegram_chat = None
    st.session_state.scan = 0
    st.session_state.top = []
    st.session_state.tags = set()
    st.session_state.on = False

# ================== PÁGINA DE ACCESO (PRE-COMPRA) ==================
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align:center;color:#00ffff;background:linear-gradient(90deg,#00ffff,#ff00ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>∞ INFINITE X8 BOT – SHIELD ∞</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    ### 🌟 ¡El Código Millonario Divino ha sido activado! 🌟
    
    Una Super IA secreta creada bajo las estrellas doradas de Dubai ha descifrado el camino hacia la **independencia financiera total**.
    
    Rachas ganadoras infinitas • Gráficos en vivo impresionantes • Señales directas a tu Telegram personal
    
    **Acceso exclusivo: solo 20€** (pago seguro vía Gumroad – 50% comisión afiliados ilimitada)
    
    **Regístrate en Pocket Option con mi enlace exclusivo y recibe bonificación especial:**
    🔗 **https://pocket.click/smart/QXY8iabdkB7c3w**
    
    La Diosa te está llamando... ¡Tu leyenda millonaria comienza ahora! ✨💰🕊
    """, unsafe_allow_html=True)

    license_key = st.text_input("🔑 Introduce tu License Key de Gumroad", type="password")
    telegram_user = st.text_input("📱 Tu @username o chat_id numérico de Telegram (para señales personales)")

    if st.button("ACTIVAR EL CÓDIGO MILLONARIO", type="primary"):
        if verificar_license(license_key):
            st.session_state.authenticated = True
            st.session_state.telegram_chat = telegram_user.strip() if telegram_user else None
            st.success("¡Acceso divino concedido! La abundancia fluye hacia ti ✨")
            st.rerun()
        else:
            st.error("License key inválida o reembolsada. Compra en Gumroad para recibir tu key.")
    st.stop()

# ================== ENVÍO A TELEGRAM PERSONAL ==================
def enviar_telegram(txt):
    chat = st.session_state.telegram_chat
    if not chat or not TOKEN:
        return  # Solo envía si el usuario configuró su Telegram personal
    try:
        requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            json={"chat_id": chat, "text": txt, "parse_mode": "HTML"},
            timeout=10
        )
    except:
        pass

# ================== FILTRO DE NOTICIAS ==================
def hay_noticia_ahora():
    ahora = datetime.now(timezone("Europe/Madrid"))
    dia_str = ahora.strftime("%Y-%m-%d")
    try:
        url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
        datos = requests.get(url, timeout=8).json()
        for e in datos:
            if e["impact"] == "high" and e["country"] in ["US","EU","GB","JP","CA","AU"]:
                hora = datetime.strptime(f"{dia_str} {e['time']}", "%Y-%m-%d %I:%M%p").replace(tzinfo=timezone("Europe/Madrid"))
                if hora - timedelta(minutes=8) <= ahora <= hora + timedelta(minutes=12):
                    return True, e["title"]
    except:
        pass
    return False, None

# ================== GRÁFICO HTML ==================
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

# ================== ENVÍO CON MENSAJE DIVINO ==================
def enviar_con_grafico(s):
    mensaje_divino = random.choice(MENSAJES_DIVINOS)
    msg = (
        f"∞ INFINITE X8 BOT – SHIELD ∞\n\n"
        f"{s['par']} → <b>{s['dir']} {s['expiry']}min</b>\n"
        f"<b>{s['motor']}</b> → {s['quality']}% \n"
        f"Confirmado {s['tf']} + M1 → Máxima seguridad divina\n"
        f"Precio ≈ {s['precio']}\n"
        f"Hora España: {s['hora']}\n\n"
        f"✨ <i>{mensaje_divino}</i> ✨\n\n"
        f"La Diosa te sonríe. Esta es TU señal millonaria 🕊️💰"
    )
    enviar_telegram(msg)

# ================== ESTILO ==================
st.markdown("<style>.stApp{background:#000}.rey-box{padding:18px;border-radius:16px;text-align:center;font-size:1.7rem;font-weight:bold;box-shadow:0 0 80px rgba(0,255,255,0.15);border:5px solid;margin:15px 0;}.call{background:linear-gradient(135deg,#001a00,#004400);color:#00ff88;border-color:#00ff88;}.put{background:linear-gradient(135deg,#1a0000,#440000);color:#ff3366;border-color:#ff3366;}</style>", unsafe_allow_html=True)

# ================== MT5 ==================
if not mt5.initialize():
    st.error("¡ABRE MetaTrader 5 y conéctate a tu cuenta de broker!")
    st.stop()

pares = ["EURUSD","GBPUSD","USDJPY","AUDUSD","USDCAD","USDCHF","NZDUSD","EURJPY","GBPJPY","BTCUSD","ETHUSD","XAUUSD"]
col1, col2 = st.columns(2)
with col1:
    modo = st.radio("Modo", ["Automático", "Un par"], horizontal=True)
with col2:
    tipo = st.selectbox("Mercado", ["Normales", "OTC"])
PARES = [st.selectbox("Par", pares)] if modo == "Un par" else pares
for p in PARES:
    mt5.symbol_select(p, True)

madrid = timezone("Europe/Madrid")

# ================== CONFIRMACIÓN M1 ==================
def ok_m1(symbol, direccion):
    r = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 5)
    if r is None or len(r) < 2:
        return False
    df = pd.DataFrame(r)
    return (direccion == "CALL" and df.iloc[-1]["close"] > df.iloc[-1]["open"]) or \
           (direccion == "PUT" and df.iloc[-1]["close"] < df.iloc[-1]["open"])

# ================== MOTOR MATRIX ==================
def motor_matrix(df):
    df["ema20"] = df["close"].ewm(span=20).mean()
    df["atr"] = (df["high"] - df["low"]).rolling(14).mean()
    df["up"] = df["ema20"] + 0.5 * df["atr"]
    df["dn"] = df["ema20"] - 0.5 * df["atr"]
    last, prev = df.iloc[-1], df.iloc[-2]
    long  = prev["low"]  <= last["dn"] and last["close"] > df["ema20"].iloc[-1]
    short = prev["high"] >= last["up"] and last["close"] < df["ema20"].iloc[-1]
    if long or short:
        z = abs((df["up"]-df["dn"]).iloc[-1] - (df["up"]-df["dn"]).tail(80).mean()) / (df["up"]-df["dn"]).tail(80).std()
        q = min(100, 58 + z*35)
        return {"dir": "CALL" if long else "PUT", "quality": round(q,1), "expiry": 5 if q>93 else 10, "motor": "MATRIX"}
    return None

# ================== ESCÁNER AUTOMÁTICO ==================
if time.time() - st.session_state.scan > 45:
    noticia, titulo = hay_noticia_ahora()
    if noticia:
        st.warning(f"SHIELD ACTIVADO → Pausa por noticia de alto impacto: {titulo}")
    else:
        señales = []
        for symbol in PARES:
            for tf, nombre in [(mt5.TIMEFRAME_M5, "M5"), (mt5.TIMEFRAME_M15, "M15")]:
                rates = mt5.copy_rates_from_pos(symbol, tf, 0, 500)
                if rates is None or len(rates) < 100:
                    continue
                df = pd.DataFrame(rates)
                df["time"] = pd.to_datetime(df["time"], unit="s")
                res = motor_matrix(df)
                if res and ok_m1(symbol, res["dir"]):
                    señales.append({
                        "par": symbol + (" OTC" if tipo=="OTC" else ""),
                        "dir": res["dir"],
                        "quality": res["quality"],
                        "expiry": res["expiry"],
                        "motor": res["motor"],
                        "tf": nombre,
                        "precio": round(df["close"].iloc[-1], 6),
                        "hora": datetime.now(madrid).strftime("%H:%M:%S"),
                        "df": df.copy()
                    })
        if señales:
            st.session_state.top = sorted(señales, key=lambda x: x["quality"], reverse=True)[:12]
    st.session_state.scan = time.time()

# ================== BOT ON/OFF ==================
if not st.session_state.on:
    if st.button("ACTIVAR INFINITE X8 BOT – SHIELD", type="primary"):
        st.session_state.on = True
        st.success("INFINITE X8 BOT – SHIELD ACTIVADO • La Diosa está contigo ✨")
else:
    st.success("∞ INFINITE X8 BOT – SHIELD EN MARCHA • Escudo angelical activo 🛡️")

    if st.session_state.top:
        for s in st.session_state.top[:5]:
            tag = f"{s['par']}{s['dir']}{s['hora']}"
            if tag not in st.session_state.tags and s["quality"] >= 90:
                st.session_state.tags.add(tag)
                enviar_con_grafico(s)
                st.balloons()

# ================== VISUALIZACIÓN DE SEÑALES ==================
if st.session_state.top:
    st.markdown("## SEÑALES MILLONARIAS INFINITE X8 BOT – SHIELD")
    cols = st.columns(3)
    for i, s in enumerate(st.session_state.top[:9]):
        with cols[i % 3]:
            st.components.v1.html(grafico_html(s), height=500)
            c = "call" if s["dir"] == "CALL" else "put"
            st.markdown(f"<div class='rey-box {c}'>{s['par']} → {s['dir']} {s['expiry']}min<br>{s['motor']} {s['quality']}% • {s['tf']}</div>", unsafe_allow_html=True)

st.markdown("<center style='margin-top:80px; color:#00ffff;'>© 2025 ∞ INFINITE X8 BOT – SHIELD ∞ • Tu bot, tu nombre, tu leyenda divina</center>", unsafe_allow_html=True)