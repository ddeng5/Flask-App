#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, json, jsonify, flash, session
from datetime import datetime
import mysql.connector
import base64
import os

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'MovieTheatre'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['SECRET_KEY'] = 'Secret String'

@app.route("/")
def main():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    try:
    	cursor.execute("ALTER TABLE Movie ADD poster BLOB")
    except Exception, e:
		print 'Poster column already exists'

    return render_template('index.html')

@app.route('/customer', methods=['POST','GET'])
def customerSearch():

#query for genres
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
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



@app.route('/attendShowing', methods=['POST','GET'])
def attendShowing():
    return render_template("attendShowing.html")


@app.route('/buyTicket', methods=['POST','GET'])
def buyTicket():
    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cxn.cursor()

    #query for first and last name
    cursor.execute("SELECT CONCAT_WS(' ', FirstName, LastName) AS wholename FROM Customer")
    name = cursor.fetchall()
    returnName = []
    for i in name:
        returnName.append(i)


    #query for showings
    cursor.execute("SELECT CONCAT(Showing.ShowingDateTime,' ', Movie.MovieName) AS timeMovie FROM Showing INNER JOIN Movie ON Movie.idMovie=Showing.Movie_idMovie")
    showings = cursor.fetchall()

    print showings
    returnShowing = []
    for i in showings:
        returnShowing.append(i)

    #get the customer selected values from the webpage
    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))
    temp = selShowing.split()



    if request.method == 'POST':
        #parse the full name to return just the first name to match with sql database/table
        firstName = selName.split()
        data_fname = firstName[0]
        dateTime = temp[0] + " " + temp[1]

        #get the customer id
        cursor.execute("SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName='%s'; "%data_fname)
        customerId = cursor.fetchone()
        finalCustomerID = int(customerId[0])

        #get the movie id
        cursor.execute("SELECT Showing.idShowing FROM Showing INNER JOIN Movie ON Showing.Movie_idMovie=Movie.idMovie WHERE Showing.ShowingDateTime='%s'; "%dateTime)
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






@app.route('/rateMovie', methods=['POST','GET'])
def rateMovie():
    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cxn.cursor()


#query for name
    cursor.execute('''SELECT CONCAT_WS(" ", FirstName, LastName) AS wholename FROM Customer''')
    name = cursor.fetchall()
    returnName = []
    for i in name:
        returnName.append(i)


#query for showings
    cursor.execute("SELECT CONCAT(Showing.ShowingDateTime,' ', Movie.MovieName) AS timeMovie FROM Showing INNER JOIN Movie ON Movie.idMovie=Showing.Movie_idMovie")
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
            data_firstName = firstName[0]
            dateTime = temp[0] + " " + temp[1]

            cursor.execute("SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName='%s'" %data_firstName)
            customerId = cursor.fetchone()
            finalCustomerID = int(customerId[0])

            cursor.execute("SELECT Showing.idShowing FROM Showing INNER JOIN Movie ON Showing.Movie_idMovie=Movie.idMovie WHERE Showing.ShowingDateTime='%s'" %dateTime)
            movieId = cursor.fetchone()
            finalMovieId = int(movieId[0])

            print finalMovieId
            print finalCustomerID
            print rating


            success = cursor.execute("UPDATE Attend SET RATING=%s WHERE Customer_idCustomer=%s AND Showing_idShowing=%s" %(rating,finalCustomerID, finalMovieId))
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

    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
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

    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
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
        data_fname = firstName[0]


        cursor.execute("SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName='%s'" %data_fname)
        customerId = cursor.fetchone()
        finalCustomerID = int(customerId[0])


        success = cursor.execute("SELECT Attend.Rating, Movie.MovieName FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie INNER JOIN Attend ON Showing.idShowing=Attend.Showing_idShowing WHERE Attend.Customer_idCustomer='%s'" %finalCustomerID)
        data=cursor.fetchall()

        if success<>0:
            flash ("Successfully pulled your past history.")
            return render_template('history.html', name=returnName, data=data)
        else:
            flash ("Unsuccessful in pulling your past history.")
            return render_template('history.html', name=returnName)


    cnx.close()

