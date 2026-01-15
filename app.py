import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Si usaste Secrets, cambialo acá. Si no, dejá la clave dura.
# CLAVE_ACCESO = st.secrets["general_password"] 
CLAVE_ACCESO = "SARAH2026"

def check_password():
    def password_entered():
        if st.session_state["password"] == CLAVE_ACCESO:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔒 ACCESO RESTRINGIDO - INGRESE CLAVE:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 ACCESO RESTRINGIDO - INGRESE CLAVE:", type="password", on_change=password_entered, key="password")
        st.error("⛔ ACCESO DENEGADO")
        return False
    else:
        return True

if not check_password():
    st.stop()

# ==========================================
# INTERFAZ PRINCIPAL
# ==========================================

st.set_page_config(page_title="Radar Eventos V2", layout="wide", page_icon="📡")

# Estilos tipo "War Room"
st.markdown("""
<style>
    .big-font { font-size:24px !important; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 5px; }
    div[data-testid="metric-container"] { background-color: #f0f2f6; padding: 10px; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.title("📡 CENTRO DE INTELIGENCIA DE MERCADO")
st.markdown(f"**Estado:** 🟢 Activo | **Hora:** {datetime.now().strftime('%H:%M')} | **Operador:** SARAH")

# --- PESTAÑAS DE NAVEGACIÓN ---
tab1, tab2, tab3 = st.tabs(["📰 RADAR DE NOTICIAS", "🕵️‍♂️ REDES SOCIALES (OSINT)", "🏢 COMPETENCIA DIRECTA"])

# ==========================================
# TAB 1: EL ESCÁNER DE GOOGLE (Lo que ya tenías)
# ==========================================
with tab1:
    st.subheader("BARRIDO DE PRENSA & WEB")
    
    KEYWORDS = [
        "Preventa", "Sold Out", "Agotado", "Nueva función", "Lineup", 
        "River Plate", "Vélez", "Movistar Arena", "Luna Park", 
        "DF Entertainment", "Popart", "Fenix", "Live Nation", 
        "AllAccess", "Ticketek", "EntradaUno", "Lollapalooza", "Quilmes Rock"
    ]

    URLS = [
        "https://news.google.com/rss/search?q=Recitales+Argentina&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Productoras+Eventos+Argentina&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Entradas+a+la+venta+Argentina&hl=es-419&gl=AR&ceid=AR:es-419"
    ]

    if st.button("🔄 ESCANEAR NOTICIAS AHORA", key="btn_news"):
        hallazgos = []
        barra = st.progress(0)
        for i, url in enumerate(URLS):
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    texto = (entry.title + " " + entry.description).lower()
                    for kw in KEYWORDS:
                        if kw.lower() in texto:
                            hallazgos.append({
                                "Alerta": kw.upper(),
                                "Título": entry.title,
                                "Link": entry.link,
                                "Fecha": entry.published,
                                "Fuente": entry.source.title if 'source' in entry else "Google"
                            })
                            break
            except: pass
            barra.progress((i + 1) / len(URLS))
        
        if hallazgos:
            df = pd.DataFrame(hallazgos)
            st.success(f"SE DETECTARON {len(df)} SEÑALES")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Sin novedades recientes en prensa.")

# ==========================================
# TAB 2: REDES SOCIALES (Búsqueda Profunda)
# ==========================================
with tab2:
    st.subheader("BÚSQUEDA TÁCTICA EN REDES")
    st.markdown("Estos botones ejecutan búsquedas avanzadas en tiempo real para detectar lo que no sale en las noticias.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🐦 X (Twitter) - El Rumor")
        # Busca gente hablando de "entradas" o "precio" en Argentina hoy
        url_tw_rumor = "https://twitter.com/search?q=entradas%20recital%20argentina%20(caro%20OR%20barato%20OR%20conseguir)&src=typed_query&f=live"
        st.link_button("🔍 BUSCAR QUEJAS DE PRECIOS", url_tw_rumor)
        
        # Busca filtraciones de lineups
        url_tw_leak = "https://twitter.com/search?q=(rumor%20OR%20filtrado)%20lineup%20argentina&src=typed_query&f=live"
        st.link_button("🕵️ BUSCAR FILTRACIONES", url_tw_leak)

    with col2:
        st.markdown("### 📸 Instagram/TikTok - La Tendencia")
        # Busca hashtags recientes
        url_ig = "https://www.instagram.com/explore/tags/recitalesargentina/"
        st.link_button("📱 VER HASHTAG #RECITALES", url_ig)
        
        url_tk = "https://www.tiktok.com/search?q=conciertos%20argentina%202026&t=1705000000000"
        st.link_button("🎥 VER TIKTOK TRENDS", url_tk)

    with col3:
        st.markdown("### 👽 Reddit - La Verdad")
        # Busca en r/Argentina y foros
        url_red = "https://www.google.com/search?q=site%3Areddit.com%2Fr%2FArgentina+recitales+estafa+OR+rumor"
        st.link_button("🧠 BUSCAR EN FOROS (REDDIT)", url_red)

# ==========================================
# TAB 3: COMPETENCIA (Watchlist)
# ==========================================
with tab3:
    st.subheader("VIGILANCIA DE COMPETENCIA")
    st.markdown("Accesos directos a las carteleras de los rivales.")
    
    competidores = {
        "DF Entertainment (AllAccess)": "https://www.allaccess.com.ar/",
        "Ticketek Cartelera": "https://www.ticketek.com.ar/",
        "Movistar Arena Agenda": "https://www.movistararena.com.ar/shows/",
        "EntradaUno": "https://entradauno.com/",
        "River Plate Eventos": "https://www.cariverplate.com.ar/estadio-monumental"
    }
    
    # Creamos una grilla de botones
    cols = st.columns(len(competidores))
    for i, (nombre, link) in enumerate(competidores.items()):
        # Usamos modulo para distribuir en columnas si son muchas
        with cols[i % 3]: 
            st.link_button(f"👁️ VER {nombre.upper()}", link)
            st.write("---")

    st.markdown("### 📝 NOTAS DEL EQUIPO")
    notas = st.text_area("Espacio para pegar rumores o datos sueltos:", height=150)
    if st.button("Guardar Nota (Simulado)"):
        st.toast("Nota guardada en memoria local.", icon="💾")
