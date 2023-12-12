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
    
@app.route('/deletepatientdetail/<id>')
def deletepatientdetail(id):
    if 'username' in session:
        delpat = Patients.query.filter_by(id = id).delete()
        db.session.commit()

        if delpat == None:
            flash('Something went wrong')
            return redirect( url_for('update_patient') )
        else:
            flash('Record deleted successfully')
            return redirect( url_for('update_patient') )

    return render_template('update_patient.html')


@app.route('/patientscreen')
def patientscreen():
    if 'username' in session:
        pts = Patients.query.filter_by( status = 'Active' )
        print("ptsss",pts)
        if not pts:
            flash('All patients discharged')
            return redirect( url_for('update_patient') )
        else:
            print("inside else")
            return render_template('patientscreen.html', pts = pts)

    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )

@app.route('/search_patient', methods=['GET', 'POST'])
def search_patient():
    if 'username' in session:
        if request.method == 'POST':
            id = request.form['id']
            
            if id != "":
                patient = Patients.query.filter_by( id = id).first()
                if patient == None:
                    flash('No patients with this ID exists')
                    return redirect( url_for('search_patient') )
                else:
                    flash('Record found')
                    return render_template('search_patient.html', patient = patient)
            
            if id == "":
                flash('Enter ID to search')
                return redirect( url_for('search_patient') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('search_patient.html')

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    #today = datetime.today().strftime('%Y-%m-%d')
    today = datetime.now()
    if 'username' in session:
        if request.method == 'POST':
            id = request.form['id']
            delta = 0
            if id != "":
                patient = Patients.query.filter_by( id = id).first()
                if patient == None:
                    flash('No Patients with this ID exists')
                    return redirect( url_for('billing') )
                elif patient.status != 'Active':
                    flash('Record not found')

                else:
                    flash('Record found')
                    x = patient.date
                    y = x.strftime("%d-%m-%Y, %H:%M:%S")
                    # z = today.strftime("%d-%m-%Y")
                    # print("Patient ",y)
                    # print("today", z)
                    delta = ( today - x ).days
                    print(delta)
                    dy = 0    
                    if delta == 0:
                        dy = 1
                    else:
                        dy = delta
                    roomtype = patient.tbed
                    bill = 0
                    print(roomtype)
                    if roomtype == 'SingleRoom':
                        bill = 8000 * dy
                    elif roomtype == 'SemiSharing':
                        bill = 4000*dy
                    else:
                        bill = 2000*dy

                    med = Medicines.query.filter_by(pid = id).all()
                    if med == None:
                        flash('No medication has been dispensed to the patient thus far')
                    else:
                        mtot = 0
                        for j in med:
                            mtot += (j.qissued * j.rate)

                    dia = Diagnostics.query.filter_by(pid = id).all()
                    if dia == None:
                        flash('The patient has not been prescribed any tests so far')
                    else:
                        tot = 0
                        for i in dia:
                            tot += i.tcharge
                        return render_template('billing.html', patient = patient, dy=dy, y=y, bill = bill, med = med, dia = dia, mtot = mtot, tot = tot)

            
            if id == "":
                flash('Enter patient ID')
                return redirect( url_for('billing') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('billing.html')

@app.route('/addMedicine', methods=['GET', 'POST'] )
def addMedicine():
    if 'username' in session:                
        if request.method == 'POST':           
            mid = request.form['mid']
            mname = request.form['mname']      
            qavailable = request.form['qavailable']
            rate = request.form['rate']

            pat = MedicineMaster.query.filter_by( mid = mid ).first()

            if pat == None:
                med = MedicineMaster(mid=mid, mname=mname, qavailable=qavailable, rate=rate)
                db.session.add(med)
                db.session.commit()
                flash('Record successfully added')
                return redirect( url_for('addMedicine') )
            
            else:
                flash('Record already exists')
                return redirect( url_for('addMedicine') )
    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )

    return render_template('addMedicine.html')

@app.route('/PharmacistPatientDetails', methods=['GET', 'POST'])
def PharmacistPatientDetails():
    if 'username' in session:
        if request.method == 'POST':
            id = request.form['id']
            
            if id != "":
                patient = Patients.query.filter_by( id = id).first()
                if patient == None:
                    flash('Record not found')
                    return redirect( url_for('PharmacistPatientDetails') )
                else:
                    flash('Record found')

                med = Medicines.query.filter_by(pid = id).all()
                print("Meddd", med)
                if med == None:
                    # nll = med.mid
                    flash('No medication has been dispensed to the patient thus far')
                    return render_template('PharmacistPatientDetails.html', patient = patient)
                else:
                    return render_template('PharmacistPatientDetails.html',patient = patient, med = med)
            
            if id == "":
                flash('Enter ID to search')
                return redirect( url_for('PharmacistPatientDetails') )
    
    else:
        return redirect( url_for('login') )
    
    return render_template('PharmacistPatientDetails.html')

@app.route('/medicinestatus')
def medicinestatus():
    if 'username' in session:
        usern = session['username']
        print(usern)
        updatep = MedicineMaster.query.all()
        print(updatep)
        if not updatep:
            flash('Record not found')
            return redirect( url_for('addMedicine') )
        else:
            print("inside else")
            return render_template('medicinestatus.html', updatep = updatep)

    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )
    return render_template('medicinestatus.html')

@app.route('/updatemed')
def updatemed():
    if 'username' in session:
        usern = session['username']
        print(usern)
        updatep = MedicineMaster.query.all()
        print(updatep)
        if not updatep:
            flash('Record not found!')
            return redirect( url_for('addMedicine') )
        else:
            print("inside else")
            return render_template('updatemed.html', updatep = updatep)

    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )
    return render_template('updatemed.html')

@app.route('/deletemed')
def deletemed():
    if 'username' in session:
        usern = session['username']
        print(usern)
        updatep = MedicineMaster.query.all()
        print(updatep)
        if not updatep:
            flash('Record not found!')
            return redirect( url_for('addMedicine') )
        else:
            print("inside else")
            return render_template('deletemed.html', updatep = updatep)

    else:
        flash('Logged out! Please login again to continue')
        return redirect( url_for('login') )
    return render_template('deletemed.html')

@app.route('/editmedicinedetail/<mid>', methods=['GET', 'POST'] )
def editmedicinedetail(mid):
    print("id is : ", mid)
    if 'username' in session:
        print("inside sesssss")
        print(datetime.now())
        editpat = MedicineMaster.query.filter_by( mid = mid )
        

        if request.method == 'POST':  
            print("inside editpat post mtd")
            mname = request.form['mname']      
            qavailable = request.form['qavailable']
            rate = request.form['rate']
            row_update = MedicineMaster.query.filter_by( mid = mid ).update(dict(mname=mname, qavailable=qavailable, rate=rate))
            db.session.commit()
            print("Roww update", row_update)

            if row_update == None:
                flash('Something went wrong')
                return redirect( url_for('medicinestatus') )
            else:
                flash('Record updated successfully')
                return redirect( url_for('medicinestatus') )

        return render_template('editmedicinedetail.html', editpat = editpat)
    
@app.route('/deletemedicinedetail/<mid>')
def deletemedicinedetail(mid):
    if 'username' in session:
        delpat = MedicineMaster.query.filter_by(mid = mid).delete()
        db.session.commit()

        if delpat == None:
            flash('Something went wrong')
            return redirect( url_for('medicinestatus') )
        else:
            flash('Record deleted successfully')
            return redirect( url_for('medicinestatus') )

    return render_template('medicinestatus.html')