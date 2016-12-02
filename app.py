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

@app.route("/")
def main():
    cnx = mysql.connect()
    cursor = cnx.cursor()
    return render_template('index.html')

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

<<<<<<< HEAD
=======





    return render_template("customer.html", genre=returnGenre, date=returnDate, name=returnName, showing=returnShowing)



@app.route('/attendShowing', methods=['POST','GET'])
def attendShowing():
    return render_template("attendShowing.html")


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



>>>>>>> dan
    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))
    temp = selShowing.split()


    try:
        if request.method == 'POST':
            firstName = selName.split()
            dateTime = temp[0] + " " + temp[1]

            cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s ''', (firstName[0]))
            customerId = cursor.fetchone()
            finalCustomerID = int(customerId[0])

            cursor.execute('''SELECT Showing.idShowing FROM Showing INNER JOIN Movie ON Showing.Movie_idMovie=Movie.idMovie WHERE Showing.ShowingDateTime=%s''', (dateTime))
            movieId = cursor.fetchone()
            finalMovieId = int(movieId[0])

            print finalMovieId
            print finalCustomerID

            cursor.execute("INSERT INTO Attend (Customer_idCustomer, Showing_idShowing) VALUES (%s, %s)", (finalCustomerID, finalMovieId))
            cxn.commit()
            flash(selName + " successfully booked the " + temp[2] + " showing at " + temp[1] + " on " + temp[0])

            return render_template("attendShowing.html", name=returnName, showing=returnShowing)

        else:
            return render_template("attendShowing.html", name=returnName, showing=returnShowing)

    except Exception as e:
        flash(selName + " could not successfully book this showing")
        return render_template('attendShowing.html')




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
            firstName = attendName.split()
            dateTime = temp[0] + " " + temp[1]

            cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s ''', (firstName[0]))
            customerId = cursor.fetchone()
            finalCustomerID = int(customerId[0])

            cursor.execute('''SELECT Showing.idShowing FROM Showing INNER JOIN Movie ON Showing.Movie_idMovie=Movie.idMovie WHERE Showing.ShowingDateTime=%s''', (dateTime))
            movieId = cursor.fetchone()
            finalMovieId = int(movieId[0])

            print finalMovieId
            print finalCustomerID
            print rating


            success = cursor.execute('''UPDATE Attend SET RATING=%s WHERE Customer_idCustomer=%s AND Showing_idShowing=%s''', (rating,finalCustomerID, finalMovieId))
            print success

            if success == 0:
                flash ("Sorry, you are unable to rate a showing you haven't seen.")
                return render_template('rateMovie.html', name=returnName, showing=returnShowing)
            else:
                cxn.commit()
                flash("You have successfully rated your showing.")
                return render_template('rateMovie.html', name=returnName, showing=returnShowing)

        except Exception as e:
            flash("Sorry, unexpected error. Please go back to the main page")
            return render_template('rateMovie.html', name=returnName, showing=returnShowing)

    else:
        return render_template('rateMovie.html', name=returnName, showing=returnShowing)






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


    if request.method=='POST':
        attendName = str(request.form.get('attendName'))

        firstName = attendName.split()


        cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s''', (firstName[0]))
        customerId = cursor.fetchone()
        finalCustomerID = int(customerId[0])


        success = cursor.execute('''SELECT Attend.Rating, Movie.MovieName FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie INNER JOIN Attend ON Showing.idShowing=Attend.Showing_idShowing WHERE Attend.Customer_idCustomer=%s ''', (finalCustomerID))
        data=cursor.fetchall()


<<<<<<< HEAD
    return render_template("customer.html", genre=returnGenre, date=returnDate, name=returnName, showing=returnShowing)
=======

>>>>>>> dan


        if success == 0:
            flash ("Sorry, please watch a movie to see your history.")
            return render_template('history.html', name=returnName, data=data)
        else:
            cxn.commit()
            flash("You have successfully viewed your history.")
            return render_template('history.html', name=returnName, data=data)

#        except Exception as e:
#            print (e)
#            return render_template('history.html')

    else:
        return render_template('history.html', name=returnName)



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


    if request.method=='POST':
        attendName = str(request.form.get('attendName'))

        firstName = attendName.split()


        cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName=%s''', (firstName[0]))
        customerId = cursor.fetchone()
        finalCustomerID = int(customerId[0])


        success = cursor.execute('''SELECT idCustomer, FirstName, LastName, EmailAddress, Sex FROM Customer WHERE idCustomer=%s ''', (finalCustomerID))
        data=cursor.fetchall()



        if success == 0:
            flash ("Sorry, we have no history of you.")
            return render_template('profile.html', name=returnName, data=data)
        else:
            cxn.commit()
            flash("You have successfully viewed your history.")
            return render_template('profile.html', name=returnName, data=data)

#        except Exception as e:
#            print (e)
#            return render_template('history.html')

    else:
        return render_template('profile.html', name=returnName)




