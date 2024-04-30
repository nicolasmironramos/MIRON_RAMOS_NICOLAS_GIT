import re

# Patron que busca caracteres son letras del alfabeto inglés:
patron_mantener = r"[^a-zA-Z0-9\s]"
patron_mantener = re.compile(patron_mantener, re.I)

# Patrón que busca letras repetidas que no sean las adecuadas en el alfabeto inglés:
letras_permitidas_repetidas= {"a","b","c","d","r","e","f","g","l","m","n","o","p","r","s","t","u","z"}
patron= r"(\w)\1"    
patron_consonantes_repetidas= r"[^ aeiou]{6,}"

#Patrón para que busca palabras repetidas:
patron_palabras_repetidas= r"(\b\w+( \w+)*?\b)(\s\1)+"    

# Patrón que busca vocales repetidas:
patron_vocales_repetidas = r"(^[aeiou]{3,})"
