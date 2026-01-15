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
        st.text_input("🔒 MARKET INTEL - INGRESE CLAVE:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("🔒 MARKET INTEL - INGRESE CLAVE:", type="password", on_change=password_entered, key="password")
        st.error("⛔ CLAVE INCORRECTA")
        return False
    else:
        return True

if not check_password():
    st.stop()

# ==========================================
# UI CONFIG (NEUTRAL)
# ==========================================
st.set_page_config(page_title="Live Ent. Intelligence", layout="wide", page_icon="📡")

st.markdown("""
<style>
    .big-font { font-size:20px !important; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #00FF00; }
    /* Estilo sutil para resaltar botones importantes */
    .stButton button { border: 1px solid #333; }
</style>
""", unsafe_allow_html=True)

st.title("📡 LIVE ENTERTAINMENT: MARKET INTELLIGENCE")
st.caption(f"📅 REPORTE AL: {datetime.now().strftime('%d/%m/%Y')} | 🌍 MERCADO: ARGENTINA")

# --- PESTAÑAS ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 BIG DATA & MARKET SHARE", 
    "🗞️ NOTICIAS: MÚSICA & NEGOCIO", 
    "📢 TOP 10 INFLUENCERS", 
    "🎯 MAPA DE PRODUCTORAS (LEADS)"
])

# ==========================================
# TAB 1: BIG DATA
# ==========================================
with tab1:
    st.subheader("🏆 MARKET SHARE ESTIMADO (Ticketing Argentina)")
    st.markdown("> *Fuentes: Pollstar, SimilarWeb Traffic, CAPIF Reports.*")

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🥇 #1 ALL ACCESS (DF)")
        st.metric("Cuota Mercado", "45%", "Dominante")
        st.caption("River, Lolla, Taylor Swift. Volúmen alto, pocos eventos.")

    with col2:
        st.markdown("### 🥈 #2 TICKETEK")
        st.metric("Cuota Mercado", "25%", "-5% YoY")
        st.caption("Teatros, Festivales Históricos. Gran capilaridad.")

    with col3:
        st.markdown("### 🥉 #3 ENTRADA UNO")
        st.metric("Cuota Mercado", "20%", "Estable")
        st.caption("Movistar Arena. Ticket promedio alto.")

    st.divider()
    st.info("📉 **Insight:** El mercado de estadios está saturado. La oportunidad de crecimiento (Blue Ocean) está en el segmento de **Clubbing, Electrónica y Ciclos Indie**.")

# ==========================================
# TAB 2: NOTICIAS FILTRADAS (Música y Negocio)
# ==========================================
with tab2:
    st.subheader("🗞️ ÚLTIMAS NOVEDADES DEL SECTOR")
    
    # Filtros agresivos para solo traer música y negocio
    URLS = [
        "https://news.google.com/rss/search?q=Recitales+Argentina+Conciertos&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=Productoras+Espectaculos+Argentina+Negocios&hl=es-419&gl=AR&ceid=AR:es-419",
        "https://news.google.com/rss/search?q=DF+Entertainment+Fenix+Popart+Live+Nation+Argentina&hl=es-419&gl=AR&ceid=AR:es-419"
    ]

    if st.button("🔄 ESCANEAR NOTICIAS DE MÚSICA"):
        hallazgos = []
        barra = st.progress(0)
        
        for i, url in enumerate(URLS):
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    # Parsear fecha
                    try:
                        fecha_obj = datetime(*entry.published_parsed[:6])
                    except:
                        fecha_obj = datetime.now()

                    hallazgos.append({
                        "Fecha_Obj": fecha_obj,
                        "Fecha": fecha_obj.strftime("%d/%m/%Y %H:%M"),
                        "Titular": entry.title,
                        "Fuente": entry.source.title if 'source' in entry else "Google",
                        "Link": entry.link
                    })
            except: pass
            barra.progress((i + 1) / len(URLS))
        
        if hallazgos:
            # Ordenar por fecha (más nuevo primero)
            df = pd.DataFrame(hallazgos)
            df = df.sort_values(by="Fecha_Obj", ascending=False)
            
            st.success(f"{len(df)} NOTICIAS RELEVANTES ENCONTRADAS")
            st.dataframe(
                df[["Fecha", "Titular", "Fuente", "Link"]], 
                use_container_width=True,
                column_config={"Link": st.column_config.LinkColumn("Leer")}
            )
        else:
            st.warning("Sin novedades recientes en el radar musical.")

# ==========================================
# TAB 3: INFLUENCERS (JERARQUÍA)
# ==========================================
with tab3:
    st.subheader("📢 VOCES AUTORIZADAS (Top 10)")
    
    influencers = [
        ("1. POGOPEDIA", "https://www.instagram.com/pogopedia/", "La Biblia del público joven."),
        ("2. FILO NEWS", "https://www.instagram.com/filonewsok/", "Agenda masiva y lanzamientos."),
        ("3. RECITALES.ARG", "https://www.instagram.com/recitales.arg/", "Calendario duro de fechas."),
        ("4. BILLBOARD AR", "https://www.instagram.com/billboardar/", "Voz de la industria."),
        ("5. ROLLING STONE AR", "https://www.instagram.com/rollingstonear/", "Prestigio."),
        ("6. INDIE HOY", "https://www.instagram.com/indiehoy/", "Clave para el nicho alternativo."),
        ("7. SILENCIO", "https://www.instagram.com/silenciorock/", "Periodismo musical."),
        ("8. GENERACIÓN B", "https://www.instagram.com/generacionb/", "Entrevistas y digital."),
        ("9. QUIERO MÚSICA", "https://www.instagram.com/quieromusicatv/", "Público tradicional."),
        ("10. TU MÚSICA HOY", "https://www.instagram.com/tumusicahoy/", "Urbano y Pop.")
    ]

    for nombre, link, desc in influencers:
        c1, c2 = st.columns([1, 3])
        c1.link_button(f"👉 {nombre}", link)
        c2.write(f"*{desc}*")
        st.divider()