@app.route("/customer/selectShowing", methods=['POST','GET'])
def selectShowing():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))

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

@app.route("/profile", methods=['POST','GET'])
def profile():

    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cxn.cursor()


#query for name
    cursor.execute("SELECT CONCAT_WS(' ', FirstName, LastName) AS wholename FROM Customer")
    name = cursor.fetchall()
    returnName = []
    for i in name:
        returnName.append(i)


    return render_template("profile.html", name=returnName)




@app.route("/grabAll", methods=['POST','GET'])
def grabAll():
    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cxn.cursor()

#query for name
    cursor.execute("SELECT CONCAT_WS(' ', FirstName, LastName) AS wholename FROM Customer")
    name = cursor.fetchall()
    returnName = []

    for i in name:
        returnName.append(i)


    if request.method=='POST':
        attendName = str(request.form.get('attendName'))
        firstName = attendName.split()
        data_fname = firstName[0]


        cursor.execute("SELECT Customer.idCustomer FROM Customer WHERE Customer.FirstName='%s'" %data_fname)
        customerId = cursor.fetchone()
        finalCustomerID = int(customerId[0])


        success = cursor.execute("SELECT idCustomer, FirstName, LastName, EmailAddress, Sex FROM Customer WHERE idCustomer='%s' "%finalCustomerID)
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

    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
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
    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
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
    cxn = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cxn.cursor()


    #query for genre
    cursor.execute("SELECT DISTINCT Genre FROM Genre")
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


        cursor.execute("CREATE OR REPLACE VIEW avail AS SELECT Showing_idShowing, Count(*) AS count FROM Attend JOIN Showing ON Attend.Showing_idShowing = Showing.idShowing GROUP BY Showing_idShowing;")
        cursor.execute("CREATE OR REPLACE VIEW avail2 AS SELECT idShowing, capacity FROM Showing JOIN TheatreRoom ON Showing.TheatreRoom_RoomNumber = TheatreRoom.RoomNumber;")


        baseSql = "SELECT Movie.MovieName, Showing.ShowingDateTime FROM Movie INNER JOIN Showing ON Movie.idMovie=Showing.Movie_idMovie INNER JOIN Genre ON Showing.Movie_idMovie=Genre.Movie_idMovie WHERE"
        genreSql = "Genre.Genre='%s' "%genre
        dateSql = "Showing.ShowingDateTime>=%s AND Showing.ShowingDateTime<=%s"%(startDate,endDate)
        seatSql = "Showing.idShowing IN (SELECT idShowing FROM avail2 JOIN avail ON avail.Showing_idShowing = avail2.idShowing WHERE avail2.capacity > avail.count)"
        searchSQL = "Movie.MovieName='%s' "%searchQuery


        if seatRequired == 'None':
            seatRequired = 'no'

        print type(seatRequired)

        if genreRequired<>"no":
            baseSql = baseSql + " " + genreSql

        if dateRequired<>"no":
            baseSql = baseSql + " AND " + dateSql

        if seatRequired<>"no":
            baseSql = baseSql + " AND " + seatSql

        if searchRequired<>"no":
            baseSql = baseSql + " AND " + searchSQL

        baseSql = baseSql + ";"
        print baseSql






        #massive compiled search
        success = cursor.execute(baseSql)
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






#===============================[PAGE REFERENCES]=================================

@app.route('/staff')
def staffLogin():
    return render_template('staff.html')

#=================================Movie============================================

@app.route('/addMovieForm')
def addMovieForm():
    return render_template('/staffComponents/movie/addMovieForm.html')

@app.route('/deleteMovieForm')
def deleteMovieForm():
    return render_template('/staffComponents/movie/deleteMovieForm.html')

@app.route('/updateMovieForm')
def updateMovieForm():
    return render_template('/staffComponents/movie/updateMovieForm.html')

#=================================Genre============================================

@app.route('/addGenreForm')
def addGenreForm():
    return render_template('/staffComponents/genre/addGenreForm.html')

@app.route('/deleteGenreForm')
def deleteGenreForm():
    return render_template('/staffComponents/genre/deleteGenreForm.html')

@app.route('/updateGenreForm')
def updateGenreForm():
    return render_template('/staffComponents/genre/updateGenreForm.html')

