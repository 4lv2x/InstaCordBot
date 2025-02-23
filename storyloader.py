import os
from typing import Final
import instaloader
from dotenv import load_dotenv

load_dotenv()

USERNAME: Final[str] = os.getenv("IG_USER")
PASSWORD: Final[str] = os.getenv("IG_PASSWRD")

if not USERNAME or not PASSWORD:
    print("ERROR: no username or password provided")
    exit(1)

L = instaloader.Instaloader()

#L.login(USERNAME, PASSWORD)

if not os.path.exists("stories"):
    os.makedirs("stories")

# Login with exception handling
try:
    # First try loading session from file if available
    L.load_session_from_file(USERNAME)
    print("Session restored.")
except FileNotFoundError:
    try:
        print("No session file found. Attempting login...")
        L.login(USERNAME, PASSWORD)
        L.save_session_to_file()  # Save session after successful login
        print("Login successful.")
    except instaloader.exceptions.LoginException as e:
        print(f"Login failed: {e}")
        print("Please verify your username and password.")
        exit(1)



def delete_old() -> None:
    """Delete old stories from the 'stories' directory."""
    for file in os.listdir("stories"):
        os.remove("stories/"+file)

def check_story(username) -> bool:
    """Check for and download available stories for a given username."""
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        stories = L.get_stories(profile)
        for story in stories:
            for item in story.get_items():
                file_path = f"stories/{story.owner_username}_{story.story_item_id}.jpg" if not item.is_video else f"stories/{story.owner_username}_{story.story_item_id}.mp4"
                L.download_storyitem(item, target=file_path)
        if len(os.listdir("stories")) > 0:
            return True
        else:
            return False
    except Exception as exc:
        print(f"Error while fetching stories for {username}: {exc}")
        return False

def download(username) -> None:
    """Download a single story for a given username."""
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        L.download_stories(userids=[profile.userid], filename_target=f"stories")
        print(f"Stories downloaded for {username}")
        return
    except Exception as exc:
        print(f"Error while fetching stories for {username}: {exc}")

def fix_duplicates(directory="stories") -> None:
    for file in os.listdir(directory):
        if file.endswith(".mp4"):
            jpg_file = file.replace(".mp4", ".jpg")
            jpg_path = os.path.join(directory, jpg_file)

            if os.path.exists(jpg_path):
                os.remove(jpg_path)
                print(f"Removed duplicate file: {jpg_file}")