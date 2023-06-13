from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy
import certifi


app = Flask(__name__)
api = Api(app)
uri = ""

client = MongoClient(uri, tlsCAFile=certifi.where())
db = client.SimilarityDB
users = db["Users"]

def UserExist(username):

    if users.count_documents({"Username": username}) == 0:
        return False
    else:
        return True
def verifyPw(username, password):
    if not UserExist(username):
        return False
    
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw)==hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username": username,
    })[0]["Tokens"]
    return tokens

class Register(Resource):
    def post(self):
        postedData  = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJSON = {
                "status":301,
                "msg": "Invalid Username"
            }
            return jsonify(retJSON)
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        retJSON = {
            "status":200,
            "msg": "You've successfully signed up to the API "
        }
        return jsonify(retJSON)

class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not UserExist(username):
            retJSON = {
                "status": "301",
                "msg": "Invalid username"
            }
            return jsonify(retJson)
        
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJSON = {
                "status": 302,
                "msg": "Invalid Password"
            }

            num_tokens = countTokens(username)

            if num_tokens <= 0:
                retJson = {
                    "status": 303,
                    "msg": "You're out of tokens, please refill!"
                }
                return jsonify(retJson)
            
        #Calculate the edit distance
        nlp = spacy.load('en_core_web_sm')

        text1 = nlp(text1)
        text2 = nlp(text2)

        #Ratio is a number between 0 and 1 the closer to 1, the more similar text
        # and text2 are
        ratio = text1.similarity(text2)

        retJson = {
            "status": ratio,
            "msg": "Similarity score calculated successfully"

        }

        current_tokens = countTokens(username)

        users.update_one({
            "Username": username,
        },{
            "$set":{
                "Tokens": current_tokens-1
            }
        
        })

        return jsonify(retJson)

class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admim_pw"]
        refill_amount = postedData['refill']

        if not UserExist(username):
            retJSON = {
                "status":301,
                "msg": "Invalid Username"
            }
            return jsonify(retJSON)
        
        correct_pw = 'abc123'
        if not password == correct_pw:
            retJSON = {
                "status": 304,
                "msg": "Invalid Admin Password"
            }
            return jsonify(retJSON)
        
        current_tokens = countTokens(username)
        users.update_one({
            "Username":username
        },{
            "$set":{
                "Tokens": refill_amount+current_tokens
            }
        
        })

        retJSON = {
            "status": 200,
            "msg": "Refilled successfully"
        }
        return jsonify(retJSON)

api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__ == "__main__":
    app.run(host='0.0.0.0')





