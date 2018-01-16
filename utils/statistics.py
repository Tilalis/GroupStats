from .group import Group
from pprint import pprint as pretify

from multiprocessing import Value, Lock

_TOKEN = "fdc75be5fdc75be5fd75206256fd9e9466ffdc7fdc75be5a56da843614668f3d7775d73"
_LOCK = Lock()

def build(group_id, *, status={}):
    max_posts = 2000
    group = Group(
        group_id=group_id, 
        access_token=_TOKEN,
        max_posts = 2000
    )
    
    members_count, members = group.members()
    posts_count, posts = group.posts()
    
    post_number = min(posts_count, max_posts)
    count = members_count + max_posts

    males = 0
    females = 0
    cities = []
    for index, item in enumerate(members, start=1):
        females = females + int(item["sex"] == 1)
        males = males + int(item["sex"] == 2)
        cities.append(
            item["city"]["title"] if item.get("city", None) else "Unknown"
        )
        
        with _LOCK:
            status["members"] = index / members_count
        

    likes = 0
    views = 0
    reposts = 0
    for index, item in enumerate(posts, start=1):
        likes = likes + item.get("likes", {}).get("count", 0)
        views = views + item.get("views", {}).get("count", 0)
        reposts = reposts + item.get("reposts", {}).get("count", 0)

        with _LOCK:
            status["posts"] = index / post_number

    stats = {
        "id": group.owner_id,
        "group_id": group_id,
        "members": {
            "count": members_count,
            "cities": {
                city: cities.count(city) 
                for city in set(cities) if cities.count(city) > 50
            },
            "sex": {
                "unknown": (members_count - males - females) / members_count * 100,
                "males": males / members_count * 100,
                "females": females / members_count * 100,
            }
        }, 
    
        "posts": {
            "count": posts_count,
            "avg": {
                "likes": likes / post_number,
                "views": views / post_number,
                "reposts": reposts / post_number
            }
        },
    
        "conversion": {
            "likes": (likes / post_number) / members_count * 100,
            "views": (views / post_number) / members_count * 100,
            "reposts": (reposts / post_number) / members_count * 100
        }
    }
    
    return stats
