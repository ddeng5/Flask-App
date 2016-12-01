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
        cxn.commit()
        flash(selName + " successfully booked the " + temp[2] + " showing at " + temp[1] + " on " + temp[0])


    return render_template("customer.html", genre=returnGenre, date=returnDate, name=returnName, showing=returnShowing)







@app.route("/customer/selectShowing", methods=['POST','GET'])
def selectShowing():

    cxn = mysql.connect()
    cursor = cxn.cursor()
    selName = str(request.form.get('selectedName'))
    selShowing = str(request.form.get('selectedShowing'))

    cursor.execute('''SELECT Customer.idCustomer FROM Customer WHERE (Customer.FirstName + " " + Customer.LastName)=%s ''', ('selName'))
    customerId=cursor.fetchone()


    for each in customerId:
        print each

    print 'wow'

    return render_template("customer.html")



@app.route('/staff')
def staffLogin():
    return render_template('staff.html')





if __name__ == "__main__":
    app.run()
