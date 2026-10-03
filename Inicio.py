"""
☁️ WordCloud Studio — interfaz estilo wellness / mobile dashboard

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run wordcloud_morning_ui.py
"""

import io
import random
import re
import textwrap
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from wordcloud import STOPWORDS, WordCloud


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PALETA INSPIRADA EN LA IMAGEN DE REFERENCIA
# =========================================================

CORAL_BG = "#C86F70"
CORAL = "#FF654D"
CORAL_DARK = "#E94E3B"
PEACH = "#FFD8C9"
CREAM = "#FFF5EC"
CREAM_2 = "#FFF0E7"
LAVENDER = "#B7A3E1"
LAVENDER_LIGHT = "#D9C9F1"
ORANGE = "#FFB12B"
BLACK = "#171516"
TEXT = "#272123"
MUTED = "#756B6B"
WHITE = "#FFFFFF"


# =========================================================
# ESTILOS
# =========================================================

st.markdown(
    textwrap.dedent(f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    * {{
        box-sizing: border-box;
    }}

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    body {{
        background: {CORAL_BG};
    }}

    .stApp {{
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(255,255,255,0.10),
                transparent 28%
            ),
            linear-gradient(
                145deg,
                #D47B7C 0%,
                {CORAL_BG} 42%,
                #7E3E43 100%
            );
        color: {TEXT};
        min-height: 100vh;
    }}

    [data-testid="stAppViewContainer"] {{
        background: transparent;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stToolbar"] {{
        visibility: hidden;
    }}

    .main .block-container {{
        max-width: 1250px;
        padding: 36px 48px 70px 48px;
    }}

    /* -----------------------------------------------------
       SIDEBAR
       ----------------------------------------------------- */

    section[data-testid="stSidebar"] {{
        background: {CREAM};
        border-right: none;
    }}

    section[data-testid="stSidebar"] > div {{
        padding: 24px 18px;
    }}

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: {TEXT} !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
    }}

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {{
        color: {MUTED} !important;
    }}

    section[data-testid="stSidebar"] hr {{
        border-color: #EBDCD2 !important;
    }}

    /* -----------------------------------------------------
       TIPOGRAFÍA
       ----------------------------------------------------- */

    h1, h2, h3 {{
        font-family: 'Manrope', sans-serif !important;
        color: {TEXT} !important;
    }}

    h1 {{
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -1.5px !important;
    }}

    h2 {{
        font-weight: 800 !important;
        letter-spacing: -0.7px !important;
    }}

    p, li {{
        color: {MUTED};
        line-height: 1.6;
    }}

    /* -----------------------------------------------------
       HEADER PRINCIPAL
       ----------------------------------------------------- */

    .hero {{
        background: {CREAM};
        border-radius: 32px;
        padding: 28px 34px;
        margin-bottom: 22px;
        box-shadow: 0 20px 45px rgba(68, 27, 30, 0.16);
        position: relative;
        overflow: hidden;
    }}

    .hero::after {{
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        border-radius: 50%;
        right: -90px;
        top: -110px;
        background: rgba(255, 177, 43, 0.25);
    }}

    .eyebrow {{
        color: {CORAL};
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .hero-title {{
        color: {BLACK};
        font-family: 'Manrope', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        line-height: 1.02;
        letter-spacing: -1.7px;
        margin: 0;
    }}

    .hero-title span {{
        color: {CORAL};
    }}

    .hero-subtitle {{
        color: {MUTED};
        font-size: 1rem;
        margin-top: 10px;
        max-width: 650px;
    }}

    .status-pill {{
        display: inline-block;
        background: {ORANGE};
        color: {BLACK};
        border-radius: 999px;
        padding: 7px 13px;
        font-size: 0.75rem;
        font-weight: 800;
        margin-top: 13px;
    }}

    /* -----------------------------------------------------
       TARJETAS
       ----------------------------------------------------- */

    .card {{
        background: {CREAM};
        border-radius: 28px;
        padding: 25px;
        margin-bottom: 18px;
        box-shadow: 0 16px 35px rgba(68, 27, 30, 0.13);
        border: 1px solid rgba(255,255,255,0.35);
    }}

    .card-coral {{
        background:
            linear-gradient(
                145deg,
                #FF624A 0%,
                #F86E5B 58%,
                #E58C9C 100%
            );
        color: white;
    }}

    .card-lavender {{
        background:
            linear-gradient(
                145deg,
                {LAVENDER} 0%,
                #C5B3E9 100%
            );
        color: {BLACK};
    }}

    .card-title {{
        font-family: 'Manrope', sans-serif;
        font-size: 1.05rem;
        font-weight: 800;
        color: {BLACK};
        margin-bottom: 8px;
    }}

    .card-coral .card-title {{
        color: white;
    }}

    .card-lavender .card-title {{
        color: {BLACK};
    }}

    .card-text {{
        color: {MUTED};
        font-size: 0.9rem;
        line-height: 1.6;
    }}

    .card-coral .card-text {{
        color: rgba(255,255,255,0.88);
    }}

    /* -----------------------------------------------------
       MÉTRICAS
       ----------------------------------------------------- */

    [data-testid="metric-container"] {{
        background: {CREAM};
        border: none;
        border-radius: 22px;
        padding: 17px 19px;
        box-shadow: 0 12px 25px rgba(68, 27, 30, 0.12);
    }}

    [data-testid="metric-container"] label {{
        color: {MUTED} !important;
        font-size: 0.72rem !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }}

    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        color: {BLACK} !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 800 !important;
        font-size: 1.45rem !important;
    }}

    /* -----------------------------------------------------
       INPUTS
       ----------------------------------------------------- */

    textarea,
    input[type="text"] {{
        background: {WHITE} !important;
        color: {BLACK} !important;
        border: 2px solid transparent !important;
        border-radius: 18px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
        padding: 13px 16px !important;
    }}

    textarea:focus,
    input[type="text"]:focus {{
        border-color: {CORAL} !important;
        box-shadow: 0 0 0 3px rgba(255,101,77,0.13) !important;
    }}

    [data-baseweb="select"] > div {{
        background: {WHITE} !important;
        border: none !important;
        border-radius: 16px !important;
        color: {BLACK} !important;
    }}

    /* -----------------------------------------------------
       BOTONES — PILLS NEGROS COMO LA REFERENCIA
       ----------------------------------------------------- */

    .stButton > button {{
        background: {BLACK} !important;
        color: {WHITE} !important;
        border: none !important;
        border-radius: 999px !important;
        min-height: 48px !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.86rem !important;
        letter-spacing: 0.2px !important;
        box-shadow: none !important;
        transition: transform 0.18s ease, background 0.18s ease !important;
    }}

    .stButton > button:hover {{
        background: #000000 !important;
        transform: translateY(-2px);
    }}

    [data-testid="stDownloadButton"] button {{
        background: {BLACK} !important;
        color: {WHITE} !important;
        border: none !important;
        border-radius: 999px !important;
        min-height: 46px !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 700 !important;
    }}

    /* -----------------------------------------------------
       WORDCLOUD
       ----------------------------------------------------- */

    .wc-container {{
        background: {CREAM};
        border-radius: 30px;
        padding: 22px;
        box-shadow: 0 18px 40px rgba(68, 27, 30, 0.14);
        margin-bottom: 18px;
    }}

    .wc-heading {{
        color: {BLACK};
        font-family: 'Manrope', sans-serif;
        font-size: 1.15rem;
        font-weight: 800;
        margin-bottom: 3px;
    }}

    .wc-meta {{
        color: {MUTED};
        font-size: 0.82rem;
        margin-bottom: 14px;
    }}

    /* -----------------------------------------------------
       FRECUENCIAS
       ----------------------------------------------------- */

    .freq-row {{
        display: flex;
        align-items: center;
        gap: 11px;
        padding: 9px 13px;
        margin: 5px 0;
        background: rgba(255,245,236,0.88);
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.45);
    }}

    .freq-row:hover {{
        background: {WHITE};
    }}

    .freq-bar {{
        height: 8px;
        background: {CORAL};
        border-radius: 99px;
        display: inline-block;
    }}

    .rank-tag {{
        background: {PEACH};
        border-radius: 999px;
        padding: 3px 8px;
        font-size: 0.68rem;
        font-weight: 800;
        color: {CORAL_DARK};
        min-width: 35px;
        text-align: center;
    }}

    /* -----------------------------------------------------
       TAGS
       ----------------------------------------------------- */

    .uso-tag {{
        display: inline-block;
        background: {PEACH};
        color: {TEXT};
        border-radius: 999px;
        padding: 7px 12px;
        font-size: 0.78rem;
        font-weight: 600;
        margin: 3px;
    }}

    /* -----------------------------------------------------
       EXPANDER
       ----------------------------------------------------- */

    div[data-testid="stExpander"] {{
        border: none !important;
        border-radius: 20px !important;
        background: {CREAM} !important;
        box-shadow: 0 10px 25px rgba(68,27,30,0.10);
    }}

    /* -----------------------------------------------------
       DIVISORES
       ----------------------------------------------------- */

    hr {{
        border-color: rgba(255,255,255,0.30) !important;
    }}

    #MainMenu,
    footer {{
        visibility: hidden;
    }}

    </style>
    """),
    unsafe_allow_html=True,
)


# =========================================================
# STOPWORDS
# =========================================================

STOPWORDS_ES = {
    "de", "la", "el", "en", "y", "a", "los", "del", "se", "las", "un", "por",
    "con", "no", "una", "su", "para", "es", "al", "lo", "como", "mas", "más",
    "pero", "sus", "le", "ya", "o", "este", "si", "sí", "porque", "esta",
    "entre", "cuando", "muy", "sin", "sobre", "tambien", "también", "me",
    "hasta", "hay", "donde", "quien", "desde", "nos", "durante", "ni",
    "contra", "ese", "eso", "ante", "bajo", "tras", "que", "fue", "son",
    "han", "ha", "ser", "era", "estan", "están", "siendo", "sido", "he",
    "has", "hemos", "habian", "habían", "tiene", "tienen", "hacer", "puede",
    "pueden", "asi", "así", "tan", "parte", "todo", "todos", "todas", "cada",
    "otro", "otra", "otros", "otras", "mismo", "misma", "nuestro", "nuestra",
    "ellos", "ellas", "nosotros", "les", "esa", "esos", "esas", "aquel",
    "aquella", "aquellos",
}


def obtener_stopwords(idioma):
    sw = set()

    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES

    if idioma in ("Inglés", "Ambos"):
        sw |= set(STOPWORDS)

    return sw


# =========================================================
# PALETAS
# =========================================================

PALETAS = {
    "Coral Wellness": [
        CORAL_DARK, CORAL, "#FF806A", ORANGE,
        "#D887A5", LAVENDER, "#8F78C8"
    ],
    "Atardecer": [
        "#7E3E43", CORAL_DARK, CORAL,
        ORANGE, "#D887A5", LAVENDER, "#9D80C8"
    ],
    "Lavanda": [
        "#5E4B8B", "#7560A8", "#8F78C8",
        LAVENDER, "#C5B3E9", "#E0D3F2", "#A38BCF"
    ],
    "Coral y negro": [
        BLACK, "#33282A", CORAL_DARK, CORAL,
        "#FF806A", ORANGE, "#F4B4A5"
    ],
    "Crema cálida": [
        "#6B4B43", "#9B665B", CORAL_DARK,
        CORAL, "#D98D76", ORANGE, "#E6B6A3"
    ],
    "Escala de grises": [
        "#111111", "#242424", "#3D3D3D",
        "#575757", "#777777", "#999999", "#BBBBBB"
    ],
}

FORMAS = {
    "Rectángulo": None,
    "Círculo": "circle",
}


# =========================================================
# FUNCIONES
# =========================================================

def crear_mascara(forma, size=500):
    if forma == "circle":
        y, x = np.ogrid[:size, :size]
        cx, cy = size // 2, size // 2

        mascara = np.ones(
            (size, size),
            dtype=np.uint8
        ) * 255

        mascara[
            (x - cx) ** 2 + (y - cy) ** 2
            <= (size // 2 - 12) ** 2
        ] = 0

        return mascara

    return None


def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()

    texto = re.sub(
        r"http\S+|www\S+",
        "",
        texto
    )

    texto = re.sub(
        r"[^a-záéíóúüñàâèêîôùûäëïöü\s]",
        " ",
        texto,
        flags=re.UNICODE
    )

    palabras = [
        p
        for p in texto.split()
        if p not in stopwords
        and len(p) >= min_longitud
    ]

    return " ".join(palabras)


def contar_palabras(texto_limpio):
    if not texto_limpio.strip():
        return pd.DataFrame(
            columns=["Palabra", "Frecuencia"]
        )

    return pd.DataFrame(
        Counter(
            texto_limpio.split()
        ).most_common(50),
        columns=["Palabra", "Frecuencia"]
    )


def generar_wordcloud(
    texto_limpio,
    paleta_nombre,
    max_words,
    fondo,
    forma,
    ancho=1000,
    alto=520,
):
    colores = PALETAS[paleta_nombre]

    def color_func(
        word,
        font_size,
        position,
        orientation,
        random_state=None,
        **kwargs
    ):
        rng = random_state or random.Random()

        return colores[
            rng.randint(0, len(colores) - 1)
        ]

    mascara = crear_mascara(
        forma,
        size=min(ancho, alto)
    )

    wc = WordCloud(
        width=ancho,
        height=alto,
        max_words=max_words,
        background_color=fondo,
        color_func=color_func,
        mask=mascara,
        collocations=False,
        min_font_size=11,
        max_font_size=120,
        prefer_horizontal=0.75,
        relative_scaling=0.5,
        margin=5,
    ).generate(texto_limpio)

    fig, ax = plt.subplots(
        figsize=(ancho / 100, alto / 100)
    )

    ax.imshow(
        wc,
        interpolation="bilinear"
    )

    ax.axis("off")

    fig.patch.set_facecolor(fondo)

    plt.tight_layout(pad=0)

    return fig


def fig_a_bytes(fig):
    buf = io.BytesIO()

    fig.savefig(
        buf,
        format="png",
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )

    buf.seek(0)

    return buf.read()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        textwrap.dedent("""
        <div style="
            font-family:Manrope;
            font-size:1.45rem;
            font-weight:800;
            color:#272123;
            margin-bottom:3px;
        ">
            ☁️ WordCloud
        </div>

        <div style="
            color:#FF654D;
            font-size:0.72rem;
            font-weight:800;
            letter-spacing:1.5px;
            margin-bottom:16px;
        ">
            STUDIO
        </div>
        """),
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### FUENTE DE TEXTO")

    fuente = st.radio(
        "fuente",
        [
            "✍️ Escribir / Pegar",
            "📂 Subir archivo"
        ],
        label_visibility="collapsed"
    )

    texto_input = ""

    if fuente == "✍️ Escribir / Pegar":

        texto_input = st.text_area(
            "Texto:",
            height=170,
            placeholder=(
                "Pega aquí un artículo, reseña, "
                "discurso o encuesta..."
            )
        )

        with st.expander(
            "Cargar texto de ejemplo"
        ):

            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial es una disciplina de la informática orientada
                a desarrollar sistemas capaces de ejecutar tareas que requieren capacidades
                cognitivas humanas. El aprendizaje automático, las redes neuronales profundas
                y el procesamiento del lenguaje natural constituyen los pilares técnicos de
                los sistemas modernos de inteligencia artificial.
                """,

                "Colombia": """
                Colombia es una nación situada en el extremo noroccidental de América del Sur,
                reconocida por su excepcional biodiversidad, riqueza cultural y diversidad
                de paisajes. Bogotá es la capital y principal centro económico, seguida de
                Medellín, Cali y Barranquilla como ciudades de relevancia nacional.
                """,

                "Tecnología 4.0": """
                La cuarta revolución industrial redefine los modelos productivos mediante
                la convergencia de tecnologías digitales avanzadas. El Internet de las cosas,
                la inteligencia artificial, el análisis de grandes datos, la robótica
                colaborativa y la automatización inteligente son pilares estratégicos.
                """,
            }

            ejemplo_sel = st.selectbox(
                "Ejemplo:",
                list(ejemplos.keys()),
                label_visibility="collapsed"
            )

            if st.button(
                "Cargar ejemplo",
                use_container_width=True
            ):
                st.session_state[
                    "texto_ejemplo"
                ] = ejemplos[ejemplo_sel]

                st.rerun()

        if (
            "texto_ejemplo" in st.session_state
            and not texto_input
        ):
            texto_input = st.session_state[
                "texto_ejemplo"
            ]

    else:

        archivo = st.file_uploader(
            "Archivo:",
            type=["txt", "csv"],
            label_visibility="collapsed"
        )

        if archivo:

            if archivo.name.endswith(".txt"):

                texto_input = archivo.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            elif archivo.name.endswith(".csv"):

                df_csv = pd.read_csv(archivo)

                col_txt = st.selectbox(
                    "Columna de texto:",
                    df_csv.columns.tolist()
                )

                texto_input = " ".join(
                    df_csv[col_txt]
                    .dropna()
                    .astype(str)
                    .tolist()
                )

            st.success(
                f"Archivo cargado — "
                f"{len(texto_input):,} caracteres"
            )

    st.divider()

    st.markdown("### PROCESAMIENTO")

    idioma = st.selectbox(
        "Stopwords:",
        [
            "Español",
            "Inglés",
            "Ambos",
            "Ninguno"
        ]
    )

    min_longitud = st.slider(
        "Longitud mínima de palabra",
        2,
        8,
        3
    )

    palabras_extra = st.text_input(
        "Excluir palabras adicionales:",
        placeholder="ej: también, así, aquí"
    )

    st.divider()

    st.markdown("### APARIENCIA")

    paleta_sel = st.selectbox(
        "Paleta:",
        list(PALETAS.keys())
    )

    fondo_sel = st.radio(
        "Fondo:",
        ["Blanco", "Negro"],
        horizontal=True
    )

    fondo_color = (
        "white"
        if fondo_sel == "Blanco"
        else "black"
    )

    forma_sel = st.selectbox(
        "Forma:",
        list(FORMAS.keys())
    )

    max_words = st.slider(
        "Máximo de palabras:",
        20,
        200,
        80
    )

    st.divider()

    generar = st.button(
        "GENERAR NUBE  ↗",
        use_container_width=True
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div class="hero">

        <div class="eyebrow">
            TEXT ANALYTICS
        </div>

        <div class="hero-title">
            WordCloud<br>
            <span>Studio.</span>
        </div>

        <div class="hero-subtitle">
            Convierte cualquier texto en una visualización
            clara de sus palabras más importantes.
        </div>

        <div class="status-pill">
            ☁️ READY TO EXPLORE
        </div>

    </div>
    """),
    unsafe_allow_html=True
)


# =========================================================
# BIENVENIDA
# =========================================================

if not generar or not texto_input.strip():

    col_izq, col_der = st.columns(
        [1.45, 1],
        gap="large"
    )

    with col_izq:

        st.markdown(
            textwrap.dedent("""
            <div class="card card-coral">

                <div class="card-title">
                    ✨ Visualiza lo que importa
                </div>

                <div class="card-text">
                    Una nube de palabras representa
                    visualmente la frecuencia de los términos
                    de un texto. Las palabras más frecuentes
                    aparecen con mayor tamaño.
                </div>

            </div>
            """),
            unsafe_allow_html=True
        )

        st.markdown(
            textwrap.dedent("""
            <div class="card">

                <div class="card-title">
                    ¿Cómo funciona?
                </div>

                <div class="card-text">
                    Escribe o carga un texto, configura los
                    filtros y genera tu nube. Después puedes
                    descargar la imagen y la tabla de frecuencias.
                </div>

            </div>
            """),
            unsafe_allow_html=True
        )

        for icono, titulo, desc in [
            (
                "📊",
                "Análisis de frecuencia",
                "Identifica los términos dominantes."
            ),
            (
                "🔍",
                "Filtrado inteligente",
                "Elimina palabras vacías."
            ),
            (
                "🎨",
                "Personalización",
                "Cambia paleta, forma y densidad."
            ),
            (
                "⬇️",
                "Exportación",
                "Descarga PNG y CSV."
            ),
        ]:

            st.markdown(
                textwrap.dedent(f"""
                <div style="
                    display:flex;
                    align-items:center;
                    gap:13px;
                    padding:13px 16px;
                    margin:7px 0;
                    background:{CREAM};
                    border-radius:18px;
                    box-shadow:0 9px 20px rgba(68,27,30,0.08);
                ">

                    <div style="
                        width:40px;
                        height:40px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        background:{PEACH};
                        border-radius:14px;
                        font-size:1.15rem;
                    ">
                        {icono}
                    </div>

                    <div>
                        <div style="
                            color:{BLACK};
                            font-weight:800;
                            font-size:0.9rem;
                        ">
                            {titulo}
                        </div>

                        <div style="
                            color:{MUTED};
                            font-size:0.78rem;
                            margin-top:2px;
                        ">
                            {desc}
                        </div>
                    </div>

                </div>
                """),
                unsafe_allow_html=True
            )

    with col_der:

        st.markdown(
            textwrap.dedent("""
            <div class="card card-lavender">

                <div class="card-title">
                    🎨 Tu espacio creativo
                </div>

                <div class="card-text">
                    Usa la barra lateral para elegir
                    colores, fondo, forma y cantidad de palabras.
                </div>

                <div style="
                    margin-top:20px;
                    background:rgba(255,255,255,0.35);
                    border-radius:22px;
                    padding:24px;
                    text-align:center;
                ">

                    <div style="
                        font-size:3.5rem;
                        line-height:1;
                    ">
                        ☁️
                    </div>

                    <div style="
                        color:#272123;
                        font-family:Manrope;
                        font-size:1.1rem;
                        font-weight:800;
                        margin-top:12px;
                    ">
                        Your words, visualized.
                    </div>

                </div>

            </div>
            """),
            unsafe_allow_html=True
        )

        st.markdown(
            textwrap.dedent("""
            <div class="card">

                <div class="card-title">
                    Aplicaciones
                </div>

                <span class="uso-tag">📰 Noticias</span>
                <span class="uso-tag">💬 Reseñas</span>
                <span class="uso-tag">🎓 Academia</span>
                <span class="uso-tag">📋 Encuestas</span>
                <span class="uso-tag">📚 Literatura</span>
                <span class="uso-tag">📊 Negocios</span>

            </div>
            """),
            unsafe_allow_html=True
        )

    if not texto_input.strip() and generar:
        st.warning(
            "Ingresa un texto en el panel lateral antes de generar la nube."
        )

    st.stop()


# =========================================================
# PROCESAMIENTO
# =========================================================

stopwords_set = (
    obtener_stopwords(idioma)
    if idioma != "Ninguno"
    else set()
)

if palabras_extra.strip():

    stopwords_set |= {
        p.strip().lower()
        for p in palabras_extra.split(",")
        if p.strip()
    }

texto_limpio = limpiar_texto(
    texto_input,
    stopwords_set,
    min_longitud
)

if not texto_limpio.strip():

    st.error(
        "El texto resultante está vacío. "
        "Reduce la longitud mínima o cambia "
        "la configuración de stopwords."
    )

    st.stop()

df_freq = contar_palabras(texto_limpio)

total_palabras = len(
    texto_limpio.split()
)

vocabulario = len(df_freq)


# =========================================================
# MÉTRICAS
# =========================================================

st.markdown(
    textwrap.dedent("""
    <div style="
        color:white;
        font-family:Manrope;
        font-size:0.82rem;
        font-weight:800;
        letter-spacing:1.5px;
        margin:10px 0 12px;
        text-transform:uppercase;
    ">
        Your text overview
    </div>
    """),
    unsafe_allow_html=True
)

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Palabras procesadas",
    f"{total_palabras:,}"
)

m2.metric(
    "Vocabulario único",
    f"{vocabulario:,}"
)

m3.metric(
    "Término más frecuente",
    (
        df_freq.iloc[0]["Palabra"]
        if not df_freq.empty
        else "—"
    )
)

m4.metric(
    "Frecuencia máxima",
    (
        int(df_freq.iloc[0]["Frecuencia"])
        if not df_freq.empty
        else 0
    )
)


# =========================================================
# NUBE
# =========================================================

with st.spinner(
    "Generando nube de palabras..."
):

    fig_wc = generar_wordcloud(
        texto_limpio,
        paleta_sel,
        max_words,
        fondo_color,
        FORMAS[forma_sel],
        ancho=1000,
        alto=520,
    )

st.markdown(
    textwrap.dedent(f"""
    <div class="wc-container">

        <div class="wc-heading">
            ☁️ Nube de palabras
        </div>

        <div class="wc-meta">
            {paleta_sel} · {fondo_sel} · {max_words} palabras máximo
        </div>

    </div>
    """),
    unsafe_allow_html=True
)

st.pyplot(
    fig_wc,
    use_container_width=True
)

img_bytes = fig_a_bytes(fig_wc)

st.download_button(
    "⬇️ Descargar imagen PNG",
    data=img_bytes,
    file_name="wordcloud.png",
    mime="image/png",
    use_container_width=True,
)


# =========================================================
# ANÁLISIS
# =========================================================

st.markdown(
    "<br>",
    unsafe_allow_html=True
)

col_freq, col_tabla = st.columns(
    [3, 2],
    gap="large"
)


with col_freq:

    st.markdown(
        textwrap.dedent("""
        <div style="
            background:#FFF5EC;
            border-radius:26px;
            padding:24px;
            box-shadow:0 14px 30px rgba(68,27,30,0.10);
        ">
        """),
        unsafe_allow_html=True
    )

    st.markdown(
        "### Frecuencia léxica — Top 20"
    )

    top20 = df_freq.head(20)

    max_freq = (
        top20["Frecuencia"].max()
        if not top20.empty
        else 1
    )

    for rank, (_, row) in enumerate(
        top20.iterrows(),
        1
    ):

        p = row["Palabra"]
        f = int(row["Frecuencia"])

        barra_w = max(
            12,
            int((f / max_freq) * 210)
        )

        opacity = (
            0.5 +
            0.5 * (f / max_freq)
        )

        st.markdown(
            textwrap.dedent(f"""
            <div class="freq-row">

                <span class="rank-tag">
                    #{rank:02d}
                </span>

                <span style="
                    font-weight:700;
                    color:{BLACK};
                    min-width:130px;
                    font-size:0.88rem;
                ">
                    {p}
                </span>

                <div
                    class="freq-bar"
                    style="
                        width:{barra_w}px;
                        opacity:{opacity:.2f};
                    ">
                </div>

                <span style="
                    font-size:0.82rem;
                    color:{TEXT};
                    min-width:28px;
                    text-align:right;
                    font-weight:700;
                ">
                    {f}
                </span>

            </div>
            """),
            unsafe_allow_html=True
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


with col_tabla:

    st.markdown(
        textwrap.dedent("""
        <div style="
            background:#FFF5EC;
            border-radius:26px;
            padding:24px;
            box-shadow:0 14px 30px rgba(68,27,30,0.10);
        ">
        """),
        unsafe_allow_html=True
    )

    st.markdown(
        "### Tabla de frecuencias"
    )

    st.dataframe(
        df_freq.head(30),
        use_container_width=True,
        height=500,
        hide_index=True,
    )

    csv_bytes = df_freq.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Exportar tabla (.csv)",
        data=csv_bytes,
        file_name="frecuencias.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# TEXTO PROCESADO
# =========================================================

with st.expander(
    "☁️ Ver texto procesado"
):

    preview = (
        texto_limpio[:2500]
        + (
            "..."
            if len(texto_limpio) > 2500
            else ""
        )
    )

    st.write(preview)


plt.close("all")
