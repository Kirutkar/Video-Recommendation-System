# Video-Recommendation-System
A recommendation system to filter video feeds based on user interaction, mood, and category
This repository contains a video recommendation system that provides personalized content suggestions using hybrid recommendation techniques and dynamic feed generation based on user preferences.

Features

Hybrid Recommendation: Combines collaborative and content-based filtering for personalized suggestions.

Feed Generation: Generates a feed based on username, category_id, and mood.

Preprocessing: Cleans and prepares raw data for analysis.

API Integration: Exposes endpoints for recommendations and feeds.

File Structure

video-recommendation/

├── app3.py                 # Main application file to start the Flask server  
├── recommendation.py      # Contains recommendation logic  
├── feed.py                # Handles feed generation based on user preferences  
├── data_preprocessing.py  # Processes and cleans raw data  
├── fetch_data.py          # Fetches the data  
├── requirements.txt       # Python dependencies  
└── README.md              # Project documentation  


Setup Instructions

Prerequisites
Python 3.8 or above installed
A virtual environment (optional but recommended)

Installation

Clone the repository:


git clone https://github.com/your-username/Video-Recommendation.git  
cd Video-Recommendation  

Create and activate a virtual environment (optional):


python -m venv venv  
source venv/bin/activate  # For Linux/macOS  
venv\Scripts\activate     # For Windows 

Install dependencies:

pip install -r requirements.txt  

Running the Application
Start the Flask server by running:
python app.py  
The server will start at http://localhost:5000.

Use Postman or any API testing tool to interact with the application.
API Endpoints

Recommendation
Hybrid Recommendation:
GET /recommendation/hybrid/<user_id>  
Parameters:  
- `top_n` (optional): Number of recommendations to return (default: 5)
  
Feed Generation:

GET /recommendation/feed  
Parameters:  
- `username`: The username of the user requesting the feed  
- `category_id` (optional): Category of content to filter  
- `mood` (optional): Current mood of the user

 
Workflow
Data Fetching:

Data is fetched using the fetch_data() function in fetch_data.py.
Data Preprocessing:

Data is cleaned and prepared using preprocess_data() in data_preprocessing.py.
Recommendation or Feed:

Recommendations or feeds are generated based on the requested API endpoint.

Example Usage

To get a hybrid recommendation:

http://localhost:5000/recommendation/hybrid/user123?top_n=10  

To generate a feed:

http://localhost:5000/recommendation/feed?username=user123&category_id=5&mood=happy 


License
This project is licensed under the MIT License. See the LICENSE file for details.


