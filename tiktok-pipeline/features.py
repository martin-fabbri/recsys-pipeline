from mimesis import Generic
from mimesis.locales import Locale
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any


def generate_interactions(num_interactions: int, users: List[Dict[str, str]], videos: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Generate a list of dictionaries, each representing an interaction between a user and a video.

    This function creates interaction data by randomly pairing users with videos and assigning
    interaction details like interaction type, watch time, and whether the video was watched till the end.
    The likelihood of a video being watched till the end is inversely proportional to its length.

    Args:
        num_interactions (int): The number of interactions to generate.
        users (List[Dict[str, str]]): A list of dictionaries, where each dictionary contains user data.
        videos (List[Dict[str, str]]): A list of dictionaries, where each dictionary contains video data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each containing interaction data.
    """
    generic = Generic(locale=Locale.EN)
    interactions = []  # List to store generated interaction data

    for _ in range(num_interactions):
        user = random.choice(users)
        video = random.choice(videos)

        interaction_types = ['like', 'dislike', 'view', 'comment', 'share', 'skip']
        weights = [1.5, 0.2, 3, 0.5, 0.8, 10]

        # Generate watch time and determine if the video was watched till the end
        watch_time = random.randint(1, video['video_length'])
        
        probability_watched_till_end = 1 - (watch_time / video['video_length'])
        watched_till_end = random.random() < probability_watched_till_end

        if watched_till_end:
            watch_time = video['video_length']  # Adjust watch time to video length if watched till the end

        # Constructing the interaction dictionary
        interaction = {
            'interaction_id': generic.person.identifier(mask='####-##-####'),
            'user_id': user['user_id'],
            'video_id': video['video_id'],
            'interaction_type': random.choices(interaction_types, weights=weights, k=1)[0],
            'watch_time': watch_time,
        }

        interactions.append(interaction)  # Add the interaction to the list

    return interactions

def generate_users(num_users: int) -> List[Dict[str, str]]:
    """
    Generate a list of dictionaries, each representing a user with various attributes.

    The function creates fake user data including user ID, gender, age, and country
    using the mimesis library. The user ID is generated based on a specified mask.

    Args:
        num_users (int): The number of user profiles to generate.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing details of a user.
    """
    generic = Generic(locale=Locale.EN)
    users = []  # List to store generated user data

    for _ in range(num_users):
        # Generate each user's details
        user = {
            'user_id': generic.person.identifier(mask='@@###@'),  # Unique user identifier
            'gender': generic.person.gender(),  # Randomly generated gender
            'age': random.randint(12, 90),  # Randomly generated age between 12 and 90
            'country': generic.address.country()  # Randomly generated country name
        }
        users.append(user)  # Add the user to the list

    return users

def generate_video_content(num_videos: int, historical=False) -> List[Dict[str, str]]:
    """
    Generate a list of dictionaries, each representing video content with various attributes.

    Each video includes details such as a unique video ID, category, views count, likes count,
    video length in seconds, and the upload date. The function uses the mimesis library
    for generating random data and Python's random module for numerical attributes.

    Args:
        num_videos (int): The number of video entries to generate.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing details of a video.
    """
    generic = Generic(locale=Locale.EN)
    videos = []  # List to store generated video data
    
    max_views = 500_000

    for _ in range(num_videos):
        if historical:
            days_ago = random.randint(0, 730)  # Choose a random number of days up to two years
            upload_date = datetime.now() - timedelta(days=days_ago)  # Compute the upload date
            
            # Views are influenced by the age of the video, simulating realistic view count accumulation
            age_factor = (730 - days_ago) / 730  # Decreases with the recency of the video
            views = random.randint(0, int(max_views * age_factor))
            
        else:
            upload_date = datetime.now()
            views = random.randint(0, max_views)
        
        # Likes should not exceed the number of views
        likes = random.randint(0, views)

        categories = ['Education', 'Entertainment', 'Lifestyle', 'Music', 'News', 'Sports', 'Technology', 'Dance', 'Cooking', 'Comedy', 'Travel']
        video_length_seconds = random.randint(10, 250)  # Video length in seconds

        video = {
            'video_id': generic.person.identifier(mask='#@@##@'),  # Unique video identifier
            'category': random.choice(categories),
            'views': views,
            'likes': likes,
            'video_length': video_length_seconds,
            'upload_date': upload_date.strftime('%Y-%m-%d')
        }

        videos.append(video)  # Add the video to the list

    return videos



