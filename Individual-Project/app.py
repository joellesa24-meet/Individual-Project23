from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={
  "apiKey": "AIzaSyBCBdnZkICwv65gxfsf9mB_CX37rOUNnf0",
  "authDomain": "mymovie-d1897.firebaseapp.com",
  "projectId": "mymovie-d1897",
  "storageBucket": "mymovie-d1897.appspot.com",
  "messagingSenderId": "174493172307",
  "appId": "1:174493172307:web:49ebab7383144b51473ca6",
  "measurementId": "G-79B3QWJQ8B",
  'databaseURL': 'https://mymovie-d1897-default-rtdb.firebaseio.com/'
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


#Code goes below here

my_films={
    "seven"         : "https://resizing.flixster.com/45blvnZjYobIB8zC7r5e2WEaTtI=/206x305/v2/https://flxt.tmsimg.com/assets/p17198_p_v12_an.jpg",
    "blackswan"     : "https://lumiere-a.akamaihd.net/v1/images/image_345538c9.jpeg?region=0%2C0%2C1400%2C2100",
    "gone girl"      : "https://geekymythology.files.wordpress.com/2015/01/gone-girl.jpg?w=640",
    "whiplash"      : "https://m.media-amazon.com/images/M/MV5BYWVlMjUwMzEtMWQyZS00OGFjLWI4ZTQtYWVjYTE0NGE5NzFmXkEyXkFqcGdeQXVyNTE4Mzg5MDY@._V1_FMjpg_UX1000_.jpg",
    "thedarkknight"    : "https://m.media-amazon.com/images/I/41HPNv+KcYL.jpg"
}





@app.route("/")
def welcome():
    return render_template('welcome.html')
@app.route("/signin",methods=['GET','POST'])
def signin():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']
        try:
            login_session['user']=auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('search'))
        except:
            error = "Authentication failed"
    return render_template('signin.html')

@app.route("/signup",methods=['GET','POST'])
def signup():
    error=""
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']


        
        try:
            login_session['user']=auth.create_user_with_email_and_password(email,password)
            user={'username':request.form['username']}
            UID=login_session['user']['localId']
            db.child('Users').child(UID).set(user)
            return redirect(url_for('search'))
        except:
            #error = "Authentication failed"
            return render_template('signup.html')
    return render_template('signup.html')

@app.route("/search")
def search():
    return render_template('search.html', films=my_films)

@app.route('/movie/<string:movie_title>', methods=['POST','GET'])
def movie(movie_title):
    # if request.method == 'POST':
    #     try:
    #         films={'title': request form['title'],'img':request.form['img']}
    if request.method=='GET':

        movie_cover = my_films[movie_title]
        comment = db.child('Reviews').child(movie_title).get().val()
        return render_template('movie.html', title = movie_title, cover = movie_cover , comments=comment)
    else:
        movie_cover = my_films[movie_title]
        UID=login_session['user']['localId']
        user=db.child("Users").child(UID).get().val()
        username=user['username']
        review={"rating": request.form['rating'],"user":username,"comment":request.form['comment']}
        db.child("Reviews").child(movie_title).child().set(review)
        comment = db.child('Reviews').child(movie_title).get().val()
        return render_template('movie.html', title = movie_title, cover = movie_cover, comments=comment)

@app.route('/movie',methods=['POST','GET'])
def secondmovie():
    error=""
    if request.method=='POST':
        try:
            UID=login_session['user']['localId']
            user=db.child("users").child(UID).get().val()
            username=user['username']
            review={"movie":request.form['movietitle'],"rating": request.form['rating'],"user":username,"comments":request.form['comment']}
            db.child("Reviews").push(review)
        except:
            #error = "Authentication failed"
            return render_template('movie.html')







#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)