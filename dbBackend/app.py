from blueprints import create_app
from flask_cors import CORS
from flask_caching import Cache
import redis
app = create_app()
app.secret_key = 'your_secret_key_here'
CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})


app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'  # Change to your Redis server's host
app.config['CACHE_REDIS_PORT'] = 6379  # Default Redis port
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

cache = Cache(app)
if __name__ == '__main__':
 app.run(debug=True)
