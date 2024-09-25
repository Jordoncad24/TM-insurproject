from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError
import os

app = Flask(__name__)

# Configuration
app.config["MONGO_URI"] = "mongodb+srv://jordoncad24:Bionicle24.@insuranceproject.sfyyy.mongodb.net/insurance?retryWrites=true&w=majority"  # Use environment variable

# Initialize PyMongo
mongo = PyMongo(app)

@app.route('/api/policies', methods=['GET'])
def get_all_policies():
    try:
        policies_collection = mongo.db.policies  # Access the policies collection
        policies = policies_collection.find()  # Retrieve all policies
        policies_list = []

        for policy in policies:
            policies_list.append({
                'id': str(policy['_id']),  # Convert ObjectId to string
                'policy_number': policy.get('policy_number'),
                'policy_holder_name': policy.get('policy_holder_name'),
                'premium_amount': policy.get('premium_amount'),
                'status': policy.get('status')
            })

        return jsonify(policies_list), 200  # Return the policies as JSON

    except PyMongoError as e:
        # Handle MongoDB-related errors
        return jsonify({"error": "Database error occurred", "message": str(e)}), 500

    except Exception as e:
        # Handle any other errors
        return jsonify({"error": "An unexpected error occurred", "message": str(e)}), 500

 # Read a policy by ID
@app.route('/api/policies/<policy_id>', methods=['GET'])
def get_policy_by_id(policy_id):
    policies_collection = mongo.db.policies

    try:
        policy = policies_collection.find_one({'_id': ObjectId(policy_id)})
    except Exception as e:
        return jsonify({'message': 'Invalid policy ID format'}), 400

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