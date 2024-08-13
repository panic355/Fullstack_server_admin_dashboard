import pwd
import grp
import json

def get_users():
    users = []
    
    for user in pwd.getpwall():
        # Skip system users with UID below 1000 (typically)
        if user.pw_uid < 1000:
            continue

        uid = user.pw_uid
        username = user.pw_name
        full_name = user.pw_gecos.split(',')[0]
        description = user.pw_gecos
        groups = [g.gr_name for g in grp.getgrall() if username in g.gr_mem]

        user_info = {
            'uid': uid,
            'username': username,
            'full_name': full_name,
            'description': description,
            'groups': groups
        }

        users.append(user_info)
    print (users)
    return users