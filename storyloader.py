import os
from typing import Final
import instaloader

USERNAME: Final[str] = os.getenv("IG_USER")
PASSWORD: Final[str] = os.getenv("IG_PASSWRD")

L = instaloader.Instaloader()

#L.login(USERNAME, PASSWORD)
#L.login("_alvaaromr", "Ug:,/te3khyT$DLK!X-2wW")

def delete_old():
    import os
    for file in os.listdir("stories"):
        os.remove("stories/"+file)

def check_story(username) -> bool:
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        stories = profile.get_stories()
        for story in stories:
            for item in story.get_items():
                file_path = f"stories/{story.owner_username}_{story.story_item_id}.jpg" if not item.is_video else f"stories/{story.owner_username}_{story.story_item_id}.mp4"
                L.download_storyitem(item, target="stories")
        if len(os.listdir("stories")) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False