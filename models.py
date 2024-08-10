from application.database import db
from sqlalchemy import String, Integer, Float
class Admin(db.Model):
    __tablename__= 'admin'
    adminID = db.Column(String,primary_key=True)
    password = db.Column(String,unique=True,nullable=False)
    name = db.Column(String,nullable=False)
    last_login = db.Column(String)

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    sponsor_id = db.Column(String,primary_key=True)
    password = db.Column(String,unique=True,nullable=False)
    name = db.Column(String,nullable=False)
    email = db.Column(String,nullable=False,unique=True)
    mobileno = db.Column(String,nullable=False)
    budget = db.Column(Float)
    industry = db.Column(String,nullable=False)
    created_date = db.Column(String,nullable=False)
    last_login = db.Column(String)
    status = db.Column(String,nullable=False)
    website_link = db.Column(String)
    profile_image = db.Column(String)

class Influencer(db.Model):
    __tablename__ = 'influencers'
    influencer_id = db.Column(String,primary_key=True)
    password = db.Column(String,unique=True,nullable=False)
    name = db.Column(String,nullable=False)
    email = db.Column(String,nullable=False,unique=True)
    mobileno = db.Column(String,nullable=False)
    niche = db.Column(String,nullable=False)
    reach = db.Column(Integer,nullable=False)
    category = db.Column(String,nullable=False)
    created_date = db.Column(String,nullable=False)
    last_login = db.Column(String)
    status = db.Column(Integer,nullable=False)
    youtube_link = db.Column(String)
    facebook_link = db.Column(String)
    tweeter_link = db.Column(String)
    insta_link = db.Column(String)
    linkedin_link = db.Column(String)
    profile_image = db.Column(String)

class Campaign(db.Model):
    __tablename__ = 'campaign'
    campaign_id = db.Column(String,primary_key=True)
    name = db.Column(String,nullable=False)
    industry = db.Column(String,nullable=False)
    start_date = db.Column(String,nullable=False)
    end_date = db.Column(String,nullable=False)
    budget = db.Column(Float,nullable=False)
    visibility = db.Column(String,nullable=False)
    goals = db.Column(String,nullable=False)
    current_status = db.Column(String,nullable=False)
    description = db.Column(String,nullable=False)
    createdby = db.Column(String,nullable=False)
    created_date = db.Column(String,nullable=False)

class Adrequest(db.Model):
    __tablename__ = 'adrequest'
    adId = db.Column(String,primary_key=True)
    campaign_id = db.Column(String,nullable=False)
    influencer_id = db.Column(String,nullable=False)
    messages = db.Column(String)
    requirements = db.Column(String,nullable=False)
    payment_amount = db.Column(Float,nullable=False)
    status = db.Column(String,nullable=False)
    type = db.Column(String,nullable=False)
    createdby = db.Column(String,nullable=False)
    send_date = db.Column(String,nullable=False)
    nego_amount = db.Column(Float)
    nego_message = db.Column(String)
    nego_status = db.Column(String)