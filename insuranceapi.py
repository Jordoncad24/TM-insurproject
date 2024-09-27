from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
import os

app = Flask(__name__)

# Configuration
app.config["MONGO_URI"] = "mongodb+srv://jordoncad24:Bionicle24.@insuranceproject.sfyyy.mongodb.net/insurance?retryWrites=true&w=majority"

# Initialize PyMongo
mongo = PyMongo(app)

# Home page route
@app.route('/')
def home():
    return render_template('index.html')  # Render the index.html file

@app.route('/api/policies', methods=['GET']) #Method for getting all policies within the database 
def get_all_policies():
    try:
        policies_collection = mongo.db.policies
        policies = policies_collection.find()
        policies_list = []

        for policy in policies: #List all details for all of the policies
            policies_list.append({
                'id': str(policy['_id']),
                'policy_number': policy.get('policy_number'),
                'policy_holder_name': policy.get('policy_holder_name'),
                'premium_amount': policy.get('premium_amount'),
                'status': policy.get('status')
            })

        return jsonify(policies_list), 200

    except PyMongoError as e:
        return jsonify({"error": "Database error occurred", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500

@app.route('/api/policies/search', methods=['GET']) #Search for a paticular policy number
def search_policy():
    policy_number = request.args.get('policy_number', '').strip()
    try:
        policies_collection = mongo.db.policies
        policies = policies_collection.find({'policy_number': {'$regex': policy_number, '$options': 'i'}})  # Case-insensitive search
        policies_list = []

        for policy in policies:
            policies_list.append({
                'id': str(policy['_id']),
                'policy_number': policy.get('policy_number'),
                'policy_holder_name': policy.get('policy_holder_name'),
                'premium_amount': policy.get('premium_amount'),
                'status': policy.get('status')
            })

        return jsonify(policies_list), 200

    except PyMongoError as e:
        return jsonify({"error": "Database error occurred", "message": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500

@app.route('/api/policies/<policy_number>', methods=['GET']) #Getting a paticular policy number
def get_policy_by_number(policy_number):
    try:
        policy = mongo.db.policies.find_one({'policy_number': policy_number})
    except Exception as e:
        return jsonify({'message': 'Error retrieving policy'}), 500

    if policy:
        return jsonify({
            'id': str(policy['_id']),
            'policy_number': policy.get('policy_number'),
            'policy_holder_name': policy.get('policy_holder_name'),
            'premium_amount': policy.get('premium_amount'),
            'status': policy.get('status')
        })
    else:
        return jsonify({'message': 'Policy not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
