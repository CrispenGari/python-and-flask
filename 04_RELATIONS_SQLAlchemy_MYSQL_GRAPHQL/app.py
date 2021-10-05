from api import app
from api.models.user import User
from api.models.profile import Profile


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True, port=3001)