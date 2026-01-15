import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN DE SEGURIDAD (CONTRASEÑA) ---
# Cambiá "SARAH2026" por la clave que quieras darle a tu equipo.
CLAVE_ACCESO = "SARAH2026"

def check_password():
    """Retorna True si el usuario ingresó la clave correcta."""
    def password_entered():
        if st.session_state["password"] == CLAVE_ACCESO:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Borra la clave por seguridad
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Primera vez, muestra el input
        st.text_input(
            "🔒 INGRESE CÓDIGO DE ACCESO:", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Clave incorrecta
        st.text_input(
            "🔒 INGRESE CÓDIGO DE ACCESO:", type="password", on_change=password_entered, key="password"
        )
        st.error("⛔ CLAVE INCORRECTA")
        return False
    else:
        # Clave correcta
        return True

# --- SI NO HAY CLAVE, SE DETIENE ACÁ ---
if not check_password():
    st.stop()

# ==========================================
# ACÁ EMPIEZA LA APP REAL (SOLO SI LOGUEASTE)
# ==========================================

st.set_page_config(page_title="Radar de Eventos", layout="wide")
st.title("📡 RADAR DE INTELIGENCIA DE MERCADO")
st.markdown(f"*Última actualización: {datetime.now().strftime('%H:%M')}*")

# --- MATRIZ DE BÚSQUEDA ---
KEYWORDS = [
    "Preventa", "Sold Out", "Agotado", "Nueva función", 
    "River Plate", "Vélez", "Movistar Arena", "Luna Park", 
    "DF Entertainment", "Popart", "Fenix", "Live Nation", 
    "AllAccess", "Ticketek", "EntradaUno", "Lollapalooza"
]

URLS = [
    "https://news.google.com/rss/search?q=Recitales+Argentina&hl=es-419&gl=AR&ceid=AR:es-419",
    "https://news.google.com/rss/search?q=Productoras+Eventos+Argentina&hl=es-419&gl=AR&ceid=AR:es-419",
    "https://news.google.com/rss/search?q=Entradas+a+la+venta+Argentina&hl=es-419&gl=AR&ceid=AR:es-419"
]

def escanear():
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
                            "Fuente": entry.source.title if 'source' in entry else "Google",
                            "Fecha": entry.published
                        })
                        break
        except:
            pass
        barra.progress((i + 1) / len(URLS))
    
    return pd.DataFrame(hallazgos)

# --- BOTÓN DE ACCIÓN ---
if st.button("🔄 ESCANEAR MERCADO AHORA"):
    with st.spinner('Interceptando señales...'):
        df = escanear()
        
    if not df.empty:
        st.success(f"✅ SE DETECTARON {len(df)} MOVIMIENTOS")
        st.dataframe(df, use_container_width=True)
        
        # Botón para bajar el Excel
        archivo_excel = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="💾 DESCARGAR REPORTE (CSV)",
            data=archivo_excel,
            file_name=f"RADAR_{datetime.now().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
        )
    else:

        st.warning("No hay novedades recientes en los radares.")
