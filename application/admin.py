import os
from flask import render_template, request,redirect,url_for,session,abort,current_app
from application.bluprint import admin_app
from werkzeug.utils import secure_filename
from application.models import Admin,Influencer,Adrequest,Campaign,Sponsor,db
from application.tools import generate_random_id,uuid4,datetime



#ALL ABOUT ADMIN ------------------------------------------------------------------------------------------

@admin_app.route("/admin_login", methods=["GET","POST"])
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
                return redirect(url_for('admin_app.admin_dashboard'))
            else:
                return 'Invalid Credentials. Admin with that ID or password not Found', 404
    return render_template("admin_login.html")

        
    
@admin_app.route("/admin_dashboard", methods=["GET","POST"])
def admin_dashboard():
    if "admin_name" not in session.keys() and "admin_id" not in session.keys():
        return redirect(url_for('admin_app.admin_login'))
    name = session.get("admin_name")
    admin_id = session.get("admin_id")
    try:
        sponsors = Sponsor.query.filter_by().all()
        influencers = Influencer.query.filter_by().all()
        campaigns = Campaign.query.filter_by().all()
        adrequests = Adrequest.query.filter_by().all()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    return render_template("admin_dashboard.html",
                           name = name,
                           sponsors=sponsors,
                           influencers=influencers,
                           campaigns = campaigns,
                           adrequests = adrequests)

@admin_app.route("/admin_dashboard/view_users/<string:flag>/<string:id>",methods=['GET','POST'])
def view_users(flag,id):
    if "admin_name" not in session.keys() and "admin_id" not in session.keys():
        return redirect(url_for('admin_app.admin_login'))
    name = session.get("admin_name")
    admin_id = session.get("admin_id") 
    if flag == 'vs':
        sponsor = Sponsor.query.filter_by(sponsor_id = id).first_or_404()
        if request.method == "POST":
            try:
                sponsor.flaged_status = request.form['choice']
            except Exception as e:
                return render_template('message.html', id = 'DBERROR', error = e),503
            else:
                db.session.commit()
        return render_template('flag_user.html',
                               name=name,
                               id = 'sponsor',
                               sponsor=sponsor)
    elif flag == 'vi':
        influencer = Influencer.query.filter_by(influencer_id = id).first_or_404()
        if request.method == "POST":
            try:
                influencer.flaged_status = request.form['choice']
            except Exception as e:
                return render_template('message.html', id = 'DBERROR', error = e),503
            else:
                db.session.commit()
        return render_template('flag_user.html',
                               name=name,
                               id = 'influencer',
                               influencer=influencer)
    elif flag == 'vc':
        campaign = Campaign.query.filter_by(campaign_id = id).first_or_404()
        if request.method == "POST":
            try:
                campaign.flaged_status = request.form['choice']
            except Exception as e:
                return render_template('message.html', id = 'DBERROR', error = e),503
            else:
                db.session.commit()
        return render_template('flag_user.html',
                               name=name,
                               id = 'campaign',
                               campaign=campaign)
    else:
        abort(404)


@admin_app.route("/admin_logout", methods=["GET","POST"])
def admin_logout():
    if "admin_name" not in session.keys() and "admin_id" not in session.keys():
        return redirect(url_for('admin_app.admin_login'))
    session.pop('admin_id')
    session.pop('admin_name')
    return redirect(url_for('admin_app.admin_login'))