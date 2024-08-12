import os
from flask import render_template, request,redirect,url_for,session
from flask import current_app as app
#from numpy import delete
from werkzeug.utils import secure_filename
from application import influencer
from application.models import Sponsor,Campaign,Influencer,Adrequest,db
from application.tools import generate_random_id,uuid4,datetime

#ALL About SPONSORS----------------------------------------------------------------------------------
@app.route("/sponsor/register", methods=["GET","POST"])
def sponsor_register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        mobNo = request.form['mobno']
        industry = request.form['industry']
        password = request.form['password']
        try:
            sponsor = Sponsor.query.filter_by(email = email).first()
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            if sponsor:
                return render_template('message.html',id='SPEX')
            else:
                newSponsor = Sponsor()
                newSponsor.sponsor_id = generate_random_id('SPON')
                newSponsor.password = password
                newSponsor.email = email
                newSponsor.mobileno = mobNo 
                newSponsor.name = name
                newSponsor.budget = 0.0
                newSponsor.status = 0
                newSponsor.industry = industry
                newSponsor.profile_image = 'default.png'
                newSponsor.created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                newSponsor.last_login = datetime.now().strftime('%Y-%m-%d %H:%M')
                newSponsor.flaged_status = 'noflaged'
                db.session.add(newSponsor)
                db.session.commit()
                return render_template('message.html', id='SPRSUCC',email=newSponsor.email,password=password)
    return render_template("sponsor_register.html")

        


@app.route("/sponsor/login", methods=["GET","POST"])
def sponsor_login():
    if request.method =="POST":
        email = request.form['sponsorEmail']
        password = request.form['password']
        try:
            sponsor = Sponsor.query.filter_by(email = email).first()
        except Exception as e:
            return render_template('message.html',id='DBERROR'),503
        else:
            if sponsor and password == sponsor.password:
                sponsor.last_login = datetime.now().strftime('%Y-%m-%d %H:%M')
                sponsor.status = 1
                db.session.commit()
                session['sponsor_id'] = sponsor.sponsor_id
                session['sponsor_name'] = sponsor.name
                session['image'] = sponsor.profile_image
                return redirect(url_for('sponsor_dashboard'))
            else:
                return render_template('message.html',id='SPINVALID'),404
    return render_template("sponsor_login.html")





