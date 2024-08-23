from utils.users import USER_ROLES


def get_user_role(user_id: int) -> str:
    user_id = str(user_id)
    for role, ids in USER_ROLES.items():
        if user_id in ids:
            return role
    return 'unknown'
