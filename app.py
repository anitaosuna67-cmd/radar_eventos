python
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
        st.markdown("<h3 style='color: #FFD700;'>🔒 PASSLINE INTEL</h3>", unsafe_allow_html=True)
        st.text_input("INGRESE CLAVE DE ACCESO:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("INGRESE CLAVE DE ACCESO:", type="password", on_change=password_entered, key="password")
        st.error("⛔ CLAVE INCORRECTA")
        return False
    else:
        return True

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Passline Radar", layout="wide", page_icon="⚡")

# --- ESTÉTICA PASSLINE (CSS) ---
# Fondo oscuro, Botones Amarillos (#FFD700), Texto contrastado
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    /* Botones estilo Passline (Amarillo fuerte) */
    div.stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border: none;
        font-weight: 800;
        border-radius: 5px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FFC300 !important;
        transform: scale(1.02);
    }
    /* Links estilo Passline */
    a {
        color: #FFD700 !important;
        text-decoration: none;
    }
    /* Métricas */
    div[data-testid="stMetricValue"] {
        color: #FFD700 !important;
    }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background-color: #FFD700 !important;
        color: #000000 !important;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

if not check_password():
    st.stop()

# ==========================================
# HEADER
# ==========================================
st.title("⚡ PASSLINE INTELLIGENCE")
st.caption(f"📅 REPORTE: {datetime.now().strftime('%d/%m/%Y')} | 🌍 MERCADO: ARGENTINA")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "💰 MARKET SHARE & VALUACIÓN", 
    "🗞️ NOTICIAS (REAL TIME)", 
    "🔥 TENDENCIAS SOCIALES (7 DÍAS)", 
    "🎯 MAPA DE CAZA (LEADS)"
])

# ==========================================
# TAB 1: MARKET SHARE & DINERO
# ==========================================
with tab1:
    st.subheader("🏆 VALOR TOTAL DE MERCADO (Estimación Ticketing AR)")
    
    # KPIs Generales (Simulación basada en industria)
    c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
    c_kpi1.metric("Volumen Anual Mercado", "$280.000 M", "ARS (Est.)")
    c_kpi2.metric("Ticket Promedio", "$45.000", "+120% Inflación")
    c_kpi3.metric("Tickets Vendidos/Año", "6.5 Millones", "Total Industria")

    st.divider()
    
    st.subheader("📊 CUOTA DE MERCADO POR JUGADOR")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥇 ALL ACCESS (DF)")
        st.metric("Share", "45%", "Líder")
        st.markdown("**Facturación Est:** $126.000 M")
        st.caption("River, Lolla, Taylor. Volumen masivo.")

    with col2:
        st.markdown("### 🥈 TICKETEK")
        st.metric("Share", "25%", "-5%")
        st.markdown("**Facturación Est:** $70.000 M")
        st.caption("Teatros, Festivales, Interior.")

    with col3:
        st.markdown("### 🥉 ENTRADA UNO")
        st.metric("Share", "20%", "Estable")
        st.markdown("**Facturación Est:** $56.000 M")
        st.caption("Movistar Arena (Alta rotación).")

    st.info("⚡ **PASSLINE TARGET:** El 10% restante ($28.000 M) está fragmentado en ticketeras chicas. Ahí está nuestro crecimiento inmediato (Boliches, Indie, Fiestas).")

# ==========================================
# TAB 2: NOTICIAS (ORDENADAS)
# ==========================================
with tab2:
    st.subheader("🗞️ RADAR DE NOTICIAS MUSICALES")
    
    URLS = [
        "https://news.google.com/rss/search?q=Recitales+Argentina+Entradas&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Productoras+Eventos+Argentina&hl=es-419&gl=AR&ceid=AR:es-419"
    ]

    if st.button("🔄 ACTUALIZAR PRENSA"):
        hallazgos = []
        barra = st.progress(0)
        
        for i, url in enumerate(URLS):
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    try:
                        fecha_obj = datetime(*entry.published_parsed[:6])
                    except:
                        fecha_obj = datetime.now()

                    hallazgos.append({
                        "Fecha_Obj": fecha_obj,
                        "Fecha": fecha_obj.strftime("%d/%m %H:%M"),
                        "Titular": entry.title,
                        "Link": entry.link
                    })
            except: pass
            barra.progress((i + 1) / len(URLS))
        
        if hallazgos:
            df = pd.DataFrame(hallazgos)
            df = df.sort_values(by="Fecha_Obj", ascending=False) # Ordenar por fecha
            
            st.dataframe(
                df[["Fecha", "Titular", "Link"]], 
                use_container_width=True,
                column_config={"Link": st.column_config.LinkColumn("Leer Nota")}
            )
        else:
            st.warning("Sin noticias nuevas en este barrido.")

