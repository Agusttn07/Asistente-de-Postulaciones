# Postulacion_Streamlit.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistente de Postulaciones", page_icon="🎓", layout="wide")

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

# ===== Carga de Carreras =====
@st.cache_data
def cargar_ponderaciones(force_update=False):
    """
    Dataset con muchas universidades y carreras. Todas las ponderaciones iniciales en 0.
    """
    data = [
        # Universidad de Chile
        {"universidad": "Universidad de Chile", "carrera": "Ingeniería y Ciencias (Plan Común)", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Chile", "carrera": "Medicina", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Chile", "carrera": "Derecho", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Chile", "carrera": "Arquitectura", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},

        # Universidad Católica de Chile
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Ingeniería (Plan Común)", "sede": "San Joaquin",
         "NEM": 20, "Ranking": 20, "Lectora": 10, "M1": 25, "M2": 10, "Ciencias": 15, "Historia": 0},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Medicina", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Arquitectura", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Derecho", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},

        # Universidad de Santiago de Chile
        {"universidad": "Universidad de Santiago de Chile", "carrera": "Arquitectura", "sede": "Concepción",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Santiago de Chile", "carrera": "Ingeniería Civil", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Santiago de Chile", "carrera": "Enfermería", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},

        # Universidad de Concepción
        {"universidad": "Universidad de Concepción", "carrera": "Medicina", "sede": "Concepción",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Concepción", "carrera": "Arquitectura", "sede": "Concepción",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Concepción", "carrera": "Derecho", "sede": "Concepción",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},

        # Universidad Austral de Chile
        {"universidad": "Universidad Austral de Chile", "carrera": "Medicina Veterinaria", "sede": "Valdivia",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad Austral de Chile", "carrera": "Ingeniería Forestal", "sede": "Valdivia",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},

        # Universidad de Valparaíso
        {"universidad": "Universidad de Valparaíso", "carrera": "Pedagogía en Matemática", "sede": "Valparaíso",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad de Valparaíso", "carrera": "Derecho", "sede": "Valparaíso",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},

        # Universidad Técnica Federico Santa María
        {"universidad": "Universidad Técnica Federico Santa María", "carrera": "Ingeniería Civil", "sede": "Valparaíso",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad Técnica Federico Santa María", "carrera": "Ingeniería en Computación", "sede": "Valparaíso",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},

        # Universidad Católica del Norte
        {"universidad": "Universidad Católica del Norte", "carrera": "Ingeniería Civil", "sede": "Antofagasta",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
        {"universidad": "Universidad Católica del Norte", "carrera": "Arquitectura", "sede": "Antofagasta",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0},
    ]
    return pd.DataFrame(data)

ponderaciones_df = cargar_ponderaciones(force_update=True)

# ===== Sidebar: datos del postulante =====
with st.sidebar:
    st.header("👤 Datos del postulante")
    nombre = st.text_input("Nombre del alumno", "")
    curso = st.text_input("Curso", "")

st.title("Asistente 🎓 \n Admisión 2026")

# ===== Layout principal =====
colL, colC, colR = st.columns([1.2, 1.1, 1.2], gap="large")

# ===== Universidad y Carrera =====
with colL:
    st.subheader("Universidad y Carrera")
    universidades = sorted(ponderaciones_df["universidad"].unique())
    uni = st.selectbox("Universidad", universidades, index=None)
    carreras = sorted(ponderaciones_df.loc[ponderaciones_df["universidad"]==uni, "carrera"].unique()) if uni else []
    car = st.selectbox("Carrera", carreras if carreras else [], index=None)
    sedes = sorted(ponderaciones_df.loc[(ponderaciones_df["universidad"]==uni) & (ponderaciones_df["carrera"]==car), "sede"].unique()) if uni and car else []
    sede = st.selectbox("Sede", sedes if sedes else [], index=None)

# ===== Puntajes =====
with colC:
    st.subheader("Puntajes PAES (100–1000)")
    nem = st.number_input("NEM", min_value=100, max_value=1000, value=100)
    ranking = st.number_input("Ranking", min_value=100, max_value=1000, value=100)
    cl = st.number_input("Competencia Lectora", min_value=100, max_value=1000, value=100)
    m1 = st.number_input("Matemática 1 (M1)", min_value=100, max_value=1000, value=100)
    m2 = st.number_input("Matemática 2 (M2)", min_value=0, max_value=1000, value=0)
    opcion_ch = st.radio("Prueba Electiva", ["Ciencias", "Historia"], horizontal=True)
    cs = st.number_input("Ciencias", min_value=0, max_value=1000, value=0)
    hs = st.number_input("Historia y Cs. Sociales", min_value=0, max_value=1000, value=0)
    corte = st.number_input("Puntaje último matriculado (100–1000)", min_value=100, max_value=1000, value=500)

# ===== Ponderaciones =====
with colR:
    st.subheader("Ponderaciones (%)")
    p_nem = st.number_input("Ponderación NEM", min_value=0, max_value=100, value=0)
    p_rank = st.number_input("Ponderación Ranking", min_value=0, max_value=100, value=0)
    p_lec = st.number_input("Ponderación Comp. Lectora", min_value=0, max_value=100, value=0)
    p_m1  = st.number_input("Ponderación Matemática 1 (M1)", min_value=0, max_value=100, value=0)
    p_m2  = st.number_input("Ponderación Matemática 2 (M2)", min_value=0, max_value=100, value=0)
    p_cie = st.number_input("Ponderación Ciencias", min_value=0, max_value=100, value=0)
    p_his = st.number_input("Ponderación Historia", min_value=0, max_value=100, value=0)

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
