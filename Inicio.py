import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import reimport streamlit as st
import matplotlib.pyplotimport streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import io
from collections import Counter
from wordcloud import WordCloud, STOPWORDS


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ESTILOS - INTERFAZ INSPIRADA EN LA IMAGEN
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

:root {
    --bg: #f3dfe0;
    --panel: #571d25;
    --panel-dark: #3d1118;
    --card: #6a242d;
    --card-light: #7b2d35;
    --accent: #f3c65d;
    --accent-soft: #e7a7a7;
    --blue: #b7d9e8;
    --text: #fff8f5;
    --muted: #d7bfc1;
    --line: rgba(255,255,255,0.10);
}

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: var(--bg);
}

.main .block-container {
    max-width: 1400px;
    padding: 28px 34px 50px 34px;
}

/* Ocultar elementos innecesarios de Streamlit */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header[data-testid="stHeader"] {
    background: transparent;
}

/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #321017 !important;
    border-right: none !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding: 25px 18px 30px 18px;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #fff7f4 !important;
    font-weight: 800 !important;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #e4cacc !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.10) !important;
}

/* =========================================================
   TITULOS
   ========================================================= */

h1, h2, h3, h4 {
    color: #fff8f5 !important;
}

p, li {
    color: #d9c3c5 !important;
}

/* =========================================================
   HERO
   ========================================================= */

.hero {
    background:
        radial-gradient(circle at 75% 20%, rgba(243,198,93,0.14), transparent 28%),
        linear-gradient(135deg, #68232c 0%, #4b151e 100%);
    border-radius: 28px;
    padding: 38px 42px;
    margin-bottom: 22px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 16px 40px rgba(61,17,24,0.18);
    position: relative;
    overflow: hidden;
}

.hero:after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    right: -70px;
    top: -80px;
    border-radius: 50%;
    background: rgba(243,198,93,0.08);
}

.eyebrow {
    color: #f3c65d;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 12px;
}

.hero-title {
    color: #fff8f5;
    font-size: 54px;
    font-weight: 900;
    line-height: 1.05;
    letter-spacing: -2px;
    margin-bottom: 14px;
    position: relative;
    z-index: 2;
}

.hero-title span {
    color: #f3c65d;
}

.hero-text {
    color: #d9c3c5;
    font-size: 16px;
    line-height: 1.65;
    max-width: 650px;
    position: relative;
    z-index: 2;
}

/* =========================================================
   CARDS
   ========================================================= */

.section-card,
.wc-container {
    background: #5c2028;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 12px 28px rgba(61,17,24,0.14);
}

.section-card h3,
.section-card h4 {
    color: #fff8f5 !important;
}

.info-item {
    padding: 13px 15px;
    margin-bottom: 9px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 13px;
}

.uso-tag {
    display: inline-block;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.08);
    color: #f6e8e5 !important;
    border-radius: 18px;
    padding: 7px 12px;
    font-size: 0.82rem;
    margin: 4px 3px;
}

/* =========================================================
   INPUTS
   ========================================================= */

