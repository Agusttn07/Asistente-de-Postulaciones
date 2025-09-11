# Postulacion_Streamlit.py
import streamlit as st
import pandas as pd
import unicodedata
from PIL import Image
import os

st.set_page_config(page_title="Asistente de Postulaciones", page_icon="🎓", layout="wide")
car = ""
sede = ""

# ===== Utilidades =====
def safe_int(x):
    try:
        return int(str(x).strip())
    except:
        return None

def clamp_0_1000(x):
    if x is None or x == "":
        return None
    try:
        v = float(x)
        if v < 0: return 0.0
        if v > 1000: return 1000.0
        return v
    except:
        return None

# ===== Normalizador =====
def normalizar(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")  # quita tildes
    return texto

# ===== Carga de Carreras =====
@st.cache_data
def cargar_ponderaciones(force_update=False):
    data = [
        #Universidad de Chile
        {"universidad": "Universidad de Chile", "carrera": "Ingeniería y Ciencias (Plan Común)", "sede": "Beauchef",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0, "Corte": 500},

        #Universidad Catolica
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Actuación","sede":"Casa Central","NEM":12,"Ranking":12,"Lectora":16,"M1":10,"M2":0,"Ciencias":0,"Historia":10,"Corte":792.18},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Administración Pública","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":20,"M1":30,"M2":0,"Ciencias":10,"Historia":10,"Corte":779.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Agronomía","sede":"San Joaquín","NEM":20,"Ranking":30,"Lectora":10,"M1":30,"M2":0,"Ciencias":10,"Historia":0,"Corte":723.20},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Antropología","sede":"San Joaquín","NEM":20,"Ranking":25,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":780.55},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Arqueología","sede":"San Joaquín","NEM":20,"Ranking":25,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":780.55},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Arquitectura","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":15,"M1":35,"M2":0,"Ciencias":10,"Historia":10,"Corte":871.20},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Arte","sede":"San Joaquín","NEM":20,"Ranking":30,"Lectora":20,"M1":15,"M2":0,"Ciencias":0,"Historia":15,"Corte":718.45},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Astronomía","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":35,"M2":0,"Ciencias":15,"Historia":0,"Corte":908.40},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Biología","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":25,"M2":0,"Ciencias":25,"Historia":0,"Corte":789.65},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Biología Marina","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":25,"M2":0,"Ciencias":25,"Historia":0,"Corte":783.35},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Bioquímica","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":30,"M2":0,"Ciencias":20,"Historia":0,"Corte":886.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Ciencia Política","sede":"Santiago","NEM":20,"Ranking":25,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":837.30},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"College Artes y Humanidades","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":25,"M1":25,"M2":0,"Ciencias":0,"Historia":10,"Corte":742.25},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"College Ciencias Naturales y Matemáticas","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":10,"M1":35,"M2":0,"Ciencias":15,"Historia":0,"Corte":859.65},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"College Ciencias Sociales","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":25,"M1":25,"M2":0,"Ciencias":0,"Historia":10,"Corte":762.50},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Construcción Civil","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":40,"M2":0,"Ciencias":10,"Historia":0,"Corte":711.10},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Derecho","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":25,"M1":10,"M2":0,"Ciencias":0,"Historia":25,"Corte":869.35},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Dirección Audiovisual","sede":"Casa Central","NEM":15,"Ranking":25,"Lectora":25,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":811.50},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Diseño","sede":"Santiago","NEM":25,"Ranking":25,"Lectora":20,"M1":20,"M2":0,"Ciencias":10,"Historia":10,"Corte":798.15},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Enfermería","sede":"San Joaquín","NEM":20,"Ranking":25,"Lectora":10,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":840.25},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Estadística","sede":"San Joaquín","NEM":20,"Ranking":10,"Lectora":10,"M1":45,"M2":5,"Ciencias":10,"Historia":0,"Corte":785.55},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Filosofía","sede":"San Joaquín","NEM":25,"Ranking":25,"Lectora":25,"M1":15,"M2":0,"Ciencias":0,"Historia":10,"Corte":673.95},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Física","sede":"San Joaquín","NEM":20,"Ranking":10,"Lectora":10,"M1":45,"M2":0,"Ciencias":15,"Historia":0,"Corte":884.15},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Fonoaudiología","sede":"Santiago","NEM":20,"Ranking":25,"Lectora":10,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":697.45},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Geografía","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":20,"M1":25,"M2":0,"Ciencias":0,"Historia":15,"Corte":658.40},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Historia","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":15,"M1":10,"M2":0,"Ciencias":0,"Historia":35,"Corte":736.15},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Ingeniería (Plan Común)","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":25,"M2":10,"Ciencias":15,"Historia":0,"Corte":899.95},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Ingeniería Comercial","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":10,"M1":30,"M2":10,"Ciencias":10,"Historia":10,"Corte":880.40},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Ingeniería en Recursos Naturales","sede":"San Joaquín","NEM":15,"Ranking":25,"Lectora":10,"M1":25,"M2":10,"Ciencias":15,"Historia":0,"Corte":677.25},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Ingeniería Forestal","sede":"San Joaquín","NEM":20,"Ranking":30,"Lectora":10,"M1":30,"M2":0,"Ciencias":10,"Historia":0,"Corte":723.20},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Interpretación Musical","sede":"Campus Oriente","NEM":12,"Ranking":12,"Lectora":12,"M1":14,"M2":0,"Ciencias":14,"Historia":14,"Corte":768.80},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Kinesiología","sede":"Santiago","NEM":20,"Ranking":25,"Lectora":10,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":801.95},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Letras Hispánicas","sede":"Santiago","NEM":25,"Ranking":25,"Lectora":25,"M1":15,"M2":0,"Ciencias":0,"Historia":10,"Corte":714.55},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Letras Inglesas","sede":"Santiago","NEM":25,"Ranking":25,"Lectora":25,"M1":15,"M2":0,"Ciencias":0,"Historia":10,"Corte":733.75},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Licenciatura en Ingeniería en Ciencia de Datos","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":30,"M2":10,"Ciencias":10,"Historia":0,"Corte":798.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Licenciatura en Ingeniería em Ciencia de la Computación","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":25,"M2":10,"Ciencias":15,"Historia":0,"Corte":810.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Matemática","sede":"San Joaquín","NEM":20,"Ranking":10,"Lectora":10,"M1":45,"M2":0,"Ciencias":15,"Historia":0,"Corte":827.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Medicina","sede":"Santiago","NEM":20,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":954.45},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Medicina Veterinaria","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":825.50},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Música","sede":"Santiago","NEM":25,"Ranking":25,"Lectora":25,"M1":25,"M2":0,"Ciencias":0,"Historia":10,"Corte":659.24},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Nutrición y Dietética","sede":"San Joaquín","NEM":20,"Ranking":25,"Lectora":10,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":760.15},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Odontología","sede":"San Joaquín","NEM":20,"Ranking":25,"Lectora":10,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":865.40},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación Especial","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":20,"Corte":725.60},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación Física y Salud para Educación Básica y Media","sede":"San Joaquín","NEM":20,"Ranking":30,"Lectora":10,"M1":30,"M2":0,"Ciencias":10,"Historia":0,"Corte":741.60},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación General Básica","sede":"San Joaquín","NEM":25,"Ranking":25,"Lectora":20,"M1":20,"M2":0,"Ciencias":10,"Historia":10,"Corte":690.00},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación Media en Ciencias Naturales y Biología","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":40,"M2":0,"Ciencias":10,"Historia":0,"Corte":765.60},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación Media en Física","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":40,"M2":0,"Ciencias":10,"Historia":0,"Corte":729.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación Media en Matemática","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":35,"M2":5,"Ciencias":10,"Historia":0,"Corte":808.35},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación Media en Química","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":40,"M2":0,"Ciencias":10,"Historia":0,"Corte":649.70},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Educación Parvularia","sede":"San Joaquín","NEM":25,"Ranking":25,"Lectora":20, "M1":20,"M2":0,"Ciencias":10,"Historia":10,"Corte":721.75},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Pedagogía en Inglés para Educación Básica y Media","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":30,"M1":20,"M2":0,"Ciencias":0,"Historia":10,"Corte":760.30},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Periodismo","sede":"Casa Central","NEM":15,"Ranking":25,"Lectora":25,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":811.50},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Psicología","sede":"San Joaquín","NEM":25,"Ranking":25,"Lectora":10,"M1":20,"M2":0,"Ciencias":20,"Historia":20,"Corte":880.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Publicidad","sede":"Casa Central","NEM":15,"Ranking":25,"Lectora":25,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":811.50},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Química","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":35,"M2":0,"Ciencias":15,"Historia":0,"Corte":847.40},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Química y Farmacia","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":10,"M1":35,"M2":0,"Ciencias":15,"Historia":0,"Corte":905.30},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Sociología","sede":"San Joaquín","NEM":20,"Ranking":25,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":703.40},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Teología","sede":"San Joaquín","NEM":25,"Ranking":25,"Lectora":25,"M1":10,"M2":0,"Ciencias":0,"Historia":15,"Corte":546.00},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Terapia Ocupacional","sede":"San Joaquín","NEM":20,"Ranking":20,"Lectora":20,"M1":20,"M2":0,"Ciencias":20,"Historia":0,"Corte":746.80},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Trabajo Social","sede":"San Joaquín","NEM":25,"Ranking":25,"Lectora":15,"M1":15,"M2":0,"Ciencias":0,"Historia":20,"Corte":690.40},
        
        
    ]
    return pd.DataFrame(data)

