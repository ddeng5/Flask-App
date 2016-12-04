#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, json, jsonify, flash, session

from datetime import datetime
from flaskext.mysql import MySQL
app = Flask(__name__)


mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'MovieTheatre'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'Secret String'
mysql.init_app(app)


#main page
@app.route("/")
def main():
    cnx = mysql.connect()
    cursor = cnx.cursor()
    return render_template('index.html')

#main customer page
@app.route('/customer', methods=['POST','GET'])
def customerSearch():

#query for genres
    cxn = mysql.connect()
    cursor = cxn.cursor()
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



    #return the customer page with the rendered elements
    return render_template("customer.html", genre=returnGenre, date=returnDate, name=returnName, showing=returnShowing)


#main page for customers who want to buy a ticket
@app.route('/attendShowing', methods=['POST','GET'])
def attendShowing():
    return render_template("attendShowing.html")


#the buy ticket page after submitting a request
@app.route('/buyTicket', methods=['POST','GET'])
def buyTicket():
    cxn = mysql.connect()
    cursor = cxn.cursor()

    #query for first and last name
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

    #get the customer selected values from the webpage
    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))
    temp = selShowing.split()

    #if the customer is requesting to book a showing
    try:
        if request.method == 'POST':
            #parse the full name to return just the first name to match with sql database/table
            firstName = selName.split()
            dateTime = temp[0] + " " + temp[1]

            #get the customer id
            cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s ''', (firstName[0]))
            customerId = cursor.fetchone()
            finalCustomerID = int(customerId[0])

            #get the movie id
            cursor.execute('''SELECT Showing.idShowing FROM Showing INNER JOIN Movie ON Showing.Movie_idMovie=Movie.idMovie WHERE Showing.ShowingDateTime=%s''', (dateTime))
            movieId = cursor.fetchone()
            finalMovieId = int(movieId[0])

            #sql query to insert customer into the Attned table
            cursor.execute("INSERT INTO Attend (Customer_idCustomer, Showing_idShowing) VALUES (%s, %s)", (finalCustomerID, finalMovieId))
            cxn.commit()
            flash(selName + " successfully booked the " + temp[2] + " showing at " + temp[1] + " on " + temp[0])

            #return the page with the submitted request
            return render_template("attendShowing.html", name=returnName, showing=returnShowing)

        else:
            return render_template("attendShowing.html", name=returnName, showing=returnShowing)

    #catch any exceptions and return error message
    except Exception as e:
        flash(selName + " could not successfully book this showing")
        return render_template('attendShowing.html')



#rate movie main page
@app.route('/rateMovie', methods=['POST','GET'])
def rateMovie():
    cxn = mysql.connect()
    cursor = cxn.cursor()


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

    if request.method=='POST':
        attendName = str(request.form.get('attendName'))
        attendShowing = str(request.form.get('attendShowing'))
        temp = attendShowing.split()
        rating = int(request.form.get('rating'))

        try:
            #split name to get the firstname to match with sql database
            firstName = attendName.split()
            dateTime = temp[0] + " " + temp[1]

            #find customer id
            cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s ''', (firstName[0]))
            customerId = cursor.fetchone()
            finalCustomerID = int(customerId[0])

            #find movie id
            cursor.execute('''SELECT Showing.idShowing FROM Showing INNER JOIN Movie ON Showing.Movie_idMovie=Movie.idMovie WHERE Showing.ShowingDateTime=%s''', (dateTime))
            movieId = cursor.fetchone()
            finalMovieId = int(movieId[0])


            #update the table with the new rating
            success = cursor.execute('''UPDATE Attend SET RATING=%s WHERE Customer_idCustomer=%s AND Showing_idShowing=%s''', (rating,finalCustomerID, finalMovieId))


            if success == 0:
                flash ("Sorry, you are unable to rate a showing you haven't seen.")
                return render_template('rateMovie.html', name=returnName, showing=returnShowing)
            else:
                cxn.commit()
                flash("You have successfully rated your showing.")
                return render_template('rateMovie.html', name=returnName, showing=returnShowing)

        #catch any exceptions and reply with an error message
        except Exception as e:
            flash("Sorry, unexpected error. Please go back to the main page")
            return render_template('rateMovie.html', name=returnName, showing=returnShowing)

    else:
        return render_template('rateMovie.html', name=returnName, showing=returnShowing)





