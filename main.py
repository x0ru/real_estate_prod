from flask import Flask, render_template, redirect, url_for, flash, request
import sqlite3
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, AnyOf, ValidationError
import secrets

app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = 'gdfhfhfdhdhg'
csrf = CSRFProtect(app)


class FilterForm(FlaskForm):
    min_rooms = SelectField('', choices=[(0, "Min pokoje"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5+")])
    max_rooms = SelectField('', choices=[(1001, "Max pokoje"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (100, "5+")])
    min_area = SelectField('', choices=[(0, "Min m2"), (10, "10m2"), (20, "20m2"), (30, "30m2"), (40, "40m2"),
                                        (50, "50m2"), (60, "60m2"), (70, "70m2"), (80, "80m2"), (90, "90m2"),
                                        (100, "100m2"), (110, "110m2"), (120, "120m2"), (130, "130m2"), (140, "140m2"),
                                        (150, "150m2+")])
    max_area = SelectField('', choices=[(1001, "Max m2"), (10, "10m2"), (20, "20m2"), (30, "30m2"), (40, "40m2"),
                                        (50, "50m2"), (60, "60m2"), (70, "70m2"), (80, "80m2"), (90, "90m2"),
                                        (100, "100m2"), (110, "110m2"), (120, "120m2"), (130, "130m2"), (140, "140m2"),
                                        (1000, "150m2+")])
    min_floor = SelectField('', choices=[(0, "Min piętro"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"),
                                         (7, "7"), (8, "8"), (9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13"),
                                         (14, "14"), (15, "15+")])
    max_floor = SelectField('', choices=[(101, "Max piętro"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"),
                                         (7, "7"), (8, "8"), (9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13"),
                                         (14, "14"), (100, "15+")])
    rent_sell = SelectField('', choices=[(0, "Na sprzedaż"), (1, "Na wynajem")])
    submit = SubmitField('Filter')


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Not in use at the moment - old code just basic query in case something go wrong



def basic_select():
    con = sqlite3.connect('property_krakow.db',
                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    statement = '''SELECT district, avg(sqr_price), avg(price), avg(area), count(*)  FROM krakow
                        group by district
                        order by avg(sqr_price) desc'''
    cur.execute(statement)
    return cur.fetchall()


def basic_select2():
    con = sqlite3.connect('property_krakow.db',
                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    statement2 = '''SELECT  avg(sqr_price), avg(price), count(*)  FROM krakow'''
    cur.execute(statement2)
    return cur.fetchall()

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def filter_select(city, min_rooms, max_rooms, min_area, max_area, min_floor, max_floor, rent_sell):

    con = sqlite3.connect('property_krakow.db',
                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()

    statement = f'''SELECT district, avg(sqr_price), avg(price), avg(area), count(*)  FROM {city}
                        where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                              area >= {min_area} and area <= {max_area} and
                              floor >= {min_floor} and floor <= {max_floor} and 
                              date = (select max(date) from {city})
                            group by district
                            order by avg(sqr_price) desc'''

    statement2 = f'''SELECT avg(sqr_price), avg(price), count(*)  FROM {city}
                            where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                                  area >= {min_area} and area <= {max_area} and
                                  floor >= {min_floor} and floor <= {max_floor} and
                                    date = (select max(date) from {city})'''

    if int(rent_sell) == 1:
        statement = f'''SELECT district, avg(price), avg(area), count(*)  FROM {city}_rent
                                where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                                      area >= {min_area} and area <= {max_area} and
                                      floor >= {min_floor} and floor <= {max_floor} and 
                                      date = (select max(date) from {city}_rent)
                                    group by district
                                    order by avg(price) desc'''

        statement2 = f'''SELECT  avg(price), count(*)  FROM {city}_rent
                                    where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                                          area >= {min_area} and area <= {max_area} and
                                          floor >= {min_floor} and floor <= {max_floor} and
                                            date = (select max(date) from {city}_rent)'''

    cur.execute(statement)
    queries = {1: cur.fetchall()}
    cur.execute(statement2)
    queries[2] = cur.fetchall()
    return queries


def validation_if_min_greater_than_max(form):

    if form.min_floor.data is None or form.max_floor.data is None:
        pass
    elif int(form.min_rooms.data) > int(form.max_rooms.data):
        form.max_rooms.data = form.max_rooms.choices[0][0]
    if form.min_area.data is None or form.max_area.data is None:
        pass
    elif int(form.min_area.data) > int(form.max_area.data):
        form.area_rooms.data = form.max_area.choices[0][0]
    if form.min_floor.data is None or form.max_floor.data is None:
        pass
    elif int(form.min_floor.data) > int(form.max_floor.data):
        form.max_floor.data = form.max_floor.choices[0][0]

    return [form.max_rooms.data, form.max_area.data, form.max_floor.data]




@app.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    validation_if_min_greater_than_max(form)
    if form.validate_on_submit():
        return render_template('index.html', data=filter_select('krakow', form.min_rooms.data, form.max_rooms.data,
                                                                form.min_area.data, form.max_area.data,
                                                                form.min_floor.data, form.max_floor.data,
                                                                form.rent_sell.data), form=form)
    return render_template('index.html', data=filter_select('krakow', 0, 100, 0, 10000, 0, 100, 0), form=form)


@app.route('/warszawa', methods=['GET', 'POST'])
def warszawa():
    form = FilterForm()
    validation_if_min_greater_than_max(form)
    if form.validate_on_submit():
        return render_template('index.html', data=filter_select('warszawa', form.min_rooms.data, form.max_rooms.data,
                                                                form.min_area.data, form.max_area.data,
                                                                form.min_floor.data, form.max_floor.data,
                                                                form.rent_sell.data), form=form,)
    return render_template('index.html', data=filter_select('warszawa', 0, 100, 0, 10000, 0, 100, 0), form=form)


if __name__ == "__main__":
    app.run(debug=True)
