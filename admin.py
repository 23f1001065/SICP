import os
from flask import render_template, request,redirect,url_for,session
from flask import current_app as app
from werkzeug.utils import secure_filename
from application.models import Admin,db
from application.tools import generate_random_id,uuid4,datetime



#ALL ABOUT ADMIN ------------------------------------------------------------------------------------------

@app.route("/admin/login", methods=["GET","POST"])
def admin_login():
    if request.method =="POST":
        adminID = request.form['userId']
        password = request.form['password']
        try:
            admin = Admin.query.filter_by(adminID = adminID).first()
        except Exception as e:
            return render_template('message.html',id='DBERROR'),503
        else:
            if admin and password == admin.password:
                session['admin_id'] = admin.adminID
                session['admin_name'] = admin.name
                admin.last_login = datetime.now().strftime('%Y-%m-%d %H:%M')
                db.session.commit()
                return redirect(url_for('admin_dashboard'))
            else:
                return 'Invalid Credentials. Admin with that ID or password not Found', 404

        
    return render_template("admin_login.html")
    
@app.route("/admin/dashboard", methods=["GET","POST"])
def admin_dashboard():
    if "admin_name" not in session.keys() and "admin_id" not in session.keys():
        return redirect(url_for('admin_login'))
    name = session.get("admin_name")
    admin_id = session.get("admin_id")
    if name and admin_id:
        return render_template("admin_dashboard.html",name = name)
    return redirect(url_for('admin_login'))
    
@app.route("/admin/logout", methods=["GET","POST"])
def admin_logout():
    if "admin_name" not in session.keys() and "admin_id" not in session.keys():
        return redirect(url_for('admin_login'))
    session['admin_id'] = None
    session['admin_name'] = None
    return redirect(url_for('admin_login'))