import streamlit as st
import pandas as pd

# ===== Carga de Carreras =====
@st.cache_data
def cargar_ponderaciones(force_update=False):
    data = [
        # Universidad de Chile
        {"universidad": "Universidad de Chile", "carrera": "Ingeniería y Ciencias (Plan Común)", "sede": "Beauchef",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0, "Corte": 500},

        # Pontificia Universidad Católica de Chile
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Actuación","sede":"Casa Central",
         "NEM":12,"Ranking":12,"Lectora":16,"M1":10,"M2":0,"Ciencias":0,"Historia":10,"Corte":792.18},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Administración Pública","sede":"Santiago",
         "NEM":20,"Ranking":20,"Lectora":20,"M1":30,"M2":0,"Ciencias":10,"Historia":10,"Corte":779.90},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Agronomía","sede":"San Joaquín",
         "NEM":20,"Ranking":30,"Lectora":10,"M1":30,"M2":0,"Ciencias":10,"Historia":0,"Corte":723.20},
        {"universidad":"Pontificia Universidad Católica de Chile","carrera":"Antropología","sede":"San Joaquín",
         "NEM":20,"Ranking":25,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":780.55},
        # ... agregar todas las demás carreras aquí
    ]
    return pd.DataFrame(data)

# ===== Cargar datos =====
df = cargar_ponderaciones()