# ==========================================
# TAB 4: MAPA DE COMPETENCIA & LEADS
# ==========================================
with tab4:
    st.subheader("🎯 MAPA DE ACTORES Y PROSPECTOS")
    
    st.markdown("### 🔭 TICKETERAS ACTIVAS (Competencia)")
    c_a, c_b, c_c = st.columns(3)
    with c_a:
        st.markdown("**Tier 1 (Gigantes)**")
        st.link_button("AllAccess", "https://www.allaccess.com.ar/")
        st.link_button("Ticketek", "https://www.ticketek.com.ar/")
        st.link_button("Movistar Arena", "https://www.movistararena.com.ar/")
    with c_b:
        st.markdown("**Tier 2 (Nicho/Emergente)**")
        st.link_button("PASSLINE", "https://home.passline.com/")
        st.link_button("Alpogo", "https://alpogo.com/")
        st.link_button("Venti", "https://venti.com.ar/")
    with c_c:
        st.markdown("**Tier 3 (Regionales)**")
        st.link_button("Ticketportal", "https://www.ticketportal.com.ar/")
        st.link_button("EntradaWeb", "https://www.entradaweb.com.ar/")

    st.divider()

    st.subheader("📋 LISTA DE CAZA: 100 PRODUCTORAS & CICLOS (Leads)")
    st.markdown("Listado de objetivos comerciales potenciales (Productoras, Venues y Fiestas que operan en Argentina).")

    with st.expander("🔥 VER LISTADO COMPLETO DE TARGETS (Click para desplegar)"):
        col_prods_1, col_prods_2, col_prods_3 = st.columns(3)
        
        with col_prods_1:
            st.markdown("#### 🏢 MAJORS & ESTADIOS")
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
            19. Producines de Barrio
            20. World Music BA
            """)
            
            st.markdown("#### 🎸 INDIE / ROCK / UNDER")
            st.write("""
            21. Geiser Discos
            22. Niceto Club (Producción propia)
            23. Konex (Agenda propia)
            24. Camping BA
            25. CC Richards
            26. La Tangente
            27. Strummer Bar
            28. Moscú
            29. Uniclub
            30. El Emergente
            31. Makena Cantina Club
            32. The Roxy Live
            33. Vorterix (Producción)
            34. Teatro Flores
            35. Groove
            36. Palermo Club
            37. Studio Crobar
            38. Beatflow
            39. Otra Historia Club
            40. Club Lucimbre
            """)

        with col_prods_2:
            st.markdown("#### 🎛️ ELECTRÓNICA & NIGHTLIFE")
            st.write("""
            41. BNP (Buenas Noches Producciones) - Cba
            42. Crobar
            43. Mandarine Park / Tent
            44. The Bow
            45. PM Open Air
            46. Rio Electronic Music
            47. Under Club
            48. Cocoliche
            49. Bahrein
            50. La Fábrica (Córdoba)
            51. Metropolitano (Rosario - Lado B)
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
            """)

        with col_prods_3:
            st.markdown("#### 🎉 FIESTAS & CICLOS (High Ticket)")
            st.write("""
            66. Fiesta Bresh
            67. Fiesta Polenta
            68. La Pardo
            69. Katana
            70. El Club de la Serpiente
            71. Fiesta Plop
            72. Puerca
            73. Hiedrah
            74. Sudan
            75. Duki / SSJ (Eventos propios)
            76. YSY A / Sponsor Dios (Prod propia)
            77. Ca7riel & Paco (Prod propia)
            78. Dillom / Bohemian Groove
            79. Fiesta Invasión
            80. Rose Girls
            """)
            
            st.markdown("#### 🌎 FEDERAL / INTERIOR")
            st.write("""
            81. Plaza de la Música (Córdoba)
            82. Quality Espacio (Córdoba)
            83. XL Abasto (Córdoba)
            84. Tribus Club de Arte (Santa Fe)
            85. La Sala de las Artes (Rosario)
            86. Teatro Broadway (Rosario)
            87. Gap (Mar del Plata)
            88. Silos Arena (Mar del Plata)
            89. Mute (Mar del Plata)
            90. At Park (Mar del Plata)
            91. Auditorio Bustelo (Mendoza)
            92. Arena Maipú (Mendoza)
            93. Club Central Córdoba (Tucumán)
            94. Sala del Rey (Córdoba)
            95. Estadio Delmi (Salta)
            96. CCP (Concepción del Uruguay)
            97. Espacio DUAM (Neuquén)
            98. Mood Live (Neuquén)
            99. Casino Magic (Neuquén)
            100. Boxing Club (Río Gallegos)
