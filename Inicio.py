"""
WORDCLOUD STUDIO
Aplicación Streamlit para crear nubes de palabras.

Instalación:
    pip install streamlit wordcloud matplotlib pandas Pillow numpy

Ejecución:
    streamlit run app.py
"""

import io
import re
import random
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from wordcloud import WordCloud, STOPWORDS


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
# ESTILO SIMPLE Y LEGIBLE
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: "DM Sans", sans-serif;
    }

    .stApp {
        background: #d68182;
    }

    .main .block-container {
        max-width: 1180px;
        padding: 35px 35px 60px 35px;
    }

    /* ---------- SIDEBAR ---------- */

    [data-testid="stSidebar"] {
        background: #fff7ef !important;
        border-right: 2px solid #e6a1a0;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #342b32 !important;
    }

    [data-testid="stSidebar"] h2 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] h3 {
        font-size: 0.9rem !important;
        margin-top: 18px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    [data-testid="stSidebar"] hr {
        border-color: #ead8d2 !important;
    }

    /* ---------- TEXTO ---------- */

    h1, h2, h3 {
        color: #342b32 !important;
    }

    p, li {
        color: #55484f !important;
    }

    /* ---------- INPUTS ---------- */

    textarea,
    input[type="text"] {
        background: #ffffff !important;
        color: #342b32 !important;
        border: 1px solid #d9c8c4 !important;
        border-radius: 12px !important;
    }

    textarea:focus,
    input[type="text"]:focus {
        border-color: #ff715b !important;
        box-shadow: 0 0 0 2px rgba(255, 113, 91, 0.15) !important;
    }

    [data-baseweb="select"] > div {
        background: #ffffff !important;
        color: #342b32 !important;
        border: 1px solid #d9c8c4 !important;
        border-radius: 10px !important;
    }

    /* ---------- BOTONES ---------- */

    .stButton > button,
    [data-testid="stDownloadButton"] button {
        background: #ff715b !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        min-height: 46px !important;
        transition: 0.2s ease;
    }

    .stButton > button:hover,
    [data-testid="stDownloadButton"] button:hover {
        background: #e95c49 !important;
        transform: translateY(-1px);
    }

    /* ---------- TARJETAS ---------- */

    .hero {
        background: #fffaf5;
        border-radius: 24px;
        padding: 35px 40px;
        margin-bottom: 22px;
        border: 1px solid rgba(90, 55, 65, 0.08);
        box-shadow: 0 8px 25px rgba(70, 35, 40, 0.12);
    }

    .eyebrow {
        color: #ff715b;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #342b32;
        font-size: 3.2rem;
        line-height: 1;
        font-weight: 700;
        margin: 0;
    }

    .hero-title span {
        color: #ff715b;
    }

    .hero-text {
        color: #66575e;
        font-size: 1rem;
        line-height: 1.6;
        max-width: 650px;
        margin-top: 14px;
    }

    .card {
        background: #fffaf5;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 18px;
        border: 1px solid rgba(90, 55, 65, 0.08);
        box-shadow: 0 6px 18px rgba(70, 35, 40, 0.09);
    }

    .card-title {
        color: #342b32;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .card-text {
        color: #66575e;
        line-height: 1.6;
        font-size: 0.95rem;
    }

    .metric-card {
        background: #fffaf5;
        border-radius: 16px;
        padding: 17px;
        border: 1px solid rgba(90, 55, 65, 0.08);
        text-align: center;
        box-shadow: 0 5px 15px rgba(70, 35, 40, 0.08);
    }

    .metric-name {
        color: #806e75;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }

    .metric-value {
        color: #342b32;
        font-size: 1.35rem;
        font-weight: 700;
        margin-top: 5px;
    }

    .cloud-card {
        background: #fffaf5;
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(90, 55, 65, 0.08);
        box-shadow: 0 6px 18px rgba(70, 35, 40, 0.09);
    }

    .tag {
        display: inline-block;
        background: #f3d7c9;
        color: #684f54;
        border-radius: 20px;
        padding: 7px 12px;
        margin: 3px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    .freq-row {
        background: #fffaf5;
        border-radius: 10px;
        padding: 9px 12px;
        margin: 5px 0;
        border: 1px solid #eadfd9;
    }

    .rank {
        color: #a2878c;
        font-size: 0.78rem;
        font-weight: 700;
        display: inline-block;
        width: 42px;
    }

    .word {
        color: #342b32;
        font-weight: 600;
        display: inline-block;
        width: 130px;
    }

    .number {
        color: #684f54;
        font-weight: 700;
        float: right;
    }

    .tip {
        background: #f5dfd7;
        border-left: 4px solid #ff715b;
        border-radius: 10px;
        padding: 13px 16px;
        color: #5e4c53;
        margin-top: 10px;
    }

    @media (max-width: 800px) {
        .main .block-container {
            padding: 20px 15px 40px 15px;
        }

        .hero-title {
            font-size: 2.3rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# STOPWORDS
# =========================================================

STOPWORDS_ES = {
    "de", "la", "el", "en", "y", "a", "los", "del", "se", "las",
    "un", "por", "con", "no", "una", "su", "para", "es", "al", "lo",
    "como", "mas", "más", "pero", "sus", "le", "ya", "o", "este", "si",
    "sí", "porque", "esta", "está", "entre", "cuando", "muy", "sin",
    "sobre", "tambien", "también", "me", "hasta", "hay", "donde",
    "dónde", "quien", "quién", "desde", "nos", "durante", "ni", "contra",
    "ese", "eso", "ante", "bajo", "tras", "que", "qué", "fue", "son",
    "han", "ha", "ser", "era", "estan", "están", "siendo", "sido",
    "he", "has", "hemos", "habian", "habían", "tiene", "tienen",
    "hacer", "puede", "pueden", "asi", "así", "tan", "parte", "todo",
    "todos", "todas", "cada", "otro", "otra", "otros", "otras",
    "mismo", "misma", "nuestro", "nuestra", "ellos", "ellas",
    "nosotros", "les", "esa", "esos", "esas", "aquel", "aquella",
    "aquellos",
}


# =========================================================
# PALETAS
# =========================================================

PALETAS = {
    "Coral": [
        "#ff5f4d", "#ff715b", "#f88379",
        "#e99a9c", "#c66f76", "#9d5963"
    ],
    "Coral + morado": [
        "#ff715b", "#ff8b68", "#b79bd6",
        "#9c83c7", "#7d68a7", "#e79a91"
    ],
    "Pastel": [
        "#eaa7a3", "#f2b9a9", "#d8bde7",
        "#b8c8e8", "#f0d6c8", "#c9a8b6"
    ],
    "Oscura": [
        "#342b32", "#4b3d45", "#63515b",
        "#806c76", "#9d8490", "#b99ba3"
    ],
}


# =========================================================
# FUNCIONES
# =========================================================

def obtener_stopwords(idioma):
    resultado = set()

    if idioma in ("Español", "Ambos"):
        resultado |= STOPWORDS_ES

    if idioma in ("Inglés", "Ambos"):
        resultado |= set(STOPWORDS)

    return resultado


def limpiar_texto(texto, stopwords, min_longitud):
    texto = texto.lower()
    texto = re.sub(r"http\S+|www\S+", " ", texto)
    texto = re.sub(
        r"[^a-záéíóúüñàâèêîôùûäëïöü\s]",
        " ",
        texto,
        flags=re.UNICODE,
    )

    palabras = [
        palabra
        for palabra in texto.split()
        if palabra not in stopwords
        and len(palabra) >= min_longitud
    ]

    return " ".join(palabras)


def contar_palabras(texto):
    palabras = texto.split()

    if not palabras:
        return pd.DataFrame(
            columns=["Palabra", "Frecuencia"]
        )

    return pd.DataFrame(
        Counter(palabras).most_common(50),
        columns=["Palabra", "Frecuencia"],
    )


def crear_mascara_circulo(size=520):
    y, x = np.ogrid[:size, :size]
    centro = size // 2
    radio = size // 2 - 12

    mascara = np.ones(
        (size, size),
        dtype=np.uint8
    ) * 255

    mascara[
        (x - centro) ** 2 + (y - centro) ** 2 <= radio ** 2
    ] = 0

    return mascara


def generar_wordcloud(
    texto,
    paleta_nombre,
    max_words,
    fondo,
    forma,
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

    mascara = None

    if forma == "Círculo":
        mascara = crear_mascara_circulo(520)

    nube = WordCloud(
        width=1000,
        height=520,
        max_words=max_words,
        background_color=fondo,
        color_func=color_func,
        mask=mascara,
        collocations=False,
        min_font_size=10,
        max_font_size=110,
        prefer_horizontal=0.75,
        relative_scaling=0.5,
        margin=5,
        random_state=42,
    ).generate(texto)

    fig, ax = plt.subplots(
        figsize=(10, 5.2)
    )

    ax.imshow(
        nube,
        interpolation="bilinear"
    )

    ax.axis("off")

    fig.patch.set_facecolor(fondo)

    plt.tight_layout(
        pad=0
    )

    return fig


def figura_a_bytes(fig):
    buffer = io.BytesIO()

    fig.savefig(
        buffer,
        format="png",
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )

    buffer.seek(0)

    return buffer.getvalue()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ☁️ WordCloud Studio")

    st.divider()

    st.markdown("### 1. Texto")

    fuente = st.radio(
        "Fuente",
        [
            "Escribir / pegar",
            "Subir archivo",
        ],
        label_visibility="collapsed",
    )

    texto_input = ""

    if fuente == "Escribir / pegar":

        texto_input = st.text_area(
            "Texto",
            height=180,
            placeholder=(
                "Escribe o pega aquí tu texto..."
            ),
            label_visibility="collapsed",
        )

        with st.expander("Usar ejemplo"):

            ejemplos = {
                "Inteligencia Artificial": """
                La inteligencia artificial transforma la tecnología.
                Los sistemas inteligentes permiten analizar datos,
                automatizar procesos y crear nuevas herramientas.
                La inteligencia artificial está presente en la educación,
                la salud, la industria y muchas áreas de la sociedad.
                """,

                "Colombia": """
                Colombia es un país con gran diversidad cultural,
                natural y geográfica. Bogotá, Medellín, Cali y
                Barranquilla son ciudades importantes. El café,
                la biodiversidad, la música y la gastronomía forman
                parte de la identidad colombiana.
                """,

                "Tecnología": """
                La tecnología permite mejorar procesos mediante
                inteligencia artificial, automatización, datos,
                internet, robótica y sistemas digitales.
                Las empresas utilizan tecnología para crear soluciones
                más rápidas, eficientes y accesibles.
                """,
            }

            ejemplo = st.selectbox(
                "Ejemplo",
                list(ejemplos.keys()),
            )

            if st.button(
                "Cargar ejemplo",
                use_container_width=True,
            ):
                st.session_state["texto_ejemplo"] = ejemplos[
                    ejemplo
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
            type=["txt", "csv"],
        )

        if archivo:

            if archivo.name.lower().endswith(".txt"):

                texto_input = archivo.read().decode(
                    "utf-8",
                    errors="ignore",
                )

            elif archivo.name.lower().endswith(".csv"):

                df_csv = pd.read_csv(
                    archivo
                )

                if len(df_csv.columns) > 0:

                    columna = st.selectbox(
                        "Columna de texto",
                        df_csv.columns.tolist(),
                    )

                    texto_input = " ".join(
                        df_csv[columna]
                        .dropna()
                        .astype(str)
                        .tolist()
                    )

    st.divider()

    st.markdown("### 2. Filtros")

    idioma = st.selectbox(
        "Stopwords",
        [
            "Español",
            "Inglés",
            "Ambos",
            "Ninguno",
        ],
    )

    min_longitud = st.slider(
        "Longitud mínima",
        2,
        8,
        3,
    )

    palabras_extra = st.text_input(
        "Palabras a excluir",
        placeholder="ej: también, aquí",
    )

    st.divider()

    st.markdown("### 3. Apariencia")

    paleta_sel = st.selectbox(
        "Paleta",
        list(PALETAS.keys()),
    )

    fondo_sel = st.radio(
        "Fondo de la nube",
        ["Claro", "Oscuro"],
        horizontal=True,
    )

    fondo_color = (
        "#fffaf5"
        if fondo_sel == "Claro"
        else "#342b32"
    )

    forma_sel = st.selectbox(
        "Forma",
        ["Rectángulo", "Círculo"],
    )

    max_words = st.slider(
        "Máximo de palabras",
        20,
        150,
        70,
    )

    st.divider()

    generar = st.button(
        "☁️ GENERAR NUBE",
        use_container_width=True,
    )


# =========================================================
# CABECERA
# =========================================================

st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)


# =========================================================
# PANTALLA INICIAL
# =========================================================

if not generar:

    col1, col2 = st.columns(
        [1.4, 1],
        gap="medium",
    )

    with col1:

        st.markdown(
            """
            <div class="card">

                <div class="card-title">
                    📊 ¿Qué hace esta herramienta?
                </div>

                <div class="card-text">
                    Analiza la frecuencia de las palabras
                    de un texto y las representa visualmente.
                    Las palabras que aparecen más veces
                    tendrán un tamaño mayor.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card">

                <div class="card-title">
                    🚀 ¿Cómo funciona?
                </div>

                <div class="card-text">
                    1. Escribe o carga un texto.<br>
                    2. Elige los filtros y la apariencia.<br>
                    3. Pulsa <b>GENERAR NUBE</b>.<br>
                    4. Descarga el resultado.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
            """
            <div class="card">

                <div class="card-title">
                    🎨 Personalización
                </div>

                <div class="card-text">
                    Puedes cambiar la paleta de colores,
                    el fondo, la forma y la cantidad
                    máxima de palabras.
                </div>

                <div style="margin-top:14px;">
                    <span class="tag">Coral</span>
                    <span class="tag">Pastel</span>
                    <span class="tag">Morado</span>
                    <span class="tag">Oscuro</span>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="tip">
                💡 <b>Consejo:</b> usa textos de varias
                líneas para obtener una nube más completa.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.stop()


# =========================================================
# VALIDAR TEXTO
# =========================================================

if not texto_input.strip():

    st.warning(
        "Escribe o carga un texto antes de generar la nube."
    )

    st.stop()


# =========================================================
# PROCESAR TEXTO
# =========================================================

stopwords_set = obtener_stopwords(
    idioma
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
    min_longitud,
)

if not texto_limpio.strip():

    st.error(
        "El texto quedó vacío después del filtrado. "
        "Prueba con una longitud mínima menor."
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

with m1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-name">
                Palabras
            </div>
            <div class="metric-value">
                {total_palabras:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-name">
                Palabras únicas
            </div>
            <div class="metric-value">
                {vocabulario:,}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m3:
    termino = (
        df_freq.iloc[0]["Palabra"]
        if not df_freq.empty
        else "—"
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-name">
                Más frecuente
            </div>
            <div class="metric-value">
                {termino}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with m4:
    frecuencia = (
        int(df_freq.iloc[0]["Frecuencia"])
        if not df_freq.empty
        else 0
    )

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-name">
                Frecuencia
            </div>
            <div class="metric-value">
                {frecuencia}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# NUBE
# =========================================================

with st.spinner("Generando nube..."):

    fig_wc = generar_wordcloud(
        texto_limpio,
        paleta_sel,
        max_words,
        fondo_color,
        forma_sel,
    )


st.markdown(
    '<div class="cloud-card">',
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    ### ☁️ Nube de palabras

    **Paleta:** {paleta_sel}
    &nbsp;&nbsp;·&nbsp;&nbsp;
    **Fondo:** {fondo_sel}
    &nbsp;&nbsp;·&nbsp;&nbsp;
    **Máximo:** {max_words}
    """,
)

st.pyplot(
    fig_wc,
    use_container_width=True,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# =========================================================
# DESCARGA PNG
# =========================================================

img_bytes = figura_a_bytes(
    fig_wc
)

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

st.markdown("<br>", unsafe_allow_html=True)

col_freq, col_table = st.columns(
    [1.2, 1],
    gap="medium",
)


with col_freq:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        "### 📊 Palabras más frecuentes"
    )

    top20 = df_freq.head(20)

    if not top20.empty:

        max_freq = int(
            top20["Frecuencia"].max()
        )

        for rank, (_, row) in enumerate(
            top20.iterrows(),
            1,
        ):

            palabra = row["Palabra"]
            frecuencia = int(
                row["Frecuencia"]
            )

            porcentaje = (
                frecuencia / max_freq
                if max_freq
                else 0
            )

            ancho = max(
                30,
                int(porcentaje * 230),
            )

            st.markdown(
                f"""
                <div class="freq-row">
                    <span class="rank">
                        #{rank:02d}
                    </span>

                    <span class="word">
                        {palabra}
                    </span>

                    <span style="
                        display:inline-block;
                        width:{ancho}px;
                        height:8px;
                        background:#ff715b;
                        border-radius:10px;
                        opacity:{0.45 + porcentaje * 0.55};
                    "></span>

                    <span class="number">
                        {frecuencia}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


with col_table:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        "### 📋 Tabla"
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
        "⬇️ Descargar CSV",
        data=csv_bytes,
        file_name="frecuencias.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# =========================================================
# TEXTO PROCESADO
# =========================================================

with st.expander(
    "Ver texto procesado"
):

    preview = texto_limpio[:3000]

    if len(texto_limpio) > 3000:
        preview += "..."

    st.write(
        preview
    )


# =========================================================
# CERRAR FIGURA
# =========================================================

plt.close(fig_wc)
