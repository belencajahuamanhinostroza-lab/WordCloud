import streamlit as st
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
# ESTILOS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f6f1ef;
}

/* CONTENEDOR */

.main .block-container {
    max-width: 1200px;
    padding: 35px 45px 60px 45px;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    background: #ffffff;
    border-radius: 18px;
    padding: 35px 40px;
    margin-bottom: 25px;
    border: 1px solid #eadfdb;
}

.eyebrow {
    color: #f26b5e;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 10px;
}

.hero-title {
    color: #222222;
    font-size: 48px;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 12px;
}

.hero-title span {
    color: #f26b5e;
}

.hero-text {
    color: #666666;
    font-size: 17px;
    line-height: 1.6;
    max-width: 650px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #fffaf8 !important;
    border-right: 1px solid #eadfdb;
}

[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #252525 !important;
}

[data-testid="stSidebar"] label {
    color: #555555 !important;
}


/* =========================================================
   INPUTS
   ========================================================= */

textarea,
input[type="text"] {
    background: #ffffff !important;
    color: #222222 !important;
    border: 1px solid #d9cfcb !important;
    border-radius: 10px !important;
}

textarea:focus,
input[type="text"]:focus {
    border-color: #f26b5e !important;
    box-shadow: 0 0 0 2px rgba(242,107,94,0.15) !important;
}


/* =========================================================
   SELECT
   ========================================================= */

[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #d9cfcb !important;
    border-radius: 10px !important;
}


/* =========================================================
   BOTONES
   ========================================================= */

.stButton > button {
    background: #f26b5e !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    min-height: 45px !important;
}

.stButton > button:hover {
    background: #df594d !important;
}

[data-testid="stDownloadButton"] button {
    background: #333333 !important;
    color: white !important;
    border-radius: 10px !important;
}


/* =========================================================
   CARDS
   ========================================================= */

.section-card {
    background: #ffffff;
    border: 1px solid #eadfdb;
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 18px;
}

.info-item {
    padding: 13px 15px;
    margin-bottom: 8px;
    background: #faf8f7;
    border: 1px solid #eee6e2;
    border-radius: 10px;
}


/* =========================================================
   MÉTRICAS
   ========================================================= */

[data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid #eadfdb;
    border-radius: 12px;
    padding: 15px;
}

[data-testid="metric-container"] label {
    color: #777777 !important;
}

[data-testid="stMetricValue"] {
    color: #222222 !important;
}


/* =========================================================
   NUBE
   ========================================================= */

.wc-container {
    background: #ffffff;
    border: 1px solid #eadfdb;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 18px;
}


/* =========================================================
   FRECUENCIA
   ========================================================= */

.freq-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    margin: 5px 0;
    background: #ffffff;
    border: 1px solid #eee6e2;
    border-radius: 8px;
}

.freq-bar {
    height: 8px;
    background: #f26b5e;
    border-radius: 10px;
}

.rank-tag {
    background: #f5efed;
    border-radius: 5px;
    padding: 3px 7px;
    font-size: 12px;
    color: #777777;
}


/* =========================================================
   EXPANDER
   ========================================================= */

div[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #eadfdb !important;
    border-radius: 10px !important;
}


/* =========================================================
   TEXTO
   ========================================================= */

h1,
h2,
h3 {
    color: #222222 !important;
}

p {
    color: #555555;
}


/* =========================================================
   RESPONSIVE
   ========================================================= */

@media (max-width: 800px) {

    .main .block-container {
        padding: 25px 18px;
    }

    .hero-title {
        font-size: 38px;
    }

    .hero {
        padding: 25px;
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
                    color:#222;
                ">
                    {palabra}
                </span>

                <div
                    class="freq-bar"
                    style="width:{ancho}px;"
                ></div>

                <span style="
                    color:#555;
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
