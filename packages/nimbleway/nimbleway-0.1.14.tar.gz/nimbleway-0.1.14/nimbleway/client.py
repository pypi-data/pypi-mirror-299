
class Client:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Basic {token}",
        }