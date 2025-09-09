import nltk
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize.punkt import PunktSentenceTokenizer

# Descargar recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')

def sumarization(text, sent_number=3):
    # Tokenizador de oraciones
    tokenizer = PunktSentenceTokenizer()
    sentences = tokenizer.tokenize(text)

    # Lista de stopwords en español
    stop_words = set(stopwords.words("spanish"))

    # Tokenización y limpieza de palabras
    words = wordpunct_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]
    words = [word for word in words if word not in stop_words]

    # Distribución de frecuencia
    freq_dist = FreqDist(words)

    # Calcular puntuación de cada oración
    sentences_score = {}
    for i, sentence in enumerate(sentences):
        sentence_words = wordpunct_tokenize(sentence.lower())
        score = sum(freq_dist[word] for word in sentence_words if word in freq_dist)
        sentences_score[i] = score

    # Seleccionar oraciones más relevantes
    sorted_scores = sorted(sentences_score.items(), key=lambda x: x[1], reverse=True)
    selected_sentences = sorted(sorted_scores[:sent_number])

    # Generar resumen
    summary = " ".join([sentences[i] for i, _ in selected_sentences])
    return summary

# Texto de prueba
texto_prueba = '''
La inteligencia artificial está transformando rápidamente el mundo en el que vivimos. Desde asistentes virtuales hasta diagnósticos médicos, su impacto es evidente en múltiples sectores. Una de las ramas más fascinantes de esta tecnología es el procesamiento del lenguaje natural, que permite a las máquinas comprender, interpretar y generar lenguaje humano.

Gracias a los avances en modelos de lenguaje y al uso de grandes cantidades de datos, hoy es posible interactuar con computadoras mediante voz o texto con resultados sorprendentes. Empresas de todo el mundo están invirtiendo en estas tecnologías para mejorar sus servicios y automatizar procesos que antes requerían intervención humana.

Sin embargo, también existen desafíos importantes. El sesgo en los datos, la privacidad de los usuarios y la seguridad de los sistemas son preocupaciones constantes. Por eso, muchos expertos abogan por una inteligencia artificial ética y responsable, que respete los derechos fundamentales y se utilice para el bien común.

En conclusión, el futuro del lenguaje y la inteligencia artificial está lleno de oportunidades, pero también exige responsabilidad, transparencia y colaboración entre disciplinas.
'''

# Ejecutar resumen
resumen = sumarization(texto_prueba)
print(resumen)
