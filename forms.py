from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

choix = [('candidat1', 'Candidat 1'), ('candidat2', 'Candidat 2'), ('candidat3', 'Candidat 3')]

class TransactionForm(FlaskForm):
    message = StringField('Message')
    candidate = SelectField('Choisir un candidat', choices=choix)
    submit = SubmitField('Ajouter la transaction')
