from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv, pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Cafe Location on Google Maps(URL)', validators=[DataRequired(), URL(require_tld=True)])
    opening_time = StringField(label="Opening Time e.g. 8AM", validators=[DataRequired()])
    closing_time = StringField(label="Closing Time e.g. 5:30PM", validators=[DataRequired()])
    coffee_rating = SelectField(label="Coffee Rating", choices=[("✘", "✘"), ("☕", "☕"), ("☕☕", "☕☕"), ("☕☕☕", "☕☕☕"), ("☕☕☕☕", "☕☕☕☕"), ("☕☕☕☕☕", "☕☕☕☕☕")])
    wifi_rating = SelectField(label="Wifi Strength Rating", choices=[("✘", "✘"), ("💪", "💪"), ("💪💪", "💪💪"), ("💪💪💪", "💪💪💪"), ("💪💪💪💪", "💪💪💪💪"), ("💪💪💪💪💪", "💪💪💪💪💪")])
    power_socket = SelectField(label="Power Socket Availability", choices=[("✘", "✘"), ("🔌", "🔌"), ("🔌🔌", "🔌🔌"), ("🔌🔌🔌", "🔌🔌🔌"), ("🔌🔌🔌🔌", "🔌🔌🔌🔌"), ("🔌🔌🔌🔌🔌", "🔌🔌🔌🔌🔌")])
    submit = SubmitField(label='Submit')

# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',  methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        form_data = {
            "Cafe Name": form.cafe.data,
            "Location": form.location.data,
            "Open": form.opening_time.data,
            "Close": form.opening_time.data,
            "Coffee": form.coffee_rating.data,
            "Wifi": form.wifi_rating.data,
            "Power": form.power_socket.data
        }
        data = pandas.DataFrame(form_data, index=[0])
        data.to_csv("cafe-data.csv", mode="a", index=False, header=False)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
