# recommendation.py
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
#df=pd.read_csv("C:\\Users\\kirut\\PycharmProjects\\codebasics\\VideoRecommendationSystem\\data\\completedataset.csv")
# Content-based Recommendation function
def content_based_recommendation(df, top_n=5):

    vectorizer = TfidfVectorizer(stop_words='english')
    content_matrix = vectorizer.fit_transform(df['content'])
    content_similarities = cosine_similarity(content_matrix)
    df['user_id'] = df['username']

    # Create an item-item similarity matrix using the engagement score
    interaction_matrix = df.pivot_table(index='username', columns='id', values='normalized_engagement', fill_value=0)
    scaler = StandardScaler()
    interaction_matrix_scaled = pd.DataFrame(
        scaler.fit_transform(interaction_matrix),
        index=interaction_matrix.index,
        columns=interaction_matrix.columns
    )

    # Item-based collaborative recommendations
    item_model = NearestNeighbors(n_neighbors=5, metric='cosine', algorithm='auto')
    item_model.fit(interaction_matrix_scaled.T)  # Fit on transposed interaction matrix (item-based)

    return content_similarities, item_model, interaction_matrix_scaled


# Hybrid Recommendation function
def hybrid_recommendation(user_id, interaction_matrix, item_model, content_similarities, df, top_n=5, alpha=0.5):
    if user_id not in interaction_matrix.index:
        return f"User {user_id} not found in the dataset."

    user_index = interaction_matrix.index.get_loc(user_id)

    # Content-based recommendations
    user_engaged_items = interaction_matrix.columns[interaction_matrix.loc[user_id] > 0]
    content_predictions = {}
    for item in user_engaged_items:
        item_index = df[df['id'] == item].index[0]
        similar_items = np.argsort(content_similarities[item_index])[-top_n:]
        content_predictions[item] = np.mean(content_similarities[item_index][similar_items])

    # Item-based collaborative recommendations
    item_predictions = {}
    for item in interaction_matrix.columns:
        distances, indices = item_model.kneighbors(interaction_matrix[item].values.reshape(1, -1))
        similar_items = interaction_matrix.columns[indices[0]]
        item_predictions[item] = np.mean(
            [interaction_matrix.loc[user_id, similar_item] for similar_item in similar_items])

    # Hybrid recommendation
    hybrid_predictions = {}
    for item in interaction_matrix.columns:
        hybrid_predictions[item] = alpha * content_predictions.get(item, 0) + (1 - alpha) * item_predictions.get(item,
                                                                                                                 0)

    top_recommendations = sorted(hybrid_predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]

    # Get details of recommended items (id, category_name, video_link)
    recommended_items = []
    for item, score in top_recommendations:
        item_info = df[df['id'] == item][['id', 'category_name', 'video_link', 'normalized_engagement']].iloc[0]
        recommended_items.append({
            'id': item_info['id'],
            'category_name': item_info['category_name'],
            'video_link': item_info['video_link'],
            'normalized_engagement': item_info['normalized_engagement'],
            'predicted_score': score
        })

    return pd.DataFrame(recommended_items)
'''user_id = 'afrobeezy'
recommendations = hybrid_recommendation(user_id, interaction_matrix, item_model, content_similarities, df, top_n=5, alpha=0.7)
print("Hybrid Recommended Items for User:")
print(recommendations)'''

emoji_to_mood = {
    '\U0001F60A':'Happy',
    '\U0001F603': 'Excited',
    '\U0001F610': 'Neutral',
}


mood_to_content = {
    "Happy": ["motivational", "fun", "positive", "relaxing", "ambient"],
    "Excited": ["high-energy", "sports", "action", "adventure"],
    "Neutral": ["calming", "nature", "meditation" "documentary", "chill"],
}



def recommend_videos_by_emoji(user_emoji, df, top_n=5):
    # Convert emoji to mood (default to 'Neutral' if emoji not found)
    user_mood = emoji_to_mood.get(user_emoji, 'Neutral')  # Default to 'Neutral'

    # Debug: Check what mood was assigned
    print(f"User Mood: {user_mood}")

    # Get the content categories corresponding to the user's mood
    content_categories = mood_to_content.get(user_mood, [])

    # Filter the content based on the mood's content categories
    # You can adjust the filtering logic to match the mood column in your dataset if needed
    filtered_content = df[df['mood'].isin(content_categories)]

    # If no content matches, fallback to random selection
    if filtered_content.empty:
        filtered_content = df.sample(top_n)

    return filtered_content[['title', 'mood', 'normalized_engagement', 'user_id']].head(top_n)



'''user_emoji = '\U0001F610'  # User is feeling happy
recommended_videos = recommend_videos_by_emoji(user_emoji, df)

# Output the recommended videos
print(recommended_videos)'''