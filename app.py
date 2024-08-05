from flask import Flask, render_template, request, redirect, url_for, flash 
from datetime import datetime
from models.models import Partido, db
from os import getcwd 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date
from sqlalchemy_utils import database_exists 
from sqlalchemy import Column, engine


app = Flask(__name__)

# configuro la URI de la base de datos, el motor y la cadena de conexion
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbFinal.db'
db.init_app(app) # Aquí incializa la database 

# primer inicio de la app debo saber si la base esta creada o NO
with app.app_context():
   if database_exists(db.engine.url):
      db.create_all()


@app.route('/')
def index():
    partidos_db = Partido.query.all()
    return render_template('index.html', partidos=partidos_db)


@app.route("/read/<partidos_id>", methods=["GET", "POST"])
def read(partidos_id):
    global partidos
    partido_db = Partido.query.filter_by(id=partidos_id).first()
    return render_template('read.html', partido=partido_db)



@app.route("/edit/<partidos_id>", methods=["GET", "POST"])
def edit(partidos_id):
    partido = Partido.query.filter_by(id=partidos_id).first() # Obtener partido o lanzar 404, hacer con filter para que devuelva un objeto o instancia en partido

    if request.method == "POST":
        partido.estadio = request.form["estadio"]
        partido.fecha = request.form["fecha"]
        partido.clubA = request.form["clubA"]
        partido.clubB = request.form["clubB"]
        partido.resultado = request.form["resultado"]

        try:
            db.session.commit()
            flash('Partido actualizado correctamente', 'success')
            return redirect('/')
        except Exception as e:
            flash(f'Error al actualizar el partido: {e}', 'error')
            return render_template("edit.html", partido=partido)

    return render_template("edit.html", partido=partido)



@app.route("/delete/<partido_id>")
def delete(partido_id):
    partido_db = Partido.query.get(partido_id)
    if partido_db:
        try:
            db.session.delete(partido_db)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f'Error al eliminar la tarea')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)



