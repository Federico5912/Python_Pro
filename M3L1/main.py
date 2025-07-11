from flask import Flask
import random

app = Flask(__name__)

Hechos = [
    "El sol es una estrella y no un planeta.",
    "Los pulpos tienen tres corazones.",
    "La miel nunca se echa a perder.",
    "Los flamencos son rosados por su dieta de camarones.",
    "Los canguros no pueden caminar hacia atrás.",
    "Las abejas pueden reconocer rostros humanos.",
    "Los tiburones son más antiguos que los árboles.",
    "Las mariposas tienen sensores de sabor en sus patas.",
    "Los colibríes son los únicos pájaros que pueden volar hacia atrás.",
    "Los delfines tienen nombres únicos para cada uno de ellos.",
    "Las estrellas de mar pueden regenerar sus brazos.",
    "Los caracoles pueden dormir durante tres años.",
    "Los pulgones pueden reproducirse sin necesidad de aparearse.",
    "Las vacas tienen amigos y se estresan cuando están separados.",
    "Los gatos tienen más huesos que los humanos.",
    "Los pingüinos tienen una glándula que les permite filtrar la sal del agua.",
]

@app.route('/')
def index():
    return """ 
    <h1>Bienvenido a la página sobre dependencia tecnológica</h1>
    <ul>
        <li><a href='/random_fact'>¡Ver un hecho al azar!</a></li>
        <li><a href='/lanzar_moneda'>¡Lanzar una moneda!</a></li>
        <li><a href='/imagen_aleatoria'>¡Ver una imagen aleatoria!</a></li>
        <li><a href='/piedra_papel_tijeras/piedra'>¡Jugar Piedra, Papel o Tijeras!</a></li>
    </ul>
    """

@app.route('/random_fact')
def facts():
    return f"<p>{random.choice(Hechos)}</p>"

@app.route('/lanzar_moneda')
def lanzar_moneda():
    resultado = random.choice(['Cara', 'Cruz'])
    return f"<h2>Resultado del lanzamiento: {resultado}</h2><br><a href='/lanzar_moneda'>Lanzar de nuevo</a> <br><a href='/'>Volver al inicio</a>"

@app.route('/imagen_aleatoria')
def imagen_aleatoria():
    imagenes = [
        "https://picsum.photos/400?random=1",
        "https://picsum.photos/400?random=2",
        "https://picsum.photos/400?random=3",
        "https://picsum.photos/400?random=4"
    ]
    url = random.choice(imagenes)
    return f"<h2>Imagen aleatoria</h2><img src='{url}' alt='Imagen aleatoria'><br><a href='/imagen_aleatoria'>Ver otra imagen</a> <br><a href='/'>Volver al inicio</a>"

@app.route('/piedra_papel_tijeras/<eleccion>')
def piedra_papel_tijeras(eleccion):
    opciones = ['piedra', 'papel', 'tijeras']
    if eleccion not in opciones:
        return "<h2>Opción no válida. Elige piedra, papel o tijeras.</h2><br><a href='/'>Volver al inicio</a>"

    robot = random.choice(opciones)
    if eleccion == robot:
        resultado = "¡Empate!"
    elif (eleccion == 'piedra' and robot == 'tijeras') or \
         (eleccion == 'papel' and robot == 'piedra') or \
         (eleccion == 'tijeras' and robot == 'papel'):
        resultado = "¡Ganaste!"
    else:
        resultado = "¡Perdiste!"

    return f"""
    <h2>Elegiste: {eleccion}</h2>
    <h2>El robot eligió: {robot}</h2>
    <h3>{resultado}</h3>
    <a href='/piedra_papel_tijeras/piedra'>Piedra</a><br>
    <a href='/piedra_papel_tijeras/papel'>Papel</a><br>
    <a href='/piedra_papel_tijeras/tijeras'>Tijeras</a><br>
    <a href='/'>Volver al inicio</a>
    """

if __name__ == '__main__':
    app.run(debug=True)