@app.route("/sqlInjection", methods=['POST','GET'])
def sqlInjection():



    return render_template("sqlInjection.html")




@app.route("/sqlInjected", methods=['POST','GET'])
def sqlInjected():

    cxn = mysql.connect()
    cursor = cxn.cursor()



    if request.method=='POST':
        attendName = str(request.form.get('searchQuery'))
        print attendName

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




    return render_template("advSearch.html", searchGenre=returnGenre, date=returnDate)




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





    if request.method=='POST':
        genre = str(request.form.get('searchGenre'))
        startDate = str(request.form.get('startDate'))
        endDate = str(request.form.get('endDate'))
        searchQuery = str(request.form.get('searchQuery'))


        genreRequired = str(request.form.get('genreRequired'))
        dateRequired = str(request.form.get('dateRequired'))
        searchRequired = str(request.form.get('searchRequired'))
        seatRequired = str(request.form.get('seatRequired'))

        print searchQuery



        #massive compiled search
        success = cursor.execute('''SELECT Movie.MovieName, Showing.ShowingDateTime FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie INNER JOIN Genre ON Showing.Movie_idMovie=Genre.Movie_idMovie WHERE Genre.Genre=%s AND Showing.ShowingDateTime>=%s AND Showing.ShowingDateTime<=%s AND Movie.MovieName=%s''', (genre, startDate, endDate, searchQuery))
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








@app.route("/searchGenre", methods=['POST','GET'])
def searchGenre():
    cxn = mysql.connect()
    cursor = cxn.cursor()


#query for genre
    cursor.execute('''SELECT DISTINCT Genre FROM Genre''')
    genre = cursor.fetchall()
    returnGenre = []

    for i in genre:
        returnGenre.append(i)


    return render_template("searchGenre.html", searchGenre=returnGenre)



@app.route("/searchedGenre", methods=['POST','GET'])
def searchedGenre():
    cxn = mysql.connect()
    cursor = cxn.cursor()


#query for genre
    cursor.execute('''SELECT DISTINCT Genre FROM Genre''')
    genre = cursor.fetchall()
    returnGenre = []

    for i in genre:
        returnGenre.append(i)


    if request.method=='POST':
        genre = str(request.form.get('searchGenre'))


        success = cursor.execute('''SELECT Movie.MovieName, Showing.ShowingDateTime FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie INNER JOIN Genre ON Showing.Movie_idMovie=Genre.Movie_idMovie WHERE Genre.Genre=%s''', (genre))
        data=cursor.fetchall()




        if success == 0:
            flash ("Sorry, no showings available.")
            return render_template('searchGenre.html', searchGenre=returnGenre, data=data)
        else:
            cxn.commit()
            flash("You have successfully searched by genre.")
            return render_template('searchGenre.html', searchGenre=returnGenre, data=data)

    else:
        return render_template("searchGenre.html", searchGenre=returnGenre)



@app.route("/searchDate", methods=['POST','GET'])
def searchDate():
    cxn = mysql.connect()
    cursor = cxn.cursor()

    #query for range of show times
    cursor.execute("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime ASC")
    dates = cursor.fetchall()
    returnDate = []
    for i in dates:
        returnDate.append(i)


    return render_template("searchDate.html", date=returnDate)



@app.route("/searchedDate", methods=['POST','GET'])
def searchedDate():
    cxn = mysql.connect()
    cursor = cxn.cursor()

    #query for range of show times
    cursor.execute("SELECT DISTINCT ShowingDateTime FROM Showing ORDER BY ShowingDateTime ASC")
    dates = cursor.fetchall()
    returnDate = []
    for i in dates:
        returnDate.append(i)

    if request.method=='POST':
        startDate = str(request.form.get('startDate'))
        endDate = str(request.form.get('endDate'))

        try:
            success = cursor.execute('''SELECT Movie.MovieName, Showing.ShowingDateTime FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie WHERE Showing.ShowingDateTime>=%s AND Showing.ShowingDateTime<=%s''', (startDate,endDate))
            data=cursor.fetchall()
        except Exception as e:
            flash ("Select a proper start date and end date.")
            return render_template("searchDate.html", date=returnDate)



        if success == 0:
            flash ("Sorry, there are no showings available for those selected dates.")
            return render_template('searchDate.html', date=returnDate, data=data)
        else:
            cxn.commit()
            flash("You have successfully searched by dates.")
            return render_template('searchDate.html', date=returnDate, data=data)



    return render_template("searchDate.html", date=returnDate)





@app.route("/searchSeat", methods=['POST','GET'])
def searchSeat():
    return render_template("searchSeat.html")



@app.route("/searchTitle", methods=['POST','GET'])
def searchTitle():
    return render_template("searchTitle.html")











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
    print result
    return render_template('/staffComponents/displayMovie.html', data=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
