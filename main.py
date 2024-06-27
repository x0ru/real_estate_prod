from flask import Flask, render_template
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SubmitField, SelectField
import secrets
import psycopg2
import os


app = Flask(__name__)
foo = secrets.token_urlsafe(16)
app.secret_key = 'gdfhfhfdhdhg'
csrf = CSRFProtect(app)


class FilterForm(FlaskForm):
    min_rooms = SelectField('', choices=[(0, "Min pokoje"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5+")],
                            validate_choice=False)
    max_rooms = SelectField('', choices=[(1001, "Max pokoje"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (100, "5+")],
                            validate_choice=False)
    min_area = SelectField('', choices=[(0, "Min m2"), (10, "10m2"), (20, "20m2"), (30, "30m2"), (40, "40m2"),
                                        (50, "50m2"), (60, "60m2"), (70, "70m2"), (80, "80m2"), (90, "90m2"),
                                        (100, "100m2"), (110, "110m2"), (120, "120m2"), (130, "130m2"), (140, "140m2"),
                                        (150, "150m2+")], validate_choice=False)
    max_area = SelectField('', choices=[(1001, "Max m2"), (10, "10m2"), (20, "20m2"), (30, "30m2"), (40, "40m2"),
                                        (50, "50m2"), (60, "60m2"), (70, "70m2"), (80, "80m2"), (90, "90m2"),
                                        (100, "100m2"), (110, "110m2"), (120, "120m2"), (130, "130m2"), (140, "140m2"),
                                        (1000, "150m2+")], validate_choice=False)
    min_area_land = SelectField('', choices=[(0, "Min m2"), (500, "500m2"), (1000, "1000m2"), (1500, "1500m2"),
                                             (2000, "2000m2"),(2500, "2500m2"), (3000, "3000m2"), (3500, "3500m2"),
                                             (4000, "4000m2"), (4500, "4500m2"), (5000, "5000m2"), (5000, "5000m2+")],
                                validate_choice=False)
    max_area_land = SelectField('', choices=[(100000, "Max m2"), (500, "500m2"), (1000, "1000m2"), (1500, "1500m2"),
                                             (2000, "2000m2"),(2500, "2500m2"), (3000, "3000m2"), (3500, "3500m2"),
                                             (4000, "4000m2"), (4500, "4500m2"), (5000, "5000m2"), (100000, "5000m2+")],
                                validate_choice=False)

    min_floor = SelectField('', choices=[(0, "Min piętro"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"),
                                         (7, "7"), (8, "8"), (9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13"),
                                         (14, "14"), (15, "15+")], validate_choice=False)
    max_floor = SelectField('', choices=[(101, "Max piętro"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6"),
                                         (7, "7"), (8, "8"), (9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13"),
                                         (14, "14"), (100, "15+")], validate_choice=False)
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

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    POSTGRES_DATABASE_HOST_ADDRESS = os.environ.get('POSTGRES_DATABASE_HOST_ADDRESS')
    POSTGRES_DATABASE_NAME = os.environ.get('POSTGRES_DATABASE_NAME')
    POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
    POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_CONNECTION_PORT = "5432"

    db_info = "host='%s' dbname='%s' user='%s' password='%s' sslmode='require'  port='%s'" % (
    POSTGRES_DATABASE_HOST_ADDRESS, POSTGRES_DATABASE_NAME, POSTGRES_USERNAME, POSTGRES_PASSWORD,
    POSTGRES_CONNECTION_PORT)
    con = psycopg2.connect(db_info)

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
database="real_estate", user='postgres', password='', host="localhost", port=5432
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


def filter_select(city, min_rooms, max_rooms, min_area, max_area, min_floor, max_floor, rent_sell):

    POSTGRES_DATABASE_HOST_ADDRESS = 'ccaml3dimis7eh.cluster-czz5s0kz4scl.eu-west-1.rds.amazonaws.com'
    POSTGRES_DATABASE_NAME = 'd2bib13eka3ngm'
    POSTGRES_USERNAME = 'uf4c8m5ko9g43g'
    POSTGRES_PASSWORD = 'p864da304922dcf7c9b57f57b3e58283892e585f147e8bfe622e89a5ab1ab1d87'
    POSTGRES_CONNECTION_PORT = "5432"

    db_info = "host='%s' dbname='%s' user='%s' password='%s' sslmode='require'  port='%s'" % (
        POSTGRES_DATABASE_HOST_ADDRESS, POSTGRES_DATABASE_NAME, POSTGRES_USERNAME, POSTGRES_PASSWORD,
        POSTGRES_CONNECTION_PORT)
    con = psycopg2.connect(db_info)
    cur = con.cursor()

    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
    #LEGACY QUERY#
    
    statement = f'''SELECT district, avg(sqr_price), avg(price), avg(area), count(*)  FROM {city}
                        where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                              area >= {min_area} and area <= {max_area} and
                              floor >= {min_floor} and floor <= {max_floor} and 
                              date = (select max(date) from {city})
                            group by district
                            order by avg(sqr_price) desc'''
                            
    """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

    statement = f'''SELECT 
                                district,
                                
                                AVG(CASE date WHEN (select max(date) from {city}) then sqr_price end),
                                
                                AVG(CASE date WHEN (select max(date) from {city}) then price end),
                                
                                AVG(CASE date WHEN (select max(date) from {city}) then area end),
                                
                                COUNT(CASE date WHEN (select max(date) from {city}) then price end),
                                
                                cast(ROUND(
                                (avg(CASE date WHEN (select max(date) from {city}) then price end) -
                                avg(CASE date WHEN (select max(date) from {city} where date < 
                                (select max(date) from {city})) then price end)) /
                                avg(CASE date WHEN (select max(date) from {city} where date < 
                                (select max(date) from {city})) then price end)
                                * 100 ,1) as float),
                                
                                COUNT(CASE date WHEN (select max(date) from {city}) then price end) -
                                COUNT(CASE date WHEN (select max(date) from {city} where date < 
                                (select max(date) from {city})) then price end)
                                
                                FROM {city}
                                
                                where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                                area >= {min_area} and area <= {max_area} and
                                floor >= {min_floor} and floor <= {max_floor} 
                                
                                group by district
                                
                                order by avg(sqr_price) desc
                                '''

    statement2 = f'''SELECT avg(sqr_price), avg(price), count(*)  FROM {city}
                            where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                                  area >= {min_area} and area <= {max_area} and
                                  floor >= {min_floor} and floor <= {max_floor} and
                                    date = (select max(date) from {city})'''

    if int(rent_sell) == 1:
        statement = f'''SELECT 
                                        district,
                                        
                                        AVG(CASE date WHEN (select max(date) from {city}_rent) then price end),
                                        
                                        AVG(CASE date WHEN (select max(date) from {city}_rent) then area end),
                                        
                                        COUNT(CASE date WHEN (select max(date) from {city}_rent) then price end),

                                        cast(ROUND(
                                        (avg(CASE date WHEN (select max(date) from {city}_rent) then price/area end) -
                                        avg(CASE date WHEN (select max(date) from {city}_rent where date < 
                                        (select max(date) from {city}_rent)) then price/area end)) /
                                        avg(CASE date WHEN (select max(date) from {city}_rent where date < 
                                        (select max(date) from {city}_rent)) then price/area end)
                                        * 100 ,1) as float),
                                        
                                        COUNT(CASE date WHEN (select max(date) from {city}_rent) then price end) -
                                        COUNT(CASE date WHEN (select max(date) from {city}_rent where date < 
                                        (select max(date) from {city}_rent)) then price end)
                                        
                                        FROM {city}_rent
                                        
                                        where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                                        area >= {min_area} and area <= {max_area} and
                                        floor >= {min_floor} and floor <= {max_floor} 
                                        
                                        group by district
                                        
                                        order by 
                                        AVG(CASE date WHEN (select max(date) from {city}_rent) then price/area end) desc
                                        '''

        statement2 = f'''SELECT  avg(price), count(*)  FROM {city}_rent
                                    where rooms >= {min_rooms} and rooms <= {max_rooms} and 
                                          area >= {min_area} and area <= {max_area} and
                                          floor >= {min_floor} and floor <= {max_floor} and
                                            date = (select max(date) from {city}_rent)'''

    if city == "krakow_land":
        print("we are her", min_area, max_area)
        statement = f'''SELECT 
                                    district,

                                    AVG(CASE date WHEN (select max(date) from {city}) then sqr_price end),

                                    AVG(CASE date WHEN (select max(date) from {city}) then price end),

                                    AVG(CASE date WHEN (select max(date) from {city}) then area end),

                                    COUNT(CASE date WHEN (select max(date) from {city}) then price end),

                                    cast(ROUND(
                                    (avg(CASE date WHEN (select max(date) from {city}) then price end) -
                                    avg(CASE date WHEN (select max(date) from {city} where date < 
                                    (select max(date) from {city})) then price end)) /
                                    avg(CASE date WHEN (select max(date) from {city} where date < 
                                    (select max(date) from {city})) then price end)
                                    * 100 ,1) as float),

                                    COUNT(CASE date WHEN (select max(date) from {city}) then price end) -
                                    COUNT(CASE date WHEN (select max(date) from {city} where date < 
                                    (select max(date) from {city})) then price end)

                                    FROM {city}

                                    where area >= {min_area} and area <= {max_area}

                                    group by district

                                    order by avg(sqr_price) desc
                                    '''

        statement2 = f'''SELECT avg(sqr_price), avg(price), count(*)  FROM {city}
                                     where area >= {min_area} and area <= {max_area} and
                                        date = (select max(date) from {city})'''

    cur.execute(statement)
    queries = {1: []}
    iteration = 0
    avg = 0
    adds_count = 0
    for record in cur.fetchall():
        try:
            iteration += 1
            avg += record[-2]
            adds_count += record[-1]
            if any(elem is None for elem in record) is False:
                # noinspection PyTypeChecker
                queries[1].append(record)
            else:
                print(record)
        except:
            None
        queries[3] = [round(avg/iteration, 1), adds_count]
    cur.execute(statement2)
    queries[2] = cur.fetchall()
    con.close()
    return queries


def validation_if_min_greater_than_max(form):

    if form.min_floor.data is None or form.max_floor.data is None:
        pass
    elif int(form.min_rooms.data) > int(form.max_rooms.data):
        form.max_rooms.data = form.max_rooms.choices[0][0]
    if form.min_area.data is None or form.max_area.data is None:
        pass
    elif int(form.min_area.data) > int(form.max_area.data):
        form.max_area.data = form.max_area.choices[0][0]
    if form.min_floor.data is None or form.max_floor.data is None:
        pass
    elif int(form.min_floor.data) > int(form.max_floor.data):
        form.max_floor.data = form.max_floor.choices[0][0]
    print([form.max_rooms.data, form.max_area.data, form.max_floor.data])
    return [form.max_rooms.data, form.max_area.data, form.max_floor.data]


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FilterForm()
    validation_if_min_greater_than_max(form)
    if form.validate_on_submit():
        return render_template('index.html', data=filter_select('krakow', form.min_rooms.data, form.max_rooms.data,
                                                                form.min_area.data, form.max_area.data,
                                                                form.min_floor.data, form.max_floor.data,
                                                                form.rent_sell.data), form=form, house=False, land=False)
    return render_template('index.html', data=filter_select('krakow', 0, 100, 0, 10000, 0, 100, 0), form=form,
                           house=False, land=False)


@app.route('/krakow-house', methods=['GET', 'POST'])
def krakow_house():
    form = FilterForm()
    validation_if_min_greater_than_max(form)
    if form.validate_on_submit():
        return render_template('index.html', data=filter_select('krakow_house', form.min_rooms.data, form.max_rooms.data,
                                                                form.min_area.data, form.max_area.data,
                                                                form.min_floor.data, form.max_floor.data,
                                                                form.rent_sell.data), form=form, house=True, land=False)
    return render_template('index.html', data=filter_select('krakow_house', 0, 100, 0, 10000, 0, 100, 0), form=form,
                           house=True, land=False)


@app.route('/krakow-land', methods=['GET', 'POST'])
def krakow_land():
    form = FilterForm()
    if form.is_submitted():
        print("yes its validates")
        return render_template('index.html', data=filter_select('krakow_land', 0, 100, form.min_area_land.data,
                                                                form.max_area_land.data, 0, 100, 0), form=form,
                               house=True, land=True)
    return render_template('index.html', data=filter_select('krakow_land', 0, 100, 0, 100000, 0, 100, 0), form=form,
                           house=True, land=True)

@app.route('/warszawa', methods=['GET', 'POST'])
def warszawa():
    form = FilterForm()
    validation_if_min_greater_than_max(form)
    if form.validate_on_submit():
        return render_template('index.html', data=filter_select('warszawa', form.min_rooms.data, form.max_rooms.data,
                                                                form.min_area.data, form.max_area.data,
                                                                form.min_floor.data, form.max_floor.data,
                                                                form.rent_sell.data), form=form, house=False, land=False)
    return render_template('index.html', data=filter_select('warszawa', 0, 100, 0, 10000, 0, 100, 0), form=form,
                           house=False, land=False)




if __name__ == "__main__":
    app.run(debug=True)
