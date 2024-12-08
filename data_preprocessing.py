import pandas as pd
import json
from sklearn.preprocessing import MinMaxScaler


def preprocess_data():
    # Load the data files
    df1 = pd.read_json("data/liked_posts.json")
    df2 = pd.read_json("data/rated_posts.json")
    df3 = pd.read_json("data/viewed_posts.json")
    df4 = pd.read_json("data/inspired_posts.json")
    df5 = pd.read_json("data/all_posts.json")
    df6 = pd.read_json("data/all_users.json")

    # Normalize nested column category in th above dataframe
    if 'category' in df1.columns:
        category_df1 = pd.json_normalize(df1['category'])
        category_df1.columns = [f'category_{col}' for col in category_df1.columns]  # Rename columns
        df1 = pd.concat([df1.drop(columns=['category']), category_df1], axis=1)
    # Dropping few columns which are irrelavant
    col_to_drop = ['thumbnail_url', 'picture_url', 'post_summary']
    df1 = df1.drop(columns=col_to_drop)
    # Normalize baseToken as it is like dict type
    if 'baseToken' in df1.columns:
        baseToken_df1 = pd.json_normalize(df1['baseToken'])
        baseToken_df1.columns = [f'baseToken_{col}' for col in baseToken_df1.columns]  # Rename columns
        df1 = pd.concat([df1.drop(columns=['baseToken']), baseToken_df1], axis=1)
    df1['engagement_score'] = (df1['view_count'] + df1['upvote_count'] - df1['exit_count']) / (df1['view_count'] + 1)
    df1['interaction_rate'] = df1['upvote_count'] / (df1['view_count'] + 1)
    # Dropping few columns which are irrelavant
    col_to_drop = ['thumbnail_url', 'picture_url', 'post_summary']
    df2 = df2.drop(columns=col_to_drop)
    # Normalize baseToken and Category as it is like dict type
    if 'baseToken' in df2.columns:
        baseToken_df2 = pd.json_normalize(df2['baseToken'])
        baseToken_df2.columns = [f'baseToken_{col}' for col in baseToken_df2.columns]  # Rename columns
        df2 = pd.concat([df2.drop(columns=['baseToken']), baseToken_df2], axis=1)
    if 'category' in df2.columns:
        category_df2 = pd.json_normalize(df2['category'])
        category_df2.columns = [f'category_{col}' for col in category_df2.columns]  # Rename columns
        df2 = pd.concat([df2.drop(columns=['category']), category_df2], axis=1)
    # Create new features (if needed)
    df2['total_interactions'] = (
            df2['comment_count'] +
            df2['upvote_count'] +
            df2['view_count']
    )
    # Normalize baseToken and Category as it is like dict type
    if 'baseToken' in df3.columns:
        baseToken_df3 = pd.json_normalize(df3['baseToken'])
        baseToken_df3.columns = [f'baseToken_{col}' for col in baseToken_df3.columns]  # Rename columns
        df3 = pd.concat([df3.drop(columns=['baseToken']), baseToken_df3], axis=1)
    if 'category' in df3.columns:
        category_df3 = pd.json_normalize(df3['category'])
        category_df3.columns = [f'category_{col}' for col in category_df3.columns]  # Rename columns
        df3 = pd.concat([df3.drop(columns=['category']), category_df3], axis=1)
    # Dropping few columns which are irrelavant
    col_to_drop = ['thumbnail_url', 'picture_url', 'post_summary']
    df3 = df3.drop(columns=col_to_drop)
    # Normalize baseToken and Category as it is like dict type
    if 'baseToken' in df4.columns:
        baseToken_df4 = pd.json_normalize(df4['baseToken'])
        baseToken_df4.columns = [f'baseToken_{col}' for col in baseToken_df4.columns]  # Rename columns
        df4 = pd.concat([df4.drop(columns=['baseToken']), baseToken_df4], axis=1)
    if 'category' in df4.columns:
        category_df4 = pd.json_normalize(df4['category'])
        category_df4.columns = [f'category_{col}' for col in category_df4.columns]  # Rename columns
        df4 = pd.concat([df4.drop(columns=['category']), category_df4], axis=1)
    col_to_drop = ['thumbnail_url', 'picture_url', 'post_summary']
    df4 = df4.drop(columns=col_to_drop)
    # Normalize baseToken and Category as it is like dict type
    if 'baseToken' in df5.columns:
        baseToken_df5 = pd.json_normalize(df5['baseToken'])
        baseToken_df5.columns = [f'baseToken_{col}' for col in baseToken_df5.columns]  # Rename columns
        df5 = pd.concat([df5.drop(columns=['baseToken']), baseToken_df5], axis=1)
    if 'category' in df5.columns:
        category_df5 = pd.json_normalize(df5['category'])
        category_df5.columns = [f'category_{col}' for col in category_df5.columns]  # Rename columns
        df5 = pd.concat([df5.drop(columns=['category']), category_df5], axis=1)
    # Dropping few columns which are irrelavant
    col_to_drop = ['thumbnail_url', 'picture_url', 'post_summary']
    df5 = df5.drop(columns=col_to_drop)


    liked_posts=df1
    rated_posts=df2
    view_posts=df3
    inspired_posts=df4
    all_posts=df5
    all_users=df6


    # Clean each dataset before processing
    for df in [liked_posts, rated_posts, view_posts, inspired_posts, all_posts, all_users]:
        df.drop_duplicates(inplace=True)

    # Convert the 'id' column to integer
    for df in [liked_posts, rated_posts, view_posts, inspired_posts, all_posts, all_users]:
        df['id'] = df['id'].astype(int)

    # Clean all_users dataset
    all_users['username'] = all_users['username'].str.lower().str.strip()



    # Define columns to drop
    drop_columns_posts = ['contract_address', 'chain_id', 'chart_url', 'gif_thumbnail_url',
                          'baseToken_address', 'baseToken_name', 'baseToken_symbol', 'baseToken_image_url']

    # Apply transformations to posts datasets
    for df in [liked_posts, rated_posts, view_posts, inspired_posts]:
        df.drop(columns=drop_columns_posts, inplace=True)
        df.fillna({
            'title': 'Unknown Title',
            'category_name': 'general',
            'view_count': 0,
            'comment_count': 0,
            'upvote_count': 0,
            'share_count': 0,
        }, inplace=True)
        df.dropna(subset=['id', 'username'], inplace=True)

    # Handle missing values in all_posts dataset
    drop_columns_all_posts = ['contract_address', 'chain_id', 'chart_url', 'gif_thumbnail_url',
                              'baseToken_address', 'baseToken_name', 'baseToken_symbol', 'baseToken_image_url']
    all_posts.drop(columns=drop_columns_all_posts, inplace=True)
    all_posts.fillna({
        'title': 'Unknown Title',
        'category_name': 'general',
        'view_count': 0,
        'comment_count': 0,
        'upvote_count': 0,
        'share_count': 0,
    }, inplace=True)
    all_posts.dropna(subset=['id'], inplace=True)

    # Clean all_users dataset
    drop_columns_users = ['bio', 'website_url', 'instagram-url', 'youtube_url', 'tictok_url',
                          'referral_code', 'latitude', 'longitude', 'has_wallet']
    all_users.drop(columns=drop_columns_users, inplace=True)
    all_users.fillna({
        'username': 'unknown_user',
        'email': 'unknown@example.com',
        'last_login': '2024-01-01',
        'follower_count': 0,
        'following_count': 0,
        'post_count': 0,
        'share_count': 0,
    }, inplace=True)

    # Add interaction type
    liked_posts['interaction_type'] = 'like'
    rated_posts['interaction_type'] = 'rate'
    view_posts['interaction_type'] = 'view'
    inspired_posts['interaction_type'] = 'inspire'

    # Concatenate all interactions
    interactions = pd.concat([liked_posts, rated_posts, view_posts, inspired_posts], ignore_index=True)

    # Retain necessary columns
    columns_to_retain = [
        'id', 'title', 'comment_count', 'upvote_count', 'view_count', 'rating_count',
        'average_rating', 'share_count', 'exit_count', 'created_at', 'username', 'interaction_type',
        'engagement_score', 'interaction_rate', 'category_id', 'video_link'
    ]
    interactions = interactions[columns_to_retain]

    # Create engagement_score and interaction_rate columns
    interactions['engagement_score'] = (interactions['view_count'] + interactions['upvote_count'] - interactions[
        'exit_count']) / (interactions['view_count'] + 1)
    interactions['interaction_rate'] = interactions['upvote_count'] / (interactions['view_count'] + 1)

    # Process all_posts dataset
    columns_to_retain_posts = [
        'id', 'title', 'comment_count', 'upvote_count', 'view_count', 'rating_count',
        'average_rating', 'share_count', 'exit_count', 'created_at', 'username', 'category_name', 'category_count',
        'category_description'
    ]
    all_posts = all_posts[columns_to_retain_posts]

    # Merge interactions with posts data
    merged_data = pd.merge(interactions, all_posts, on='id', how='inner')

    # Clean up column names after merging
    merged_data = merged_data.drop(
        columns=['title_y', 'comment_count_y', 'upvote_count_y', 'view_count_y', 'rating_count_y', 'average_rating_y',
                 'share_count_y', 'created_at_y', 'username_y', 'exit_count_y'])
    merged_data.rename(columns={
        'username_x': 'username', 'title_x': 'title', 'comment_count_x': 'comment_count',
        'upvote_count_x': 'upvote_count',
        'view_count_x': 'view_count', 'rating_count_x': 'rating_count', 'average_rating_x': 'average_rating',
        'share_count_x': 'share_count',
        'exit_count_x': 'exit_count', 'created_at_x': 'created_at'
    }, inplace=True)

    # Clean all_users dataset
    columns_to_retain_users = [
        'id', 'username', 'email', 'first_name', 'last_name', 'role', 'profile_url', 'isVerified', 'last_login',
        'share_count', 'post_count', 'following_count', 'follower_count'
    ]
    all_users = all_users[columns_to_retain_users]

    # Merge merged_data with all_users dataset
    final_data = pd.merge(merged_data, all_users, on='username', how='inner')

    # Drop unnecessary columns and rename
    final_data = final_data.drop(columns=['id_y', 'share_count_y'])
    final_data.rename(columns={'id_x': 'id', 'share_count_x': 'share_count'}, inplace=True)

    # Add mood column based on category_name
    category_mood_map = {
        'Bloom Scroll': 'Happy', 'Pumptok': 'Excited', 'Vible': 'Happy', 'SolTok': 'Neutral',
        'InstaRama': 'Happy', 'E/ACC': 'Neutral', 'Flic': 'Excited', 'Gratitube': 'Happy'
    }

    def get_mood_from_category(category_name):
        return category_mood_map.get(category_name, 'Neutral')

    final_data['mood'] = final_data['category_name'].apply(get_mood_from_category)
    final_data['content'] = final_data['category_name'] + " " + final_data['category_description']


    scaler = MinMaxScaler()
    final_data['normalized_engagement'] = scaler.fit_transform(final_data[['engagement_score']])

    return final_data
