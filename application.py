import os, re
from flask import Flask, jsonify, request
from models import db, BlackList, BlackListSchema

black_list_schema = BlackListSchema()
token = "Bearer bearer_token"

application = Flask(__name__)
application.config['PROPAGATE_EXCEPTIONS'] = True
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if "RDS_DB_NAME" in os.environ:
    application.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://"+ str(os.environ.get("RDS_USERNAME")) +":"+ str(os.environ.get("RDS_PASSWORD")) +"@"+ str(os.environ.get("RDS_HOSTNAME")) +":"+ str(os.environ.get("RDS_PORT")) +"/"+ str(os.environ.get("RDS_DB_NAME"))
else:
    application.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///black-list.db"
    application.config["TESTING"] = True
app_context = application.app_context()
app_context.push()

db.init_app(application)
db.create_all()

@application.route("/")
def index():
    return "pong cambio con test fallido"

@application.route("/blacklists/", methods=['POST'])
def post():
    if 'Authorization' not in request.headers:
        return {'msg': 'token is not in header'}, 400
    if request.headers['Authorization'] != token:
        return {'msg': 'token is not valid'}, 401
    
    data = request.get_json()
    
    if "email" not in data or data['email'].strip()=='' or not re.match(r"^\S+@\S+\.\S+$", data['email']):
        return {'msg': 'email parameter not valid'}, 400
    if "app_uuid" not in data or data['app_uuid'].strip()=='':
        return {'msg': 'app_uuid parameter not valid'}, 400
        
    app_uuid = data['app_uuid']
    email = data['email']
    ip_origin = request.remote_addr

    blocked_reason = ''
    if "blocked_reason" in data:
        blocked_reason = data['blocked_reason']

    if len(blocked_reason)>255:
        blocked_reason = blocked_reason[0:255]

    new_email_black_list = BlackList(
        email = email,
        appUuid = app_uuid,
        blockedReason = blocked_reason,
        ipOrigin = ip_origin,
    )
    db.session.add(new_email_black_list)
    db.session.commit()
    return black_list_schema.dump(new_email_black_list), 201

@application.route("/blacklists/<string:email>", methods=['GET'])
def get_email(email):
    if 'Authorization' not in request.headers:
        return {'msg': 'token is not in header'}, 400
    if request.headers['Authorization'] != token:
        return {'msg': 'token is not valid'}, 401

    # result = [black_list_schema.dump(emailBlocked) for emailBlocked in BlackList.query.filter(BlackList.email == email).all()]
    result = BlackList.query.filter(BlackList.email == email).first()
    blocked = False
    reason = ''
    if result is not None:
        #print("get_email: ", result)
        blocked = True
        reason = result.blockedReason
    return {'blocked': blocked, 'blocked_reason': reason}, 200
    # return jsonify(result), 200

if __name__ == "__main__":
    application.run(port = 5000, debug = True)