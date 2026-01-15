import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# --- SEGURIDAD ---
CLAVE_ACCESO = "SARAH2026"

def check_password():
    def password_entered():
        if st.session_state["password"] == CLAVE_ACCESO:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("🔒 SYSTEM LOCKED - ENTER PASSWORD:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 SYSTEM LOCKED - ENTER PASSWORD:", type="password", on_change=password_entered, key="password")
        st.error("⛔ ACCESO DENEGADO")
        return False
    else:
        return True

if not check_password():
    st.stop()

# ==========================================
# UI CONFIG
# ==========================================
st.set_page_config(page_title="Radar Estratégico V3", layout="wide", page_icon="🧿")

st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00FF00; }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size: 1.2rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🧿 RADAR DE INTELIGENCIA: INDUSTRIA DEL ENTRETENIMIENTO")
st.caption(f"📅 FECHA: {datetime.now().strftime('%d/%m/%Y')} | 🌍 REGIÓN: ARGENTINA | 🕵️ OPERADOR: SARAH")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 BIG DATA DE MERCADO", 
    "📰 NOTICIAS & MACRO", 
    "🕵️ REDES E INFLUENCERS", 
    "🏢 COMPETENCIA (WATCHLIST)"
])

# ==========================================
# TAB 1: BIG DATA & TOP 3 (Estimación de Mercado)
# ==========================================
with tab1:
    st.subheader("🏆 TOP 3 TICKETERAS ARGENTINA (Dominancia de Mercado)")
    st.info("Ranking basado en volumen de tickets cortados (Estadios + Arenas) y exclusividad de venues principales.")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥇 #1 ALL ACCESS (DF)")
        st.metric(label="Dominio de Mercado", value="45%", delta="Líder Indiscutido")
        st.markdown("**Fortaleza:** Monopolio de River Plate + Lollapalooza + Taylor Swift/Coldplay.")
        st.markdown("**Punto Débil:** Alta dependencia de mega-shows internacionales.")

    with col2:
        st.markdown("### 🥈 #2 TICKETEK (PopArt)")
        st.metric(label="Dominio de Mercado", value="25%", delta="-5% vs 2024")
        st.markdown("**Fortaleza:** Volumen histórico, capilaridad en teatros y festivales locales (Cosquín).")
        st.markdown("**Punto Débil:** Pérdida de venues grandes ante AllAccess.")

    with col3:
        st.markdown("### 🥉 #3 ENTRADA UNO")
        st.metric(label="Dominio de Mercado", value="20%", delta="+ Crecimiento Rápido")
        st.markdown("**Fortaleza:** Dueños del Movistar Arena (el venue con más fechas al año).")
        st.markdown("**Punto Débil:** Menor catálogo de festivales propios.")

    st.divider()
    
    st.subheader("📉 TERMÓMETRO DEL SECTOR (Estimación Q1 2026)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Inflación Entradas (YoY)", "140%", "Alta Fricción")
    m2.metric("Ocupación Arenas", "85%", "Saturado")
    m3.metric("Dólar Artista", "Estable/Alto", "Riesgo Medio")
    m4.metric("Nuevos Players", "Passline/Alpogo", "Creciendo en Nicho")