textarea,
input[type="text"] {
    background: #4a171f !important;
    color: #fff8f5 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}

textarea::placeholder,
input::placeholder {
    color: #bfa6a9 !important;
}

textarea:focus,
input[type="text"]:focus {
    border-color: #f3c65d !important;
    box-shadow: 0 0 0 2px rgba(243,198,93,0.15) !important;
}

/* Selectbox */

[data-baseweb="select"] > div {
    background: #4a171f !important;
    color: #fff8f5 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}

[data-baseweb="select"] span {
    color: #fff8f5 !important;
}

/* Radio / checkbox */

[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label {
    color: #e6cfd1 !important;
}

/* Slider */

[data-testid="stSlider"] {
    color: #f3c65d !important;
}

/* =========================================================
   BOTONES
   ========================================================= */

.stButton > button {
    background: #f3c65d !important;
    color: #45151b !important;
    border: none !important;
    border-radius: 13px !important;
    min-height: 45px !important;
    font-weight: 800 !important;
    letter-spacing: 0.2px !important;
    box-shadow: 0 8px 18px rgba(243,198,93,0.18) !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    background: #ffe08a !important;
    color: #351016 !important;
    transform: translateY(-1px);
}

[data-testid="stDownloadButton"] button {
    background: #7b2d35 !important;
    color: #fff8f5 !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: #8e3540 !important;
}

/* =========================================================
   MÉTRICAS
   ========================================================= */

[data-testid="metric-container"] {
    background: #5c2028 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 18px !important;
    padding: 17px !important;
    box-shadow: 0 10px 24px rgba(61,17,24,0.12);
}

[data-testid="metric-container"] label {
    color: #cbaeb1 !important;
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.7px !important;
}

[data-testid="stMetricValue"] {
    color: #fff8f5 !important;
    font-weight: 800 !important;
}

/* =========================================================
   FRECUENCIAS
   ========================================================= */

.freq-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 9px 12px;
    margin: 5px 0;
    background: #4e1921;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 11px;
}

.freq-row:hover {
    background: #64222b;
}

.freq-bar {
    height: 8px;
    background: #f3c65d;
    border-radius: 10px;
    display: inline-block;
}

.rank-tag {
    background: rgba(243,198,93,0.13);
    border: 1px solid rgba(243,198,93,0.20);
    color: #f3c65d !important;
    border-radius: 7px;
    padding: 3px 7px;
    font-size: 11px;
    font-weight: 800;
    min-width: 35px;
    text-align: center;
}

/* =========================================================
   DATAFRAME
   ========================================================= */

[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden;
}

/* =========================================================
   EXPANDER
   ========================================================= */

div[data-testid="stExpander"] {
    background: #5c2028 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
}

div[data-testid="stExpander"] summary {
    color: #fff8f5 !important;
}

/* =========================================================
   ALERTAS
   ========================================================= */

[data-testid="stAlert"] {
    border-radius: 13px !important;
}

/* =========================================================
   FILE UPLOADER
   ========================================================= */

[data-testid="stFileUploader"] {
    background: #4a171f !important;
    border-radius: 12px !important;
    border: 1px dashed rgba(255,255,255,0.15) !important;
}

/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    .main .block-container {
        padding: 20px 16px 40px 16px;
    }

    .hero {
        padding: 28px;
        border-radius: 20px;
    }

    .hero-title {
        font-size: 40px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# STOPWORDS
# =========================================================

STOPWORDS_ES = {
    "de", "la", "el", "en", "y", "a", "los", "del", "se",
    "las", "un", "por", "con", "no", "una", "su", "para",
    "es", "al", "lo", "como", "mas", "pero", "sus", "le",
    "ya", "o", "este", "si", "porque", "esta", "entre",
    "cuando", "muy", "sin", "sobre", "tambien", "me",
    "hasta", "hay", "donde", "quien", "desde", "nos",
    "durante", "ni", "contra", "ese", "eso", "ante",
    "bajo", "tras", "que", "fue", "son", "han", "ha",
    "ser", "era", "estan", "siendo", "sido", "he", "has",
    "hemos", "habian", "tiene", "tienen", "hacer",
    "puede", "pueden", "asi", "tan", "parte", "todo",
    "todos", "todas", "cada", "otro", "otra", "otros",
    "otras", "mismo", "misma", "nuestro", "nuestra",
    "ellos", "ellas", "nosotros", "les", "esa", "esos",
    "esas", "aquel", "aquella", "aquellos"
}


def obtener_stopwords(idioma):
    sw = set(STOPWORDS)

    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES

    return sw


# =========================================================
# PALETAS
# =========================================================

PALETAS = {
    "Dorado": [
        "#f3c65d",
        "#ffe08a",
        "#e8b84f",
        "#f7d77c",
        "#dca83d"
    ],

    "Coral": [
        "#ff7b72",
        "#ff9189",
        "#e96058",
        "#d94f4a",
        "#ffaaa3"
    ],

    "Azul": [
        "#75b9d4",
        "#8dcae0",
        "#5ca2c2",
        "#4a8eae",
        "#b0ddeb"
    ],

    "Verde": [
        "#68b58d",
        "#7bc89d",
        "#4f9d78",
        "#8dd2aa",
        "#3e8061"
    ],

    "Grises": [
        "#f4eeee",
        "#d8cacc",
        "#bcaeb1",
        "#9e9094",
        "#7d6e72"
    ]
}


FORMAS = {
    "Rectángulo": None,
    "Círculo": "circle"
}


# =========================================================
# MÁSCARA
# =========================================================

def crear_mascara(forma, size=500):

    if forma == "circle":

        y, x = np.ogrid[:size, :size]

        cx = size // 2
        cy = size // 2

        mascara = np.ones(
            (size, size),
            dtype=np.uint8
        ) * 255

        mascara[
            (x - cx) ** 2 +
            (y - cy) ** 2
            <= (size // 2 - 12) ** 2
        ] = 0

        return mascara

    return None


# =========================================================
# LIMPIAR TEXTO
# =========================================================

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
        palabra
        for palabra in texto.split()
        if palabra not in stopwords
        and len(palabra) >= min_longitud
    ]

    return " ".join(palabras)


# =========================================================
# CONTAR PALABRAS
# =========================================================

def contar_palabras(texto):

    datos = Counter(
        texto.split()
    ).most_common(50)

    return pd.DataFrame(
        datos,
        columns=["Palabra", "Frecuencia"]
    )


# =========================================================
# GENERAR WORDCLOUD
# =========================================================

def generar_wordcloud(
    texto,
    paleta,
    max_words,
    fondo,
    forma
):

    import random

    colores = PALETAS[paleta]

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
            rng.randint(
                0,
                len(colores) - 1
            )
        ]

    mascara = crear_mascara(
        forma,
        500
    )

    wc = WordCloud(
        width=1000,
        height=520,
        max_words=max_words,
        background_color=fondo,
        color_func=color_func,
        mask=mascara,
        collocations=False,
        min_font_size=11,
        max_font_size=120,
        prefer_horizontal=0.75,
        relative_scaling=0.5,
        margin=5
    ).generate(texto)

    fig, ax = plt.subplots(
        figsize=(10, 5.2)
    )

    ax.imshow(
        wc,
        interpolation="bilinear"
    )

    ax.axis("off")

    fig.patch.set_facecolor(
        fondo
    )

    plt.tight_layout(
        pad=0
    )

    return fig


# =========================================================
# CONVERTIR FIGURA A PNG
# =========================================================

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
        "## ☁️ WordCloud"
    )

    st.markdown(
        "<p style='color:#f3c65d !important; font-weight:700; margin-top:-12px;'>STUDIO</p>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        "### FUENTE DE TEXTO"
    )

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
            "Texto",
            height=170,
            placeholder="Escribe o pega aquí tu texto..."
        )

        with st.expander("Cargar texto de ejemplo"):

            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial es una disciplina de la informática
                orientada a desarrollar sistemas capaces de ejecutar tareas
                que requieren capacidades cognitivas humanas. El aprendizaje
                automático, las redes neuronales y el procesamiento del lenguaje
                natural son tecnologías importantes de la inteligencia artificial.
                """,

                "Colombia": """
                Colombia es un país de América del Sur reconocido por su
                biodiversidad, riqueza cultural y diversidad de paisajes.
                Bogotá es la capital y Medellín es una de las ciudades más
                importantes del país. Colombia posee regiones naturales como
                los Andes, el Caribe, el Pacífico y la Amazonía.
                """,

                "Tecnología": """
                La tecnología transforma la manera en que las personas trabajan,
                estudian y se comunican. La inteligencia artificial, el Internet
                de las cosas, la robótica, la automatización y el análisis de
                datos son herramientas fundamentales para la transformación digital.
                """
            }

            ejemplo_sel = st.selectbox(
                "Ejemplo",
                list(ejemplos.keys())
            )

            if st.button(
                "Cargar ejemplo",
                use_container_width=True
            ):
                st.session_state["texto_ejemplo"] = ejemplos[
                    ejemplo_sel
                ]
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
            "Archivo",
            type=["txt", "csv"]
        )

        if archivo:

            if archivo.name.endswith(".txt"):

                texto_input = archivo.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            elif archivo.name.endswith(".csv"):

                df_csv = pd.read_csv(
                    archivo
                )

                columna = st.selectbox(
                    "Columna de texto",
                    df_csv.columns.tolist()
                )

                texto_input = " ".join(
                    df_csv[columna]
                    .dropna()
                    .astype(str)
                    .tolist()
                )

    st.divider()

    st.markdown(
        "### PROCESAMIENTO"
    )

    idioma = st.selectbox(
        "Stopwords",
        [
            "Español",
            "Inglés",
            "Ambos",
            "Ninguno"
        ]
    )

    min_longitud = st.slider(
        "Longitud mínima",
        2,
        8,
        3
    )

    palabras_extra = st.text_input(
        "Excluir palabras",
        placeholder="ej: también, aquí"
    )

    st.divider()

    st.markdown(
        "### APARIENCIA"
    )

    paleta_sel = st.selectbox(
        "Paleta",
        list(PALETAS.keys())
    )

    fondo_sel = st.radio(
        "Fondo",
        [
            "Blanco",
            "Negro"
        ],
        horizontal=True
    )

    fondo_color = (
        "white"
        if fondo_sel == "Blanco"
        else "black"
    )

    forma_sel = st.selectbox(
        "Forma",
        list(FORMAS.keys())
    )

    max_words = st.slider(
        "Máximo de palabras",
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
# HERO PRINCIPAL
# =========================================================

st.markdown("""
<div class="hero">

    <div class="eyebrow">
        TEXT ANALYTICS
    </div>

    <div class="hero-title">
        WordCloud <span>Studio.</span>
    </div>

    <div class="hero-text">
        Convierte cualquier texto en una nube de palabras
        clara, visual y fácil de analizar. Las palabras más
        frecuentes aparecerán con mayor tamaño.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# PANTALLA DE INICIO
# =========================================================

