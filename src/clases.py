import pandas as pd
import re
import joblib
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import spacy
from src.constantes import *
from src.funciones import *

# Clase para cargar datos:
class LectorCSV:
    def __init__(self, path_csv):
        """
        Inicializa el objeto LectorCSV.

        Parámetros:
        -----------
        path_csv : str
            La ruta al archivo CSV que se va a leer.
        """
        self.path_csv = path_csv

    def crear_dataframe(self):
        """
        Carga un archivo CSV en un DataFrame de pandas.

        Devoluciones:
        ------------
        pandas.DataFrame o None:
            Devuelve un DataFrame de pandas si el archivo CSV se carga correctamente,
            de lo contrario devuelve None.

        Excepciones:
        ------------
        FileNotFoundError:
            Si el archivo CSV especificado no se encuentra.
        Exception:
            Si ocurre cualquier otro error durante el proceso de carga del archivo CSV.
        """
        try:
            return pd.read_csv(self.path_csv)
        except FileNotFoundError:
            print("El archivo CSV especificado no fue encontrado")
            return None
        except Exception as e:
            print("Ocurrió un error al cargar el archivo CSV:", str(e))
            return None

class GuardarCSV:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def guardar_dataframe(self, path_guardado, columnas=None):
        try:
            if columnas:
                self.dataframe[columnas].to_csv(path_guardado, index=False)
            else:
                self.dataframe.to_csv(path_guardado, index=False)
            print("El DataFrame fue guardado correctamente en", path_guardado)
        except Exception as e:
            print("Ocurrió un error al guardar el DataFrame como CSV:", str(e))

# Clase para el preprocesado del texto:
class Preprocesado:
    def __init__(self, df: pd.DataFrame, text_column: str):
        """
        Inicializa el objeto Preprocesado.

        Parámetros:
        -----------
        df : pandas.DataFrame
            El DataFrame que contiene los datos.
        text_column : str
            El nombre de la columna que contiene el texto a preprocesar.
        """
        self.df = df  
        self.text_column = text_column
        self.STEMMER_EN = SnowballStemmer("english")  # Inicializa el stemmer en inglés
        self.SPACY_NLP_EN = spacy.load("en_core_web_sm")  # Carga el modelo de procesamiento de lenguaje en inglés
        self.STOPWORDS = stopwords.words('english')  # Obtiene la lista de stopwords en inglés

    def limpieza(self):
        """
        Realiza el preprocesamiento del texto en el DataFrame.

        Devoluciones:
        ------------
        pandas.DataFrame:
            El DataFrame con el texto preprocesado.

        Excepciones:
        ------------
        None
        """
        # Elimina patrones específicos del texto
        self.df['TEXTO_LIMPIO'] = self.df[self.text_column].apply(lambda x: re.sub(patron_mantener, ' ', x))
        # Elimina espacios en blanco adicionales
        self.df['TEXTO_LIMPIO'] = self.df['TEXTO_LIMPIO'].apply(lambda x: re.sub(r'\s+', ' ', x))
        # Realiza validaciones sobre el texto limpio
        self.df['TEXTO_LIMPIO'] = self.df['TEXTO_LIMPIO'].apply(lambda x: validacion(x, letras_permitidas_repetidas, patron_palabras_repetidas, patron_consonantes_repetidas))
        # Elimina palabras repetidas
        self.df['TEXTO_LIMPIO'] = self.df['TEXTO_LIMPIO'].apply(lambda x: palabras_repetidas(x, patron_palabras_repetidas))
        # Realiza validaciones sobre las vocales del texto
        self.df['TEXTO_LIMPIO'] = self.df['TEXTO_LIMPIO'].apply(lambda x: validacion_vocales(x, patron_vocales_repetidas))
        # Filtra las filas que contienen palabras con longitud mayor a 1
        self.df = self.df[self.df['TEXTO_LIMPIO'].apply(lambda x: longitud_palabras(x))]
        # Convierte el texto a minúsculas
        self.df['TEXTO_LIMPIO'] = self.df['TEXTO_LIMPIO'].apply(lambda x: x.lower())

        # Realiza el preprocesamiento con eliminación de stopwords pero sin stemming ni lematización
        # self.df['TEXTO_STOPWORDS'] = self.df['TEXTO_LIMPIO'].apply(lambda texto: preprocesamiento(texto, rm_stopwords=True, stemming=False, lematizar=False))
        # Realiza el preprocesamiento con eliminación de stopwords y stemming
        # self.df['TEXTO_STOPWORDS_STEMMING'] = self.df['TEXTO_LIMPIO'].apply(lambda texto: preprocesamiento(texto, rm_stopwords=True, stemming=True, lematizar=False))
        # Realiza el preprocesamiento con eliminación de stopwords y lematización
        self.df['TEXTO_STOPWORDS_LEMATIZACION'] = self.df['TEXTO_LIMPIO'].apply(lambda texto: preprocesamiento(texto, rm_stopwords=True, stemming=False, lematizar=True))
        # Realiza el preprocesamiento con lematización pero sin eliminación de stopwords ni stemming
        # self.df['TEXTO_LEMATIZACION'] = self.df['TEXTO_LIMPIO'].apply(lambda texto: preprocesamiento(texto, rm_stopwords=False, stemming=False, lematizar=True))
        # Realiza el preprocesamiento con stemming pero sin eliminación de stopwords ni lematización
        # self.df['TEXTO_STEMMING'] = self.df['TEXTO_LIMPIO'].apply(lambda texto: preprocesamiento(texto, rm_stopwords=False, stemming=True, lematizar=False))
        
        # Filtra las filas que contienen valores no nulos en ciertas columnas
        # self.df = self.df[self.df[['TEXTO_STOPWORDS', 'TEXTO_STOPWORDS_STEMMING','TEXTO_STOPWORDS_LEMATIZACION','TEXTO_LEMATIZACION','TEXTO_STEMMING']].notnull().all(axis=1)]
        self.df = self.df[self.df[['TEXTO_STOPWORDS_LEMATIZACION']].notnull().all(axis=1)]
        return self.df

