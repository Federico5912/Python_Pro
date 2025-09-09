import requests
from bs4 import BeautifulSoup
import pandas as pd

dict_news = {
    "titulos_noticias": [],
    "links_noticias": [],
    "comentarios_noticias": [],
    "fecha_publicación": [],
    "tag": []
}

url = "https://www.xataka.com/tag/"
temas = ["ciencia-y-tecnologia", "google", "nasa", "videojuegos"]

for tema in temas:
    response = requests.get(url+tema)
    bs = BeautifulSoup(response.text, "lxml")
    articulos = bs.find_all("article", "recent-abstract", "abstract-article")
    for post in articulos:
        dict_news["links_noticias"].append(post.h2.a.get("href"))
        dict_news["titulos_noticias"].append(post.h2.a.text)
        dict_news["comentarios_noticias"].append(post.span.text)
        dict_news["fecha_publicación"].append(post.time.get("datetime")[:10])
        dict_news["tag"].append(tema)

df_news = pd.DataFrame(dict_news)
df_news.to_csv("saved_data.csv", index=False)
print("Archivo guardado como saved_data.csv")