if not generar:

    col1, col2 = st.columns(
        [3, 2],
        gap="large"
    )

    with col1:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ¿Cómo funciona?"
        )

        st.markdown(
            """
            Una nube de palabras permite identificar rápidamente
            cuáles son los términos más utilizados dentro de un texto.
            """
        )

        pasos = [
            ("01", "Ingresa un texto", "Escribe, pega o sube un archivo."),
            ("02", "Configura el análisis", "Selecciona stopwords, colores y forma."),
            ("03", "Genera la nube", "Presiona el botón de generación."),
            ("04", "Descarga", "Obtén la imagen PNG y los datos CSV.")
        ]

        for numero, titulo, descripcion in pasos:

            st.markdown(
                f"""
                <div class="info-item">
                    <div>
                        <span style="
                            color:#f3c65d;
                            font-weight:900;
                            font-size:12px;
                        ">
                            {numero}
                        </span>
                    </div>

                    <div>
                        <strong style="color:#fff8f5;">
                            {titulo}
                        </strong>

                        <p style="
                            margin:3px 0 0 0;
                            color:#d0b9bc !important;
                            font-size:13px;
                        ">
                            {descripcion}
                        </p>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### Características"
        )

        caracteristicas = [
            "📊 Análisis de frecuencia",
            "🔍 Eliminación de stopwords",
            "🎨 Paletas personalizadas",
            "⭕ Forma circular o rectangular",
            "⬇️ Exportación PNG",
            "📄 Exportación CSV"
        ]

        for item in caracteristicas:

            st.markdown(
                f"""
                <div class="uso-tag">
                    {item}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.stop()


# =========================================================
# VALIDAR TEXTO
# =========================================================

if not texto_input.strip():

    st.warning(
        "Escribe o sube un texto antes de generar la nube."
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
        palabra.strip().lower()
        for palabra in palabras_extra.split(",")
        if palabra.strip()
    }


texto_limpio = limpiar_texto(
    texto_input,
    stopwords_set,
    min_longitud
)


if not texto_limpio.strip():

    st.error(
        "El texto quedó vacío. Reduce la longitud mínima "
        "o cambia las stopwords."
    )

    st.stop()


df_freq = contar_palabras(
    texto_limpio
)


if df_freq.empty:

    st.error(
        "No se encontraron palabras válidas para generar la nube."
    )

    st.stop()


total_palabras = len(
    texto_limpio.split()
)

vocabulario = len(
    df_freq
)


# =========================================================
# MÉTRICAS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Palabras",
    f"{total_palabras:,}"
)

m2.metric(
    "Palabras únicas",
    f"{vocabulario:,}"
)

m3.metric(
    "Más frecuente",
    df_freq.iloc[0]["Palabra"]
)

m4.metric(
    "Frecuencia",
    int(
        df_freq.iloc[0]["Frecuencia"]
    )
)


st.markdown(
    "<br>",
    unsafe_allow_html=True
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
        FORMAS[forma_sel]
    )