# # Clase para la predicción del modelo:
class CLasificadorTexto:
    def __init__(self, modelo_path, vectorizador_path, df=None, columna_texto=None):
        """
        Inicializa el objeto CLasificadorTexto.

        Parámetros:
        -----------
        modelo_path : str
            La ruta al archivo .pkl que contiene el modelo entrenado.
        vectorizador_path : str
            La ruta al archivo .pkl que contiene el vectorizador entrenado.
        df : pandas.DataFrame, opcional
            El DataFrame que contiene la columna de texto a clasificar.
        columna_texto : str, opcional
            El nombre de la columna de texto en el DataFrame.

        """
        self.modelo = joblib.load(modelo_path)
        self.vectorizador = joblib.load(vectorizador_path)
        self.df = df
        self.columna_texto = columna_texto

    def clasificar_texto(self, texto):
        """
        Clasifica un texto dado utilizando el modelo y el vectorizador cargados.

        Parámetros:
        -----------
        texto : str
            El texto que se va a clasificar.

        Devoluciones:
        ------------
        int:
            La categoría predicha para el texto.
        """
        texto_vectorizado = self.vectorizador.transform([texto])
        categoria_predicha = self.modelo.predict(texto_vectorizado)[0]
        return categoria_predicha

    def predecir_probabilidades(self, texto):
        """
        Predice las probabilidades de pertenencia a cada categoría para un texto dado.

        Parámetros:
        -----------
        texto : str
            El texto para el cual se van a predecir las probabilidades.

        Devoluciones:
        ------------
        dict:
            Un diccionario que mapea cada categoría a su probabilidad de pertenencia para el texto dado.
        """
        texto_vectorizado = self.vectorizador.transform([texto])
        probabilidades = self.modelo.predict_proba(texto_vectorizado)[0]
        categorias = self.modelo.classes_
        probabilidades_dict = {categoria: probabilidad for categoria, probabilidad in zip(categorias, probabilidades)}
        return probabilidades_dict

    def clasificar_columna_texto(self):
        """
        Clasifica toda la columna de texto en el DataFrame utilizando el clasificador.

        Devoluciones:
        ------------
        pandas.Series:
            Una Serie de pandas que contiene las categorías predichas para cada texto en la columna.
        """
        if self.df is None or self.columna_texto is None:
            raise ValueError("Se requiere un DataFrame y el nombre de la columna de texto.")
        categorias_predichas = self.df[self.columna_texto].apply(self.clasificar_texto)
        self.df['CATEGORIA_MODELO'] = categorias_predichas
        return categorias_predichas

    def predecir_probabilidades_columna_texto(self):
        """
        Predice las probabilidades de pertenencia a cada categoría para toda la columna de texto en el DataFrame.

        Devoluciones:
        ------------
        pandas.DataFrame:
            Un DataFrame que contiene las probabilidades de pertenencia a cada categoría para cada texto en la columna.
            Las columnas del DataFrame incluyen 'TEXTO' y las probabilidades de cada categoría.
        """
        if self.df is None or self.columna_texto is None:
            raise ValueError("Se requiere un DataFrame y el nombre de la columna de texto.")
        probabilidades = self.df[self.columna_texto].apply(self.predecir_probabilidades)
        probabilidades_df = pd.DataFrame(probabilidades.tolist(), index=self.df.index)
        self.df['PROBABILIDADES_CATEGORIAS'] = probabilidades_df.values.tolist()
        self.df['PROBABILIDAD_MAXIMA'] = self.df['PROBABILIDADES_CATEGORIAS'].apply(lambda x: max(x))
        return probabilidades_df 
    
