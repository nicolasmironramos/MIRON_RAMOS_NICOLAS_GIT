# Imports pertinentes:
import re 

# Se importa 'emoji' para futurois usos:
# import emoji

# Función que elimina emojis:
# def remove_emoji(text):
#   return emoji.replace_emoji(text, '')

# Esta función forma parte de unn conjunto de 4 funciones que nos permiten eliminar las letras de relleno.
# La función busca si el ratio de letras total de una palabra, entre el de letras únicas es menor o igual a 2. 
# Si es así, devuelve TRUE:
def ratio(palabra):
    """
    Calcula la relación entre el número total de letras y el número de letras únicas en una palabra.

    Parámetros:
    -----------
    palabra : str
        La palabra para la cual se calculará la relación.

    Devoluciones:
    ------------
    bool:
        True si la relación es menor o igual a 2, False en caso contrario.
    """
    letras = list(palabra)
    numero_letras = len(letras)
    unicas = set(letras)
    numero_unicas = len(unicas)
    ratio = numero_letras / numero_unicas
    if ratio <= 2:
        return True
    return False

# Esta función forma parte de unn conjunto de 4 funciones que permiten eliminar las letras de relleno.
# La función busca si una palabra sigue el patrón establecido. Si es igual a una de las letras permitidas, nos dará TRUE (0).
# Sino, será FALSE, y por lo tanto, una letra repetido no permitida:
def letras_repetidas(palabra,letras_permitidas_rep,pat):
    """
    Verifica si una palabra sigue el patrón establecido.

    Parámetros:
    -----------
    palabra : str
        La palabra a verificar.
    letras_permitidas_rep : set
        Conjunto de letras permitidas.
    pat : patrón regex
        Patrón de expresión regular para comparar con la palabra.

    Devoluciones:
    ------------
    bool:
        True si la palabra coincide con el patrón de letras permitidas, False en caso contrario.
    """
    if set(re.findall(pat,palabra))-letras_permitidas_rep:
        return False
    return True

# Esta función forma parte de unn conjunto de 4 funciones que permiten eliminar las letras de relleno.
# La función busca si en una palabra existen 6 o mas consonantes seguidas. Si esto ocurre, devuelve FALSE:
def consonantes_repetidas(palabra,patron_consonantes_repetidas):
    """
    Verifica si una palabra contiene 6 o más consonantes consecutivas.

    Parámetros:
    -----------
    palabra : str
        La palabra a verificar.
    patron_consonantes_repetidas : patrón regex
        Patrón de expresión regular para buscar consonantes consecutivas.

    Devoluciones:
    ------------
    bool:
        True si la palabra no contiene 6 o más consonantes consecutivas, False en caso contrario.
    """
    if re.search(patron_consonantes_repetidas,palabra) is not None:
        return False
    return True

# Función que engloba las tres anteriores y permite eliminar las letras de relleno:
# Si se cumplen las condiciones anteriores, eliminará las letras repetidas no permitidas, y se quedará con las permitidas. 
# En conclusión, devuelve una cadena nueva limpia:
def validacion(palabras,letras_permitidas_repetidas,patron, patron_consonantes_repetidas):
    """
    Valida palabras según varios criterios y devuelve una cadena limpia.

    Parámetros:
    -----------
    palabras : str
        La cadena de entrada que contiene palabras para validar.
    letras_permitidas_repetidas : set
        Conjunto de letras permitidas para ocurrencias repetidas.
    patron : patrón regex
        Patrón de expresión regular para comparar con letras permitidas.
    patron_consonantes_repetidas : patrón regex
        Patrón de expresión regular para buscar consonantes consecutivas.

    Devoluciones:
    ------------
    str:
        La cadena limpia después de eliminar palabras inválidas.
    """
    lista_palabras = palabras.split()
    lista = []
    for palabra in lista_palabras:
        if ratio(palabra) and letras_repetidas(palabra, letras_permitidas_repetidas, patron) and consonantes_repetidas(palabra, patron_consonantes_repetidas):
            lista.append(palabra)
    cadena_nueva = " ".join(lista)
    return cadena_nueva

