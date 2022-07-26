from core.users.models import User


# ----------- GETTING USER BY ID ------------------

def user_exists(user_id: int) -> bool:
    """Function that check if users exists in database"""

    return User.objects.filter(id=user_id).exists()
