import requests
import json
import os


API_URLS = {
    "viewed_posts": "https://api.socialverseapp.com/posts/view",
    "liked_posts": "https://api.socialverseapp.com/posts/like",
    "inspired_posts": "https://api.socialverseapp.com/posts/inspire",
    "rated_posts": "https://api.socialverseapp.com/posts/rating",
    "all_posts": "https://api.socialverseapp.com/posts/summary/get",
    "all_users": "https://api.socialverseapp.com/users/get_all"
}



HEADERS = {
    "Flic-Token": "flic_6e2d8d25dc29a4ddd382c2383a903cf4a688d1a117f6eb43b35a1e7fadbb84b8"
}
page_size= 1000



def fetch_data(url,output_file):
    page = 1
    all_data=[]

    while True:
        response = requests.get(f"{url}?page={page}&page_size={page_size}", headers=HEADERS)
        if response.status_code == 200:
            response_data = response.json()
            if "users" in response_data:
                data = response_data.get("users", [])
            elif "data" in response_data:
                data = response_data.get("data", [])
            elif "posts" in response_data:
                data = response_data.get("posts", [])
            else:
                print(f"Unknown response structure: {response_data.keys()}")
                break
            if not data:
                break
            all_data.extend(data)
            print(f"Fetched {len(data)} items from page {page}.")
            page += 1
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            break

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(all_data, f, indent=4)
    print(f"Saved {len(all_data)} items to {output_file}.")


if __name__ == "__main__":

    for api_name,url in API_URLS.items():
        output_file=f"data/{api_name}.json"
        print(f"Fetching data for {api_name}..")
        fetch_data(url,output_file)

print("Data Fetching Completed")



