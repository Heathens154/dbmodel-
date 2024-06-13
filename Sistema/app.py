from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flaskuser:flaskpassword@localhost/inventory_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

# Ruta para la página de inicio
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

# Ruta para crear un nuevo ítem
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        quantity = request.form['quantity']
        new_item = Item(name=name, description=description, quantity=quantity)
        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')
        except:
            return "Hubo un problema al agregar el ítem"
    else:
        return render_template('create.html')

# Ruta para actualizar un ítem
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        item.quantity = request.form['quantity']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "Hubo un problema al actualizar el ítem"
    else:
        return render_template('update.html', item=item)

# Ruta para eliminar un ítem
@app.route('/delete/<int:id>')
def delete(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect('/')
    except:
        return "Hubo un problema al eliminar el ítem"

if __name__ == '__main__':
    with app.app_context():
     db.create_all()
    app.run(debug=True)



