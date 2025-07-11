from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary0.db'

db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f"<Card('{self.id}')>"

with app.app_context():
    db.create_all()
@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle')
        text = request.form.get('text')
        card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(card)
        db.session.commit()
    cards = Card.query.order_by(Card.id).all()
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)