import ntlk
from nltk.tokenize import send_tokenize, word_tokenize
from nltk.corpus import stopwords
from ntkl.probability import FreqDist
import pymorphy2 as pm2

def resumen_noticias(text, sent_number=3):
    sentences = sent_tokenize(text, language= "spanish")
    
    stop_words = set(stopwords.words("spanish"))

    word = word_tokenize(text, language="spanish")

    words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    words = [word for word in words if word not in stop_words]

    morph, = pm2.MorphAnalyzer()

    words = [morph.parse(word)[0].normal_form for word in words]

    freq_dist = FreqDist(words)
    sentences_score = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower, language="spanish")
        score = sum(freq_dist[word] for word in sentence_words if word in freq_dist)
        sentences_score[i] = score

    sorted_scores = sorted(sentences_score.items(), key=lambda x: x[1], reverse=True)

    selected_sentences = sorted(sorted_scores[:sent_number])

    sumary = " ".join([sentences[i] for i, _ in selected_sentences])
    return sumary