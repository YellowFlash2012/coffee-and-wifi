from os import close
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.core import SelectField
from wtforms.validators import URL, DataRequired, InputRequired, InputRequired
import csv
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = token
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', render_kw={'autofocus': True}, validators=[DataRequired()])
    
    location = StringField('Cafe Location on Google Maps (URL)', validators=[URL()])
    
    open = StringField('Opening @ (e.g 8AM)', validators=[DataRequired()])
    
    close = StringField('Closing @ (e.g 5:30PM)', validators=[DataRequired()])
    
    coffee = SelectField('Coffee rating', choices=[(
        '☕️'), ('☕️☕️'), ('☕️☕️☕️'), ('☕️☕️☕️☕️'), ('☕️☕️☕️☕️☕️')], validators=[DataRequired()])
    
    wifi = SelectField(
        'WiFi Strength Rating', choices=[('✘'), ('💪'), ('💪💪'), ('💪💪💪'), ('💪💪💪💪'), ('💪💪💪💪💪')], validators=[DataRequired()])
    
    power = SelectField(
        'Power Socket Availability', choices=[('✘'), ('🔌'), ('🔌🔌'), ('🔌🔌🔌'), ('🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌')], validators=[DataRequired()])
    
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True", flush=True)
        # print(form.data, flush=True)
        with open('/Users/Cyclo/Documents/full-stack/back-end/100-days-code/day-62-coffee-wifi/coffee-and-wifi/cafe-data.csv', mode="a", encoding="utf8") as file:
            file.write(f"\n{form.cafe.data},"
                       f"{form.location.data},"
                       f"{form.open.data},"
                       f"{form.close.data},"
                       f"{form.coffee.data},"
                       f"{form.wifi.data},"
                       f"{form.power.data}")
        return redirect(url_for('cafes')) #to redirect to cafes.html after submit
    
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('/Users/Cyclo/Documents/full-stack/back-end/100-days-code/day-62-coffee-wifi/coffee-and-wifi/cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
            # print(list_of_rows, flush=True)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
