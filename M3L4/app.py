from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=('GET', 'POST'))
def meme():
    top_text = 'Cuando empieza la clase por Zoom'
    bottom_text = "Y tu internet es del siglo pasado"
    selected_image = "meme1.jpg" 
    if request.method == 'POST':
        top_text = request.form.get('top_text', "top_text")
        bottom_text = request.form.get('bottom_text', "")

    return render_template('meme.html', top_text=top_text, bottom_text=bottom_text, selected_image=selected_image)

if __name__ == '__main__':
    app.run(debug=True)