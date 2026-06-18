import os
from flask import render_template, request,redirect,url_for,session
from flask import current_app as app
from werkzeug.utils import secure_filename
from application.models import Influencer,Campaign,Adrequest,Sponsor,db
from application.sponsor import campaigns
from application.tools import generate_random_id,uuid4,datetime



@app.route("/influencer/login", methods=["GET","POST"])
def influencer_login():
    if request.method =="POST":
        email = request.form['influencerEmail']
        password = request.form['password']
        try:
            influencer = Influencer.query.filter_by(email = email).first()
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
            
        else:
            if influencer and password == influencer.password:
                influencer.last_login = datetime.now().strftime('%Y-%m-%d %H:%M')
                influencer.status = 1
                db.session.commit()
                session['influencer_id'] = influencer.influencer_id
                session['influencer_name'] = influencer.name
                session['influencer_image'] = influencer.profile_image
                return redirect(url_for('influencer_dashboard'))
            else:
                return render_template('message.html',id='ININVALID'),404
    return render_template("influencer_login.html")
        



@app.route("/influencer/register", methods=["GET","POST"])
def influencer_register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        mobNo = request.form['mobno']
        category = request.form['category']
        password = request.form['password']
        niche = request.form['niche']
        reach = request.form['reach']
        try:
            influencer = Influencer.query.filter_by(email=email).first()
            if influencer:
                return render_template('message.html',id='INEX')
            else:
                newInfluencer = Influencer()
                newInfluencer.influencer_id = generate_random_id('INFE')
                newInfluencer.password = password
                newInfluencer.email = email
                newInfluencer.mobileno = mobNo 
                newInfluencer.name = name
                newInfluencer.niche = niche
                newInfluencer.reach = reach
                newInfluencer.category = category
                newInfluencer.created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                newInfluencer.last_login = datetime.now().strftime('%Y-%m-%d %H:%M')
                newInfluencer.status = 0
                newInfluencer.profile_image = "default.png"
                newInfluencer.flaged_status = 'noflaged'
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            db.session.add(newInfluencer)
            db.session.commit()
            return render_template('message.html', 
                                id='INRSUCC',
                                influencer_email=newInfluencer.email,
                                password=password)
            
        
    return render_template("influencer_register.html")

@app.route("/influencer_dashboard", methods=["GET","POST"])
def influencer_dashboard():
    if "influencer_name" not in session.keys() and "influencer_id" not  in session.keys():
        return redirect(url_for('influencer_login'))
    name = session["influencer_name"]
    influencer_id = session['influencer_id']
    image = session['influencer_image']
    try:
        privateADrequests = Adrequest.query.filter_by(influencer_id=influencer_id,type='private').all()
        publicADrequests = Adrequest.query.filter_by(influencer_id=influencer_id,type='public').all()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        return render_template("influencer_dashboard.html",
                               id='adrequest',
                               name=name,
                               image=image,
                               privateAD = privateADrequests,
                               publicAD = publicADrequests)
    





@app.route("/influencer_dashboard/profile_pic/upload", methods=["GET","POST"])
def influencer_update_profile():   
    if "influencer_name" not in session.keys() and "influencer_id" not  in session.keys():
            return redirect(url_for('influencer_login'))
    influencer_id = session['influencer_id']
    if request.method == 'POST':
        image = request.files['profile_pic']
        try:
            influencer = Influencer.query.filter_by(influencer_id=influencer_id).first()
            if influencer and image and image.filename:
                filename = str(uuid4()) + "_" + secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                image.save(filepath)

                if influencer.profile_image != 'default.png':
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'],influencer.profile_image)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                influencer.profile_image = filename
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            db.session.commit()
            session['influencer_image'] = filename
    return redirect(url_for('influencer_profile'))
        
        
            


    