st.markdown(
    '<div class="wc-container">',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        color:#fff8f5;
        font-size:18px;
        font-weight:800;
        margin-bottom:14px;
    ">
        Nube de palabras
        <span style="
            color:#c9aaad;
            font-size:13px;
            font-weight:500;
        ">
            · {paleta_sel} · {fondo_sel}
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

st.pyplot(
    fig_wc,
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# DESCARGA PNG
# =========================================================

img_bytes = fig_a_bytes(
    fig_wc
)

st.download_button(
    "⬇️ Descargar imagen PNG",
    data=img_bytes,
    file_name="wordcloud.png",
    mime="image/png",
    use_container_width=True
)


# =========================================================
# FRECUENCIAS
# =========================================================

st.divider()

col_freq, col_tabla = st.columns(
    [3, 2],
    gap="large"
)


with col_freq:

    st.markdown(
        "### Frecuencia de palabras"
    )

    top20 = df_freq.head(20)

    max_freq = top20[
        "Frecuencia"
    ].max()

    for rank, (_, row) in enumerate(
        top20.iterrows(),
        1
    ):

        palabra = row["Palabra"]

        frecuencia = int(
            row["Frecuencia"]
        )

        ancho = max(
            20,
            int(
                frecuencia
                / max_freq
                * 230
            )
        )

        st.markdown(
            f"""
            <div class="freq-row">

                <span class="rank-tag">
                    #{rank:02d}
                </span>

                <span style="
                    min-width:130px;
                    font-weight:600;
                    color:#fff8f5;
                ">
                    {palabra}
                </span>

                <div
                    class="freq-bar"
                    style="width:{ancho}px;"
                ></div>

                <span style="
                    color:#d8c5c7;
                    font-weight:700;
                    margin-left:auto;
                ">
                    {frecuencia}
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )


with col_tabla:

    st.markdown(
        "### Tabla"
    )

    st.dataframe(
        df_freq.head(30),
        use_container_width=True,
        height=500
    )

    csv_bytes = (
        df_freq
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "⬇️ Descargar CSV",
        data=csv_bytes,
        file_name="frecuencias.csv",
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# TEXTO PROCESADO
# =========================================================

with st.expander(
    "Ver texto procesado"
):

    st.markdown(
        f"""
        <div style="
            background:#43151d;
            color:#d9c3c5;
            padding:16px;
            border-radius:12px;
            border:1px solid rgba(255,255,255,0.08);
            line-height:1.8;
        ">
            {texto_limpio[:2500]}
        </div>
        """,
        unsafe_allow_html=True
    )


plt.close("all")
 as plt
import pandas as pd
import numpy as np
import re
import io

from collections import Counter
from wordcloud import WordCloud, STOPWORDS


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #f8dfe0;
    --wine: #571b22;
    --wine-dark: #421419;
    --wine-light: #69232b;
    --card: #68232b;
    --card-dark: #48171d;
    --coral: #d9585d;
    --coral-light: #e86c6b;
    --cream: #fff5e9;
    --white: #ffffff;
    --muted: #cfa8a8;
    --yellow: #f5d36b;
}


/* =========================================================
   GENERAL
   ========================================================= */

html,
body,
[class*="css"] {
    font-family: 'Poppins', sans-serif !important;
}

.stApp {
    background-color: var(--bg) !important;
}


/* =========================================================
   CONTENEDOR PRINCIPAL
   ========================================================= */

.main .block-container {
    max-width: 1250px !important;

    background: var(--wine);

    border-radius: 30px;

    padding: 28px 38px 50px 38px;

    margin-top: 22px;
    margin-bottom: 30px;

    box-shadow:
        0 25px 60px rgba(72, 20, 25, 0.25);
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background-color: #421419 !important;
}

[data-testid="stSidebar"] > div {
    background-color: #421419 !important;
}

[data-testid="stSidebar"] * {
    font-family: 'Poppins', sans-serif !important;
}

[data-testid="stSidebar"] h2 {
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] h3 {
    color: #f3b6b5 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
}

[data-testid="stSidebar"] label {
    color: #d8b7b7 !important;
    font-size: 12px !important;
}

[data-testid="stSidebar"] p {
    color: #d8b7b7 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.10) !important;
}


/* =========================================================
   TOP BAR
   ========================================================= */

.dashboard-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 22px;
}

.greeting {
    color: #e9c6c6;
    font-size: 13px;
    font-weight: 500;
}

.greeting strong {
    color: #ffffff;
    font-weight: 700;
}

.brand-mini {
    color: #ffffff;
    font-size: 18px;
    font-weight: 800;
}


/* =========================================================
   HERO
   ========================================================= */

.hero-dashboard {

    position: relative;

    min-height: 205px;

    padding: 28px 32px;

    border-radius: 23px;

    background:
        linear-gradient(
            120deg,
            #d85b61 0%,
            #b8444d 48%,
            #742832 100%
        );

    overflow: hidden;

    margin-bottom: 28px;

    box-shadow:
        0 15px 35px rgba(30, 5, 8, 0.20);
}


.hero-dashboard::after {

    content: "";

    position: absolute;

    width: 250px;
    height: 250px;

    right: -70px;
    top: -80px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(255,255,255,0.16),
            rgba(255,255,255,0)
        );
}


.hero-eyebrow {

    color: #ffe8d8;

    font-size: 10px;

    font-weight: 700;

    letter-spacing: 2px;

    text-transform: uppercase;

    margin-bottom: 7px;
}


.hero-title {

    color: #ffffff;

    font-size: 38px;

    line-height: 1.05;

    font-weight: 800;

    margin: 0 0 10px 0;

    letter-spacing: -1px;
}


.hero-title span {
    color: var(--yellow);
}


.hero-description {

    color: #ffe5e1;

    font-size: 12px;

    line-height: 1.65;

    max-width: 430px;

    margin-bottom: 18px;
}


.hero-badge {

    display: inline-block;

    background: #fff7e9;

    color: #652027;

    border-radius: 30px;

    padding: 7px 14px;

    font-size: 10px;

    font-weight: 700;
}


/* =========================================================
   TÍTULOS
   ========================================================= */

.dashboard-section-title {

    display: flex;

    align-items: center;

    justify-content: space-between;

    margin: 22px 0 12px 0;
}

.dashboard-section-title h3 {

    color: #ffffff !important;

    font-size: 16px !important;

    font-weight: 700 !important;

    margin: 0 !important;
}

.dashboard-section-title span {

    color: #b98b8d;

    font-size: 10px;
}


/* =========================================================
   TARJETAS
   ========================================================= */

.section-card {

    background: var(--card);

    border: 1px solid rgba(255,255,255,0.04);

    border-radius: 19px;

    padding: 22px;

    margin-bottom: 16px;

    box-shadow:
        0 10px 25px rgba(30,5,8,0.12);
}

.section-card h3,
.section-card h4 {
    color: #ffffff !important;
}


/* =========================================================
   ITEMS
   ========================================================= */

.info-item {

    display: flex;

    align-items: center;

    gap: 12px;

    padding: 12px;

    margin-bottom: 8px;

    background: rgba(255,255,255,0.055);

    border-radius: 12px;

    border: 1px solid rgba(255,255,255,0.04);
}

.info-item strong {

    color: #ffffff !important;

    font-size: 12px;
}

.info-item p {

    color: #cdaaaa !important;

    font-size: 10px !important;

    line-height: 1.4 !important;

    margin: 2px 0 0 0 !important;
}


/* =========================================================
   TAGS
   ========================================================= */

.uso-tag {

    display: inline-block;

    background: #7b3038;

    color: #ffe9e5;

    border-radius: 20px;

    padding: 6px 12px;

    font-size: 10px;

    font-weight: 600;

    margin: 4px 3px;

    border: 1px solid rgba(255,255,255,0.05);
}


/* =========================================================
   MÉTRICAS
   ========================================================= */

[data-testid="metric-container"] {

    background: var(--card);

    border: none !important;

    border-radius: 17px;

    padding: 17px 18px;

    box-shadow:
        0 8px 20px rgba(30,5,8,0.13);
}

[data-testid="metric-container"] label {

    color: #c59b9d !important;

    font-size: 9px !important;

    font-weight: 600 !important;

    text-transform: uppercase;

    letter-spacing: 0.8px;
}

[data-testid="stMetricValue"] {

    color: #ffffff !important;

    font-size: 22px !important;

    font-weight: 700 !important;
}


/* =========================================================
   INPUTS
   ========================================================= */

textarea,
input[type="text"] {

    background: #4a181e !important;

    color: #ffffff !important;

    border: 1px solid #7c3037 !important;

    border-radius: 11px !important;

    font-family: 'Poppins', sans-serif !important;

    font-size: 11px !important;
}

textarea::placeholder,
input::placeholder {

    color: #a8797c !important;
}

textarea:focus,
input[type="text"]:focus {

    border-color: #e36a6d !important;

    box-shadow:
        0 0 0 2px rgba(227,106,109,0.15) !important;
}


/* =========================================================
   SELECT
   ========================================================= */

[data-baseweb="select"] > div {

    background: #4a181e !important;

    border: 1px solid #7c3037 !important;

    border-radius: 11px !important;

    color: #ffffff !important;
}

[data-baseweb="select"] * {
    color: #ffffff !important;
}


/* =========================================================
   RADIO
   ========================================================= */

[data-testid="stRadio"] label {
    color: #d9b6b6 !important;
}


/* =========================================================
   BOTÓN PRINCIPAL
   ========================================================= */

.stButton > button {

    background:
        linear-gradient(
            135deg,
            #e66b6c,
            #c94b55
        ) !important;

    color: #ffffff !important;

    border: none !important;

    border-radius: 12px !important;

    font-family: 'Poppins', sans-serif !important;

    font-weight: 700 !important;

    font-size: 11px !important;

    min-height: 44px !important;

    box-shadow:
        0 8px 18px rgba(185,65,75,0.25);

    transition: all 0.2s ease !important;
}

.stButton > button:hover {

    background:
        linear-gradient(
            135deg,
            #f07878,
            #d6555d
        ) !important;

    transform: translateY(-1px);

    box-shadow:
        0 10px 24px rgba(185,65,75,0.35);
}


/* =========================================================
   BOTONES DESCARGA
   ========================================================= */

[data-testid="stDownloadButton"] button {

    background: #7a3038 !important;

    color: #ffffff !important;

    border: 1px solid rgba(255,255,255,0.08) !important;

    border-radius: 11px !important;

    font-family: 'Poppins', sans-serif !important;

    font-size: 11px !important;

    font-weight: 600 !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: #914049 !important;
}


/* =========================================================
   WORDCLOUD
   ========================================================= */

.wc-container {

    background: #48171d;

    border: none;

    border-radius: 20px;

    padding: 18px;

    margin-bottom: 18px;

    box-shadow:
        0 10px 28px rgba(30,5,8,0.15);
}


/* =========================================================
   FRECUENCIA
   ========================================================= */

.freq-row {

    display: flex;

    align-items: center;

    gap: 10px;

    padding: 9px 12px;

    margin: 5px 0;

    background: #68232b;

    border: none;

    border-radius: 10px;
}

.freq-bar {

    height: 7px;

    background:
        linear-gradient(
            90deg,
            #d9585d,
            #f09a91
        );

    border-radius: 20px;
}

.rank-tag {

    background: #48171d;

    color: #dcb7b7;

    border-radius: 6px;

    padding: 3px 7px;

    font-size: 9px;

    font-weight: 700;

    min-width: 34px;

    text-align: center;
}


/* =========================================================
   TABLA
   ========================================================= */

[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}


/* =========================================================
   EXPANDER
   ========================================================= */

div[data-testid="stExpander"] {

    background: #68232b !important;

    border: 1px solid #793038 !important;

    border-radius: 13px !important;
}

div[data-testid="stExpander"] summary {
    color: #ffffff !important;
}


/* =========================================================
   TEXTOS
   ========================================================= */

h1,
h2,
h3,
h4 {
    color: #ffffff !important;
    font-family: 'Poppins', sans-serif !important;
}

p,
li {
    color: #d5b0b0 !important;
    font-family: 'Poppins', sans-serif !important;
}


/* =========================================================
   DIVISORES
   ========================================================= */

hr {
    border-color: rgba(255,255,255,0.08) !important;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 900px) {

    .main .block-container {

        margin: 10px;

        padding: 22px;

        border-radius: 22px;
    }

    .hero-title {
        font-size: 32px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# STOPWORDS
# =========================================================

STOPWORDS_ES = {
    "de", "la", "el", "en", "y", "a", "los", "del", "se",
    "las", "un", "por", "con", "no", "una", "su", "para",
    "es", "al", "lo", "como", "mas", "pero", "sus", "le",
    "ya", "o", "este", "si", "porque", "esta", "entre",
    "cuando", "muy", "sin", "sobre", "tambien", "me",
    "hasta", "hay", "donde", "quien", "desde", "nos",
    "durante", "ni", "contra", "ese", "eso", "ante",
    "bajo", "tras", "que", "fue", "son", "han", "ha",
    "ser", "era", "estan", "siendo", "sido", "he", "has",
    "hemos", "habian", "tiene", "tienen", "hacer",
    "puede", "pueden", "asi", "tan", "parte", "todo",
    "todos", "todas", "cada", "otro", "otra", "otros",
    "otras", "mismo", "misma", "nuestro", "nuestra",
    "ellos", "ellas", "nosotros", "les", "esa", "esos",
    "esas", "aquel", "aquella", "aquellos"
}


def obtener_stopwords(idioma):

    sw = set(STOPWORDS)

    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES

    return sw


# =========================================================
# PALETAS
# =========================================================

PALETAS = {

    "Escala de grises": [
        "#111827",
        "#1f2937",
        "#374151",
        "#4b5563",
        "#6b7280",
        "#9ca3af",
        "#d1d5db"
    ],

    "Azul corporativo": [
        "#1e3a5f",
        "#1d4ed8",
        "#2563eb",
        "#3b82f6",
        "#60a5fa",
        "#93c5fd",
        "#0f2942"
    ],

    "Verde institucional": [
        "#064e3b",
        "#065f46",
        "#047857",
        "#059669",
        "#10b981",
        "#34d399",
        "#6ee7b7"
    ],

    "Gris azulado": [
        "#0f172a",
        "#1e293b",
        "#334155",
        "#475569",
        "#64748b",
        "#94a3b8",
        "#cbd5e1"
    ],

    "Terracota": [
        "#7c2d12",
        "#9a3412",
        "#c2410c",
        "#ea580c",
        "#f97316",
        "#fb923c",
        "#fdba74"
    ],

    "Índigo profundo": [
        "#1e1b4b",
        "#312e81",
        "#3730a3",
        "#4338ca",
        "#4f46e5",
        "#6366f1",
        "#818cf8"
    ],

    "Monocromático negro": [
        "#000000",
        "#111111",
        "#222222",
        "#444444",
        "#666666",
        "#888888",
        "#aaaaaa"
    ]
}


FORMAS = {
    "Rectángulo": None,
    "Círculo": "circle"
}


# =========================================================
# MÁSCARA
# =========================================================

def crear_mascara(forma, size=500):

    if forma == "circle":

        y, x = np.ogrid[:size, :size]

        cx = size // 2
        cy = size // 2

        mascara = np.ones(
            (size, size),
            dtype=np.uint8
        ) * 255

        mascara[
            (x - cx) ** 2 +
            (y - cy) ** 2
            <= (size // 2 - 12) ** 2
        ] = 0

        return mascara

    return None


# =========================================================
# LIMPIAR TEXTO
# =========================================================

def limpiar_texto(
    texto,
    stopwords,
    min_longitud
):

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
        palabra
        for palabra in texto.split()
        if palabra not in stopwords
        and len(palabra) >= min_longitud
    ]

    return " ".join(palabras)


# =========================================================
# CONTAR PALABRAS
# =========================================================

def contar_palabras(texto_limpio):

    datos = Counter(
        texto_limpio.split()
    ).most_common(50)

    return pd.DataFrame(
        datos,
        columns=[
            "Palabra",
            "Frecuencia"
        ]
    )


# =========================================================
# GENERAR WORDCLOUD
# =========================================================

def generar_wordcloud(
    texto_limpio,
    paleta_nombre,
    max_words,
    fondo,
    forma,
    ancho=1000,
    alto=520
):

    import random

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
            rng.randint(
                0,
                len(colores) - 1
            )
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
        margin=5
    ).generate(texto_limpio)

    fig, ax = plt.subplots(
        figsize=(
            ancho / 100,
            alto / 100
        )
    )

    ax.imshow(
        wc,
        interpolation="bilinear"
    )

    ax.axis("off")

    fig.patch.set_facecolor(fondo)

    plt.tight_layout(
        pad=0
    )

    return fig


# =========================================================
# CONVERTIR FIGURA A PNG
# =========================================================

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

    st.markdown("""
    <div style="
        color:#ffffff;
        font-size:19px;
        font-weight:800;
        margin-bottom:20px;
    ">
        ☁️ WordCloud
    </div>
    """, unsafe_allow_html=True)

    st.divider()


    # =====================================================
    # FUENTE
    # =====================================================

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
            height=190,
            placeholder="Pega aquí un artículo, reseña, discurso..."
        )


        with st.expander(
            "Cargar texto de ejemplo"
        ):

            ejemplos = {

                "Inteligencia Artificial":
                """
                La inteligencia artificial es una disciplina
                de la informática orientada a desarrollar
                sistemas capaces de ejecutar tareas que
                requieren capacidades cognitivas humanas.

                El aprendizaje automático, las redes neuronales
                profundas y el procesamiento del lenguaje natural
                constituyen los pilares técnicos de los sistemas
                modernos de inteligencia artificial.

                La inteligencia artificial transforma sectores
                como la salud, la educación, la manufactura,
                las finanzas y el transporte.
                """,

                "Colombia":
                """
                Colombia es una nación situada en el extremo
                noroccidental de América del Sur, reconocida por
                su biodiversidad, riqueza cultural y diversidad
                de paisajes.

                Bogotá es la capital y principal centro económico,
                seguida de Medellín, Cali y Barranquilla.

                El café colombiano goza de reconocimiento
                internacional por su calidad.

                El país alberga ecosistemas del Amazonas,
                los Andes, el Caribe y el Pacífico.
                """,

                "Tecnología 4.0":
                """
                La cuarta revolución industrial redefine los
                modelos productivos mediante la convergencia
                de tecnologías digitales avanzadas.

                El Internet de las cosas, la inteligencia
                artificial, el análisis de grandes datos,
                la robótica colaborativa y la automatización
                inteligente son pilares estratégicos.

                Las fábricas inteligentes integran sensores,
                conectividad y analítica para optimizar
                procesos en tiempo real.
                """
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

                st.session_state["texto_ejemplo"] = (
                    ejemplos[ejemplo_sel]
                )

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
            type=[
                "txt",
                "csv"
            ],
            label_visibility="collapsed"
        )

        if archivo:

            if archivo.name.endswith(".txt"):

                texto_input = archivo.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            elif archivo.name.endswith(".csv"):

                df_csv = pd.read_csv(
                    archivo
                )

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


    # =====================================================
    # PROCESAMIENTO
    # =====================================================

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
        "Longitud mínima:",
        2,
        8,
        3
    )


    palabras_extra = st.text_input(
        "Excluir palabras:",
        placeholder="ej: también, aquí"
    )


    st.divider()


    # =====================================================
    # APARIENCIA
    # =====================================================

    st.markdown("### APARIENCIA")


    paleta_sel = st.selectbox(
        "Paleta:",
        list(PALETAS.keys())
    )


    fondo_sel = st.radio(
        "Fondo:",
        [
            "Blanco",
            "Negro"
        ],
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


    # =====================================================
    # GENERAR
    # =====================================================

    generar = st.button(
        "GENERAR NUBE ↗",
        use_container_width=True
    )


# =========================================================
# DASHBOARD SUPERIOR
# =========================================================

st.markdown("""
<div class="dashboard-top">

    <div class="greeting">
        good evening, <strong>WORDCLOUD</strong>
    </div>

    <div class="brand-mini">
        ☁️
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero-dashboard">

    <div class="hero-eyebrow">
        TEXT ANALYTICS
    </div>

    <div class="hero-title">
        WordCloud <span>Studio.</span>
    </div>

    <div class="hero-description">
        Convierte cualquier texto en una
        visualización clara de las palabras
        más importantes y frecuentes.
    </div>

    <div class="hero-badge">
        ✦ ANALYZE YOUR TEXT
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# PANTALLA DE INICIO
# =========================================================

if not generar:

    col_izq, col_der = st.columns(
        [3, 2],
        gap="large"
    )


    # =====================================================
    # TARJETA PRINCIPAL
    # =====================================================

    with col_izq:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ¿Cómo funciona?"
        )

        st.markdown("""
        <p style="
            color:#d5b0b0 !important;
            font-size:11px;
            line-height:1.7;
        ">
        Una nube de palabras representa visualmente
        la frecuencia de los términos presentes en
        un texto. Las palabras más frecuentes aparecen
        con mayor tamaño.
        </p>
        """,
        unsafe_allow_html=True)


        pasos = [
            (
                "01",
                "Ingresa un texto",
                "Escribe, pega o carga un archivo."
            ),
            (
                "02",
                "Configura",
                "Selecciona idioma, colores y forma."
            ),
            (
                "03",
                "Genera",
                "Presiona el botón GENERAR NUBE."
            ),
            (
                "04",
                "Descarga",
                "Guarda tu resultado en PNG o CSV."
            )
        ]


        for numero, titulo, descripcion in pasos:

            st.markdown(
                f"""
                <div class="info-item">

                    <div style="
                        min-width:35px;
                        height:35px;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        background:#4a181e;
                        color:#f5d36b;
                        border-radius:10px;
                        font-size:10px;
                        font-weight:800;
                    ">
                        {numero}
                    </div>

                    <div>

                        <strong>
                            {titulo}
                        </strong>

                        <p>
                            {descripcion}
                        </p>

                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    # =====================================================
    # APLICACIONES
    # =====================================================

    with col_der:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### Aplicaciones"
        )


        aplicaciones = [
            "📰 Noticias",
            "📋 Encuestas",
            "💬 Reseñas",
            "🎓 Textos académicos",
            "📚 Literatura",
            "📊 Business Intelligence"
        ]


        for caso in aplicaciones:

            st.markdown(
                f'<span class="uso-tag">{caso}</span>',
                unsafe_allow_html=True
            )


        st.markdown(
            "<br>",
            unsafe_allow_html=True
        )


        st.markdown(
            """
            <p style="
                color:#cdaaaa !important;
                font-size:10px;
                line-height:1.6;
            ">
            Utiliza WordCloud Studio para detectar
            rápidamente los conceptos que aparecen
            con mayor frecuencia en tus documentos.
            </p>
            """,
            unsafe_allow_html=True
        )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


        # =================================================
        # PALETAS
        # =================================================

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### Paletas"
        )


        for nombre, colores in PALETAS.items():

            circulos = ""

            for color in colores[:5]:

                circulos += (
                    f"""
                    <span style="
                        display:inline-block;
                        width:13px;
                        height:13px;
                        border-radius:50%;
                        background:{color};
                        margin-right:3px;
                    "></span>
                    """
                )


            st.markdown(
                f"""
                <div style="
                    display:flex;
                    align-items:center;
                    justify-content:space-between;
                    padding:7px 0;
                    border-bottom:1px solid rgba(255,255,255,0.05);
                ">

                    <span style="
                        color:#d9b6b6;
                        font-size:10px;
                    ">
                        {nombre}
                    </span>

                    <span>
                        {circulos}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )


        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


    st.stop()


# =========================================================
# VALIDAR TEXTO
# =========================================================

if not texto_input.strip():

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
        palabra.strip().lower()
        for palabra in palabras_extra.split(",")
        if palabra.strip()
    }


texto_limpio = limpiar_texto(
    texto_input,
    stopwords_set,
    min_longitud
)


if not texto_limpio.strip():

    st.error(
        "El texto resultante está vacío. "
        "Reduce la longitud mínima o cambia las stopwords."
    )

    st.stop()


df_freq = contar_palabras(
    texto_limpio
)


total_palabras = len(
    texto_limpio.split()
)


vocabulario = len(
    df_freq
)


# =========================================================
# TÍTULO DE RESULTADOS
# =========================================================

st.markdown("""
<div class="dashboard-section-title">

    <h3>
        Your Statistics
    </h3>

    <span>
        TEXT ANALYSIS
    </span>

</div>
""", unsafe_allow_html=True)


# =========================================================
# MÉTRICAS
# =========================================================

m1, m2, m3, m4 = st.columns(4)


m1.metric(
    "Palabras",
    f"{total_palabras:,}"
)


m2.metric(
    "Palabras únicas",
    f"{vocabulario:,}"
)


m3.metric(
    "Más frecuente",
    (
        df_freq.iloc[0]["Palabra"]
        if not df_freq.empty
        else "—"
    )
)


m4.metric(
    "Frecuencia",
    (
        int(df_freq.iloc[0]["Frecuencia"])
        if not df_freq.empty
        else 0
    )
)


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =========================================================
# GENERAR NUBE
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
        alto=520
    )


