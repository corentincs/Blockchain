from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

choix = [('candidat1', 'Candidat 1'), ('candidat2', 'Candidat 2'), ('candidat3', 'Candidat 3'), ('candidat4', 'Candidat 4'), ('candidat5', 'Candidat 5')]

class TransactionForm(FlaskForm):    
    choix1 = SelectField('Choix 1', choices=choix)
    choix2 = SelectField('Choix 2', choices=choix)
    choix3 = SelectField('Choix 3', choices=choix)
    choix4 = SelectField('Choix 4', choices=choix)
    choix5 = SelectField('Choix 5', choices=choix)
    submit = SubmitField('Voter')
