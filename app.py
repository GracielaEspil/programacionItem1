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
app.config['SECRET_KEY'] = 'supersecretkey'
db.init_app(app) # Aquí incializa la database 

# primer inicio de la app debo saber si la base esta creada o NO
with app.app_context():
   if database_exists(db.engine.url):
      db.create_all()


@app.route('/')
def index():
    partido = Partido.query.all()
    return render_template('index.html', partidos=partido)


@app.route("/read/<partido_id>", methods=["GET", "POST"])
def read(partido_id):
    partido = Partido.query.filter_by(id=partido_id).first()
    return render_template('read.html', partido=partido)

@app.route("/edit/<partido_id>", methods=["GET", "POST"])
def edit(partido_id):
    partido = Partido.query.filter_by(id=partido_id).first()

    if request.method == "POST":
        partido.estadio = request.form["estadio"]
        partido.fecha = request.form["fecha"]
        partido.clubA = request.form["clubA"]
        partido.clubB = request.form["clubB"]
        partido.resultado = request.form["resultado"]

        # Validar que la fecha no sea futura
        fecha_ingresada = datetime.strptime(partido.fecha, '%Y-%m-%d')
        fecha_actual = datetime.now()

        if fecha_ingresada > fecha_actual:
            flash('La fecha del partido no puede ser futura', 'error')
            return render_template("edit.html", partido=partido)

        # Convertir la fecha al formato deseado antes de guardarla
        partido.fecha = fecha_ingresada.strftime('%d-%m-%Y')

        try:
            db.session.commit()
            flash('Partido actualizado correctamente', 'success')
            return redirect('/')
        except Exception as e:
            flash(f'Error al actualizar el partido: {e}', 'error')
            return render_template("edit.html", partido=partido)
    return render_template("edit.html", partido=partido)


@app.route("/delete/<partido_id>", methods=["GET", "POST"])
def delete(partido_id):
    #partido = Partido.query.filter_by(id=partido_id).first()
    partido = db.session.query(Partido).get(partido_id)
    if not partido:
        flash('Partido no encontrado', 'error')
        print(f'Partido no encontrado') #preguntar a Daniel como se hace print y en donde sale
        return redirect('/')

    if request.method == "POST":
        try:
            db.session.delete(partido)
            db.session.commit()
            flash('Partido eliminado correctamente', 'success')
            return redirect('/')
        except Exception as e:
            flash('Error al eliminar el partido', 'error')
            print(f'Error al eliminar el partido: {e}')
            return redirect('/')
        
    return render_template('delete.html', partido=partido)


if __name__ == '__main__':
    app.run(debug=True)



