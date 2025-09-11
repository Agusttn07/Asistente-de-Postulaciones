# Postulacion_Streamlit.py
import streamlit as st
import pandas as pd
from typing import Optional

st.set_page_config(page_title="Asistente de Postulaciones", page_icon="🎓", layout="wide")

st.title("Asistente de postulaciones 🎓")

st.markdown(
    """
    <h2 style="color:#6E7DAB; margin-top: -15px;">
        Admisión 2026
    </h2>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div style="background-color:#d6e4ff; padding:12px; border-radius:10px; border:1px solid #99b3ff; margin-bottom:15px;">
        📌 <b style="color:black;">¿No conoces las ponderaciones de alguna universidad?</b><br>
        👉 <a href="https://demre.cl/publicaciones/2025/2025-24-09-25-oferta-carreras-vacantes-ponderaciones-p2025" target="_blank" style="color:#1a73e8; text-decoration:none; font-weight:bold;">
        Haz clic aquí para ver la oferta oficial en el DEMRE
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


# ===== Utilidades =====
def safe_int(x: Optional[str]) -> Optional[int]:
    try:
        return int(str(x).strip())
    except:
        return None

def clamp_0_1000(x: Optional[str]) -> Optional[float]:
    if x is None or x == "":
        return None
    try:
        v: float = float(x)
        if v < 0:
            return 0.0
        if v > 1000:
            return 1000.0
        return v
    except:
        return None

# ===== Normalizador de opciones =====
@st.cache_data
def normalizar_texto(texto: str) -> str:
    return texto.lower().replace("á", "a").replace("é", "e") \
                       .replace("í", "i").replace("ó", "o") \
                       .replace("ú", "u").replace("ñ", "n") \
                       .strip()

# ===== Cargar carreras =====
df_carreras = pd.DataFrame(cargar_ponderaciones())

# ===== Selección de filtros =====
universidades = sorted(df_carreras['universidad'].unique())
universidad_sel = st.selectbox("Selecciona Universidad", universidades)

df_filtrado = df_carreras[df_carreras['universidad'] == universidad_sel]

carreras = sorted(df_filtrado['carrera'].unique())
carrera_sel = st.selectbox("Selecciona Carrera", carreras)

df_filtrado_carrera = df_filtrado[df_filtrado['carrera'] == carrera_sel]

sedes = sorted(df_filtrado_carrera['sede'].unique())
sede_sel = st.selectbox("Selecciona Sede", sedes)

# ===== Mostrar ponderaciones y corte =====
df_resultado = df_filtrado_carrera[df_filtrado_carrera['sede'] == sede_sel]
df_resultado_display = df_resultado[['NEM','Ranking','Lectora','M1','M2','Ciencias','Historia','Corte']]

st.markdown(f"### Resultados para {carrera_sel} - {sede_sel}")
st.dataframe(df_resultado_display)


@st.cache_data
def cargar_ponderaciones(force_update=False):
    data = [
        #Universidad de Chile
        {"universidad":"Universidad de Chile","carrera":"Artes Visuales, Lic. en Artes con mención en","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":35,"M1":10,"M2":0,"Ciencias":25,"Historia":0,"Corte":645.05},
        {"universidad":"Universidad de Chile","carrera":"Danza","sede":"Casa Central","NEM":10,"Ranking":10,"Lectora":10,"M1":10,"M2":0,"Ciencias":10,"Historia":0,"Corte":741.00},
        {"universidad":"Universidad de Chile","carrera":"Diseño Teatral","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":25,"M1":20,"M2":0,"Ciencias":25,"Historia":0,"Corte":616.50},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería en Sonido","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":30,"M2":10,"Ciencias":0,"Historia":10,"Corte":789.90},
        {"universidad":"Universidad de Chile","carrera":"Teoría de la Música","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":30,"M1":15,"M2":0,"Ciencias":25,"Historia":0,"Corte":636.5},
        {"universidad":"Universidad de Chile","carrera":"Teoría e Historia del Arte, con mención en Lic. en Artes","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":35,"M1":10,"M2":0,"Ciencias":25,"Historia":0,"Corte":540.55},
        {"universidad":"Universidad de Chile","carrera":"Composición","sede":"Casa Central","NEM":10,"Ranking":10,"Lectora":10,"M1":10,"M2":0,"Ciencias":10,"Historia":0,"Corte":637.60},
        {"universidad":"Universidad de Chile","carrera":"Biología, Lic. en Ciencias","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":15,"M2":15,"Ciencias":20,"Historia":0,"Corte":694.75},
        {"universidad":"Universidad de Chile","carrera":"Biología con mención en Medio Ambiente","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":10,"M2":15,"Ciencias":25,"Historia":0,"Corte":706.35},
        {"universidad":"Universidad de Chile","carrera":"Física, Lic. en Ciencias con mención en","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":20,"M2":20,"Ciencias":10,"Historia":0,"Corte":793.40},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería en Biotecnología Molecular","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":10,"M2":15,"Ciencias":25,"Historia":0,"Corte":831.45},
        {"universidad":"Universidad de Chile","carrera":"Matemáticas, Lic. en Ciencias","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":20,"M2":20,"Ciencias":10,"Historia":0,"Corte":610.70},
        {"universidad":"Universidad de Chile","carrera":"Pedagogía en Ed. Media en Biología y Química","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":15,"M2":10,"Ciencias":25,"Historia":0,"Corte":508.60},
        {"universidad":"Universidad de Chile","carrera":"Pedagogía en Ed. Media en Matemática y Física","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":20,"M2":15,"Ciencias":15,"Historia":0,"Corte":637.40},
        {"universidad":"Universidad de Chile","carrera":"Química, Lic. en Ciencias","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":10,"M2":15,"Ciencias":25,"Historia":0,"Corte":578.10},
        {"universidad":"Universidad de Chile","carrera":"Química Ambiental","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":10,"M2":15,"Ciencias":25,"Historia":0,"Corte":616.2},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería Agronómica","sede":"Casa Central","NEM":20,"Ranking":40,"Lectora":10,"M1":20,"M2":0,"Ciencias":10,"Historia":10,"Corte":637.50},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería en Recursos Naturales Renovables","sede":"Casa Central","NEM":20,"Ranking":40,"Lectora":10,"M1":15,"M2":5,"Ciencias":10,"Historia":10,"Corte":538.55},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería (Plan Común)","sede":"Casa Central","NEM":10,"Ranking":25,"Lectora":10,"M1":20,"M2":20,"Ciencias":15,"Historia":0,"Corte":834.65},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería Forestal","sede":"Casa Central","NEM":10,"Ranking":35,"Lectora":10,"M1":25,"M2":0,"Ciencias":20,"Historia":20,"Corte":437.7},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería en Recursos Hídricos","sede":"Casa Central","NEM":10,"Ranking":30,"Lectora":10,"M1":25,"M2":5,"Ciencias":20,"Historia":20,"Corte":508.45},
        {"universidad":"Universidad de Chile","carrera":"Bioquímica","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":10,"M1":20,"M2":10,"Ciencias":30,"Historia":0,"Corte":794.40},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería en Alimentos","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":10,"M1":20,"M2":10,"Ciencias":30,"Historia":0,"Corte":632.80},
        {"universidad":"Universidad de Chile","carrera":"Química","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":10,"M1":20,"M2":10,"Ciencias":30,"Historia":0,"Corte":726.70},
        {"universidad":"Universidad de Chile","carrera":"Química y Farmacia","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":10,"M1":20,"M2":10,"Ciencias":30,"Historia":0,"Corte":801.60},
        {"universidad":"Universidad de Chile","carrera":"Antropología - Arqueología","sede":"Casa Central","NEM":20,"Ranking":20,"Lectora":20,"M1":15,"M2":0,"Ciencias":25,"Historia":25,"Corte":742.4},
        {"universidad":"Universidad de Chile","carrera":"Pedagogía en Educación Parvularia","sede":"Casa Central","NEM":30,"Ranking":20,"Lectora":20,"M1":15,"M2":0,"Ciencias":15,"Historia":15,"Corte":669},
        {"universudad":"Universidad de Chile","carrera":"Psicología","sede":"Casa Central","NEM":10,"Ranking":30,"Lectora":25,"M1":20,"M2":0,"Ciencias":15,"Historia":15,"Corte":862.95},
        {"universidad":"Universidad de Chile","carrera":"Sociología","sede":"Casa Central","NEM":20,"Ranking":20,"Lectora":25,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":709.15},
        {"universidad":"Universidad de Chile","carrera":"Trabajo Social","sede":"Casa Central","NEM":20,"Ranking":20,"Lectora":25,"M1":20,"M2":0,"Ciencias":15,"Historia":15,"Corte":680.55},
        {"universidad":"Universidad de Chile","carrera":"Pedagogía en Educación Física","sede":"Casa Central","NEM":20,"Ranking":20,"Lectora":20,"M1":15,"M2":0,"Ciencias":25,"Historia":25,"Corte":665.15},
        {"universidad":"Universidad de Chile","carrera":"Pedagogía en Educación Especial","sede":"Casa Central","NEM":20,"Ranking":20,"Lectora":20,"M1":20,"M2":0,"Ciencias":20,"Historia":20,"Corte":648.00},
        {"universidad":"Universidad de Chile","carrera":"Medicina Veterinaria","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":35,"M2":0,"Ciencias":15,"Historia":0,"Corte":766.20},
        {"universidad":"Universidad de Chile","carrera":"Cine y Televisión","sede":"Casa Central","NEM":15,"Ranking":25,"Lectora":25,"M1":20,"M2":0,"Ciencias":15,"Historia":15,"Corte":724.6},
        {"universidad":"Universidad de Chile","carrera":"Periodismo","sede":"Casa Central","NEM":15,"Ranking":25,"Lectora":25,"M1":20,"M2":0,"Ciencias":0,"Historia":15,"Corte":718.25},
        {"universidad":"Universidad de Chile","carrera":"Derecho, Lic. en Ciencias Jurídicas y Sociales","sede":"Casa Central","NEM":20,"Ranking":20,"Lectora":25,"M1":10,"M2":0,"Ciencias":0,"Historia":25,"Corte":844.9},
        {"universidad":"Universidad de Chile","carrera":"Contador Auditor","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":10,"M1":35,"M2":15,"Ciencias":10,"Historia":10,"Corte":764.35},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería en Información y Control de Gestión","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":10,"M1":35,"M2":15,"Ciencias":10,"Historia":10,"Corte":777.65},
        {"universidad":"Universidad de Chile","carrera":"Ingeniería Comercial","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":10,"M1":35,"M2":15,"Ciencias":10,"Historia":10,"Corte":833.75},
        {"universidad":"Universidad de Chile","carrera":"Estudios Internacionales","sede":"Casa Central","NEM":15,"Ranking":20,"Lectora":25,"M1":20,"M2":0,"Ciencias":20,"Historia":20,"Corte":836.85},
        {"universidad":"Universidad de Chile","carrera":"Filosofía, Licenciatura en","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":35,"M1":15,"M2":0,"Ciencias":20,"Historia":20,"Corte":464.05},
        {"universidad":"Universidad de Chile","carrera":"Historia, Licenciatura en","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":15,"M2":0,"Ciencias":35,"Historia":35,"Corte":688.40},
        {"universidad":"Universidad de Chile","carrera":"Lingüística y Literatura con mención, Lic. en","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":35,"M1":15,"M2":0,"Ciencias":20,"Historia":20,"Corte":623.4},
        {"universidad":"Universidad de Chile","carrera":"Lingüística y Literatura Inglesas, Lic. en","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":30,"M1":15,"M2":0,"Ciencias":25,"Historia":25,"Corte":542.25},
        {"universidad":"Universidad de Chile","carrera":"Pedagogía en Educación Básica","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":25,"M1":25,"M2":0,"Ciencias":20,"Historia":20,"Corte":662.45},
        {"universidad":"Universidad de Chile","carrera":"Administración Pública","sede":"Casa Central","NEM":10,"Ranking":30,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":20,"Corte":759.6},
        {"universidad":"Universidad de Chile","carrera":"Ciencia Política","sede":"Casa Central","NEM":10,"Ranking":30,"Lectora":20,"M1":20,"M2":0,"Ciencias":0,"Historia":20,"Corte":770.6},
        {"universidad":"Universidad de Chile","carrera":"Enfermería","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":783.75},
        {"universidad":"Universidad de Chile","carrera":"Fonoaudiología","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":619.10},
        {"universidad":"Universidad de Chile","carrera":"Kinesiología","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":760.45},
        {"universidad":"Universidad de Chile","carrera":"Medicina","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":924.80},
        {"universidad":"Universidad de Chile","carrera":"Nutrición y Dietética","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":693.2},
        {"universidad":"Universidad de Chile","carrera":"Obstetricia y Puericultura","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":778.9},
        {"universidad":"Universidad de Chile","carrera":"Tecnología Médica","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":796.2},
        {"universidad":"Universidad de Chile","carrera":"Terapia Ocupacional","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":20,"M1":20,"M2":0,"Ciencias":30,"Historia":0,"Corte":689.2},
        {"universidad":"Universidad de Chile","carrera":"Odontología","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":782.8},
        {"universidad":"Universidad de Chile","carrera":"Programa Académico de Bachillerato","sede":"Casa Central","NEM":10,"Ranking":20,"Lectora":15,"M1":20,"M2":0,"Ciencias":35,"Historia":0,"Corte":800.35},



        #Universidad Técnica Federico Santa María
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Arquitectura (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":737.25},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Arquitectura (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":759.90},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Construcción Civil","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":625.95},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":747.35},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":798.45},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Ambiental","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":690.35},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil de Minas","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":799.35},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Eléctrica (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":782.30},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Eléctrica (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":803.45},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Electrónica","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":748.95},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil en Biotecnología","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":756.85},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Física (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":718.50},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Física (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":762.05},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Industrial (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":810.65},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Industrial (Vitacura)","sede":"Campus Santiago Vitacura","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":840.05},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Informática (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":771.15},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Informática (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":830.00},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Matemática (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":795.95},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Matemática (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":815.35},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Mecánica (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":758.55},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Mecánica (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":811.35},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Metalúrgica","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":730.30},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Plan Común (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":745.50},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Plan Común (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":815.60},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Química (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":769.25},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Química (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":806.95},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Telemática (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":685.95},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Civil Telemática (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":750.00},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Comercial (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":724.90},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería Comercial (Vitacura)","sede":"Campus Santiago Vitacura","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":786.45},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Aviación Comercial","sede":"Campus Santiago Vitacura","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":709.40},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Biotecnología (Viña del Mar)","sede":"Sede Viña Del Mar","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":598.10},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Biotecnología (Concepción)","sede":"Sede Concepción","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":545.05},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Diseño de Productos (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":624.90},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Diseño de Productos (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":638.50},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Fabricación y Diseño Industrial","sede":"Sede Viña Del Mar","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":583.00},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Informática (Viña del Mar)","sede":"Sede Viña Del Mar","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":663.30},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Informática (Concepción)","sede":"Sede Concepcion","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":591.60},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Mantenimiento Industrial (Viña del Mar)","sede":"Sede Viña Del Mar","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":587.90},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Mantenimiento Industrial (Concepción)","sede":"Sede Concepcion","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":593.05},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Prevención de Riesgos Laborales y Ambientales (Viña del Mar)","sede":"Sede Viña Del Mar","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":544.20},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Ingeniería en Prevención de Riesgos Laborales y Ambientales (Concepción)","sede":"Sede Concepcion","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":500.70},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Licenciatura en Astrofísica (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":706.45},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Licenciatura en Astrofísica (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":738.55},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Licenciatura en Física (Valparaíso)","sede":"Campus Casa Central Valparaíso","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":694.15},
        {"universidad":"Universidad Técnica Federico Santa María","carrera":"Licenciatura en Física (San Joaquin)","sede":"Campus Santiago San Joaquin","NEM":15,"Ranking":20,"Lectora":10,"M1":35,"M2":10,"Ciencias":10,"Historia":10,"Corte":721.70},





         

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

ponderaciones_df: pd.DataFrame = cargar_ponderaciones(force_update=True)

# ===== Sidebar: datos del postulante =====
with st.sidebar:
    st.header("👤 Datos del postulante")
    nombre: str = st.text_input("Nombre del alumno", "")
    curso: str = st.text_input("Curso", "")

# ===== Layout principal =====
colL, colC, colR = st.columns([1.2, 1.1, 1.2], gap="large")

# ===== Universidad y Carrera =====
with colL:
    st.subheader("Universidad y Carrera")
    universidades = sorted(ponderaciones_df["universidad"].astype(str).unique().tolist())
    universidades.append("Otra")
    uni: str = st.selectbox("Universidad", universidades, index=None)

    if uni != "Otra":
        carreras: list[str] = sorted(
            ponderaciones_df.loc[ponderaciones_df["universidad"] == uni, "carrera"].unique()
        )
        car: str = st.selectbox("Carrera", carreras if carreras else [], index=None)

        sedes: list[str] = sorted(
            ponderaciones_df.loc[
                (ponderaciones_df["universidad"] == uni) & (ponderaciones_df["carrera"] == car),
                "sede"
            ].unique()
        ) if uni and car else []
        sede: str = st.selectbox("Sede", sedes if sedes else [], index=None)
    else:
        car: str = st.text_input("Carrera (otra)", "")
        sede: str = st.text_input("Sede (otra)", "")

# ===== Puntajes =====
with colC:
    st.subheader("Puntajes PAES (100–1000)")
    nem: int = st.number_input("NEM", min_value=100, max_value=1000, value=100)
    ranking: int = st.number_input("Ranking", min_value=100, max_value=1000, value=100)
    cl: int = st.number_input("Competencia Lectora", min_value=100, max_value=1000, value=100)
    m1: int = st.number_input("Matemática 1 (M1)", min_value=100, max_value=1000, value=100)
    m2: int = st.number_input("Matemática 2 (M2)", min_value=0, max_value=1000, value=0)

    opcion_ch: str = st.radio("Prueba Electiva", ["Ciencias", "Historia"], horizontal=True)
    cs: int = st.number_input("Ciencias", min_value=0, max_value=1000, value=0)
    hs: int = st.number_input("Historia y Cs. Sociales", min_value=0, max_value=1000, value=0)

    # Puntaje de corte por carrera
    corte_default: int = int(
        ponderaciones_df.loc[(ponderaciones_df["universidad"] == uni) & (ponderaciones_df["carrera"] == car), "Corte"].values[0]
    ) if uni != "Otra" and car else 500
    corte: int = st.number_input(
        "Puntaje último matriculado (100–1000)", min_value=100, max_value=1000, value=corte_default
    )

# ===== Ponderaciones =====
with colR:
    st.subheader("Ponderaciones (%)")
    if uni != "Otra" and car:
        fila: pd.DataFrame = ponderaciones_df.loc[
            (ponderaciones_df["universidad"] == uni) & (ponderaciones_df["carrera"] == car)
        ]
        p_nem_default: int = int(fila["NEM"].values[0])
        p_rank_default: int = int(fila["Ranking"].values[0])
        p_lec_default: int = int(fila["Lectora"].values[0])
        p_m1_default: int = int(fila["M1"].values[0])
        p_m2_default: int = int(fila["M2"].values[0])
        p_cie_default: int = int(fila["Ciencias"].values[0])
        p_his_default: int = int(fila["Historia"].values[0])
    else:
        p_nem_default = p_rank_default = p_lec_default = p_m1_default = p_m2_default = p_cie_default = p_his_default = 0

    p_nem: int = st.number_input("Ponderación NEM", min_value=0, max_value=100, value=p_nem_default)
    p_rank: int = st.number_input("Ponderación Ranking", min_value=0, max_value=100, value=p_rank_default)
    p_lec: int = st.number_input("Ponderación Comp. Lectora", min_value=0, max_value=100, value=p_lec_default)
    p_m1: int = st.number_input("Ponderación Matemática 1 (M1)", min_value=0, max_value=100, value=p_m1_default)
    p_m2: int = st.number_input("Ponderación Matemática 2 (M2)", min_value=0, max_value=100, value=p_m2_default)
    p_cie: int = st.number_input("Ponderación Ciencias", min_value=0, max_value=100, value=p_cie_default)
    p_his: int = st.number_input("Ponderación Historia", min_value=0, max_value=100, value=p_his_default)

    suma_p: int = p_nem + p_rank + p_lec + p_m1 + p_m2 + p_cie + p_his


# ===== Botón Calcular =====
if st.button("PONDERAR"):
    opt_cie: int = cs if opcion_ch == "Ciencias" else 0
    opt_his: int = hs if opcion_ch == "Historia" else 0
    p_opt_cie: int = p_cie if opcion_ch == "Ciencias" else 0
    p_opt_his: int = p_his if opcion_ch == "Historia" else 0

    ptotal: float = (
        nem * p_nem / 100 +
        ranking * p_rank / 100 +
        cl * p_lec / 100 +
        m1 * p_m1 / 100 +
        m2 * p_m2 / 100 +
        opt_cie * p_opt_cie / 100 +
        opt_his * p_opt_his / 100
    )

    progreso: float = min((ptotal / corte) * 100, 100)
    st.success(f"**{nombre or 'Postulante'}**, tu puntaje ponderado es **{ptotal:.2f}**.")

    if ptotal >= corte:
        st.info(f"Estás sobre el corte por {ptotal - corte:.2f} puntos ({progreso:.1f}% del corte).")
    else:
        st.warning(f"No alcanzas el corte ({corte}). Progreso: {progreso:.1f}%.")


# ===== Información de la fuente =====
st.info(
    "Toda la información presentada en esta plataforma ha sido recopilada y organizada a partir "
    "de los datos oficiales publicados por el Departamento de Evaluación, Medición y Registro Educacional (DEMRE) de la Universidad de Chile."
)