@app.route("/sponsor_dashboard/profile_pic/upload", methods=["GET","POST"])
def sponsor_update_profile():  
    if request.method == 'POST':
        if "sponsor_name" not in session.keys() and "sponsor_id" not  in session.keys():
            return redirect(url_for('sponsor_login'))
        sponsor_id = session['sponsor_id']
        image = request.files['profile_pic']
        try:
            sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first_or_404()
            if sponsor and image and image.filename:
                filename = str(uuid4()) + "_" + secure_filename(image.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
                image.save(filepath)

                if sponsor.profile_image != 'default.png':
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'],sponsor.profile_image)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                sponsor.profile_image = filename
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            db.session.commit()
            session['image'] = filename
    return redirect(url_for('sponsor_profile'))
            



@app.route("/sponsor_dashboard/profile", methods=["GET","POST"])
def sponsor_profile():
    if "sponsor_name" not in session.keys() and "sponsor_id" not  in session.keys():
        return redirect(url_for('sponsor_login'))
    name = session["sponsor_name"]
    sponsor_id = session['sponsor_id']
    image = session['image']
    if request.method == 'POST':
        try:
            sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()
            if sponsor:
                sponsor.name = request.form['name']
                sponsor.email = request.form['email']
                sponsor.mobileno = request.form['mobno']
                sponsor.password = request.form['password']
                sponsor.budget = request.form['budget']
                sponsor.industry = request.form['industry']
                sponsor.website_link = request.form['website']
        except Exception as e:
             return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            if sponsor:
                db.session.commit()
                return render_template('message.html', 
                                        id='SUPSUCC',
                                        email=sponsor.email,
                                        password=sponsor.password)
            
        
    try:
        sponsor = Sponsor.query.filter_by(sponsor_id=sponsor_id).first()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        return render_template("sponsor_dashboard.html",id = 'profile',sponsor=sponsor,name=name,image=image) 



@app.route("/sponsor_dashboard", methods=["GET","POST"])
def sponsor_dashboard():
    if "sponsor_name" not in session.keys() and "sponsor_id" not in session.keys():
        return redirect(url_for('sponsor_login'))
    name = session['sponsor_name']
    sponsor_id = session['sponsor_id']
    image = session['image']
    try:
        privateADadrequests = Adrequest.query.filter_by(createdby=sponsor_id).all()
        campaigns_ids = db.session.query(Campaign.campaign_id).filter_by(createdby=sponsor_id,visibility='public').all()
        ids = [id[0] for id in campaigns_ids]
        publicADrequests = Adrequest.query.filter(
            Adrequest.campaign_id.in_(ids)
        ).all()

    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        return render_template('sponsor_dashboard.html',
                               id='Adrequest',
                               name=name,
                               image=image,
                               privateADrequests=privateADadrequests,
                               publicADrequests=publicADrequests)
    
    #return render_template("sponsor_dashboard.html",name = name,image=image)




@app.route('/sponsor_dashboard/<string:flag>/<string:ad_id>',methods=["GET","POST"])
def about_adrequest(flag,ad_id):
    if "sponsor_name" not in session.keys() and "sponsor_id" not in session.keys():
        return redirect(url_for('sponsor_login'))
    name = session['sponsor_name']
    sponsor_id = session['sponsor_id']
    image = session['image']
    
    adrequest = Adrequest.query.filter_by(adId = ad_id).first_or_404()
    
    if flag == 'v':
        return render_template('Adrequest_view.html',id='view',name=name,image=image,adrequest=adrequest)
    elif flag == 'e':
        if adrequest and request.method == 'POST':
            try:
                adrequest.messages = request.form['message']
                adrequest.requirements = request.form['requirements']
                adrequest.payment_amount = request.form['amount']
            except Exception as e:
                return render_template('message.html', id = 'DBERROR', error = e),503
            else:
                db.session.commit()
                return render_template('Adrequest_view.html',id='view',name=name,image=image,adrequest=adrequest)
        return render_template('Adrequest_view.html',id='edit',name=name,image=image,adrequest=adrequest)
    elif flag == 'ng':
        if adrequest and request.method == 'POST':
            choice = request.form['choice']
            if choice == 'yes':
                try:
                    adrequest.payment_amount = adrequest.nego_amount
                    adrequest.nego_status = 'accepted'
                except Exception as e:
                    return render_template('message.html', id = 'DBERROR', error = e),503
                else:
                    db.session.commit()
                    
            return render_template('Adrequest_view.html',id='view',name=name,image=image,adrequest=adrequest)
        return render_template('Adrequest_view.html',id='delete',name=name,image=image,adrequest=adrequest)
    else:
        if adrequest and request.method=='POST':
            choice = request.form['choice']
            if choice == 'yes':
                try:
                    db.session.delete(adrequest)
                except Exception as e:
                    return render_template('message.html', id = 'DBERROR', error = e),503
                else:
                    db.session.commit()
                    return redirect(url_for('sponsor_dashboard'))
            return render_template('Adrequest_view.html',id='view',name=name,image=image,adrequest=adrequest)
        return render_template('Adrequest_view.html',id='delete',name=name,image=image,adrequest=adrequest)



@app.route('/sponsor_campaigns/create',methods=["GET","POST"])  
def  create_campaigns():
    if 'sponsor_id' not in session.keys() and "sponsor_name" not in session.keys():
        return redirect(url_for('sponsor_login')) 
    sponsor_id = session['sponsor_id']
    name = session['sponsor_name']
    image = session['image'] 
    if request.method == 'POST':
        try:
            newCampaing = Campaign()
            newCampaing.campaign_id = generate_random_id("CAMP")
            newCampaing.name = request.form['name']
            newCampaing.industry = request.form['industry']
            newCampaing.start_date = (request.form['start_date'])
            newCampaing.end_date = (request.form['end_date'])
            newCampaing.budget = request.form['budget']
            newCampaing.visibility = request.form['visibility']
            newCampaing.goals = request.form['goals']
            newCampaing.current_status = request.form['status']
            newCampaing.description = request.form['description']
            newCampaing.createdby = session['sponsor_id']
            newCampaing.created_date = datetime.now().strftime('%Y-%m-%d %H:%M')
            newCampaing.flaged_status = 'noflaged'
            db.session.add(newCampaing)
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            db.session.commit()
            return redirect(url_for('campaigns'))
    return render_template('sponsor_dashboard.html', id='create' ,name=name,image=image)
    




@app.route('/sponsor_campaigns',methods=["GET","POST"])
def campaigns():
    if 'sponsor_id' not in session.keys() and "sponsor_name" not in session.keys():
        return redirect(url_for('sponsor_login'))
    sponsor_id = session['sponsor_id']
    name = session['sponsor_name']
    image = session['image']
    try:
        campaigns = Campaign.query.filter_by(createdby=sponsor_id).all()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    
    return render_template('sponsor_dashboard.html',id='campaigns',name=name,image=image,campaigns=campaigns)
     



@app.route('/sponsor_camp/<string:flag>/<string:camp_id>',methods=["GET","POST"])
def about_camp(flag,camp_id):
    if 'sponsor_id' not in session.keys() and "sponsor_name" not in session.keys():
        return redirect(url_for('sponsor_login'))
    sponsor_id = session['sponsor_id']
    name = session['sponsor_name']
    image = session['image']
    
    campaign = Campaign.query.filter_by(campaign_id = camp_id).first_or_404()
    
      
    if flag == 'v':
        return render_template('about_campaign.html',id='campaignView',name=name,image=image,campaign=campaign)
    elif flag == 'edit':
        if campaign and request.method == 'POST':
            try:
                campaign.name = request.form['name']
                campaign.start_date = (request.form['start_date'])
                campaign.end_date = (request.form['end_date'])
                campaign.budget = request.form['budget']
                campaign.visibility = request.form['visibility']
                campaign.goals = request.form['goals']
                campaign.current_status = request.form['status']
                campaign.description = request.form['description']
                campaign.createdby = session['sponsor_id']
            except Exception as e:
                return render_template('message.html', id = 'DBERROR', error = e),503
            else:
                db.session.commit()
                return render_template('about_campaign.html',id='campaignView',name=name,image=image,campaign=campaign)
        return render_template('about_campaign.html',id='campaignEdit',name=name,image=image,campaign=campaign)
    else:
        if campaign and request.method=='POST':
            choice = request.form['choice']
            if choice == 'yes':
                try:
                    db.session.query(Adrequest).filter_by(campaign_id = camp_id).delete()
                    db.session.delete(campaign)
                except Exception as e:
                    return render_template('message.html', id = 'DBERROR', error = e),503
                else:
                    db.session.commit()
                    return redirect(url_for('campaigns'))
            return render_template('about_campaign.html',id='campaignView',name=name,image=image,campaign=campaign)
        return render_template('about_campaign.html',id='campaignDelete',name=name,image=image,campaign=campaign)

    



@app.route('/sponsor_dashboard/search_influencers',methods=["GET","POST"])
def search_influencers():
    if 'sponsor_id' not in session.keys() and "sponsor_name" not in session.keys():
        return redirect(url_for('sponsor_login'))
    sponsor_id = session['sponsor_id']
    name = session['sponsor_name']
    image = session['image'] 
    query_niche = request.args.get('niche')
    min_follower = request.args.get('min_follower')
    if query_niche == None or min_follower == None:
        return render_template('sponsor_dashboard.html', id='search', name=name,image=image,empty_q=True)
    try:
        influencers = Influencer.query.filter(
            Influencer.niche.ilike(f'%{query_niche}%'),
            Influencer.reach >= int(min_follower)
        ).all()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        return render_template('sponsor_dashboard.html', id='search', name=name,image=image,influencers=influencers,empty_q=False)

@app.route('/sponsor_dashboard/search_influencers/v/<string:influencer_id>',methods=["GET","POST"])
def find_influencers(influencer_id):
    if 'sponsor_id' not in session.keys() and "sponsor_name" not in session.keys():
        return redirect(url_for('sponsor_login'))
    sponsor_id = session['sponsor_id']
    name = session['sponsor_name']
    image = session['image'] 
    try:
        influencer = Influencer.query.filter_by(influencer_id=influencer_id).first()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        return render_template('find_influencer.html',id='view',name=name,image=image,influencer=influencer)

@app.route('/sponsor_dashboard/adrequest/<string:influencer_id>',methods=["GET","POST"])
def make_request(influencer_id):
    if 'sponsor_id' not in session.keys() and "sponsor_name" not in session.keys():
        return redirect(url_for('sponsor_login'))
    sponsor_id = session['sponsor_id']
    name = session['sponsor_name']
    image = session['image'] 
    try:
        influencer = Influencer.query.filter_by(influencer_id=influencer_id).first_or_404()
        campaigns = Campaign.query.filter_by(createdby=sponsor_id,visibility='private',current_status='open').all()
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    if request.method == "POST":
        try:
            adrequest = Adrequest.query.filter_by(campaign_id=request.form['campaign'], influencer_id=influencer_id).first()
            if not adrequest:
                newAdrequest = Adrequest()
                newAdrequest.adId = generate_random_id('AD')
                newAdrequest.campaign_id = request.form['campaign']
                newAdrequest.influencer_id = request.form['id']
                newAdrequest.messages = request.form['message']
                newAdrequest.requirements = request.form['requirements']
                newAdrequest.payment_amount = request.form['amount']
                newAdrequest.status = 'pending'
                newAdrequest.type = 'private'
                newAdrequest.createdby = sponsor_id
                newAdrequest.send_date = datetime.now().strftime('%Y-%m-%d %H:%M')
                db.session.add(newAdrequest)
            else:
                return render_template('find_influencer.html',id='alreadySend',name=name,image=image,influencer=influencer)
        except Exception as e:
            return render_template('message.html', id = 'DBERROR', error = e),503
        else:
            db.session.commit()
            return render_template('find_influencer.html',id='success',name=name,image=image,influencer=influencer)
    return render_template('find_influencer.html',id='send',name=name,image=image,influencer=influencer,campaigns=campaigns)
            
        
    


@app.route("/sponsor/logout", methods=["GET","POST"])
def sponsor_logout():
    if 'sponsor_id' not in session.keys() and "sponsor_name" not in session.keys():
        return redirect(url_for('sponsor_login'))
    sponsor_id = session['sponsor_id']
    
    
    session.pop('sponsor_id')
    session.pop('sponsor_name')
    session.pop('image')
    try:
        sponsor = Sponsor.query.filter_by(sponsor_id = sponsor_id).first()
        sponsor.status = 0  # type: ignore
    except Exception as e:
        return render_template('message.html', id = 'DBERROR', error = e),503
    else:
        db.session.commit()
    return redirect(url_for('sponsor_login'))
        
