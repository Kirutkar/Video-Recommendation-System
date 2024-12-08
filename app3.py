from flask import Flask, jsonify, request
import pandas as pd
from fetch_data import fetch_data
from data_preprocessing import preprocess_data  # Import the preprocess function from preprocess.py
from recommendation import hybrid_recommendation, content_based_recommendation, recommend_videos_by_emoji
from feed import get_feed_by_category, get_feed_by_username
app = Flask(__name__)


# Fetch and preprocess data
def fetch_and_preprocess_data():
    # Step 1: Fetch data using fetch_data
    # fetch_data()  # Assuming this function fetches and saves data files
    # Step 2: Preprocess the data
    final_data = preprocess_data()  # Assuming preprocess_data function returns the processed dataframe
    return final_data


# Load and preprocess data initially
final_data = fetch_and_preprocess_data()

# Precompute models for content-based and item-based recommendations
content_similarities, item_model, interaction_matrix_scaled = content_based_recommendation(final_data)


# Hybrid Recommendation Endpoint
@app.route('/recommendation/hybrid/<user_id>', methods=['GET'])
def get_hybrid_recommendation(user_id):
    top_n = request.args.get('top_n', 10, type=int)
    recommendations = hybrid_recommendation(user_id, interaction_matrix_scaled, item_model, content_similarities,
                                            final_data, top_n)
    return jsonify(recommendations.to_dict(orient='records'))


# Recommendation by Emoji Endpoint
@app.route('/recommendation/emoji', methods=['GET'])
def get_recommendation_by_emoji():
    user_emoji = request.args.get('emoji', type=str)
    top_n = request.args.get('top_n', 10, type=int)
    recommendations = recommend_videos_by_emoji(user_emoji, final_data, top_n)
    return jsonify(recommendations.to_dict(orient='records'))





@app.route('/recommendation/feed/category', methods=['GET'])
def get_feed_by_category_endpoint():
    username = request.args.get('username')
    category_id = request.args.get('category_id', type=int)

    if not username or category_id is None:
        return jsonify({"error": "Missing parameters"}), 400

    recommended_posts = get_feed_by_category(final_data, category_id)

    return jsonify({
        "username": username,
        "category_id": category_id,
        "recommended_posts": recommended_posts
        })


@app.route('/recommendation/feed/username', methods=['GET'])
def get_feed_by_username_endpoint():
    username = request.args.get('username')

    if not username:
        return jsonify({"error": "Missing username parameter"}), 400

    recommended_posts = get_feed_by_username(final_data, username)

    return jsonify({
        "username": username,
        "recommended_posts": recommended_posts
    })


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
