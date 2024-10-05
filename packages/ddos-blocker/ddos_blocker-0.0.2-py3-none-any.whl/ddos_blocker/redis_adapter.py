from datetime import datetime
from django.conf import settings
import redis

class RedisAdapter:
    def __init__(self):
        # Получаем настройки из settings.py
        self.host = getattr(settings, 'REDIS_HOST', 'localhost')
        self.port = getattr(settings, 'REDIS_PORT', 6379)
        self.db = getattr(settings, 'REDIS_DB', 0)
        self.password = getattr(settings, 'REDIS_PASSWORD', None)

        self.client = redis.StrictRedis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True
        )

        try:
            self.client.ping()
        except redis.ConnectionError as e:
            print(f"Error connecting to Redis: {e}")
            raise


    def set_ip_mask(self, ip):
        """Sets the value for the IP address with timestamp."""
        key = f"{ip}:{datetime.now()}"
        self.client.setex(key, 5 * 60, 1)

    def get_keys(self, ip):
        """Returns all keys that match the pattern for the given IP."""
        return self.client.keys(f"{ip}:*")

    def count_keys(self, ip):
        """Counts the number of keys for a given IP."""
        return len(self.get_keys(ip))