# =========================================================
# NUBE
# =========================================================

st.markdown(
    '<div class="wc-container">',
    unsafe_allow_html=True
)


st.markdown(
    f"""
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:12px;
    ">

        <span style="
            color:#ffffff;
            font-size:14px;
            font-weight:700;
        ">
            ☁️ Nube de palabras
        </span>

        <span style="
            color:#c99ea0;
            font-size:9px;
        ">
            {paleta_sel} · {max_words} palabras
        </span>

    </div>
    """,
    unsafe_allow_html=True
)


st.pyplot(
    fig_wc,
    use_container_width=True
)


st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DESCARGAR PNG
# =========================================================

img_bytes = fig_a_bytes(
    fig_wc
)


st.download_button(
    "⬇️ Descargar imagen PNG",
    data=img_bytes,
    file_name="wordcloud.png",
    mime="image/png",
    use_container_width=True
)


# =========================================================
# ANÁLISIS
# =========================================================

st.markdown("""
<div class="dashboard-section-title">

    <h3>
        Word Frequency
    </h3>

    <span>
        TOP 20
    </span>

</div>
""", unsafe_allow_html=True)


col_freq, col_tabla = st.columns(
    [3, 2],
    gap="large"
)


# =========================================================
# FRECUENCIAS
# =========================================================

