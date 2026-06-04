from pathlib import Path
import streamlit as st


COLORES_CATEGORIA = {
    "tecnologia": "#4A90E2",
    "ciencia": "#4CAF7D",
    "videojuegos": "#1F4E79",
    "salud": "#E07A5F",
    "economia": "#D4A017",
    "politica": "#8E5EA2",
    "general": "#7A7A7A"
}

COLORES_SENTIMIENTO = {
    "positivo": "#2EAD6B",
    "negativo": "#C0392B",
    "neutral": "#7F8C8D",
    "?": "#7F8C8D"
}


def cargar_css(ruta="assets/styles.css"):
    css = Path(ruta).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def color_categoria(categoria):
    return COLORES_CATEGORIA.get(str(categoria).lower(), COLORES_CATEGORIA["general"])


def color_sentimiento(sentimiento):
    return COLORES_SENTIMIENTO.get(str(sentimiento).lower(), COLORES_SENTIMIENTO["?"])


def badge(texto, color):
    return f'<span class="tag" style="background:{color};">{texto}</span>'


def card(titulo, valor, descripcion):
    st.markdown(
        f"""
        <div class="simanw-card">
            <div class="simanw-card-title">{titulo}</div>
            <div class="simanw-card-value">{valor}</div>
            <div class="simanw-card-desc">{descripcion}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def noticia_card(titulo, snippet, categoria, sentimiento, similitud=None, fuente=None, url=None):
    categoria_badge = badge(categoria, color_categoria(categoria))
    sentimiento_badge = badge(sentimiento, color_sentimiento(sentimiento))

    similitud_html = ""
    if similitud is not None:
        similitud_html = badge(f"{similitud:.1f}% similitud", "#B55239")

    fuente_html = ""
    if fuente:
        fuente_html = f"<p><strong>Fuente:</strong> {fuente}</p>"

    url_html = ""
    if url:
        url_html = f'<p><a href="{url}" target="_blank">Ver noticia original</a></p>'

    st.markdown(
        f"""
        <div class="news-card">
            <div class="news-title">{titulo}</div>
            <div class="news-snippet">{snippet}</div>
            <div>
                {categoria_badge}
                {sentimiento_badge}
                {similitud_html}
            </div>
            {fuente_html}
            {url_html}
        </div>
        """,
        unsafe_allow_html=True
    )


def chat_bubble(rol, mensaje):
    clase = "user-bubble" if rol == "Usuario" else "bot-bubble"
    st.markdown(
        f"""
        <div class="{clase}">
            <strong>{rol}:</strong><br>
            {mensaje}
        </div>
        """,
        unsafe_allow_html=True
    )

def tabla_html(df):
    html = """
    <div class="tabla-contenedor">
        <table class="tabla-simanw">
            <thead>
                <tr>
    """

    for col in df.columns:
        html += f"<th>{col}</th>"

    html += """
                </tr>
            </thead>
            <tbody>
    """

    for _, row in df.iterrows():
        html += "<tr>"
        for col in df.columns:
            html += f"<td>{row[col]}</td>"
        html += "</tr>"

    html += """
            </tbody>
        </table>
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)