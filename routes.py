from application import app, db
from flask import render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integr, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime, date
import re

class Userstore(db.Model):
    __tablename__ = 'userstore'
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20))
    password = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.now)

class Patients(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer)
    pname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)
    ldate = db.Column(db.DateTime, default=datetime.now)
    tbed = db.column(db.String(10))
    address = db.Column(db.String(20))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    status = db.Column(db.String(20))

    # children = relationship("Medicines")
    # children1 = relationship("Diagnostics")

class Medicines(db.Model):
    __tablename__ = 'medicines'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    mname = Column(db.String(20))
    mid = db.Column(db.Integer)
    rate = db.Column(db.Integer)
    qissued = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)

    children = relationship("MedicineMaster")

class MedicineMaster(db.Model):
    __tablename__ = 'medicinemaster'
    mid = Column(Integer, ForeignKey('medicine.mid'), primary_key=True)
    mname = Column(db.String(20))
    qavailable = Column(db.Integer)
    rate = Column(db.Integer)

class Diagnostics(db.Model):
    __tablename__ = 'diagnostics'
    id = db.Column(db.Integer, primary_key=True)
    pid = db.Column(db.Integer)
    tname = Column(db.String(20))
    tid = db.Column(db.Integer)
    tcharge = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now)

    children = relationship("DiagnosticsMaster")

class DiagnosticsMaster(db.Model):
    __tablename__ = 'diagnosticsmaster'
    tid = Column(Integer, ForeignKey('diagnostics.tid'), primary_key=True)
    tname = Column(db.String(20))
    tcharge = Column(db.Integer)

db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect( url_for('home') )
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        usr = Userstore.query.filter_by(uname = username).first()
        if usr == None:
            flash('User not found', category='error')
            return redirect( url_for('login') )
        
        elif username == usr.uname and password == usr.password:
            session['username'] = username
            return redirect( url_for('home') )
        
        else:
            flash('Login Failed', category="error")

    return render_template("login.html")


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['pass']
        cnfrm_password = request.form['cpass']

        query = Userstore.query.filter_by(uname = uname).first()

        if query !=None:
            if uname == str(query.uname):
                flash('User already exist')
                return redirect( url_for('registration') )
            
        if password !=cnfrm_password:
            flash('Passwords do not match')
            return redirect( url_for('registration') )
        
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&][A-Za-z\d@$!#%*?&]{6.20}$"
        pattern = re.compile(regex)

        match = re.search(pattern, password)
        
        if match:
            user = Userstore(uname = uname, password = password)
            db.session.add(user)
            db.session.commit()
            flash('Successfully registered', category='info')
            return redirect( url_for('login') )
        else:
            flash('The password must include an uppercase letter, a special character, and a numeric character')
            return redirect( url_for('registration') )
    return render_template('staff_registration.html')


@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html')
    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') ) 

@app.route('/create_patient', methods=['GET', 'POST'])
def create_patient():
    if 'username' in session:                
        if request.method == 'POST':           
            ssn_id = request.form['ssn_id']
            pname = request.form['pname']      
            age = request.form['age']
            tbed = request.form['tbed']
            address = request.form['address']
            state = request.form['state']
            city = request.form['city']
            status = request.form['status']

            pat = Patients.query.filter_by( ssn_id = ssn_id ).first()

            if pat == None:
                patient = Patients(ssn_id=ssn_id, pname=pname, age=age, tbed=tbed, address=address, state=state, city=city,  status = status)
                db.session.add(patient)
                db.session.commit()
                flash('Record created successfully')
                return redirect( url_for('create_patient') )
            
            else:
                flash('SSN ID already exists')
                return redirect( url_for('create_patient') )
    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )

    return render_template('create_patient.html')


@app.route('/update_patient')
def update_patient():
    if 'username' in session:
        usern = session['username']
        print(usern)
        updatep = Patients.query.all()


        if not updatep:
            flash('Record not found')
            return redirect( url_for('create_patient') )
        else:
            print("inside else")
            return render_template('update_patient.html', updatep = updatep)

    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )
    return render_template('update_patient.html')

@app.route('/deletepat')
def deletepat():
    if 'username' in session:
        usern = session['username']
        print(usern)
        updatep = Patients.query.all()


        if not updatep:
            flash('Record not found')
            return redirect( url_for('create_patient') )
        else:
            print("inside else")
            return render_template('deletepat.html', updatep = updatep)

    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )
    return render_template('deletepat.html')


@app.route('/editpatientdetail/<id>', methods=['GET', 'POST'])
def editpatientdetail(id):
    print("id is : ", id)
    if 'username' in session:
        print("inside sesssss")
        print(datetime.now())
        editpat = Patients.query.filter_by( id = id )


        if request.method == 'POST':  
            print("inside editpat post mtd")
            pname = request.form['npname']      
            age = request.form['nage']
            tbed = request.form['tbed']
            address = request.form['naddress']
            status = request.form['status']
            state = request.form['nstate']
            city = request.form['ncity']
            ldate = datetime.today()
            row_update = Patients.query.filter_by( id = id ).update(dict(pname=pname, age=age, tbed=tbed, address=address, state=state, city=city, status = status, ldate=ldate))
            db.session.commit()
            print("Roww update", row_update)

            if row_update == None:
                flash('Something went wrong')
                return redirect( url_for('update_patient') )
            else:
                flash('Patient updated successfully')
                return redirect( url_for('update_patient') )

        return render_template('editpatientdetail.html', editpat = editpat)
    