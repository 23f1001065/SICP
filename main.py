from flask import Flask, render_template
from application.config import ProjectDevelopmentConfig
from application.database import db
from application.bluprint import influencer_app, sponsor_app, admin_app
"""`this app is the main application context.
    Here it is main flask object and in this application it is only one application context.
    We can create many application context , which is called 'Blueprint'.
    This is like a container that do every logic of the application
"""
app = Flask(__name__,static_folder='static')
app.config.from_object(ProjectDevelopmentConfig)
db.init_app(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

from application.influencer import *
from application.sponsor import *
from application.admin import*


app.register_blueprint(influencer_app)
app.register_blueprint(sponsor_app)
app.register_blueprint(admin_app)




if __name__ == '__main__':
    app.run(debug=True)
    






