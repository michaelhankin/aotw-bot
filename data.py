class DataStore:
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection

    def save_nomination(self, nomination_url, user_id):
        print('nomination URL:', nomination_url)
        print('user ID:', user_id)
        result = self.redis_connection.hset(
            'nominations', user_id, nomination_url)
        print(result)
