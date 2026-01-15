import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
import time

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
        st.text_input("🔒 PASSLINE INTEL - INGRESE CLAVE:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 PASSLINE INTEL - INGRESE CLAVE:", type="password", on_change=password_entered, key="password")
        st.error("⛔ CLAVE INCORRECTA")
        return False
    else:
        return True

if not check_password():
    st.stop()

# ==========================================
# UI CONFIG
# ==========================================
st.set_page_config(page_title="Passline Intelligence", layout="wide", page_icon="⚡")

st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00FF00; }
    /* Destacar Passline */
    a[href="https://home.passline.com/"] {
        border: 2px solid #00FF00 !important;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ PASSLINE: CENTRO DE INTELIGENCIA")
st.caption(f"📅 DATA REPORT: {datetime.now().strftime('%d/%m/%Y %H:%M')} | 🎯 OBJETIVO: DOMINIO DE MERCADO")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 BIG DATA DE MERCADO", 
    "📰 NOTICIAS (TIEMPO REAL)", 
    "📢 TOP 10 INFLUENCERS", 
    "🏢 MAPA DE COMPETENCIA"
])

# ==========================================
# TAB 1: BIG DATA & FUENTES
# ==========================================
with tab1:
    st.subheader("🏆 TOP 3 TICKETERAS ARGENTINA (Estado de Situación)")
    st.markdown("""
    > **Fuentes de Datos:** Estimaciones cruzadas basadas en:
    > *   *Pollstar (Global Concert Pulse)*
    > *   *SimilarWeb (Tráfico Mensual Argentina)*
    > *   *CAPIF (Reportes de Mercado Digital)*
    > *   *Google Trends (Volumen de Búsqueda)*
    """)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥇 #1 ALL ACCESS (DF)")
        st.metric("Market Share", "45%", "Holding Dominante")
        st.caption("Base: River Plate, Lollapalooza. Tráfico web sostenido por mega-eventos.")

    with col2:
        st.markdown("### 🥈 #2 TICKETEK")
        st.metric("Market Share", "25%", "-5% Tendencia")
        st.caption("Base: Festivales históricos (Cosquín) y Teatros. Perdiendo terreno en estadios.")

    with col3:
        st.markdown("### 🥉 #3 ENTRADA UNO")
        st.metric("Market Share", "20%", "Crecimiento Arenas")
        st.caption("Base: Movistar Arena. Alta rotación de tickets semanales.")

    st.divider()
    st.info("💡 **Oportunidad para PASSLINE:** El segmento 'Emergente/Clubbing/Indie' está fragmentado. El crecimiento está en capturar la 'Long Tail' (muchos eventos medianos) donde los gigantes son lentos.")

# ==========================================
# TAB 2: NOTICIAS (ORDEN CRONOLÓGICO)
# ==========================================
with tab2:
    st.subheader("🗞️ BARRIDO DE PRENSA (ÚLTIMOS 90 DÍAS)")
    
    # URLS optimizadas para buscar por fecha reciente
    URLS = [
        "https://news.google.com/rss/search?q=Industria+Eventos+Argentina+after:2025-10-01&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Recitales+Argentina+after:2025-10-01&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Venta+entradas+Argentina+after:2025-10-01&hl=es-419&gl=AR&ceid=AR:es-419"
    ]

    if st.button("🔄 ACTUALIZAR NOTICIAS AHORA"):
        hallazgos = []
        barra = st.progress(0)
        
        for i, url in enumerate(URLS):
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    # Convertimos fecha a formato legible y objeto datetime para ordenar
                    fecha_obj = datetime(*entry.published_parsed[:6])
                    hallazgos.append({
                        "Fecha": fecha_obj,
                        "Fecha_Str": fecha_obj.strftime("%d/%m/%Y %H:%M"),
                        "Título": entry.title,
                        "Fuente": entry.source.title if 'source' in entry else "Google News",
                        "Link": entry.link
                    })
            except: pass
            barra.progress((i + 1) / len(URLS))
        
        if hallazgos:
            # ORDENAR POR FECHA (MÁS NUEVO ARRIBA)
            df = pd.DataFrame(hallazgos)
            df = df.sort_values(by="Fecha", ascending=False)
            
            # Mostramos la tabla limpia sin la columna objeto fecha
            st.success(f"SE CARGARON {len(df)} NOTICIAS ORDENADAS")
            st.dataframe(
                df[["Fecha_Str", "Título", "Fuente", "Link"]], 
                use_container_width=True,
                column_config={"Link": st.column_config.LinkColumn("Leer Nota")}
            )
        else:
            st.warning("No se encontraron noticias nuevas en este barrido.")

