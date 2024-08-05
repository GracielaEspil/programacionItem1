from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists 
from sqlalchemy import Column, Integer, String, ForeignKey



# Creo la variable que se conecta a la base de datos
db = SQLAlchemy()

# Creo los modelos de la tabla Partidos de la Base de datos dbFinal.db
class Partido(db.Model):
    __tablename__ = 'partidos' # nombre de la tabla
    id = db.Column(db.Integer, primary_key=True)
    estadio = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.String(10), nullable=False)
    clubA = db.Column(db.String(25), nullable=False)
    clubB = db.Column(db.String(25), nullable=False)
    resultado = db.Column(db.String(3), nullable=False)



# planteo un objeto
    def __str__(self):
        return f'Estadio: {self.estadio}'


   