#=================================Room============================================

@app.route('/addRoomForm')
def addRoomForm():
    return render_template('/staffComponents/room/addRoomForm.html')

@app.route('/deleteRoomForm')
def deleteRoomForm():
    return render_template('/staffComponents/room/deleteRoomForm.html')

@app.route('/updateRoomForm')
def updateRoomForm():
    return render_template('/staffComponents/room/updateRoomForm.html')

#=================================Showing==========================================

@app.route('/addShowingForm')
def addShowingForm():
    return render_template('/staffComponents/showing/addShowingForm.html')

@app.route('/deleteShowingForm')
def deleteShowingForm():
    return render_template('/staffComponents/showing/deleteShowingForm.html')

@app.route('/updateShowingForm')
def updateShowingForm():
    return render_template('/staffComponents/showing/updateShowingForm.html')

#=================================Customer==========================================

@app.route('/addCustomerForm')
def addCustomerForm():
    return render_template('/staffComponents/customer/addCustomerForm.html')

@app.route('/deleteCustomerForm')
def deleteCustomerForm():
    return render_template('/staffComponents/customer/deleteCustomerForm.html')

@app.route('/updateCustomerForm')
def updateCustomerForm():
    return render_template('/staffComponents/customer/updateCustomerForm.html')

#===============================[DISPLAY PAGE REFERENCE]=================================

@app.route('/displayMovie_page')
def displayMovie_page():
    result = displayMovie()
    return render_template('/staffComponents/movie/displayMovie.html', data=result)

@app.route('/displayGenre_page')
def displayGenre_page():
    result = displayGenre()
    return render_template('/staffComponents/genre/displayGenre.html', data=result)

@app.route('/displayRoom_page')
def displayRoom_page():
    result = displayRoom()
    return render_template('/staffComponents/room/displayRoom.html', data=result)

@app.route('/displayShowing_page')
def displayShowing_page():
    result = displayShowing()
    return render_template('/staffComponents/showing/displayShowing.html', data=result)

@app.route('/displayCustomer_page')
def displayCustomer_page():
    result = displayCustomer()
    return render_template('/staffComponents/customer/displayCustomer.html', data=result)

@app.route('/displayAttend_page')
def displayAttend_page():
    result = displayAttend()
    return render_template('/staffComponents/attend/displayAttend.html', data=result)

#===============================[MOVIE]=================================

#poster functions
#@app.route('/readfile', methods=['POST'])
#def read_file(filename):
#	with open(filename, 'rb') as f:
#		poster = base64.encodestring(f.read())
#	return poster

#@app.route('/writefile', methods=['POST'])
#def write_file(data, filename):
#	with open(filename, 'rb') as f:
#		poster = f.write(data)
#	return poster

#add movies
@app.route('/addmovie', methods=['POST'])
def addMovie():
    #create connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #query to be passed to the database

    if request.form['movieYear'] == '':
        insertFunc = ("INSERT INTO Movie (MovieName, idMovie) VALUES (%s, %s)")
        #data to be used
        data = (request.form['movieName'], request.form['movieID'])

    else:
        insertFunc = ("INSERT INTO Movie (MovieName, idMovie, movieYear) VALUES (%s, %s, %s)")
    	#data to be used
    	data = (request.form['movieName'], request.form['movieID'], request.form['movieYear'])
    #execution of the query
    success = cursor.execute(insertFunc, data)
    print success
    cnx.commit()
    cnx.close()

	#poster functions
	#if(request.form['poster'] is not None):
	#	cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
	#	cursor = cnx.cursor()
	#	posterUpload = ("UPDATE Movie SET poster = %s WHERE idMovie = %s"
	#		)
	#	posterimg = read_file(request.form['poster'])
	#	images have to be uploaded to the templates/staffComponents/movie/posters folder
	#	posterimg = read_file('/vagrant/Flask-App/templates/staffComponents/movie/posters/Capture.PNG')
	#	data = (posterimg, request.form['movieID'])
	#	cursor.execute(posterUpload, data)
	#	cnx.commit()
	#	cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/movie/addMovieForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/movie/addMovieForm.html')




