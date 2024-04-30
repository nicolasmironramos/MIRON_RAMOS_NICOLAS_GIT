# 1) Carga de librerías
    # Cálculo de tiempo de ejecución:
import time
    # General:
from src.constantes import *
from src.funciones import *
from src.clases import *

# 2) Carga de datos:
    # Registra el tiempo de inicio
tiempo_inicio = time.time()
archivo_csv = '/ruta_de_datos/.csv'  # Introducir ruta
    # Crear una instancia de CSVReader
csv_reader = LectorCSV(archivo_csv)
df = csv_reader.crear_dataframe()
    # Cambiao de los nombres de las columnas
df = df.rename(columns={"Unnamed: 0": "ID", "text": "TEXTO", "label": "CATEGORIA"})

# 3) Preprocesamiento de datos:
    # Convertimos las variables a su tipo correspondiente:
df['ID'] = df['ID'].astype(int)
df['TEXTO'] = df['TEXTO'].astype(str)
df['CATEGORIA'] = df['CATEGORIA'].astype(int)

    # Preprocesado y limpieza de la columna TEXTO:
preprocesamiento = Preprocesado(df,'TEXTO')
df = preprocesamiento.limpieza()

# 4) Clasificación y predicción:
    # Se instancia el clasificador con el DataFrame y la columna de texto:
modelo_path_RL = "/ruta_del_modelo/modelo_TF_SDG_SW_L.pkl"  # Introducir ruta
vectorizador_path_RL = "/ruta_del_vectorizador/vectorizador_TF_SDG_SW_L.pkl"  # Introducir ruta
df_1 = df
columna_texto_1 = 'TEXTO_STOPWORDS_LEMATIZACION'
clasificador_RL = CLasificadorTexto(modelo_path=modelo_path_RL, vectorizador_path=vectorizador_path_RL, df=df_1, columna_texto=columna_texto_1)
clasificaciones_RL = clasificador_RL.clasificar_columna_texto()
probabilidades_RL= clasificador_RL.predecir_probabilidades_columna_texto()

# 5) Guardado de datos:
    # Se cambian los códigos de las clases por los nombres de las emociones antes de guardar el csv.
columnas_deseadas = ['ID', 'TEXTO', 'TEXTO_LIMPIO', 'CATEGORIA', 'CATEGORIA_MODELO', 'PROBABILIDADES_CATEGORIAS', 'PROBABILIDAD_MAXIMA']
df = df.loc[:, columnas_deseadas]
# Se define un diccionario de mapeo
mapeo_emociones = {
    0: 'Tristeza',
    1: 'Alegría',
    2: 'Amor',
    3: 'Ira',
    4: 'Miedo',
    5: 'Sorpresa'
}
# Se reemplazan los números por las emociones correspondientes
df['CATEGORIA_MODELO'] = df['CATEGORIA_MODELO'].replace(mapeo_emociones)
df['CATEGORIA'] = df['CATEGORIA'].replace(mapeo_emociones)

    # Guardado
clasificacion_csv = '/ruta_de_destino/clasificacion_automatica.csv' # Introducir ruta
if df is not None:
    guardar = GuardarCSV(df)
    guardar.guardar_dataframe(clasificacion_csv, columnas=columnas_deseadas) 

    # Registra el tiempo de finalización
tiempo_fin = time.time()
    # Calcula el tiempo total de ejecución
tiempo_total = tiempo_fin - tiempo_inicio
    # Imprime el tiempo total de ejecución
print("Tiempo total de ejecución:", tiempo_total, "segundos")