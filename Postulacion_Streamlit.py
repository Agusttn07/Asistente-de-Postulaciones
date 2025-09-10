# Postulacion_Streamlit.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Asistente de Postulaciones", page_icon="🎓", layout="wide")

# ===== Mensaje emergente de Bienvenida con Session State =====
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

if st.session_state.show_welcome:
    st.markdown("""
        <style>
        /* Popup principal */
        .welcome-popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: #e6f0fa;
            border: 2px solid #1f77b4;
            border-radius: 20px;
            padding: 40px 20px;
            z-index: 9999;
            width: 70%;
            max-width: 500px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            color: #000000;
            font-family: Arial, sans-serif;
        }
        h2 {
            color: #1f77b4;
            font-size: 24px;
            margin-bottom: 15px;
        }
        p {
            font-size: 16px;
            color: #000000;
            margin: 0 10px;
        }
        /* Botón X */
        .close-btn {
            position: absolute;
            top: 10px;
            right: 15px;
            font-size: 20px;
            font-weight: bold;
            color: #1f77b4;
            cursor: pointer;
            background: none;
            border: none;
        }
        /* Responsivo para celular */
        @media only screen and (max-width: 600px) {
            .welcome-popup {
                width: 90%;
                padding: 30px 15px;
            }
            h2 { font-size: 20px; }
            p { font-size: 14px; }
        }
        </style>
        <div class="welcome-popup">
            <button class="close-btn" onclick="document.getElementById('popup-close').click()">×</button>
            <h2>🎓 Bienvenido al Asistente de Postulaciones!</h2>
            <p>En esta página podrás simular tus puntajes en la universidad y carrera que desees.</p>
        </div>
    """, unsafe_allow_html=True)

    # Botón invisible de Streamlit para cerrar popup
    if st.button("popup-close", key="popup-close"):
        st.session_state.show_welcome = False

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
    data = [
        {"universidad": "Universidad de Chile", "carrera": "Ingeniería y Ciencias (Plan Común)", "sede": "Santiago",
         "NEM": 0, "Ranking": 0, "Lectora": 0, "M1": 0, "M2": 0, "Ciencias": 0, "Historia": 0, "Corte": 500},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Ingeniería (Plan Común)", "sede": "San Joaquín",
         "NEM": 20, "Ranking": 20, "Lectora": 10, "M1": 25, "M2": 10, "Ciencias": 15, "Historia": 0, "Corte": 900},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Medicina", "sede": "Casa Central",
         "NEM": 20, "Ranking": 20, "Lectora": 15, "M1": 20, "M2": 0, "Ciencias": 25, "Historia": 0, "Corte": 955},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Derecho", "sede": "Casa Central",
         "NEM": 20, "Ranking": 20, "Lectora": 25, "M1": 10, "M2": 0, "Ciencias": 0, "Historia": 25, "Corte": 870},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Enfermería", "sede": "San Joaquín",
         "NEM": 20, "Ranking": 25, "Lectora": 10, "M1": 20, "M2": 0, "Ciencias": 25, "Historia": 0, "Corte": 841},
        {"universidad": "Pontificia Universidad Católica de Chile", "carrera": "Arquitectura", "sede": "Lo Contador",
         "NEM": 20, "Ranking": 20, "Lectora": 15, "M1": 35, "M2": 0, "Ciencias": 10, "Historia": 10, "Corte": 872},
    ]
    return pd.DataFrame(data)

ponderaciones_df = cargar_ponderaciones(force_update=True)

# ===== Sidebar: datos del postulante =====
with st.sidebar:
    st.header("👤 Datos del postulante")
    nombre = st.text_input("Nombre del alumno", "")
    curso = st.text_input("Curso", "")

st.title("Asistente de postulaciones 🎓 \n Admisión 2026")

# ===== Layout principal =====
colL, colC, colR = st.columns([1.2, 1.1, 1.2], gap="large")

# ===== Universidad y Carrera =====
with colL:
    st.subheader("Universidad y Carrera")
    universidades = sorted(ponderaciones_df["universidad"].unique())
    universidades.append("Otra")
    uni = st.selectbox("Universidad", universidades, index=None)

    if uni != "Otra":
        carreras = sorted(ponderaciones_df.loc[ponderaciones_df["universidad"]==uni, "carrera"].unique())
        car = st.selectbox("Carrera", carreras if carreras else [], index=None)
        sedes = sorted(ponderaciones_df.loc[(ponderaciones_df["universidad"]==uni) & (ponderaciones_df["carrera"]==car), "sede"].unique()) if uni and car else []
        sede = st.selectbox("Sede", sedes if sedes else [], index=None)
    else:
        car = st.text_input("Carrera (otra)", "")
        sede = st.text_input("Sede (otra)", "")

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

    if uni != "Otra" and car:
        corte_default = int(ponderaciones_df.loc[(ponderaciones_df["universidad"]==uni) & (ponderaciones_df["carrera"]==car), "Corte"].values[0])
    else:
        corte_default = 500
    corte = st.number_input("Puntaje último matriculado (100–1000)", min_value=100, max_value=1000, value=corte_default)

# ===== Ponderaciones =====
with colR:
    st.subheader("Ponderaciones (%)")
    if uni != "Otra" and car:
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
