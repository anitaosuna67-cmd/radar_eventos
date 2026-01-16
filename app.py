import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime, timedelta

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
        st.markdown("<h3 style='color: #FFD700;'>🔒 ACCESO RESTRINGIDO</h3>", unsafe_allow_html=True)
        st.text_input("CLAVE DE OPERACIONES:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("CLAVE DE OPERACIONES:", type="password", on_change=password_entered, key="password")
        st.error("⛔ DENEGADO")
        return False
    else:
        return True

# --- CONFIGURACIÓN UI ---
st.set_page_config(page_title="Market Intel", layout="wide", page_icon="👁️")

# Estética "Dark/Yellow" (Identidad visual implícita, sin logo)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    div.stButton > button {
        background-color: #FFD700 !important; color: #000000 !important;
        border: none; font-weight: 800; border-radius: 4px;
    }
    div.stButton > button:hover { background-color: #FFC300 !important; transform: scale(1.02); }
    a { color: #FFD700 !important; text-decoration: none; }
    div[data-testid="stMetricValue"] { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

if not check_password():
    st.stop()

# --- CÁLCULO DE FECHAS PARA FILTROS ---
hoy = datetime.now()
hace_una_semana = (hoy - timedelta(days=7)).strftime('%Y-%m-%d')

# ==========================================
# HEADER NEUTRAL
# ==========================================
st.title("👁️ MARKET INTELLIGENCE: LIVE ENTERTAINMENT")
st.caption(f"📅 REPORTE OPERATIVO | 🌍 ARGENTINA | 🛡️ NIVEL: ESTRATÉGICO")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 MACRO DATA", 
    "🗞️ NOTICIAS SECTORIALES", 
    "🔥 TENDENCIAS & TECH", 
    "🎯 PRODUCTORAS (TARGETS)"
])

# ==========================================
# TAB 1: MACRO DATA
# ==========================================
with tab1:
    st.subheader("🏆 CUOTA DE MERCADO ESTIMADA")
    c1, c2, c3 = st.columns(3)
    c1.metric("ALL ACCESS", "45%", "Mega Estadios")
    c2.metric("TICKETEK", "25%", "Teatros/Interior")
    c3.metric("ENTRADA UNO", "20%", "Arenas")
    
    st.divider()
    st.markdown("### 💰 VALUACIÓN DEL MERCADO")
    k1, k2 = st.columns(2)
    k1.metric("Volumen Anual (ARS)", "$280.000 M", "Estimado")
    k2.metric("Ticket Promedio", "$45.000", "+ Inflación")

# ==========================================
# TAB 2: NOTICIAS (SOLO MÚSICA/NEGOCIO)
# ==========================================
with tab2:
    st.subheader("🗞️ NOVEDADES DE LA INDUSTRIA")
    
    # Filtro 'when:7d' fuerza a Google a traer cosas de la última semana
    URLS = [
        "https://news.google.com/rss/search?q=Recitales+Argentina+Entradas+when:7d&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Negocio+Musica+En+Vivo+Argentina+when:7d&hl=es-419&gl=AR&ceid=AR:es-419"
    ]

    if st.button("🔄 ACTUALIZAR NOTICIAS"):
        hallazgos = []
        for url in URLS:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    hallazgos.append({
                        "Fecha": entry.published,
                        "Titular": entry.title,
                        "Link": entry.link
                    })
            except: pass
        
        if hallazgos:
            df = pd.DataFrame(hallazgos)
            st.dataframe(df, use_container_width=True, column_config={"Link": st.column_config.LinkColumn("Leer")})
        else:
            st.info("Sin noticias de alto impacto en las últimas horas.")

# ==========================================
# TAB 3: TENDENCIAS SOCIALES & TECH (EL CEREBRO)
# ==========================================
with tab3:
    col_social, col_tech = st.columns([1, 1])

    with col_social:
        st.subheader("🔥 PULSO SOCIAL (Filtro 7 Días)")
        st.markdown("Búsquedas forzadas a la última semana.")
        
        # Twitter con filtro de fecha dinámico
        tw_query = f"entradas argentina since:{hace_una_semana} (estafa OR precio OR fila)"
        url_tw = f"https://twitter.com/search?q={tw_query}&src=typed_query&f=live"
        st.link_button("🐦 X: QUEJAS ESTA SEMANA", url_tw)
        
        # TikTok (Intento de filtro reciente)
        url_tk = "https://www.tiktok.com/search?q=recitales%20argentina%202026&t=1705000000000&publish_time=7"
        st.link_button("🎵 TIKTOK: TRENDS SEMANALES", url_tk)

    with col_tech:
        st.subheader("🤖 ALGORITMOS & ADS (Updates)")
        st.markdown("Novedades de Meta/Google que afectan la pauta.")
        
        # RSS Específico de Tech Marketing en Español
        url_tech = "https://news.google.com/rss/search?q=Novedades+Meta+Ads+Google+Ads+Algoritmo+Instagram+when:14d&hl=es-419&gl=AR&ceid=AR:es-419"
        
        try:
            feed_tech = feedparser.parse(url_tech)
            if feed_tech.entries:
                for entry in feed_tech.entries[:3]: # Solo las 3 últimas
                    st.info(f"**{entry.title}**\n\n[Leer más]({entry.link})")
            else:
                st.write("Sin cambios de algoritmo reportados esta semana.")
        except:
            st.write("Error conectando con radar tech.")

# ==========================================
# TAB 4: PRODUCTORAS (LISTA DE NICHO)
# ==========================================
with tab4:
    st.subheader("🎯 PRODUCTORAS (NICHO & OPORTUNIDAD)")
    st.markdown("Foco: Organizadores medianos/indie que podrían migrar de sistema.")
    
    # Botón discreto al admin
    st.link_button("⚡ ACCESO ADMIN", "https://home.passline.com/")
    
    st.write("---")

    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### 🎸 INDIE / ROCK / TRAP (Targets)")
        st.write("""
        *Objetivo: Migrar de Alpogo/Venti/Ticketek*
        
        1. **Niceto Club** (Produce ciclos propios)
        2. **CC Konex** (Agenda cultural masiva)
        3. **Bohemian Groove** (Dillom y asociados)
        4. **Gonna Go** (Festivales en La Plata/Interior)
        5. **Club de la Serpiente** (Fiesta temática High Ticket)
        6. **Fiesta Polenta** (Gran volumen joven)
        7. **La Tangente** (Palermo, alto tráfico indie)
        8. **Strummer Bar** (Rock clásico/under)
        9. **Camping BA** (Ciclos al aire libre)
        10. **Indie Folks** (Productora de nicho internacional)
        11. **Refugiados** (Ciclos de trap/urbano)
        12. **Teatro Vorterix** (Agenda propia)
        13. **Groove** (Fiestas y recitales medios)
        14. **Uniclub** (Under fuerte)
        15. **El Emergente** (Semillero)
        16. **Producciones de Barrio** (Trap/RKT)
        17. **Moscú** (Costanera)
        18. **Beatflow** (Palermo)
        19. **Cultural Morán** (Agenda alternativa)
        20. **Teatro Flores** (Metal/Rock barrial)
        """)

    with col_b:
        st.markdown("#### 🎛️ ELECTRÓNICA & NIGHTLIFE")
        st.write("""
        *Objetivo: Migrar de Venti/BAM/Tickets*
        
        21. **Crobar / Studio** (La catedral techno)
        22. **The Bow** (House/Electrónica Costanera)
        23. **PM Open Air** (Ciclos diurnos masivos)
        24. **Rio Electronic Music** (Grandes fechas outdoor)
        25. **Under Club** (Techno purista)
        26. **Cocoliche** (Under histórico)
        27. **Bahrein** (Centro, público fiel)
        28. **BNP (Córdoba)** (El gigante del interior)
        29. **La Fábrica (Córdoba)** (Fechas internacionales)
        30. **Metropolitano (Rosario)** (Lado B / Fechas grandes)
        31. **Switch (Rosario)** (Clubbing)
        32. **Mute (Mar del Plata)** (Temporada verano)
        33. **Silos Arena (MDP)** (Nuevo player fuerte)
        34. **Desert in Me** (Productora High End)
        35. **Savage** (Ciclos)
        36. **BANANA** (Costanera, Cachengue/Elec)
        37. **Jet BA** (High End)
        38. **Bayside** (Punta Carrasco)
        39. **Club 69** (Histórico Jueves)
        40. **Human Club** (Nuevas tendencias)
        """)

      

    
                        


    
   
            
           