# Función que elimina las palabras repetidas. 
# Se calcula iterativamente con una función recursiva hasta que no encuentre más patrones. 
# Así se eliminan los patrones de palabras o grupos de palabras.
def palabras_repetidas(frase, patron_palabras_repetidas):
    """
    Elimina palabras repetidas o patrones de palabras de una cadena.

    Parámetros:
    -----------
    frase : str
        La cadena de entrada que contiene palabras para verificar la repetición.
    patron_palabras_repetidas : patrón regex
        Patrón de expresión regular para comparar palabras o patrones repetidos.

    Devoluciones:
    ------------
    str:
        La cadena después de eliminar palabras o patrones repetidos.
    """
    frase_original = frase  
    while True:
        frase = re.sub(patron_palabras_repetidas, r"\1", frase, flags=re.I)  
        if frase == frase_original: 
            break 
        frase_original = frase  
    return frase

# Función para eliminar las vocales repetidas:
def vocales_repetidas(palabra,patron_vocales):
    """
    Verifica si una palabra contiene vocales repetidas.

    Parámetros:
    -----------
    palabra : str
        La palabra a verificar.
    patron_vocales : patrón regex
        Patrón de expresión regular para buscar vocales repetidas.

    Devoluciones:
    ------------
    bool:
        True si la palabra no contiene vocales repetidas, False en caso contrario.
    """
    if re.search(palabra,patron_vocales) is not None:
        return False
    return True

def validacion_vocales(palabras, patron_vocales):
    """
    Valida palabras según vocales repetidas y devuelve una cadena limpia.

    Parámetros:
    -----------
    palabras : str
        La cadena de entrada que contiene palabras para validar.
    patron_vocales : patrón regex
        Patrón de expresión regular para buscar vocales repetidas.

    Devoluciones:
    ------------
    str:
        La cadena limpia después de eliminar palabras con vocales repetidas.
    """
    lista = []
    for palabra in palabras.split():
        if vocales_repetidas(palabra, patron_vocales):
            lista.append(palabra)
    cad_nueva = " ".join(lista)
    return cad_nueva

def longitud_palabras(fila):
    """
    Verifica si una cadena contiene más de una palabra.

    Parámetros:
    -----------
    fila : str
        La cadena de entrada para verificar.

    Devoluciones:
    ------------
    bool:
        True si la cadena contiene más de una palabra, False en caso contrario.
    """
    palabras = fila.split()
    if len(palabras) > 1:  
        return True
    return False

# Función para aplicar stemming, lematización o stopwords a nuestro texto: 
def preprocesamiento(texto: str,
                        rm_stopwords: bool,
                        stemming: bool,
                        lematizar: bool,
                        STEMMER_EN=None,
                        SPACY_NLP_EN=None,
                        STOPWORDS=None) -> str:
    """
    Preprocesa el texto según las operaciones especificadas.

    Parámetros:
    -----------
    texto : str
        El texto de entrada para preprocesar.
    rm_stopwords : bool
        Si se deben eliminar las palabras vacías o no.
    stemming : bool
        Si se debe realizar el stemming o no.
    lematizar : bool
        Si se debe realizar la lematización o no.
    STEMMER_EN : SnowballStemmer
        Objeto stemmer en inglés.
    SPACY_NLP_EN : spacy.language.Language
        Objeto de modelo de procesamiento de lenguaje en inglés.
    STOPWORDS : set
        Conjunto de palabras vacías para eliminar del texto.

    Devoluciones:
    ------------
    str:
        El texto preprocesado.
    """
    lista_palabras = texto.split()
    if rm_stopwords and STOPWORDS:
        lista_palabras = [palabra for palabra in lista_palabras if palabra.lower() not in STOPWORDS]
    if stemming and STEMMER_EN:
        lista_palabras = [STEMMER_EN.stem(palabra) for palabra in lista_palabras]
    if lematizar and SPACY_NLP_EN:
        doc_spacy = SPACY_NLP_EN(" ".join(lista_palabras))
        lista_palabras = [palabra.lemma_ for palabra in doc_spacy]
    texto = " ".join(lista_palabras)
    return texto
