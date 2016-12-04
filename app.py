#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, json, jsonify, flash, session

from datetime import datetime
import mysql.connector
import base64
app = Flask(__name__)

@app.route("/")
def main():
    cnx = mysql.connector.connect(user='root', database='MovieTheatre')
    cursor = cnx.cursor()
    try:
    	cursor.execute("ALTER TABLE Movie ADD poster BLOB")
    except Exception, e: 
		print 'Poster column already exists'    	

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

    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))
    temp = selShowing.split()

    print selName

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
        cnx.commit()
        flash(selName + " successfully booked the " + temp[2] + " showing at " + temp[1] + " on " + temp[0])

    return render_template("customer.html", genre=returnGenre, date=returnDate, name=returnName, showing=returnShowing)

@app.route("/customer/selectShowing", methods=['POST','GET'])
def selectShowing():
    cnx = mysql.connector.connect()
    cursor = cnx.cursor()
    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))

    cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE (Customer.FirstName + " " + Customer.LastName)=%s ''', ('selName'))
    customerId=cursor.fetchone()


    for each in customerId:
        print each

    print 'wow'

    return render_template("customer.html")

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

#add movies
@app.route('/readfile', methods=['POST'])
#def read_file(filename):
#	with open(filename, 'rb') as f:
#		poster = base64.decodestring(f.read())
#	return poster

@app.route('/addmovie', methods=['POST'])
def addMovie():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
			"INSERT INTO Movie (MovieName, idMovie, movieYear)"
			"VALUES (%s, %s, %s)"
		)
	data = (request.form['movieName'], request.form['movieID'], request.form['movieYear'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()

	#if(request.form['poster'] is not None):
	#	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	#	cursor = cnx.cursor()
		#posterUpload = ("UPDATE Movie SET poster = %s WHERE idMovie = %s"
	#		)
		#posterimg = read_file(request.form['poster'])
		#images have to be uploaded to the templates/staffComponents/movie/posters folder
		#posterimg = read_file('/vagrant/Flask-App/templates/staffComponents/movie/posters/Capture.PNG')
		#print request.form['poster']
		#data = (posterimg, request.form['movieID'])
	#	cursor.execute(posterUpload, data)
	#	cnx.commit()
	#	cnx.close()
	return render_template('/staffComponents/movie/addMovieForm.html')
        
#delete movies
@app.route('/deletemovie', methods=['POST'])
def deleteMovie():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data = (request.form['movieID'])
	insertFunc = (
		"DELETE FROM Movie WHERE idMovie = '%s'; "%data
		)
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/movie/deleteMovieForm.html')

#modify movies
@app.route('/updatemovie', methods=['POST'])
def updateMovie():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
		"UPDATE Movie SET MovieName = %s WHERE idMovie = %s"
	)
	data = (request.form['movieName'], request.form['movieID'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
		"UPDATE Movie SET MovieYear = %s WHERE idMovie = %s"
	)
	data = (request.form['movieYear'], request.form['movieID'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()	

	return render_template('/staffComponents/movie/updateMovieForm.html')

#list all movies and all attributes sorted alphabetically by movie name
@app.route('/displayMovie', methods=['POST','GET'])
def displayMovie():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = ("SELECT * FROM Movie order by MovieName")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	#for movie in result:
	#	print movie[3]
		#movie[3] = movie[3].decode('base64')
	cnx.close()
	return result 



#===============================[GENRE]=================================

#add genre
@app.route('/addgenre', methods=['POST'])
def addGenre():	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
			"INSERT INTO Genre (Genre, Movie_idMovie)"
			"VALUES (%s, %s)"
		)
	data = (request.form['genre'], request.form['movieID'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/genre/addGenreForm.html')
        
#delete genre
@app.route('/deletegenre', methods=['POST'])
def deleteGenre():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
		"DELETE FROM Genre WHERE genre = %s and Movie_idMovie = %s"
		)
	data = (request.form['genre'], request.form['movieID'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/genre/deleteGenreForm.html')

#list all genres and movies
@app.route('/displayGenre', methods=['POST','GET'])
def displayGenre():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = ("SELECT Genre, idMovie, MovieName FROM Genre JOIN Movie ON Movie.idMovie = Genre.Movie_idMovie ORDER BY Genre")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	cnx.close()
	return result

#===============================[ROOM]=================================

#add rooms
@app.route('/addroom', methods=['POST'])
def addRoom():	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
			"INSERT INTO TheatreRoom (RoomNumber, Capacity)"
			"VALUES (%s, %s)"
		)
	data = (request.form['roomNumber'], request.form['capacity'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/room/addRoomForm.html')
        
#delete room
@app.route('/deleteroom', methods=['POST'])
def deleteRoom():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data = (request.form['roomNumber'])
	insertFunc = (
		"DELETE FROM TheatreRoom WHERE roomNumber = '%s'; "%data
		)
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/room/deleteRoomForm.html')

#modify rooms
@app.route('/updateroom', methods=['POST'])
def updateRoom():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
		"UPDATE TheatreRoom SET Capacity = %s WHERE RoomNumber = %s"
	)
	data = (request.form['capacity'], request.form['roomNumber'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/room/updateRoomForm.html')

#list all rooms and all attributes
@app.route('/displayRoom', methods=['POST','GET'])
def displayRoom():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = ("SELECT * FROM TheatreRoom")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	cnx.close()
	return result 

#===============================[SHOWING]=================================

#add showings
@app.route('/addshowing', methods=['POST'])
def addShowing():	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
			"INSERT INTO Showing (idShowing, ShowingDateTime, Movie_idMovie,TheatreRoom_RoomNumber, TicketPrice)"
			"VALUES (%s, %s, %s, %s, %s)"
		)
	data = (request.form['showingID'], request.form['showTime'], request.form['movieID'], request.form['roomNumber'], request.form['ticketPrice'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/showing/addShowingForm.html')
        
#delete showings
@app.route('/deleteshowing', methods=['POST'])
def deleteShowing():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data = (request.form['showingID'])
	insertFunc = (
		"DELETE FROM Showing WHERE idShowing = '%s'; "%data
		)
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/showing/deleteShowingForm.html')

#modify showings
@app.route('/updateshowing', methods=['POST'])
def updateShowing():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
		"UPDATE Showing SET ShowingDateTime = %s, Movie_idMovie = %s,TheatreRoom_RoomNumber = %s, TicketPrice = %s WHERE idShowing = %s"
	)
	data = (request.form['showTime'], request.form['movieID'], request.form['roomNumber'], request.form['ticketPrice'], request.form['showingID'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/showing/updateShowingForm.html')

#list all showings and all attributes sorted alphabetically by movie name
@app.route('/displayshowing', methods=['POST','GET'])
def displayShowing():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = ("SELECT * FROM Showing")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	cnx.close()
	return result 

#===============================[CUSTOMER]=================================

#add customers
@app.route('/addcustomer', methods=['POST'])
def addCustomer():	
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
			"INSERT INTO Customer (idCustomer, FirstName, LastName, EmailAddress, Sex)"
			"VALUES (%s, %s, %s, %s, %s)"
		)
	data = (request.form['customerID'], request.form['fname'], request.form['lname'], request.form['email'], request.form['sex'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/customer/addCustomerForm.html')
        
#delete customer
@app.route('/deletecustomer', methods=['POST'])
def deleteCustomer():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	data = (request.form['customerID'])
	insertFunc = (
		"DELETE FROM Customer WHERE idCustomer = '%s'; "%data
		)
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/customer/deleteCustomerForm.html')

#modify customers
@app.route('/updatecustomer', methods=['POST'])
def updateCustomer():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = (
		"UPDATE Customer SET FirstName = %s, LastName = %s, EmailAddress = %s, Sex = %s WHERE idCustomer = %s"
	)
	data = (request.form['fname'], request.form['lname'], request.form['email'], request.form['sex'], request.form['customerID'])
	cursor.execute(insertFunc, data)
	cnx.commit()
	cnx.close()
	return render_template('/staffComponents/customer/updateCustomerForm.html')

#list all customers and all attributes
@app.route('/displaycustomer', methods=['POST','GET'])
def displayCustomer():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = ("SELECT * FROM Customer")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	cnx.close()
	return result

#===============================[ATTEND]=================================

#list all attendances and all attributes sorted alphabetically by rating
@app.route('/displayattend', methods=['POST','GET'])
def displayAttend():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insertFunc = ("SELECT Rating, Customer_idCustomer, Showing_idShowing, FirstName, LastName, ShowingDateTime, MovieName, idMovie FROM Attend JOIN Customer ON Attend.Customer_idCustomer = Customer.idCustomer JOIN Showing ON Attend.Showing_idShowing = Showing.idShowing JOIN Movie ON Showing.Movie_idMovie = Movie.idMovie ORDER BY Rating")
	cursor.execute(insertFunc)
	result = cursor.fetchall()
	cnx.close()
	return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
