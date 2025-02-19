from urllib import request
from flask import Flask, render_template, request, redirect,session,url_for
from urllib.parse import quote_plus
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
password = quote_plus("sahilparul")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{password}@localhost/userinfo'
# app.config['SQLALCHEMY__DATABASE__URI'] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)

class Entry(db.Model):
    srno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.now)
    

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET','POST'])
def signup():
    message=None
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        
        if not email or not password:
            message="Please enter both email and password."
            
        elif password!=repassword:
            message="Password do not match!"
          
        else:
            existing_user=UserInfo.query.filter_by(email=email).first()
            if existing_user:
                return redirect('login')
            else:
                 credentials = UserInfo(email=email, password=password)
                 db.session.add(credentials)
                 db.session.commit()
                 return redirect('login')  
       
    
    return render_template('signup.html',alert_message=message)

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if request.method=='POST':
        title=request.form.get('title')
        desc=request.form.get('desc')
        entry=Entry(title=title,desc=desc)
        db.session.add(entry)
        db.session.commit()
    entries=Entry.query.all()
    return render_template('dashboard.html',allEntries=entries)



@app.route("/login",methods=['GET','POST'])
def login():
    message=None
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        
        if not email or not password:
            message="Please enter both email and password."
            
        else:
            user=UserInfo.query.filter_by(email=email,password=password).first()
            if not user:
                message="User not found. please sign up."
            elif user.password!=password:
                message="Incorrect password."
            else:
                return redirect('dashboard')
    return render_template('login.html',alert_message=message)


@app.route('/update/<int:srno>',methods=['GET','POST'])
def update(srno):
    if request.method=='POST':
        title= request.form['title']
        desc= request.form['desc']
        entry=Entry.query.filter_by(srno=srno).first()
        entry.title=title
        entry.desc=desc
        db.session.commit()
        return redirect(url_for('dashboard'))
    
    entry=Entry.query.filter_by(srno=srno).first()
    return render_template('update.html',entry=entry)

@app.route('/delete/<int:srno>')
def delete(srno):
    entry=Entry.query.filter_by(srno=srno).first()
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    return render_template('about.html')
        
        

if __name__ == "__main__":
    app.run(debug=True)