#delete movies
@app.route('/deletemovie', methods=['POST'])
def deleteMovie():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    data = (request.form['movieID'])
    #delete query
    insertFunc = (
        "DELETE FROM Movie WHERE idMovie = '%s'; "%data
    )
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/movie/deleteMovieForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/movie/deleteMovieForm.html')


#modify movies
@app.route('/updatemovie', methods=['POST'])
def updateMovie():
    #separate queries for the movie name and movie year
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    insertFunc = ("UPDATE Movie SET MovieName = %s WHERE idMovie = %s")
    data = (request.form['movieName'], request.form['movieID'])
    cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    insertFunc = ("UPDATE Movie SET MovieYear = %s WHERE idMovie = %s")
    data = (request.form['movieYear'], request.form['movieID'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/movie/updateMovieForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/movie/updateMovieForm.html')

#list all movies and all attributes sorted alphabetically by movie name
@app.route('/displayMovie', methods=['POST','GET'])
def displayMovie():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
	cursor = cnx.cursor()
	insertFunc = ("SELECT * FROM Movie order by MovieName")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	#display poster
	#for movie in result:
	#	if movie[3] is not None:
	#		img = movie[3]
	#		missing_padding = len(img) % 4
	#		if missing_padding != 0:
	#			img += b'='*(4-missing_padding)
	#			movie[3] = base64.decodestring(img)
	#			cnx.close()
	#	print movie[3]
	return result

#===============================[GENRE]=================================

#add genre
@app.route('/addgenre', methods=['POST'])
def addGenre():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #MySQL query
    insertFunc = ("INSERT INTO Genre (Genre, Movie_idMovie) VALUES (%s, %s)")
    #data to be passed
    data = (request.form['genre'], request.form['movieID'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/genre/addGenreForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/genre/addGenreForm.html')

#delete genre
@app.route('/deletegenre', methods=['POST'])
def deleteGenre():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    insertFunc = ("DELETE FROM Genre WHERE genre = %s and Movie_idMovie = %s")
    data = (request.form['genre'], request.form['movieID'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/genre/deleteGenreForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/genre/deleteGenreForm.html')

#list all genres and movies
@app.route('/displayGenre', methods=['POST','GET'])
def displayGenre():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
	cursor = cnx.cursor()
	insertFunc = ("SELECT Genre, idMovie, MovieName FROM Genre JOIN Movie ON Movie.idMovie = Genre.Movie_idMovie ORDER BY Genre")
	cursor.execute(insertFunc)
	#gets all data and returns an array
	result = cursor.fetchall()
	cnx.close()
	return result

#===============================[ROOM]=================================

#add rooms
@app.route('/addroom', methods=['POST'])
def addRoom():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #query
    insertFunc = ("INSERT INTO TheatreRoom (RoomNumber, Capacity) VALUES (%s, %s)")
    #data
    data = (request.form['roomNumber'], request.form['capacity'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/room/addRoomForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/room/addRoomForm.html')


#delete room
@app.route('/deleteroom', methods=['POST'])
def deleteRoom():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #data
    data = (request.form['roomNumber'])
    #query
    insertFunc = ("DELETE FROM TheatreRoom WHERE roomNumber = '%s'; "%data)
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/room/deleteRoomForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/room/deleteRoomForm.html')

#modify rooms
@app.route('/updateroom', methods=['POST'])
def updateRoom():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #query
    insertFunc = ("UPDATE TheatreRoom SET Capacity = %s WHERE RoomNumber = %s")
    #data
    data = (request.form['capacity'], request.form['roomNumber'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/room/updateRoomForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/room/updateRoomForm.html')

#list all rooms and all attributes
@app.route('/displayRoom', methods=['POST','GET'])
def displayRoom():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
	cursor = cnx.cursor()
	insertFunc = ("SELECT * FROM TheatreRoom")
	cursor.execute(insertFunc)
	#return an array
	result = cursor.fetchall()
	cnx.close()
	return result

#===============================[SHOWING]=================================

#add showings
@app.route('/addshowing', methods=['POST'])
def addShowing():
    #open conneciton
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #query
    insertFunc = ("INSERT INTO Showing (idShowing, ShowingDateTime, Movie_idMovie,TheatreRoom_RoomNumber, TicketPrice) VALUES (%s, %s, %s, %s, %s)")
    #data
    data = (request.form['showingID'], request.form['showTime'], request.form['movieID'], request.form['roomNumber'], request.form['ticketPrice'])
    sucess = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/showing/addShowingForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/showing/addShowingForm.html')

#delete showings
@app.route('/deleteshowing', methods=['POST'])
def deleteShowing():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #data
    data = (request.form['showingID'])
    #query
    insertFunc = ("DELETE FROM Showing WHERE idShowing = '%s'; "%data)
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/showing/deleteShowingForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/showing/deleteShowingForm.html')

#modify showings
@app.route('/updateshowing', methods=['POST'])
def updateShowing():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #query
    insertFunc = ("UPDATE Showing SET ShowingDateTime = %s, Movie_idMovie = %s,TheatreRoom_RoomNumber = %s, TicketPrice = %s WHERE idShowing = %s")
    #data
    data = (request.form['showTime'], request.form['movieID'], request.form['roomNumber'], request.form['ticketPrice'], request.form['showingID'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/showing/updateShowingForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/showing/updateShowingForm.html')

#list all showings and all attributes sorted alphabetically by movie name
@app.route('/displayshowing', methods=['POST','GET'])
def displayShowing():
	#open connection
	cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
	cursor = cnx.cursor()
	#query
	insertFunc = ("SELECT * FROM Showing")
	success = cursor.execute(insertFunc)
	#return array
	result = cursor.fetchall()
	cnx.close()
	return result

#===============================[CUSTOMER]=================================

#add customers
@app.route('/addcustomer', methods=['POST'])
def addCustomer():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #query
    insertFunc = ("INSERT INTO Customer (idCustomer, FirstName, LastName, EmailAddress, Sex) VALUES (%s, %s, %s, %s, %s)")
    #data
    data = (request.form['customerID'], request.form['fname'], request.form['lname'], request.form['email'], request.form['sex'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/customer/addCustomerForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/customer/addCustomerForm.html')

#delete customer
@app.route('/deletecustomer', methods=['POST'])
def deleteCustomer():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #data
    data = (request.form['customerID'])
    #query
    insertFunc = ("DELETE FROM Customer WHERE idCustomer = '%s'; "%data)
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/customer/deleteCustomerForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/customer/deleteCustomerForm.html')

#modify customers
@app.route('/updatecustomer', methods=['POST'])
def updateCustomer():
    #open connection
    cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
    cursor = cnx.cursor()
    #query
    insertFunc = ("UPDATE Customer SET FirstName = %s, LastName = %s, EmailAddress = %s, Sex = %s WHERE idCustomer = %s")
    #data
    data = (request.form['fname'], request.form['lname'], request.form['email'], request.form['sex'], request.form['customerID'])
    success = cursor.execute(insertFunc, data)
    cnx.commit()
    cnx.close()

    if success<>0:
        flash("Successful Query")
        return render_template('/staffComponents/customer/updateCustomerForm.html')
    else:
        flash("Fail")
        return render_template('/staffComponents/customer/updateCustomerForm.html')

#list all customers and all attributes
@app.route('/displaycustomer', methods=['POST','GET'])
def displayCustomer():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
	cursor = cnx.cursor()
	insertFunc = ("SELECT * FROM Customer")
	cursor.execute(insertFunc)
	#return array
	result = cursor.fetchall()
	cnx.close()
	return result

#===============================[ATTEND]=================================

#list all attendances and all attributes sorted alphabetically by rating
@app.route('/displayattend', methods=['POST','GET'])
def displayAttend():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre', host = 'localhost')
	cursor = cnx.cursor()
	#joins customer, showing, movie, and returns the required columns
	insertFunc = ("SELECT Rating, Customer_idCustomer, Showing_idShowing, FirstName, LastName, ShowingDateTime, MovieName, idMovie FROM Attend JOIN Customer ON Attend.Customer_idCustomer = Customer.idCustomer JOIN Showing ON Attend.Showing_idShowing = Showing.idShowing JOIN Movie ON Showing.Movie_idMovie = Movie.idMovie ORDER BY Rating")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	cnx.close()
	return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
