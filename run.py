from app import app
from config import SECRET_KEY

app.secret_key = SECRET_KEY

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
