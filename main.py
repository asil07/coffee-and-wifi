from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Asilbek'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Map Link', validators=[DataRequired(), URL()])
    open_time = StringField('Open time e.g 9AM', validators=[DataRequired()])
    close_time = StringField('Close time e.g. 5.30PM', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee rating', choices=["☕", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"],
                                validators=[DataRequired()])
    wifi_rating = SelectField("wifi rating", choices=["💪", "💪💪", "💪💪💪"], validators=[DataRequired()])
    power_outlet_rate = SelectField('Power outlet', choices=["🔌", "🔌🔌", "🔌🔌🔌"], validators=[DataRequired()])

    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])  # shu yerda method ni
# yozmasdan submit button ni ishlatolamayotgan edm
def add_cafe():
    my_form = CafeForm()
    if my_form.validate_on_submit():
        print("True")
        with open("cafe-data.csv", "a", encoding='utf-8') as file:
            file.write(f"\n{request.form['cafe']},"
                       f"{request.form['location']},"
                       f"{request.form['open_time']},"
                       f"{request.form['close_time']},"
                       f"{request.form['coffee_rating']},"
                       f"{request.form['wifi_rating']},"
                       f"{request.form['power_outlet_rate']}")

            return redirect(url_for('cafes'))
    return render_template('add.html', form=my_form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        length = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, len=length)


if __name__ == '__main__':
    app.run(debug=True)
