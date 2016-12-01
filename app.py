from flask import Flask, render_template, request, json, jsonify
from datetime import datetime
from flaskext.mysql import MySQL
app = Flask(__name__)


mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'MovieTheatre'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route("/")
def main():
    return render_template('index.html')

@app.route('/customer', methods=['POST','GET'])
def customerSearch():

#query for genres
    cnx = mysql.connector.connect()
    cursor = cnx.cursor()
    cursor.execute("SELECT DISTINCT Genre FROM Genre")
    genres = cursor.fetchall()

    returnGenre = []
    for i in genres:
        returnGenre.append(i)


#query for range of show times
    cursor.execute("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime ASC")
    dates = cursor.fetchall()
    returnDate = []
    for i in dates:
        returnDate.append(i)


#query for name
    cursor.execute('''SELECT CONCAT_WS(" ", FirstName, LastName) AS wholename FROM Customer''')
    name = cursor.fetchall()
    returnName = []
    for i in name:
        returnName.append(i)


#query for showings
    cursor.execute('''SELECT CONCAT(Showing.ShowingDateTime,' ', Movie.MovieName) AS timeMovie FROM Showing INNER JOIN Movie ON Movie.idMovie=Showing.Movie_idMovie''')
    showings = cursor.fetchall()
    returnShowing = []
    for i in showings:
        returnShowing.append(i)







    return render_template("customer.html", genre=returnGenre, date=returnDate, name=returnName, showing=returnShowing)







@app.route("/customer/selectShowing", methods=['POST','GET'])
def selectShowing():
    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))

    cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s ''', ('Will'))
    customerId=cursor.fetchone()


    for each in customerId:
        print each

    print 'wow'

    return render_template("customer.html")



@app.route('/staff')
def staffLogin():
    return render_template('staff.html')


#add movies
@app.route('/submit', methods=['POST'])
def addMovie():
    insertFunc = (
        "INSERT INTO Movie (movieName, movieID, movieYear) "
    "VALUES (%s, %s)"
    )
    data = (request.form['movieName'], request.form['movieID'], request.form['movieYear']) 
    cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()
    return render_template('movieForm.html',request.form['movieName'], request.form['movieID'], request.form['movieYear'])

#delete movies
@app.route('/submit', methods=['POST'])
def addMovie():
    insertFunc = (
        "DELETE FROM Movie where idMovie = movieID)"
    )
    data = (request.form['movieName'], request.form['movieID'], request.form['movieYear']) 
    cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()
    return render_template('movieForm.html',request.form['movieName'], request.form['movieID'], request.form['movieYear'])


if __name__ == "__main__":
    app.run()