# ==========================================
# TAB 3: TENDENCIAS (7 DÍAS)
# ==========================================
with tab3:
    st.subheader("🔥 TERMÓMETRO SOCIAL (Última Semana)")
    st.markdown("Búsquedas filtradas para detectar tendencias recientes.")

    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("### 📱 TIKTOK & INSTAGRAM")
        # Links con filtros de fecha (donde es posible)
        url_tk = "https://www.tiktok.com/search?q=recitales%20argentina&t=1705000000000&publish_time=7" # Filtro 7 días
        st.link_button("🎵 TIKTOK: TENDENCIAS (7 DÍAS)", url_tk)
        
        url_ig = "https://www.instagram.com/explore/tags/recitalesargentina/"
        st.link_button("📸 INSTAGRAM: HASHTAG RECIENTE", url_ig)

    with c2:
        st.markdown("### 🐦 X (TWITTER) - EL PULSO")
        # Filtro 'f=live' muestra lo último
        url_tw = "https://twitter.com/search?q=entradas%20argentina%20(precio%20OR%20fila%20virtual)&src=typed_query&f=live"
        st.link_button("🐦 VER QUEJAS EN TIEMPO REAL", url_tw)

    st.divider()
    st.markdown("### 📢 TOP INFLUENCERS SECTORIALES")
    
    influencers = [
        ("POGOPEDIA", "https://www.instagram.com/pogopedia/"),
        ("RECITALES.ARG", "https://www.instagram.com/recitales.arg/"),
        ("INDIE HOY", "https://www.instagram.com/indiehoy/"),
        ("FILO NEWS", "https://www.instagram.com/filonewsok/"),
        ("BILLBOARD AR", "https://www.instagram.com/billboardar/")
    ]
    
    cols_inf = st.columns(len(influencers))
    for i, (nombre, link) in enumerate(influencers):
        with cols_inf[i]:
            st.link_button(nombre, link)

# ==========================================
# TAB 4: MAPA DE CAZA (LEADS)
# ==========================================
with tab4:
    st.subheader("🎯 OBJETIVOS COMERCIALES (100 PRODUCTORAS)")
    st.markdown("Lista de prospectos para contactar. **Objetivo: Migrar a Passline.**")

    # Botón a Passline Admin
    st.link_button("⚡ IR AL ADMIN DE PASSLINE", "https://home.passline.com/")
    
    with st.expander("📂 VER LISTADO COMPLETO (Click para abrir)"):
        col_leads_1, col_leads_2 = st.columns(2)
        
        with col_leads_1:
            st.markdown("#### 🏢 MAJORS & ROCK")
            st.write("""
            1. DF Entertainment
            2. Fenix Entertainment
            3. PopArt Music
            4. Move Concerts
            5. T4F (Time For Fun)
            6. Live Nation Argentina
            7. 6 Pasos
            8. Ake Music
            9. Gonna Go
            10. 300 Producciones
            11. En Vivo Producciones
            12. MTS Producciones
            13. S-Music
            14. Ozono Producciones
            15. RGB Entertainment
            16. Lauria Dale Play
            17. Rimas Producciones
            18. EB Producciones
            19. Producciones de Barrio
            20. World Music BA
            21. Geiser Discos
            22. Niceto Club
            23. Konex
            24. Camping BA
            25. CC Richards
            26. La Tangente
            27. Strummer Bar
            28. Moscú
            29. Uniclub
            30. El Emergente
            31. Makena Cantina Club
            32. The Roxy Live
            33. Vorterix
            34. Teatro Flores
            35. Groove
            36. Palermo Club
            37. Studio Crobar
            38. Beatflow
            39. Otra Historia Club
            40. Club Lucimbre
            """)

        with col_leads_2:
            st.markdown("#### 🎛️ NOCHE & FEDERAL")
            st.write("""
            41. BNP (Córdoba)
            42. Crobar
            43. Mandarine Park
            44. The Bow
            45. PM Open Air
            46. Rio Electronic Music
            47. Under Club
            48. Cocoliche
            49. Bahrein
            50. La Fábrica (Córdoba)
            51. Metropolitano (Rosario)
            52. Desert in Me
            53. Savage
            54. BNN
            55. Jet BA
            56. Afrika
            57. Bayside
            58. Moscu
            59. Rose in Rio
            60. Banana
            61. Kika Club
            62. Amerika
            63. Rheo
            64. Club 69
            65. Human Club
            66. Fiesta Bresh
            67. Fiesta Polenta
            68. La Pardo
            69. Katana
            70. El Club de la Serpiente
            71. Fiesta Plop
            72. Puerca
            73. Hiedrah
            74. Sudan
            75. Duki / SSJ
            76. YSY A / Sponsor Dios
            77. Ca7riel & Paco
            78. Dillom / Bohemian Groove
            79. Fiesta Invasión
            80. Rose Girls
            81. Plaza de la Música (Cba)
            82. Quality Espacio (Cba)
            83. XL Abasto (Cba)
            84. Tribus (Santa Fe)
            85. La Sala de las Artes (Rosario)
            86. Teatro Broadway (Rosario)
            87. Gap (MDP)
            88. Silos Arena (MDP)
            89. Mute (MDP)
            90. At Park (MDP)
            91. Auditorio Bustelo (Mza)
            92. Arena Maipú (Mza)
            93. Club Central Córdoba (Tuc)
            94. Sala del Rey (Cba)
            95. Estadio Delmi (Salta)
            96. CCP (Entre Ríos)
            97. Espacio DUAM (Neuquén)
            98. Mood Live (Neuquén)
            99. Casino Magic (Neuquén)
            100. Boxing Club (Río Gallegos)
            """)
    
   
