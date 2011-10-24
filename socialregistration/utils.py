import uuid

def generate_username(user, profile, client):
    """
    Default function to generate usernames using the built in `uuid` library.
    """
    return str(uuid.uuid4())[:30]