@app.route("/influencer_dashboard/profile", methods=["GET","POST"])
def influencer_profile():
    if "influencer_name" not in session.keys() and "influencer_id" not  in session.keys():
        return redirect(url_for('influencer_login'))
    name = session["influencer_name"]
    influencer_id = session['influencer_id']
    image = session['influencer_image']
    if request.method == 'POST':
        try:
            influencer = Influencer.query.filter_by(influencer_id=influencer_id).first()
            if influencer:
                influencer.name = request.form['name']
                influencer.email = request.form['email']
                influencer.mobileno = request.form['mobno']
                influencer.password = request.form['password']
                influencer.category = request.form['category']
                influencer.niche = request.form['niche']
                influencer.reach = request.form['reach']
                influencer.youtube_link = request.form['youtube']
                influencer.facebook_link = request.form['facebook']
                influencer.tweeter_link = request.form['tweeter']
                influencer.insta_link = request.form['insta']
                influencer.linkedin_link = request.form['linkedin']
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            if influencer:
                db.session.commit()
                return render_template('message.html', 
                                        id='IUPSUCC',
                                        email=influencer.email,
                                        password=influencer.password)
    try:
        influencer = Influencer.query.filter_by(influencer_id=influencer_id).first()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        return render_template("influencer_dashboard.html",id = 'profile',name=name,image=image,influencer=influencer)
            
        


@app.route("/influencer_dashboard/search_campaign", methods=["GET","POST"])
def influencer_search():
    if "influencer_name" not in session.keys() and "influencer_id" not  in session.keys():
        return redirect(url_for('influencer_login'))
    name = session["influencer_name"]
    influencer_id = session['influencer_id']
    image = session['influencer_image']
    industry = request.args.get('industry')
    budget = request.args.get('budget')
    if industry == None:
        return render_template('influencer_dashboard.html',id="search",name=name,image=image,empty_q=True)
    try:
        campaigns = Campaign.query.filter(
            Campaign.industry.ilike(f'%{industry}%'),
            Campaign.visibility == 'public',
            Campaign.budget >= budget
        ).all()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        return render_template('influencer_dashboard.html', id='search', name=name,image=image,campaigns=campaigns,empty_q=False)




@app.route("/influencer_dashboard/view_campaign/<string:camp_id>", methods=["GET","POST"])
def view_campaign(camp_id):
    if "influencer_name" not in session.keys() and "influencer_id" not  in session.keys():
        return redirect(url_for('influencer_login'))
    name = session["influencer_name"]
    influencer_id = session['influencer_id']
    image = session['influencer_image']
    try:
        campaign = Campaign.query.filter_by(campaign_id=camp_id).first_or_404()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    
    return render_template('influencer_dashboard.html',id='view',name=name,image=image,campaign=campaign)


