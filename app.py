#!/usr/bin/env python
# -*- coding: utf-8 -*- 

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
    cnx = mysql.connector.connect()
    cursor = cnx.cursor()
    return render_template('index.html')

@app.route('/customer', methods=['POST','GET'])
def customerSearch():

#query for genres
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

@app.route('/displaymovie_page')
def displaymovie_page():
    return render_template('/staffComponents/displayMovie.html')



#add movies
@app.route('/addmovie', methods=['POST'])
def addMovie():
    
    if (movieYear == ''):
        insertFunc = (
            "INSERT INTO Movie (movieName, movieID)"
            "VALUES (%s, %s)"
        )
        data = (request.form['movieName'], request.form['movieID']) 
        cursor.execute(insertFunc, data)
        cnx.commit()
        cnx.close()
        return render_template('movieForm.html',request.form['movieName'], request.form['movieID'])
    else:
        insertFunc = (
            "INSERT INTO Movie (movieName, movieID)"
            "VALUES (%s, %s)"
        )
        data = (request.form['movieName'], request.form['movieID'], request.form['movieYear']) 
        cursor.execute(insertFunc, data)
        cnx.commit()
        cnx.close()
        return render_template('movieForm.html',request.form['movieName'], request.form['movieID'], request.form['movieYear'])


#delete movies
@app.route('/deletemovie', methods=['POST'])
def deleteMovie():
    insertFunc = (
        "DELETE FROM Attend where Showing_idShowing IN (SELECT idShowing FROM Showing WHERE idMovie = movieID)"
        "DELETE FROM Showing where idMovie = movieID"
        "DELETE FROM Movie where idMovie = movieID"
    )
    data = (request.form['movieName'], request.form['movieID'], request.form['movieYear']) 
    cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()
    return render_template('movieForm.html',request.form['movieName'], request.form['movieID'], request.form['movieYear'])

#modify movies
@app.route('/updatemovie', methods=['POST'])
def updateMovie():
    insertFunc = (
        "UPDATE Movie SET MovieName = movieName WHERE idMovie = MovieID" 
        "UPDATE Movie SET MovieYEAR = movieYear WHERE idMovie = MovieID"
    )
    data = (request.form['movieName'], request.form['movieID'], request.form['movieYear']) 
    cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()
    return render_template('movieForm.html',request.form['movieName'], request.form['movieID'], request.form['movieYear'])

#list all movies and all attributes sorted alphabetically by movie name
@app.route('/displaymovie', methods=['POST','GET'])
def displayMovie():
    insertFunc = ("SELECT * FROM Movie order by MovieName")
    cursor.execute(insertFunc)
    result = cursor.fetchall()
    cnx.close()
    print result
    return render_template('/staffComponents/displayMovie.html', data=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