with col_freq:

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )


    top20 = df_freq.head(20)


    if not top20.empty:

        max_freq = top20[
            "Frecuencia"
        ].max()


        for rank, (_, row) in enumerate(
            top20.iterrows(),
            1
        ):

            palabra = row["Palabra"]

            frecuencia = int(
                row["Frecuencia"]
            )


            barra_w = max(
                15,
                int(
                    (
                        frecuencia /
                        max_freq
                    ) * 210
                )
            )


            st.markdown(
                f"""
                <div class="freq-row">

                    <span class="rank-tag">
                        #{rank:02d}
                    </span>

                    <span style="
                        color:#ffffff;
                        font-weight:600;
                        min-width:120px;
                        font-size:10px;
                    ">
                        {palabra}
                    </span>

                    <div
                        class="freq-bar"
                        style="
                            width:{barra_w}px;
                        "
                    ></div>

                    <span style="
                        color:#d8b7b7;
                        font-size:10px;
                        font-weight:600;
                        margin-left:auto;
                    ">
                        {frecuencia}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# TABLA
# =========================================================

with col_tabla:

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )


    st.markdown(
        "### Tabla"
    )


    st.dataframe(
        df_freq.head(30),
        use_container_width=True,
        height=500
    )


    csv_bytes = (
        df_freq
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        "⬇️ Exportar CSV",
        data=csv_bytes,
        file_name="frecuencias.csv",
        mime="text/csv",
        use_container_width=True
    )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# TEXTO PROCESADO
# =========================================================

with st.expander(
    "Ver texto procesado"
):

    preview = texto_limpio[:2500]

    if len(texto_limpio) > 2500:
        preview += "..."


    st.markdown(
        f"""
        <div style="
            background:#48171d;
            border-radius:12px;
            padding:18px;
            color:#d9b6b6;
            font-size:11px;
            line-height:1.8;
        ">
            {preview}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CERRAR FIGURAS
# =========================================================

plt.close("all")
import io

from collections import Counter
from wordcloud import WordCloud, STOPWORDS


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="WordCloud Studio",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# ESTILOS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background-color: #151515;
}

