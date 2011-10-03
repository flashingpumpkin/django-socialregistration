import uuid

def generate_username(user, profile, client):
    return str(uuid.uuid4())[:30]