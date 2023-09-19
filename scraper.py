import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Instagram profile data
def scrape_instagram_profile(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        profile_data = soup.find_all('meta', attrs={'property': 'og:description'})[0]['content'].split()

        # Extracting data
        num_followers = int(profile_data[0])
        num_following = int(profile_data[2])
        num_posts = int(profile_data[4])

        # Check for privacy settings
        is_private = 'private' in str(soup)

        # Extracting other features
        profile_pic_element = soup.find('img', alt= 'Profile photo')
        if profile_pic_element:
            has_profile_pic = 1  # Profile picture is present
        else:
            has_profile_pic = 0  # Profile picture is not present

        username_length = len(username)

        # Extract the full name
        full_name_element = soup.find('div', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj')
        if full_name_element:
            full_name = full_name_element.text.strip()
            full_name_words = len(full_name.split())
        else:
            full_name = None
            full_name_words = 0

        # Extract description and URL presence
        description = soup.find('meta', attrs={'name': 'description'})['content']
        description_length = len(description)
        external_url_present = 'external_url' in description

        return {
            'Profile Pic': has_profile_pic,
            'Username Length': username_length,
            'Full Name Words': full_name_words,
            'Full Name Length': len(full_name) if full_name else 0,
            'Name Equals Username': username.lower() == full_name.lower() if full_name else False,
            'Description Length': description_length,
            'External URL': external_url_present,
            'Private': is_private,
            'Number of Posts': num_posts,
            'Number of Followers': num_followers,
            'Number of Following': num_following
        }

    else:
        print(f"Error: Could not fetch data for {username}")
        return None

if __name__ == "__main__":
    usernames = ["aditya_vishwa"]
    results = []

    for username in usernames:
        data = scrape_instagram_profile(username)
        if data:
            results.append(data)

    # Create a DataFrame from the results
    df = pd.DataFrame(results)

    # Save the DataFrame to a CSV file
    df.to_csv('insta_test.csv', index=False)