/* CONTENEDOR PRINCIPAL */

.main .block-container {
    max-width: 1200px;
    padding: 40px 45px 60px 45px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background-color: #101010 !important;
}

section[data-testid="stSidebar"] * {
    color: #eeeeee;
}

section[data-testid="stSidebar"] hr {
    border-color: #303030;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    padding: 20px 0 40px 0;
}

.eyebrow {
    color: #65c7f5;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 3px;
    margin-bottom: 12px;
}

.hero-title {
    color: #ffffff;
    font-size: 58px;
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: 18px;
}

.hero-title span {
    color: #ffe45b;
}

.hero-text {
    color: #aaaaaa;
    font-size: 17px;
    line-height: 1.6;
    max-width: 600px;
}


/* =========================================================
   TARJETAS
   ========================================================= */

.section-card {
    background-color: #1d1d1d;
    border: 1px solid #303030;
    border-radius: 14px;
    padding: 25px;
    margin-bottom: 20px;
}

.wc-container {
    background-color: #1d1d1d;
    border: 1px solid #303030;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}


/* =========================================================
   TEXTOS
   ========================================================= */

h1, h2, h3 {
    color: #ffffff !important;
}

p {
    color: #b5b5b5;
}


/* =========================================================
   INPUTS
   ========================================================= */

textarea {
    background-color: #202020 !important;
    color: #ffffff !important;
    border: 1px solid #383838 !important;
    border-radius: 10px !important;
}

input {
    background-color: #202020 !important;
    color: #ffffff !important;
}

textarea::placeholder,
input::placeholder {
    color: #777777 !important;
}


/* =========================================================
   SELECT
   ========================================================= */

div[data-baseweb="select"] > div {
    background-color: #202020 !important;
    color: #ffffff !important;
    border-color: #383838 !important;
}


/* =========================================================
   BOTONES
   ========================================================= */

.stButton > button {
    background-color: #ffe45b !important;
    color: #151515 !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 800 !important;
    min-height: 45px !important;
}

.stButton > button:hover {
    background-color: #fff080 !important;
}

[data-testid="stDownloadButton"] button {
    background-color: #65c7f5 !important;
    color: #111111 !important;
    border: none !important;
    border-radius: 9px !important;
    font-weight: 800 !important;
}


/* =========================================================
   MÉTRICAS
   ========================================================= */

[data-testid="metric-container"] {
    background-color: #1d1d1d;
    border: 1px solid #303030;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="metric-container"] label {
    color: #888888 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}


/* =========================================================
   FRECUENCIAS
   ========================================================= */

.freq-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 12px;
    margin: 5px 0;
    background-color: #1d1d1d;
    border: 1px solid #303030;
    border-radius: 8px;
}

.freq-bar {
    height: 8px;
    background-color: #ffe45b;
    border-radius: 10px;
}

.rank-tag {
    background-color: #292929;
    color: #999999;
    border-radius: 5px;
    padding: 3px 7px;
    font-size: 12px;
}


/* =========================================================
   TABLA
   ========================================================= */

[data-testid="stDataFrame"] {
    border: 1px solid #303030;
}


/* =========================================================
   EXPANDER
   ========================================================= */

[data-testid="stExpander"] {
    background-color: #1d1d1d !important;
    border: 1px solid #303030 !important;
    border-radius: 10px !important;
}


/* =========================================================
   DIVISORES
   ========================================================= */

hr {
    border-color: #303030 !important;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 800px) {

    .main .block-container {
        padding: 25px 18px 40px 18px;
    }

    .hero-title {
        font-size: 40px;
    }

    .hero-text {
        font-size: 16px;
    }

}

</style>
""", unsafe_allow_html=True)


# =========================================================
# STOPWORDS
# =========================================================

STOPWORDS_ES = {
    "de", "la", "el", "en", "y", "a", "los", "del", "se",
    "las", "un", "por", "con", "no", "una", "su", "para",
    "es", "al", "lo", "como", "mas", "pero", "sus", "le",
    "ya", "o", "este", "si", "porque", "esta", "entre",
    "cuando", "muy", "sin", "sobre", "tambien", "me",
    "hasta", "hay", "donde", "quien", "desde", "nos",
    "durante", "ni", "contra", "ese", "eso", "ante",
    "bajo", "tras", "que", "fue", "son", "han", "ha",
    "ser", "era", "estan", "siendo", "sido", "he", "has",
    "hemos", "habian", "tiene", "tienen", "hacer",
    "puede", "pueden", "asi", "tan", "parte", "todo",
    "todos", "todas", "cada", "otro", "otra", "otros",
    "otras", "mismo", "misma", "nuestro", "nuestra",
    "ellos", "ellas", "nosotros", "les", "esa", "esos",
    "esas", "aquel", "aquella", "aquellos"
}


def obtener_stopwords(idioma):

    sw = set(STOPWORDS)

    if idioma in ("Español", "Ambos"):
        sw |= STOPWORDS_ES

    return sw


# =========================================================
# PALETAS
# =========================================================

PALETAS = {

    "Coral": [
        "#f26b5e",
        "#ff806f",
        "#e85b50",
        "#d94d45",
        "#ff9b8f"
    ],

    "Azul": [
        "#315c72",
        "#407a96",
        "#5b9ab5",
        "#78b7cf",
        "#9bcfe0"
    ],

    "Verde": [
        "#356859",
        "#4d806f",
        "#6d9b89",
        "#8bb5a2",
        "#b0cdbd"
    ],

    "Grises": [
        "#222222",
        "#444444",
        "#666666",
        "#888888",
        "#aaaaaa"
    ]
}


FORMAS = {
    "Rectángulo": None,
    "Círculo": "circle"
}


# =========================================================
# MÁSCARA
# =========================================================

def crear_mascara(forma, size=500):

    if forma == "circle":

        y, x = np.ogrid[:size, :size]

        cx = size // 2
        cy = size // 2

        mascara = np.ones(
            (size, size),
            dtype=np.uint8
        ) * 255

        mascara[
            (x - cx) ** 2 +
            (y - cy) ** 2
            <= (size // 2 - 12) ** 2
        ] = 0

        return mascara

    return None


# =========================================================
# LIMPIAR TEXTO
# =========================================================

def limpiar_texto(
    texto,
    stopwords,
    min_longitud
):

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
        palabra
        for palabra in texto.split()
        if palabra not in stopwords
        and len(palabra) >= min_longitud
    ]

    return " ".join(palabras)


# =========================================================
# CONTAR PALABRAS
# =========================================================

def contar_palabras(texto):

    datos = Counter(
        texto.split()
    ).most_common(50)

    return pd.DataFrame(
        datos,
        columns=[
            "Palabra",
            "Frecuencia"
        ]
    )


# =========================================================
# GENERAR WORDCLOUD
# =========================================================

def generar_wordcloud(
    texto,
    paleta,
    max_words,
    fondo,
    forma
):

    import random

    colores = PALETAS[paleta]

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
            rng.randint(
                0,
                len(colores) - 1
            )
        ]

    mascara = crear_mascara(
        forma,
        500
    )

    wc = WordCloud(
        width=1000,
        height=520,
        max_words=max_words,
        background_color=fondo,
        color_func=color_func,
        mask=mascara,
        collocations=False,
        min_font_size=11,
        max_font_size=120,
        margin=5
    ).generate(texto)

    fig, ax = plt.subplots(
        figsize=(10, 5.2)
    )

    ax.imshow(
        wc,
        interpolation="bilinear"
    )

    ax.axis("off")

    fig.patch.set_facecolor(
        fondo
    )

    plt.tight_layout(
        pad=0
    )

    return fig


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ☁️ WordCloud Studio")

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
            "Texto",
            height=180,
            placeholder="Escribe o pega aquí tu texto..."
        )

    else:

        archivo = st.file_uploader(
            "Archivo",
            type=["txt", "csv"]
        )

        if archivo:

            if archivo.name.endswith(".txt"):

                texto_input = archivo.read().decode(
                    "utf-8",
                    errors="ignore"
                )

            elif archivo.name.endswith(".csv"):

                df_csv = pd.read_csv(
                    archivo
                )

                columna = st.selectbox(
                    "Columna de texto",
                    df_csv.columns.tolist()
                )

                texto_input = " ".join(
                    df_csv[columna]
                    .dropna()
                    .astype(str)
                    .tolist()
                )

    st.divider()

    st.markdown("### PROCESAMIENTO")

    idioma = st.selectbox(
        "Stopwords",
        [
            "Español",
            "Inglés",
            "Ambos",
            "Ninguno"
        ]
    )

    min_longitud = st.slider(
        "Longitud mínima",
        2,
        8,
        3
    )

    palabras_extra = st.text_input(
        "Excluir palabras",
        placeholder="ej: también, aquí"
    )

    st.divider()

    st.markdown("### APARIENCIA")

    paleta_sel = st.selectbox(
        "Paleta",
        list(PALETAS.keys())
    )

    fondo_sel = st.radio(
        "Fondo",
        [
            "Blanco",
            "Negro"
        ],
        horizontal=True
    )

    fondo_color = (
        "white"
        if fondo_sel == "Blanco"
        else "black"
    )

    forma_sel = st.selectbox(
        "Forma",
        list(FORMAS.keys())
    )

    max_words = st.slider(
        "Máximo de palabras",
        20,
        200,
        80
    )

    st.divider()

    generar = st.button(
        "GENERAR NUBE",
        use_container_width=True
    )


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

    <div class="eyebrow">
        TEXT ANALYTICS
    </div>

    <div class="hero-title">
        WordCloud <span>Studio.</span>
    </div>

    <div class="hero-text">
        Convierte un texto en una nube de palabras
        clara y fácil de leer. Las palabras más
        frecuentes aparecerán con mayor tamaño.
    </div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# INICIO
# =========================================================

if not generar:

    col1, col2 = st.columns(
        [3, 2],
        gap="large"
    )

    with col1:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ¿Cómo funciona?"
        )

        st.write(
            "Escribe o pega un texto en el panel "
            "lateral, configura las opciones y "
            "presiona GENERAR NUBE."
        )

        st.markdown(
            """
            **1.** Ingresa un texto.

            **2.** Configura el análisis.

            **3.** Genera la nube.

            **4.** Descarga el resultado.
            """
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="section-card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "### ✨ Características"
        )

        st.write(
            "• Análisis de frecuencia"
        )

        st.write(
            "• Eliminación de stopwords"
        )

        st.write(
            "• Diferentes colores"
        )

        st.write(
            "• Forma circular o rectangular"
        )

        st.write(
            "• Descarga en PNG y CSV"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.stop()


# =========================================================
# VALIDAR TEXTO
# =========================================================

if not texto_input.strip():

    st.warning(
        "Escribe o sube un texto antes de generar la nube."
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
        palabra.strip().lower()
        for palabra in palabras_extra.split(",")
        if palabra.strip()
    }


texto_limpio = limpiar_texto(
    texto_input,
    stopwords_set,
    min_longitud
)


if not texto_limpio.strip():

    st.error(
        "El texto quedó vacío. "
        "Reduce la longitud mínima "
        "o cambia las stopwords."
    )

    st.stop()


df_freq = contar_palabras(
    texto_limpio
)

total_palabras = len(
    texto_limpio.split()
)

vocabulario = len(
    df_freq
)


# =========================================================
# MÉTRICAS
# =========================================================

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Palabras",
    f"{total_palabras:,}"
)

m2.metric(
    "Palabras únicas",
    f"{vocabulario:,}"
)

m3.metric(
    "Más frecuente",
    df_freq.iloc[0]["Palabra"]
)

m4.metric(
    "Frecuencia",
    int(
        df_freq.iloc[0]["Frecuencia"]
    )
)


st.markdown(
    "<br>",
    unsafe_allow_html=True
)


# =========================================================
# NUBE
# =========================================================

with st.spinner(
    "Generando nube..."
):

    fig_wc = generar_wordcloud(
        texto_limpio,
        paleta_sel,
        max_words,
        fondo_color,
        FORMAS[forma_sel]
    )


st.markdown(
    '<div class="wc-container">',
    unsafe_allow_html=True
)

st.markdown(
    "### Nube de palabras"
)

st.pyplot(
    fig_wc,
    use_container_width=True
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# =========================================================
# DESCARGA PNG
# =========================================================

buf = io.BytesIO()

fig_wc.savefig(
    buf,
    format="png",
    dpi=150,
    bbox_inches="tight"
)

buf.seek(0)

st.download_button(
    "⬇️ Descargar PNG",
    data=buf.getvalue(),
    file_name="wordcloud.png",
    mime="image/png",
    use_container_width=True
)


# =========================================================
# FRECUENCIAS
# =========================================================

st.divider()

col1, col2 = st.columns(
    [3, 2],
    gap="large"
)


with col1:

    st.markdown(
        "### Frecuencia de palabras"
    )

    top20 = df_freq.head(20)

    max_freq = top20[
        "Frecuencia"
    ].max()

    for rank, (_, row) in enumerate(
        top20.iterrows(),
        1
    ):

        palabra = row["Palabra"]

        frecuencia = int(
            row["Frecuencia"]
        )

        ancho = max(
            20,
            int(
                frecuencia /
                max_freq *
                250
            )
        )

        st.markdown(
            f"""
            <div class="freq-row">

                <span class="rank-tag">
                    #{rank}
                </span>

                <span style="
                    min-width:130px;
                    font-weight:600;
                    color:#ffffff;
                ">
                    {palabra}
                </span>

                <div
                    class="freq-bar"
                    style="width:{ancho}px;"
                ></div>

                <span style="
                    color:#bbbbbb;
                    font-weight:600;
                ">
                    {frecuencia}
                </span>

            </div>
            """,
            unsafe_allow_html=True
        )


with col2:

    st.markdown(
        "### Tabla"
    )

    st.dataframe(
        df_freq.head(30),
        use_container_width=True,
        height=500
    )

    csv_bytes = (
        df_freq
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        "⬇️ Descargar CSV",
        data=csv_bytes,
        file_name="frecuencias.csv",
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# TEXTO PROCESADO
# =========================================================

with st.expander(
    "Ver texto procesado"
):

    st.write(
        texto_limpio[:2500]
    )


plt.close("all")
