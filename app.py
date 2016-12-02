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
    print ("yay")
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





        if success == 0:
            flash ("Sorry, please watch a movie to see your history.")
            return render_template('history.html', name=returnName, data=data)
        else:
            cxn.commit()
            flash("You have successfully rated your showing.")
            return render_template('history.html', name=returnName, data=data)

#        except Exception as e:
#            print (e)
#            return render_template('history.html')

    else:
        return render_template('history.html', name=returnName)







@app.route('/staff')
def staffLogin():
    return render_template('staff.html')





if __name__ == "__main__":
    app.run()
