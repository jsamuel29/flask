from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'admin.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)
CORS(app)
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=False)
    password = db.Column(db.String(144), unique=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class AdminSchema(ma.Schema):
    class Meta:
        fields = ('username', 'password')


admin_schema = AdminSchema()
admins_schema = AdminSchema(many=True)

# Endpoint to create a new guide
@app.route('/admin', methods=["POST"])
def add_admin():
    username = request.json['username']
    password = request.json['password']

    new_admin = Admin(username, password)

    db.session.add(new_admin)
    db.session.commit()

    admin = Admin.query.get(new_admin.id)

    return admin_schema.jsonify(admin)

@app.route("/admins", methods=["GET"])
def get_admins():
    all_admins = Admin.query.all()
    result = admins_schema.dump(all_admins)
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)