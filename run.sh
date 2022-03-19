export FLASK_APP=server
export FLASK_ENV=development
export DATABASE_URI='mysql://root:dijkstr4@localhost/acoder'
export REDIS_URL='redis://localhost:6379/0'
export SECRET_KEY='ilovejustinbieber'
export CODEX_PLUS_PLUS_BASE_URL='http://127.0.0.1:5000'
flask run --port 1234