#main history page
@app.route("/history", methods=['POST','GET'])
def history():

    cxn = mysql.connect()
    cursor = cxn.cursor()


    #query for name
    cursor.execute('''SELECT CONCAT_WS(" ", FirstName, LastName) AS wholename FROM Customer''')
    name = cursor.fetchall()
    returnName = []
    for i in name:
        returnName.append(i)


    return render_template("history.html", name=returnName)


#after submit request, redirect customer to this page
@app.route("/grabHistory", methods=['POST','GET'])
def grabHistory():

    cxn = mysql.connect()
    cursor = cxn.cursor()


    #query for name
    cursor.execute('''SELECT CONCAT_WS(" ", FirstName, LastName) AS wholename FROM Customer''')
    name = cursor.fetchall()
    returnName = []

    for i in name:
        returnName.append(i)

    #if the customer is posting, we need to do the necessary back end stuff with the sql database
    if request.method=='POST':
        attendName = str(request.form.get('attendName'))
        #get the first name
        firstName = attendName.split()

        #grab customer id
        cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s''', (firstName[0]))
        customerId = cursor.fetchone()
        finalCustomerID = int(customerId[0])

        #grab the customers history
        success = cursor.execute('''SELECT Attend.Rating, Movie.MovieName FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie INNER JOIN Attend ON Showing.idShowing=Attend.Showing_idShowing WHERE Attend.Customer_idCustomer=%s ''', (finalCustomerID))
        data=cursor.fetchall()



        if success == 0:
            flash ("Sorry, please watch a movie to see your history.")
            return render_template('history.html', name=returnName, data=data)
        else:
            cxn.commit()
            flash("You have successfully viewed your history.")
            return render_template('history.html', name=returnName, data=data)


    else:
        return render_template('history.html', name=returnName)


#main page for customer profile
@app.route("/profile", methods=['POST','GET'])
def profile():

    cxn = mysql.connect()
    cursor = cxn.cursor()


    #query for name
    cursor.execute('''SELECT CONCAT_WS(" ", FirstName, LastName) AS wholename FROM Customer''')
    name = cursor.fetchall()
    returnName = []
    for i in name:
        returnName.append(i)


    return render_template("profile.html", name=returnName)



#redirect page from the main profile page
@app.route("/grabAll", methods=['POST','GET'])
def grabAll():

    cxn = mysql.connect()
    cursor = cxn.cursor()


    #query for name
    cursor.execute('''SELECT CONCAT_WS(" ", FirstName, LastName) AS wholename FROM Customer''')
    name = cursor.fetchall()
    returnName = []

    for i in name:
        returnName.append(i)

    #if the customer is posting, do the necessary back end sql queries
    if request.method=='POST':
        attendName = str(request.form.get('attendName'))
        #grab first name
        firstName = attendName.split()

        #get customer id
        cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s''', (firstName[0]))
        customerId = cursor.fetchone()
        finalCustomerID = int(customerId[0])

        #grab customer's profile information
        success = cursor.execute('''SELECT idCustomer, FirstName, LastName, EmailAddress, Sex FROM Customer WHERE idCustomer=%s ''', (finalCustomerID))
        data=cursor.fetchall()



        if success == 0:
            flash ("Sorry, we have no history of you.")
            return render_template('profile.html', name=returnName, data=data)
        else:
            cxn.commit()
            flash("You have successfully viewed your history.")
            return render_template('profile.html', name=returnName, data=data)


    else:
        return render_template('profile.html', name=returnName)



#main page for sql injection
@app.route("/sqlInjection", methods=['POST','GET'])
def sqlInjection():
    return render_template("sqlInjection.html")



#sql injection
@app.route("/sqlInjected", methods=['POST','GET'])
def sqlInjected():

    cxn = mysql.connect()
    cursor = cxn.cursor()


    #if the customer is posting, do appropriate actions
    if request.method=='POST':
        attendName = str(request.form.get('searchQuery'))

        #add the customer input to the sql query string
        success = cursor.execute("SELECT idCustomer, FirstName, LastName, EmailAddress, Sex FROM Customer WHERE idCustomer= '%s'; " % attendName)
        data=cursor.fetchall()



        if success == 0:
            flash ("Sorry, we have no history of you.")
            return render_template('sqlInjection.html', data=data)
        else:
            cxn.commit()
            flash("You have successfully viewed your history.")
            return render_template('sqlInjection.html', data=data)

