from .group import Group
from pprint import pprint as pretify

from functools import reduce

_TOKEN = "fdc75be5fdc75be5fd75206256fd9e9466ffdc7fdc75be5a56da843614668f3d7775d73"


def build(group_id):
    group = Group(
        group_id=group_id, 
        access_token=_TOKEN
    )
    
    members_count = len(group.members)
    posts_count = len(group.posts)

    members = reduce(lambda acc, item: {
        "sex": {
            "males": acc["sex"]["males"] + int(item["sex"] == 1),
            "females": acc["sex"]["females"] + int(item["sex"] == 2)
        },
        "cities": acc["cities"] + [item["city"]["title"] if item.get("city", None) else "Unknown"]
    }, group.members, {
        "sex": {
            "males": 0,
            "females": 0
        },
        "cities": []
    })

    posts = reduce(lambda acc, item: {
        "likes": acc["likes"] + item["likes"]["count"],
        "views": acc["views"] + item["views"]["count"],
        "reposts": acc["reposts"] + item["reposts"]["count"],
    }, group.posts, {
        "likes": 0,
        "views": 0,
        "reposts": 0
    })

    stats = {
        "id": group.owner_id,
        "group_id": group_id,
        "members": {
            "count": members_count,
            "cities": {
                city: members["cities"].count(city) 
                for city in set(members["cities"]) if members["cities"].count(city) > 100
            },
            "sex": {
                "unknown": (members_count - members["sex"]["males"] - members["sex"]["females"]) / members_count * 100,
                "males": members["sex"]["males"] / members_count * 100,
                "females": members["sex"]["females"] / members_count * 100,
            }
        }, 
    
        "posts": {
            "count": posts_count,
            "avg": {
                "likes": posts["likes"] / posts_count,
                "views": posts["views"] / posts_count,
                "reposts": posts["reposts"] / posts_count
            }
        },
    
        "conversion": {
            "likes": (posts["likes"] / posts_count) / members_count * 100,
            "views": (posts["views"] / posts_count) / members_count * 100,
            "reposts": (posts["reposts"] / posts_count) / members_count * 100
        }
    }
    
    return stats
