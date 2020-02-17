class DataStore:
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection

    def save_nomination(self, nomination_url, user_id):
        result = self.redis_connection.hsetnx(
            'nominations', user_id, nomination_url)
        return result