#        except Exception as e:
#            print (e)
#            return render_template('history.html')

    else:
        return render_template('sqlInjection.html')




#main advanced search page
@app.route("/search", methods=['POST','GET'])
def search():
    cxn = mysql.connect()
    cursor = cxn.cursor()


    #query for genre
    cursor.execute('''SELECT DISTINCT Genre FROM Genre''')
    genre = cursor.fetchall()
    returnGenre = []

    for i in genre:
        returnGenre.append(i)


    #query for range of show times
    cursor.execute("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime ASC")
    dates = cursor.fetchall()
    returnDate = []
    for i in dates:
        returnDate.append(i)



    #return the advance search page with the rendered elements
    return render_template("advSearch.html", searchGenre=returnGenre, date=returnDate)



#redirect page from the main advanced search page
@app.route("/searched", methods=['POST','GET'])
def searched():
    cxn = mysql.connect()
    cursor = cxn.cursor()


    #query for genre
    cursor.execute('''SELECT DISTINCT Genre FROM Genre''')
    genre = cursor.fetchall()
    returnGenre = []

    for i in genre:
        returnGenre.append(i)


    #query for range of show times
    cursor.execute("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime ASC")
    dates = cursor.fetchall()
    returnDate = []
    for i in dates:
        returnDate.append(i)



    #if customer is posting their selections, take appropriate actions
    if request.method=='POST':
        #grab the user selections from the html page
        genre = str(request.form.get('searchGenre'))
        startDate = str(request.form.get('startDate'))
        endDate = str(request.form.get('endDate'))
        searchQuery = str(request.form.get('searchQuery'))


        genreRequired = str(request.form.get('genreRequired'))
        dateRequired = str(request.form.get('dateRequired'))
        searchRequired = str(request.form.get('searchRequired'))
        seatRequired = str(request.form.get('seatRequired'))


        #setup views for checking availability for movies and their respective theatre capacities
        cursor.execute("CREATE OR REPLACE VIEW avail AS SELECT Showing_idShowing, Count(*) AS count FROM Attend JOIN Showing ON Attend.Showing_idShowing = Showing.idShowing GROUP BY Showing_idShowing;")
        cursor.execute("CREATE OR REPLACE VIEW avail2 AS SELECT idShowing, capacity FROM Showing JOIN theatreRoom ON Showing.TheatreRoom_RoomNumber = TheatreRoom.RoomNumber;")

        #set up sql queries for different selected search criteria
        baseSql = "SELECT Movie.MovieName, Showing.ShowingDateTime FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie INNER JOIN Genre ON Showing.Movie_idMovie=Genre.Movie_idMovie WHERE"
        genreSql = "Genre.Genre=\'%s\'" % genre
        dateSql = "Showing.ShowingDateTime>=\'%s\' AND Showing.ShowingDateTime<=\'%s\'" % (startDate,endDate)
        seatSql = "Showing.idShowing IN (SELECT idShowing FROM avail2 JOIN avail ON avail.Showing_idShowing = avail2.idShowing WHERE avail2.capacity > avail.count)"
        searchSQL = "Movie.MovieName=\'%s\'" % searchQuery


        #check the search criteria
        if genreRequired<>"no":
            baseSql = baseSql + " " + genreSql

        if dateRequired<>"no":
            baseSql = baseSql + " AND " + dateSql

        if seatRequired<>"yes":
            baseSql = baseSql + " AND " + seatSql

        if searchRequired<>"no":
            baseSql = baseSql + " AND " + searchSQL



        #execute massive compiled search
        success = cursor.execute(baseSql)

        #grab the returned data
        data=cursor.fetchall()



        if success == 0:
            flash ("Sorry, no showings available.")
            return render_template('advSearch.html', searchGenre=returnGenre, date=returnDate, data=data)
        else:
            cxn.commit()
            flash("You have successfully searched by genre.")
            return render_template('advSearch.html', searchGenre=returnGenre, date=returnDate, data=data)


    else:
        return render_template("advSearch.html", searchGenre=returnGenre, date=returnDate)








@app.route('/staff')
def staffLogin():
    return render_template('staff.html')

@app.route('/displaymovie_page')
def displaymovie_page():
    displayMovie()
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
    return render_template('/staffComponents/displayMovie.html', data=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