# ===== Streamlit App =====
st.title("Buscador de Carreras UC y U. de Chile")

# Selección de universidad
universidad = st.selectbox("Selecciona universidad", df["universidad"].unique())

# Filtrar carreras de la universidad seleccionada
carreras_univ = df[df["universidad"] == universidad]["carrera"].sort_values()
carrera = st.selectbox("Selecciona carrera", carreras_univ)

# Mostrar los datos de la carrera seleccionada en una tabla
df_seleccion = df[(df["universidad"] == universidad) & (df["carrera"] == carrera)]

if not df_seleccion.empty:
    st.subheader(f"Datos de la carrera: {carrera}")

    # Mostrar información general
    st.table(df_seleccion[["sede","Corte"]].reset_index(drop=True))

    # Mostrar ponderaciones (%) para cálculo
    st.subheader("Ponderaciones (%)")
    ponderaciones_cols = ["NEM","Ranking","Lectora","M1","M2","Ciencias","Historia"]
    st.table(df_seleccion[ponderaciones_cols].reset_index(drop=True))

else:
    st.warning("No se encontraron datos para la carrera seleccionada.")


# ===== Sidebar: datos del postulante =====
with st.sidebar:
    st.header("👤 Datos del postulante")
    nombre = st.text_input("Nombre del alumno", "")
    curso = st.text_input("Curso", "")

# ===== Título principal =====
st.title("Asistente de postulaciones 🎓 \n Admisión 2026")

# ===== Logos de universidades =====
logos_universidad = {
    "Pontificia Universidad Católica de Chile": "logos_universidad/u_catolica.png",
    "Universidad de Chile": "logos_universidad/u_chile.png",
    # agrega más universidades y sus logos
}

# ===== SECCIÓN UNIVERSIDAD Y CARRERA =====
st.subheader("Universidad y Carrera")

uni = None
universidades = sorted(ponderaciones_df["universidad"].unique())
for u in universidades:
    logo_path = logos_universidad.get(u, None)
    col1, col2 = st.columns([0.1, 0.9])
    with col1:
        if logo_path and os.path.exists(logo_path):
            st.image(logo_path, width=30)
    with col2:
        if st.button(u, key=u):
            uni = u

# Selección de carrera y sede
if uni:
    carreras = sorted(ponderaciones_df.loc[ponderaciones_df["universidad"]==uni, "carrera"].unique())
    car = st.selectbox("Carrera", [""] + carreras)
    if car:
        sedes = sorted(ponderaciones_df.loc[(ponderaciones_df["universidad"]==uni) & (ponderaciones_df["carrera"]==car), "sede"].unique())
        sede = st.selectbox("Sede", [""] + list(sedes))