@app.route('/influencer_dashboard/adrequest/<string:flag>/<string:ad_id>',methods=["GET","POST"])
def take_action(flag,ad_id):
    if "influencer_name" not in session.keys() and "influencer_id" not  in session.keys():
        return redirect(url_for('influencer_login'))
    name = session["influencer_name"]
    influencer_id = session['influencer_id']
    image = session['influencer_image']
    try:
        adrequest = Adrequest.query.filter_by(adId = ad_id).first_or_404()
        sponsor = Sponsor.query.filter_by(sponsor_id = adrequest.createdby).first_or_404()
        camp = Campaign.query.filter_by(campaign_id = adrequest.campaign_id).first_or_404()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503 
    if flag == 'rv':
        return render_template('action_by_influencer_on_ad.html',
                               name=name,
                               image=image,
                               id='rview',
                               adrequest=adrequest,
                               sponsor=sponsor,
                               camp = camp)
    elif flag == 'ra':
        if adrequest and request.method=='POST':
            choice = request.form['choice']
            if choice == 'yes':
                try:
                    adrequest.status = 'accepted'
                    
                except Exception as e:
                    return render_template('message.html', id = 'DBERROR', error = e),503
                else:
                    db.session.commit()
                    return redirect(url_for('influencer_dashboard'))
            return render_template('action_by_influencer_on_ad.html',
                                   id='rview',
                                   name=name,
                                   image=image,
                                   adrequest=adrequest,
                                   sponsor=sponsor,
                                   camp = camp)
        return render_template('action_by_influencer_on_ad.html',
                               id='raccept',
                               name=name,
                               image=image,
                               adrequest=adrequest)
    elif flag == 'rr':
        if adrequest and request.method=='POST':
            choice = request.form['choice']
            if choice == 'yes':
                try:
                    adrequest.status = 'rejected'
                except Exception as e:
                    return render_template('message.html', id = 'DBERROR', error = e),503
                else:
                    db.session.commit()
                    return redirect(url_for('influencer_dashboard'))
            return render_template('action_by_influencer_on_ad.html',
                                   id='rview',
                                   name=name,
                                   image=image,
                                   adrequest=adrequest,
                                   sponsor=sponsor,
                                   camp = camp)
        return render_template('action_by_influencer_on_ad.html',
                               id='rreject',
                               name=name,
                               image=image,
                               adrequest=adrequest)
    elif flag == 'ng':
        if adrequest and request.method=='POST':
            amount = request.form['negotiate']
            message = request.form['message']
            try:
                adrequest.nego_amount = amount
                adrequest.nego_message = message
                adrequest.nego_status = 'pending'
            except Exception as e:
                return render_template('message.html', id = 'DBERROR', error = e),503
            else:
                db.session.commit()
                return render_template('action_by_influencer_on_ad.html',
                                   id='rview',
                                   name=name,
                                   image=image,
                                   adrequest=adrequest,
                                   sponsor=sponsor,
                                   camp = camp)
        return render_template('action_by_influencer_on_ad.html',
                               id='rnegotiate',
                               name=name,
                               image=image,
                               adrequest=adrequest)    
            

@app.route('/influencer_dashboard/adrequest/<string:campaign_id>',methods=["GET","POST"])
def send_request(campaign_id):
    if "influencer_name" not in session.keys() and "influencer_id" not  in session.keys():
        return redirect(url_for('influencer_login'))
    name = session["influencer_name"]
    influencer_id = session['influencer_id']
    image = session['influencer_image']
    try:
        campaign = Campaign.query.filter_by(campaign_id=campaign_id).first_or_404()
        adrequest = Adrequest.query.filter_by(campaign_id = campaign_id, influencer_id = influencer_id).first()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    if request.method == "POST" and not adrequest:
        try:
            newAdrequest = Adrequest()
            newAdrequest.adId = generate_random_id('AD')
            newAdrequest.campaign_id = campaign.campaign_id
            newAdrequest.influencer_id = influencer_id
            newAdrequest.messages = request.form['message']
            newAdrequest.requirements = request.form['requirements']
            newAdrequest.payment_amount = request.form['amount']
            newAdrequest.status = 'pending'
            newAdrequest.type = 'public'
            newAdrequest.createdby = influencer_id
            newAdrequest.send_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            db.session.add(newAdrequest)
            
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            db.session.commit()
            return render_template('influencer_dashboard.html',id='success',name=name,image=image,campaign=campaign)
    return render_template('influencer_dashboard.html',id='send',name=name,image=image,campaign=campaign,influencer_id=influencer_id)

@app.route("/influencer_dashboard/stat", methods=["GET","POST"])
def influencer_stat():
    return 'statistics'
    
@app.route("/influencer/logout", methods=["GET","POST"])
def influencer_logout():
    if 'influencer_id' not in session.keys() and "influencer_name" not in session.keys():
         return redirect(url_for('influencer_login'))
    
    influencer_id = session['influencer_id']
    
    session.pop('influencer_id')
    session.pop('influencer_name')
    try:
        influencer = Influencer.query.filter_by(influencer_id = influencer_id).first()
    except Exception as e:
        return render_template('message.html',id='DBERROR'),503
    else:
        influencer.status = 0 #type:ignore
        db.session.commit()
    return redirect(url_for('influencer_login'))
    