# ==========================================
# TAB 2: NOTICIAS MACRO Y SECTORIALES
# ==========================================
with tab2:
    st.subheader("🗞️ ESCÁNER DE PRENSA (Incluye Historial Reciente)")
    
    # Agregamos términos económicos para buscar balances y crisis del sector
    KEYWORDS = [
        "Preventa", "Sold Out", "Lollapalooza", "Cosquín Rock",
        "Crisis productoras", "Consumo cultural", "Caída ventas entradas",
        "DF Entertainment", "Fenix", "Popart", "Live Nation",
        "Impuestos espectáculos", "Dólar Coldplay", "Sponsoring música"
    ]

    URLS = [
        "https://news.google.com/rss/search?q=Industria+Espectaculo+Argentina+Economia&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Recitales+Argentina&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Entradas+recitales+precios+argentina&hl=es-419&gl=AR&ceid=AR:es-419"
    ]

    if st.button("🔄 EJECUTAR BARRIDO DE NOTICIAS"):
        hallazgos = []
        barra = st.progress(0)
        for i, url in enumerate(URLS):
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    hallazgos.append({
                        "Título": entry.title,
                        "Fuente": entry.source.title if 'source' in entry else "Google",
                        "Fecha": entry.published,
                        "Link": entry.link
                    })
            except: pass
            barra.progress((i + 1) / len(URLS))
        
        if hallazgos:
            df = pd.DataFrame(hallazgos)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("El radar no detectó señales nuevas en prensa.")

# ==========================================
# TAB 3: REDES E INFLUENCERS (La Voz de la Calle)
# ==========================================
with tab3:
    st.subheader("🕵️ INTELIGENCIA DE REDES SOCIALES")
    st.markdown("Monitoreo de cuentas clave que mueven la aguja en Argentina.")

    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 📢 CUENTAS INFLUENCERS (Data & Rumores)")
        influencers = {
            "Pogopedia (La Biblia)": "https://www.instagram.com/pogopedia/",
            "Recitales.Arg (Data)": "https://www.instagram.com/recitales.arg/",
            "Indie Hoy (Nicho)": "https://www.instagram.com/indiehoy/",
            "Rolling Stone Ar": "https://www.instagram.com/rollingstonear/",
            "Filo News (Masivo)": "https://www.instagram.com/filonewsok/"
        }
        for nombre, link in influencers.items():
            st.link_button(f"👉 {nombre}", link)

    with c2:
        st.markdown("### 🔎 BUSCADORES PROFUNDOS")
        url_tw = "https://twitter.com/search?q=(estafa%20OR%20robo%20OR%20carisimo)%20entradas%20argentina&src=typed_query&f=live"
        st.link_button("🐦 BUSCAR ENOJO EN TWITTER (Real Time)", url_tw)
        
        url_tk = "https://www.tiktok.com/search?q=recitales%20argentina%202026%20rumores"
        st.link_button("🎵 BUSCAR RUMORES EN TIKTOK", url_tk)

# ==========================================
# TAB 4: COMPETENCIA COMPLETA
# ==========================================
with tab4:
    st.subheader("🔭 VIGILANCIA DE COMPETENCIA")
    
    st.markdown("#### 🦖 LOS GIGANTES (Mainstream)")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.link_button("DF / ALL ACCESS", "https://www.allaccess.com.ar/")
        st.caption("River, Lolla, Taylor")
    with col_b:
        st.link_button("TICKETEK / POPART", "https://www.ticketek.com.ar/")
        st.caption("Obras, Festivales, Teatros")
    with col_c:
        st.link_button("MOVISTAR ARENA / E1", "https://www.movistararena.com.ar/")
        st.caption("El venue con más tráfico")

    st.write("---")

    st.markdown("#### 🚀 LOS EMERGENTES & NICHO (Ojo acá)")
    col_d, col_e, col_f, col_g = st.columns(4)
    with col_d:
        st.link_button("PASSLINE", "https://www.passline.com/ar")
        st.caption("Fiestas, Boliches, Indie")
    with col_e:
        st.link_button("ALPOGO", "https://alpogo.com/")
        st.caption("Fuerte en Córdoba/Interior")
    with col_f:
        st.link_button("VENTI", "https://venti.com.ar/")
        st.caption("Electrónica / Boliches")
    with col_g:
        st.link_button("TICKETPORTAL", "https://www.ticketportal.com.ar/")
        st.caption("Luna Park (Vieja Escuela)")

    st.write("---")
    st.markdown("#### 🌍 VIGILANCIA INTERNACIONAL (Para anticipar giras)")
    st.link_button("LIVE NATION LATAM", "https://www.livenation.lat/")
