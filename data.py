class DataStore:
    def __init__(self, redis_connection):
        self.redis_connection = redis_connection

    def save_nomination(self, nomination_url, user_id):
        current_competition = self.redis_connection.get('aotw-current')
        if current_competition is None:
            # TODO create new competition

        self.redis_connection.sadd(f"{user_id}:{nomination_url}")