# ===== COLUMNAS DE PUNTAJES Y PONDERACIONES =====
colPAES, colPond = st.columns([1, 1])

with colPAES:
    st.subheader("Puntajes PAES (100–1000)")
    nem = st.number_input("NEM", min_value=100, max_value=1000, value=100)
    ranking = st.number_input("Ranking", min_value=100, max_value=1000, value=100)
    cl = st.number_input("Competencia Lectora", min_value=100, max_value=1000, value=100)
    m1 = st.number_input("Matemática 1 (M1)", min_value=100, max_value=1000, value=100)
    m2 = st.number_input("Matemática 2 (M2)", min_value=0, max_value=1000, value=0)
    opcion_ch = st.radio("Prueba Electiva", ["Ciencias", "Historia"], horizontal=True)
    cs = st.number_input("Ciencias", min_value=0, max_value=1000, value=0)
    hs = st.number_input("Historia y Cs. Sociales", min_value=0, max_value=1000, value=0)

    # Puntaje de corte seguro
    if uni and car:
        fila_corte = ponderaciones_df.loc[(ponderaciones_df["universidad"]==uni) & (ponderaciones_df["carrera"]==car)]
        corte_default = int(fila_corte["Corte"].values[0]) if not fila_corte.empty else 500
    else:
        corte_default = 500

    corte = st.number_input("Puntaje último matriculado (100–1000)", min_value=100, max_value=1000, value=corte_default)

with colPond:
    st.subheader("Ponderaciones (%)")
    if uni and car:
        fila = ponderaciones_df.loc[(ponderaciones_df["universidad"]==uni) & (ponderaciones_df["carrera"]==car)]
        p_nem_default = int(fila["NEM"].values[0])
        p_rank_default = int(fila["Ranking"].values[0])
        p_lec_default = int(fila["Lectora"].values[0])
        p_m1_default = int(fila["M1"].values[0])
        p_m2_default = int(fila["M2"].values[0])
        p_cie_default = int(fila["Ciencias"].values[0])
        p_his_default = int(fila["Historia"].values[0])
    else:
        p_nem_default = p_rank_default = p_lec_default = p_m1_default = p_m2_default = p_cie_default = p_his_default = 0

    p_nem = st.number_input("Ponderación NEM", min_value=0, max_value=100, value=p_nem_default)
    p_rank = st.number_input("Ponderación Ranking", min_value=0, max_value=100, value=p_rank_default)
    p_lec = st.number_input("Ponderación Comp. Lectora", min_value=0, max_value=100, value=p_lec_default)
    p_m1  = st.number_input("Ponderación Matemática 1 (M1)", min_value=0, max_value=100, value=p_m1_default)
    p_m2  = st.number_input("Ponderación Matemática 2 (M2)", min_value=0, max_value=100, value=p_m2_default)
    p_cie = st.number_input("Ponderación Ciencias", min_value=0, max_value=100, value=p_cie_default)
    p_his = st.number_input("Ponderación Historia", min_value=0, max_value=100, value=p_his_default)

    suma_p = p_nem + p_rank + p_lec + p_m1 + p_m2 + p_cie + p_his
    if suma_p != 100:
        st.warning(f"La suma de ponderaciones debe ser 100%. Actual: {suma_p}%")

# ===== Botón Calcular =====
if st.button("PONDERAR"):
    opt_cie = cs if opcion_ch=="Ciencias" else 0
    opt_his = hs if opcion_ch=="Historia" else 0
    p_opt_cie = p_cie if opcion_ch=="Ciencias" else 0
    p_opt_his = p_his if opcion_ch=="Historia" else 0

    ptotal = (
        nem * p_nem/100 + ranking * p_rank/100 + cl * p_lec/100 +
        m1 * p_m1/100 + m2 * p_m2/100 +
        opt_cie * p_opt_cie/100 + opt_his * p_opt_his/100
    )

    progreso = min((ptotal / corte) * 100, 100)
    st.success(f"**{nombre or 'Postulante'}**, tu puntaje ponderado es **{ptotal:.2f}**.")
    if ptotal >= corte:
        st.info(f"Estás sobre el corte por {ptotal-corte:.2f} puntos ({progreso:.1f}% del corte).")
    else:
        st.warning(f"No alcanzas el corte ({corte}). Progreso: {progreso:.1f}%.")

# ===== Información de la fuente =====
st.info(
    "Toda la información presentada en esta plataforma ha sido recopilada y organizada a partir "
    "de los datos oficiales publicados por el Departamento de Evaluación, Medición y Registro Educacional (DEMRE) de la Universidad de Chile."
)






