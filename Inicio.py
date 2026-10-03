"""
☁️ WordCloud Studio — Nube de Palabras Profesional
Aplicación Streamlit con diseño corporativo limpio

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

# ─────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS — interfaz moderna azul / lila
# ─────────────────────────────────────────────
st.markdown("""
<style>

    /* =====================================================
       TIPOGRAFÍA
       ===================================================== */

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(155, 185, 255, 0.25), transparent 25%),
            radial-gradient(circle at 10% 30%, rgba(200, 180, 255, 0.18), transparent 25%),
            #f8faff;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #ffffff 0%,
                #f4f7ff 55%,
                #eef3ff 100%
            ) !important;

        border-right: 1px solid #e1e8f8 !important;
    }

    [data-testid="stSidebar"] h2 {
        color: #202a44 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        letter-spacing: -0.3px !important;
        text-transform: none !important;
    }

    [data-testid="stSidebar"] h3 {
        color: #536180 !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.78rem !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
    }

    [data-testid="stSidebar"] label {
        color: #536180 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] p {
        color: #71809d !important;
        font-size: 0.84rem !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #dfe6f5 !important;
        margin: 18px 0 !important;
    }


    /* =====================================================
       INPUTS
       ===================================================== */

    textarea,
    input[type="text"] {
        background: #ffffff !important;
        border: 1px solid #dce4f5 !important;
        border-radius: 14px !important;
        color: #202a44 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.86rem !important;
        box-shadow: 0 3px 12px rgba(74, 104, 170, 0.05) !important;
    }

    textarea::placeholder,
    input::placeholder {
        color: #a0abc0 !important;
    }

    textarea:focus,
    input[type="text"]:focus {
        border-color: #7d9cff !important;
        box-shadow:
            0 0 0 3px rgba(125, 156, 255, 0.13),
            0 4px 14px rgba(74, 104, 170, 0.08) !important;
    }


    /* =====================================================
       SELECTBOX
       ===================================================== */

    [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #dce4f5 !important;
        border-radius: 12px !important;
        color: #202a44 !important;
        font-size: 0.84rem !important;
        box-shadow: 0 2px 10px rgba(74, 104, 170, 0.04) !important;
    }

    [data-baseweb="select"] > div:hover {
        border-color: #9ab2ff !important;
    }


    /* =====================================================
       TÍTULOS
       ===================================================== */

    h1 {
        font-family: 'Poppins', sans-serif !important;
        color: #202a44 !important;
        font-weight: 700 !important;
        letter-spacing: -1px !important;
    }

    h2 {
        font-family: 'Poppins', sans-serif !important;
        color: #26324f !important;
        font-weight: 700 !important;
    }

    h3 {
        font-family: 'Poppins', sans-serif !important;
        color: #35415f !important;
        font-weight: 600 !important;
    }

    p,
    li {
        color: #687694 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 0.88rem !important;
        line-height: 1.7 !important;
    }


    /* =====================================================
       BOTONES PRINCIPALES
       ===================================================== */

    .stButton > button {
        background: linear-gradient(
            135deg,
            #658cff 0%,
            #8069ed 100%
        ) !important;

        color: #ffffff !important;

        border: none !important;
        border-radius: 14px !important;

        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;

        letter-spacing: 0.1px !important;

        padding: 0.72rem 1.3rem !important;

        min-height: 44px !important;

        box-shadow:
            0 6px 18px rgba(104, 126, 235, 0.28) !important;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease,
            filter 0.2s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(
            135deg,
            #557dff 0%,
            #735ce5 100%
        ) !important;

        color: #ffffff !important;

        transform: translateY(-2px) !important;

        box-shadow:
            0 9px 24px rgba(104, 126, 235, 0.35) !important;
    }

    .stButton > button:active {
        transform: translateY(0px) !important;
    }


    /* =====================================================
       BOTÓN DE DESCARGA
       ===================================================== */

    [data-testid="stDownloadButton"] button {
        background: #ffffff !important;

        color: #566bdb !important;

        border: 1px solid #d5def8 !important;
        border-radius: 13px !important;

        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.82rem !important;

        min-height: 42px !important;

        box-shadow:
            0 4px 14px rgba(74, 104, 170, 0.08) !important;

        transition:
            background 0.2s ease,
            border 0.2s ease,
            transform 0.2s ease !important;
    }

    [data-testid="stDownloadButton"] button:hover {
        background: #f1f4ff !important;
        color: #4659c4 !important;
        border-color: #aebeff !important;
        transform: translateY(-1px) !important;
    }


    /* =====================================================
       MÉTRICAS
       ===================================================== */

    [data-testid="metric-container"] {
        background:
            linear-gradient(
                145deg,
                #ffffff 0%,
                #f7f9ff 100%
            );

        border: 1px solid #e1e7f5;

        border-radius: 18px;

        padding: 18px 20px;

        box-shadow:
            0 6px 20px rgba(65, 91, 150, 0.07);

        position: relative;

        overflow: hidden;
    }

    [data-testid="metric-container"]::before {
        content: "";
        position: absolute;

        top: 0;
        left: 0;

        width: 100%;
        height: 4px;

        background: linear-gradient(
            90deg,
            #6c91ff,
            #8b70ed
        );
    }

    [data-testid="metric-container"] label {
        color: #8792a9 !important;

        font-family: 'Poppins', sans-serif !important;

        font-size: 0.68rem !important;

        font-weight: 600 !important;

        text-transform: uppercase !important;

        letter-spacing: 0.7px !important;
    }

    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #202a44 !important;

        font-family: 'Poppins', sans-serif !important;

        font-weight: 700 !important;

        font-size: 1.45rem !important;
    }


    /* =====================================================
       HEADER PRINCIPAL
       ===================================================== */

    .header-card {
        position: relative;

        background:
            linear-gradient(
                135deg,
                #ffffff 0%,
                #f1f5ff 55%,
                #edf0ff 100%
            );

        border: 1px solid #e0e7f7;

        border-radius: 24px;

        padding: 32px 38px;

        margin-bottom: 25px;

        box-shadow:
            0 10px 30px rgba(67, 92, 153, 0.08);

        overflow: hidden;
    }

    .header-card::after {
        content: "";

        position: absolute;

        width: 180px;
        height: 180px;

        right: -60px;
        top: -80px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(122, 150, 255, 0.28),
                rgba(122, 150, 255, 0)
            );
    }

    .header-card h1 {
        color: #202a44 !important;

        font-size: 1.9rem !important;

        font-weight: 700 !important;

        position: relative;

        z-index: 2;
    }

    .header-card p {
        color: #71809d !important;

        position: relative;

        z-index: 2;
    }


    /* =====================================================
       TARJETAS
       ===================================================== */

    .section-card {
        background: rgba(255,255,255,0.94);

        border: 1px solid #e1e7f4;

        border-radius: 20px;

        padding: 25px 28px;

        margin-bottom: 17px;

        box-shadow:
            0 7px 24px rgba(67, 92, 153, 0.06);
    }

    .section-card h3 {
        color: #26324f !important;
    }


    /* =====================================================
       ITEMS DE INFORMACIÓN
       ===================================================== */

    .info-item {
        display: flex;

        align-items: flex-start;

        gap: 13px;

        padding: 13px 16px;

        background:
            linear-gradient(
                135deg,
                #ffffff,
                #f6f8ff
            );

        border: 1px solid #e5eaf6;

        border-radius: 14px;

        margin-bottom: 9px;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .info-item:hover {
        transform: translateY(-1px);

        box-shadow:
            0 5px 15px rgba(72, 96, 160, 0.08);
    }


    /* =====================================================
       ETIQUETAS
       ===================================================== */

    .uso-tag {
        display: inline-block;

        background:
            linear-gradient(
                135deg,
                #f0f4ff,
                #f4f0ff
            );

        border: 1px solid #dce3f8;

        border-radius: 30px;

        padding: 7px 14px;

        font-size: 0.78rem;

        font-weight: 500;

        color: #596b9a;

        margin: 4px 3px;

        transition:
            background 0.2s ease,
            transform 0.2s ease;
    }

    .uso-tag:hover {
        background: #e9efff;

        transform: translateY(-1px);
    }


    /* =====================================================
       NUBE DE PALABRAS
       ===================================================== */

    .wc-container {
        background:
            linear-gradient(
                145deg,
                #ffffff 0%,
                #f6f8ff 100%
            );

        border: 1px solid #e0e7f5;

        border-radius: 22px;

        padding: 22px;

        box-shadow:
            0 8px 25px rgba(67, 92, 153, 0.07);

        margin-bottom: 16px;
    }


    /* =====================================================
       BARRAS DE FRECUENCIA
       ===================================================== */

    .freq-row {
        display: flex;

        align-items: center;

        gap: 14px;

        padding: 8px 14px;

        margin: 5px 0;

        background: #ffffff;

        border: 1px solid #e8ecf5;

        border-radius: 12px;

        transition:
            background 0.2s ease,
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .freq-row:hover {
        background: #f5f7ff;

        transform: translateX(2px);

        box-shadow:
            0 4px 12px rgba(67, 92, 153, 0.06);
    }

    .freq-bar {
        height: 8px;

        background:
            linear-gradient(
                90deg,
                #7195ff,
                #8b72eb
            );

        border-radius: 10px;

        display: inline-block;

        vertical-align: middle;
    }


    /* =====================================================
       RANKING
       ===================================================== */

    .rank-tag {
        background: #eef2ff;

        border: 1px solid #dce3fb;

        border-radius: 8px;

        padding: 2px 8px;

        font-size: 0.68rem;

        font-weight: 700;

        color: #6475b3;

        font-family: 'Poppins', sans-serif;

        min-width: 38px;

        text-align: center;
    }


    /* =====================================================
       EXPANDER
       ===================================================== */

    div[data-testid="stExpander"] {
        border: 1px solid #e0e7f5 !important;

        border-radius: 16px !important;

        background: #ffffff !important;

        box-shadow:
            0 5px 18px rgba(67, 92, 153, 0.05) !important;
    }

    div[data-testid="stExpander"] summary {
        color: #4d5d82 !important;

        font-weight: 600 !important;
    }


    /* =====================================================
       TABLA
       ===================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 14px !important;

        overflow: hidden !important;

        border: 1px solid #e1e7f4 !important;

        box-shadow:
            0 4px 15px rgba(67, 92, 153, 0.05) !important;
    }


    /* =====================================================
       DIVISORES
       ===================================================== */

    hr {
        border-color: #e1e7f4 !important;
    }


    /* =====================================================
       RADIO BUTTONS
       ===================================================== */

    [data-testid="stRadio"] label {
        color: #566582 !important;
    }


    /* =====================================================
       SLIDER
       ===================================================== */

    [data-testid="stSlider"] {
        padding-top: 5px;
    }


    /* =====================================================
       ALERTAS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 14px !important;

        border: 1px solid #dce5fa !important;
    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f2f5fb;
    }

    ::-webkit-scrollbar-thumb {
        background: #c2cceb;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #9daada;
    }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# STOPWORDS
# ─────────────────────────────────────────────
STOPWORDS_ES = {
    "de","la","el","en","y","a","los","del","se","las","un","por","con","no","una","su",
    "para","es","al","lo","como","mas","pero","sus","le","ya","o","este","si","porque",
    "esta","entre","cuando","muy","sin","sobre","tambien","me","hasta","hay","donde",
    "quien","desde","nos","durante","ni","contra","ese","eso","ante","bajo","tras",
    "que","fue","son","han","ha","ser","era","estan","siendo","sido","he","has","hemos",
    "habian","tiene","tienen","hacer","puede","pueden","asi","tan","parte","todo","todos",
    "todas","cada","otro","otra","otros","otras","mismo","misma","nuestro","nuestra",
    "ellos","ellas","nosotros","les","esa","esos","esas","aquel","aquella","aquellos",
}

def obtener_stopwords(idioma):
    sw = set(STOPWORDS)
    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES
    return sw


# ─────────────────────────────────────────────
# PALETAS PROFESIONALES
# ─────────────────────────────────────────────
PALETAS = {
    "Escala de grises":     ["#111827","#1f2937","#374151","#4b5563","#6b7280","#9ca3af","#d1d5db"],
    "Azul corporativo":     ["#1e3a5f","#1d4ed8","#2563eb","#3b82f6","#60a5fa","#93c5fd","#0f2942"],
    "Verde institucional":  ["#064e3b","#065f46","#047857","#059669","#10b981","#34d399","#6ee7b7"],
    "Gris azulado":         ["#0f172a","#1e293b","#334155","#475569","#64748b","#94a3b8","#cbd5e1"],
    "Terracota":            ["#7c2d12","#9a3412","#c2410c","#ea580c","#f97316","#fb923c","#fdba74"],
    "Índigo profundo":      ["#1e1b4b","#312e81","#3730a3","#4338ca","#4f46e5","#6366f1","#818cf8"],
    "Monocromático negro":  ["#000000","#111111","#222222","#444444","#666666","#888888","#aaaaaa"],
}

FORMAS = {
    "Rectángulo": None,
    "Círculo":    "circle",
}

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2
        mascara = np.ones((size, size), dtype=np.uint8) * 255
        mascara[(x - cx)**2 + (y - cy)**2 <= (size // 2 - 12)**2] = 0
        return mascara
    return None


# ─────────────────────────────────────────────
# FUNCIONES CORE
# ─────────────────────────────────────────────
def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", "", texto)
    texto = re.sub(r"[^a-záéíóúüñàâèêîôùûäëïöü\s]", " ", texto, flags=re.UNICODE)
    palabras = [p for p in texto.split() if p not in stopwords and len(p) >= min_longitud]
    return " ".join(palabras)


def contar_palabras(texto_limpio):
    return pd.DataFrame(Counter(texto_limpio.split()).most_common(50),
                        columns=["Palabra", "Frecuencia"])


def generar_wordcloud(texto_limpio, paleta_nombre, max_words, fondo, forma, ancho=1000, alto=520):
    import random
    colores = PALETAS[paleta_nombre]

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        rng = random_state or random.Random()
        return colores[rng.randint(0, len(colores) - 1)]

    mascara = crear_mascara(forma, size=min(ancho, alto))
    wc = WordCloud(
        width=ancho, height=alto, max_words=max_words,
        background_color=fondo, color_func=color_func,
        mask=mascara, collocations=False,
        min_font_size=11, max_font_size=120,
        prefer_horizontal=0.75, relative_scaling=0.5, margin=5,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(figsize=(ancho / 100, alto / 100))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    fig.patch.set_facecolor(fondo)
    plt.tight_layout(pad=0)
    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ☁️ WordCloud Studio")
    st.divider()

    # ── Fuente ──
    st.markdown("### FUENTE DE TEXTO")
    fuente = st.radio("fuente", ["✍️ Escribir / Pegar", "📂 Subir archivo"],
                      label_visibility="collapsed")
    texto_input = ""

    if fuente == "✍️ Escribir / Pegar":
        texto_input = st.text_area(
            "Texto:", height=190,
            placeholder="Pega aquí un artículo, reseña, discurso, encuesta...")

        with st.expander("Cargar texto de ejemplo"):
            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial es una disciplina de la informática orientada a desarrollar
                sistemas capaces de ejecutar tareas que requieren capacidades cognitivas humanas.
                El aprendizaje automático, las redes neuronales profundas y el procesamiento del
                lenguaje natural constituyen los pilares técnicos de los sistemas modernos de
                inteligencia artificial. Los modelos de lenguaje de gran escala, la visión
                computacional y la robótica autónoma representan aplicaciones de vanguardia.
                La inteligencia artificial transforma sectores como la salud, la educación,
                la manufactura, las finanzas y el transporte, generando eficiencias significativas.
                """,
                "Colombia": """
                Colombia es una nación situada en el extremo noroccidental de América del Sur,
                reconocida por su excepcional biodiversidad, riqueza cultural y diversidad de paisajes.
                Bogotá es la capital y principal centro económico, seguida de Medellín, Cali y
                Barranquilla como ciudades de relevancia nacional. El café colombiano goza de
                reconocimiento internacional por su calidad y perfil aromático. La floricultura
                colombiana abastece mercados globales con alta competitividad. El país alberga
                ecosistemas del Amazonas, los Andes, el Caribe y el Pacífico, constituyéndose
                como uno de los territorios con mayor biodiversidad del planeta.
                """,
                "Tecnología 4.0": """
                La cuarta revolución industrial redefine los modelos productivos mediante la
                convergencia de tecnologías digitales avanzadas. El Internet de las cosas,
                la inteligencia artificial, el análisis de grandes datos, la robótica colaborativa
                y la automatización inteligente son pilares estratégicos de la industria moderna.
                Las fábricas inteligentes integran sensores, conectividad y analítica para
                optimizar procesos en tiempo real. La manufactura aditiva, los gemelos digitales
                y la realidad aumentada transforman la ingeniería de producción. La computación
                en la nube y la ciberseguridad son habilitadores fundamentales de la
                transformación digital empresarial.
                """,
            }
            ejemplo_sel = st.selectbox("Ejemplo:", list(ejemplos.keys()),
                                       label_visibility="collapsed")
            if st.button("Cargar texto seleccionado"):
                st.session_state["texto_ejemplo"] = ejemplos[ejemplo_sel]
                st.rerun()

        if "texto_ejemplo" in st.session_state and not texto_input:
            texto_input = st.session_state["texto_ejemplo"]

    else:
        archivo = st.file_uploader("Archivo:", type=["txt", "csv"],
                                   label_visibility="collapsed")
        if archivo:
            if archivo.name.endswith(".txt"):
                texto_input = archivo.read().decode("utf-8", errors="ignore")
            elif archivo.name.endswith(".csv"):
                df_csv = pd.read_csv(archivo)
                col_txt = st.selectbox("Columna de texto:", df_csv.columns.tolist())
                texto_input = " ".join(df_csv[col_txt].dropna().astype(str).tolist())
            st.success(f"Archivo cargado — {len(texto_input):,} caracteres")

    st.divider()

    # ── Procesamiento ──
    st.markdown("### PROCESAMIENTO")
    idioma         = st.selectbox("Stopwords:", ["Español", "Inglés", "Ambos", "Ninguno"])
    min_longitud   = st.slider("Longitud mínima de palabra", 2, 8, 3)
    palabras_extra = st.text_input("Excluir palabras adicionales:",
                                   placeholder="ej: también, así, aquí")

    st.divider()

    # ── Apariencia ──
    st.markdown("### APARIENCIA")
    paleta_sel  = st.selectbox("Paleta:", list(PALETAS.keys()))
    fondo_sel   = st.radio("Fondo:", ["Blanco", "Negro"], horizontal=True)
    fondo_color = "white" if fondo_sel == "Blanco" else "black"
    forma_sel   = st.selectbox("Forma:", list(FORMAS.keys()))
    max_words   = st.slider("Máximo de palabras:", 20, 200, 80)

    st.divider()
    generar = st.button("GENERAR NUBE  ↗", use_container_width=True)


# ─────────────────────────────────────────────
# CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────

# Header
st.markdown("""
<div class="header-card">
    <h1 style="margin:0; font-size:1.9rem;">☁️ WordCloud Studio</h1>
    <p style="margin:6px 0 0 0; color:#6b7280 !important; font-size:0.97rem;">
        Análisis de frecuencia léxica y visualización de nubes de palabras
    </p>
</div>
""", unsafe_allow_html=True)

# ── Pantalla de bienvenida ──
if not generar or not texto_input.strip():
    col_izq, col_der = st.columns([3, 2], gap="large")

    with col_izq:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### Acerca de esta herramienta")
        st.markdown("""
        Una **nube de palabras** representa visualmente la frecuencia de términos en un texto:
        las palabras más frecuentes aparecen con mayor tamaño, permitiendo identificar
        los temas centrales de un corpus de manera intuitiva.
        """)

        for icono, titulo, desc in [
            ("📊", "Análisis de frecuencia", "Identifica los términos dominantes de cualquier corpus textual."),
            ("🔍", "Filtrado inteligente", "Elimina palabras vacías (*stopwords*) en español e inglés."),
            ("🎨", "Personalización visual", "Selecciona paleta, forma y densidad de la nube."),
            ("⬇️", "Exportación", "Descarga la imagen en alta resolución y la tabla de frecuencias en CSV."),
        ]:
            st.markdown(
                f'<div class="info-item">'
                f'<span style="font-size:1.3rem; flex-shrink:0;">{icono}</span>'
                f'<div><strong style="color:#111827;">{titulo}</strong>'
                f'<p style="margin:2px 0 0 0; color:#6b7280 !important; font-size:0.88rem;">{desc}</p></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Instrucciones")
        for i, paso in enumerate([
            "Ingresa o sube un texto en el panel lateral.",
            "Configura el idioma de *stopwords*, paleta y número de palabras.",
            "Haz clic en **GENERAR NUBE ↗**.",
            "Descarga la imagen PNG o la tabla CSV.",
        ], 1):
            st.markdown(f"**{i}.** {paso}")

        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown("### Aplicaciones frecuentes")
        for caso in [
            "📰 Análisis de prensa y noticias",
            "📋 Resultados de encuestas abiertas",
            "💬 Reseñas y comentarios de clientes",
            "🎓 Análisis de textos académicos",
            "🗳️ Discursos y documentos políticos",
            "📚 Estudios literarios y de corpus",
            "📊 Informes de inteligencia de negocio",
        ]:
            st.markdown(
                f'<span class="uso-tag">{caso}</span>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card" style="margin-top:16px;">', unsafe_allow_html=True)
        st.markdown("### Paletas disponibles")
        for nombre in PALETAS.keys():
            st.markdown(
                f'<div style="padding:5px 0; border-bottom:1px solid #f3f4f6;">'
                f'<span style="color:#374151; font-size:0.88rem; font-weight:500;">{nombre}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    if not texto_input.strip() and generar:
        st.warning("Ingresa un texto en el panel lateral antes de generar la nube.")
    st.stop()


# ─────────────────────────────────────────────
# PROCESAMIENTO
# ─────────────────────────────────────────────
stopwords_set = obtener_stopwords(idioma) if idioma != "Ninguno" else set()
if palabras_extra.strip():
    stopwords_set |= {p.strip().lower() for p in palabras_extra.split(",") if p.strip()}

texto_limpio = limpiar_texto(texto_input, stopwords_set, min_longitud)

if not texto_limpio.strip():
    st.error("El texto resultante está vacío. Reduce la longitud mínima o cambia la configuración de stopwords.")
    st.stop()

df_freq        = contar_palabras(texto_limpio)
total_palabras = len(texto_limpio.split())
vocabulario    = len(df_freq)

# ── Métricas ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("Palabras procesadas",     f"{total_palabras:,}")
m2.metric("Vocabulario único",       f"{vocabulario:,}")
m3.metric("Término más frecuente",   df_freq.iloc[0]["Palabra"] if not df_freq.empty else "—")
m4.metric("Frecuencia máxima",       int(df_freq.iloc[0]["Frecuencia"]) if not df_freq.empty else 0)

st.markdown("<br>", unsafe_allow_html=True)

# ── Nube ──
with st.spinner("Generando nube de palabras..."):
    fig_wc = generar_wordcloud(
        texto_limpio, paleta_sel, max_words, fondo_color,
        FORMAS[forma_sel], ancho=1000, alto=520,
    )

st.markdown('<div class="wc-container">', unsafe_allow_html=True)
st.markdown(f"**Nube de palabras** &nbsp;·&nbsp; Paleta: *{paleta_sel}* &nbsp;·&nbsp; Fondo: *{fondo_sel}* &nbsp;·&nbsp; {max_words} palabras máx.")
st.pyplot(fig_wc, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

img_bytes = fig_a_bytes(fig_wc)
st.download_button(
    "⬇️ Descargar imagen PNG",
    data=img_bytes, file_name="wordcloud.png", mime="image/png",
    use_container_width=True,
)

st.divider()

# ── Análisis ──
col_freq, col_tabla = st.columns([3, 2], gap="large")

with col_freq:
    st.markdown("### Frecuencia léxica — Top 20")
    top20    = df_freq.head(20)
    max_freq = top20["Frecuencia"].max()

    for rank, (_, row) in enumerate(top20.iterrows(), 1):
        p = row["Palabra"]
        f = int(row["Frecuencia"])
        barra_w = max(12, int((f / max_freq) * 210))
        st.markdown(
            f'<div class="freq-row">'
            f'<span class="rank-tag">#{rank:02d}</span>'
            f'<span style="font-weight:600; color:#111827; min-width:130px; font-size:0.93rem;">{p}</span>'
            f'<div class="freq-bar" style="width:{barra_w}px; opacity:{0.5 + 0.5*(f/max_freq):.2f};"></div>'
            f'<span style="font-family:\'IBM Plex Mono\',monospace; font-size:0.88rem; '
            f'color:#374151; min-width:28px; text-align:right; font-weight:500;">{f}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

with col_tabla:
    st.markdown("### Tabla de frecuencias")
    st.dataframe(
        df_freq.head(30).style
               .background_gradient(subset=["Frecuencia"], cmap="Greys")
               .format({"Frecuencia": "{:,}"}),
        use_container_width=True, height=500,
    )
    csv_bytes = df_freq.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Exportar tabla (.csv)",
        data=csv_bytes, file_name="frecuencias.csv", mime="text/csv",
        use_container_width=True,
    )

st.divider()

with st.expander("Ver texto procesado (tras eliminación de stopwords)"):
    preview = texto_limpio[:2500] + ("..." if len(texto_limpio) > 2500 else "")
    st.markdown(
        f'<p style="font-family:IBM Plex Mono,monospace; font-size:0.85rem; '
        f'color:#374151; background:#f9fafb; padding:16px; border-radius:6px; '
        f'border:1px solid #e5e7eb; line-height:1.8;">{preview}</p>',
        unsafe_allow_html=True,
    )

plt.close("all")
