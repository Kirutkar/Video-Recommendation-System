# feed.py
import pandas as pd


def get_feed_by_category(final_data, category_id, top_n=10):
    """
    Fetch and return the top N posts for a specific category.
    """
    # Filter the data based on category_id
    filtered_data = final_data[final_data['category_id'] == category_id]

    # Sort posts by engagement score or any other metric you prefer (e.g., upvote_count, view_count)
    filtered_data = filtered_data.sort_values(by='engagement_score', ascending=False)

    # Select the top N recommended posts
    recommended_posts = []
    for idx, row in filtered_data.head(top_n).iterrows():
        recommended_posts.append({
            "post_id": row['id'],
            "title": row['title'],
            "category_id": row['category_id'],
            "category_name": row['category_name'],
            "category_description": row['category_description'],
            "engagement_score": row['engagement_score'],
            "upvote_count": row['upvote_count'],
            "view_count": row['view_count'],
            "rating_count": row['rating_count'],
            "average_rating": row['average_rating'],
            "video_link": row['video_link'],
            "content": row['content']
        })

    return recommended_posts


'''def get_feed_by_mood(final_data, mood, top_n=10):
    """
    Fetch and return the top N posts for a specific mood.
    """
    # Filter the data based on mood
    filtered_data = final_data[final_data['mood'] == mood]

    # Sort posts by engagement score or any other metric you prefer (e.g., upvote_count, view_count)
    filtered_data = filtered_data.sort_values(by='engagement_score', ascending=False)

    # Select the top N recommended posts
    recommended_posts = []
    for idx, row in filtered_data.head(top_n).iterrows():
        recommended_posts.append({
            "post_id": row['id'],
            "title": row['title'],
            "mood": row['mood'],
            "category_name": row['category_name'],
            "engagement_score": row['engagement_score'],
            "upvote_count": row['upvote_count'],
            "view_count": row['view_count'],
            "rating_count": row['rating_count'],
            "average_rating": row['average_rating'],
            "video_link": row['video_link'],
            "content": row['content']
        })

    return recommended_posts'''


def get_feed_by_username(final_data, username, top_n=10):
    """
    Fetch and return the top N posts for a specific username.
    """
    # Filter the data based on username
    filtered_data = final_data[final_data['username'] == username]

    # Sort posts by engagement score or any other metric you prefer (e.g., upvote_count, view_count)
    filtered_data = filtered_data.sort_values(by='engagement_score', ascending=False)

    # Select the top N recommended posts
    recommended_posts = []
    for idx, row in filtered_data.head(top_n).iterrows():
        recommended_posts.append({
            "post_id": row['id'],
            "title": row['title'],
            "username": row['username'],
            "category_name": row['category_name'],
            "engagement_score": row['engagement_score'],
            "upvote_count": row['upvote_count'],
            "view_count": row['view_count'],
            "rating_count": row['rating_count'],
            "average_rating": row['average_rating'],
            "video_link": row['video_link'],
            "content": row['content']
        })

    return recommended_posts