# ==========================================
# TAB 3: TOP 10 INFLUENCERS
# ==========================================
with tab3:
    st.subheader("📢 VOCES AUTORIZADAS (Jerarquía de Influencia)")
    st.markdown("Ordenados por capacidad de marcar agenda y viralizar.")

    influencers = [
        ("1. POGOPEDIA", "https://www.instagram.com/pogopedia/", "👑 La Biblia del público joven. Si sale acá, existe."),
        ("2. FILO NEWS", "https://www.instagram.com/filonewsok/", "📢 Masivo. Marca agenda general."),
        ("3. RECITALES.ARG", "https://www.instagram.com/recitales.arg/", "📅 Agenda dura. La gente entra para ver fechas."),
        ("4. BILLBOARD AR", "https://www.instagram.com/billboardar/", "💼 Industria. Voz oficial del chart."),
        ("5. ROLLING STONE AR", "https://www.instagram.com/rollingstonear/", "🎸 Prestigio y notas de profundidad."),
        ("6. INDIE HOY", "https://www.instagram.com/indiehoy/", "🚀 Nicho Indie/Alternativo (Target Passline)."),
        ("7. SILENCIO", "https://www.instagram.com/silenciorock/", "📝 Periodismo musical serio."),
        ("8. GENERACIÓN B", "https://www.instagram.com/generacionb/", "📱 Contenido digital y entrevistas."),
        ("9. QUIERO MÚSICA", "https://www.instagram.com/quieromusicatv/", "📺 TV + Redes. Público más tradicional."),
        ("10. TU MÚSICA HOY", "https://www.instagram.com/tumusicahoy/", "🎤 Urbano y Pop. Viralidad rápida.")
    ]

    for nombre, link, desc in influencers:
        with st.container():
            c1, c2 = st.columns([1, 3])
            c1.link_button(f"👉 {nombre}", link)
            c2.markdown(f"*{desc}*")
            st.divider()

# ==========================================
# TAB 4: MAPA DE COMPETENCIA (Passline HQ)
# ==========================================
with tab4:
    st.subheader("🔭 RADAR DE COMPETENCIA")
    
    st.markdown("### 🏠 NUESTRA CASA")
    st.link_button("⚡ IR A PASSLINE HOME (ADMIN)", "https://home.passline.com/")
    
    st.write("---")
    
    st.markdown("### ⚔️ LOS RIVALES (Watchlist)")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Tier 1: Los Gigantes**")
        st.link_button("DF / AllAccess", "https://www.allaccess.com.ar/")
        st.link_button("Ticketek", "https://www.ticketek.com.ar/")
        st.link_button("Movistar Arena", "https://www.movistararena.com.ar/")
    
    with col_b:
        st.markdown("**Tier 2: Competencia Directa (Nicho)**")
        st.link_button("Alpogo", "https://alpogo.com/")
        st.link_button("Venti", "https://venti.com.ar/")
        st.link_button("Ticketportal", "https://www.ticketportal.com.ar/")
        
    with col_c:
        st.markdown("**Tier 3: Regionales / Otros**")
        st.link_button("EntradaWeb (Mendoza)", "https://www.entradaweb.com.ar/")
        st.link_button("Plateanet (Teatro)", "https://www.plateanet.com/")
