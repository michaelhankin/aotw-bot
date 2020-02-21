class DataStore:
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection

    def save_nomination(self, nomination_url, user_id):
        return self.redis_connection.hsetnx(
            'nominations', user_id, nomination_url)

    def list_nominations(self):
        return self.redis_connection.hgetall('nominations')
