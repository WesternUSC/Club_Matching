from clubmatcher import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return Club.query.get(int(user_id))


class Club(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    ecommerce = db.Column(db.Text, nullable=False, default='https://www.westernusc.store/club-memberships/')
    facebook = db.Column(db.Text)
    instagram = db.Column(db.Text)
    twitter = db.Column(db.Text)
    website = db.Column(db.Text)
    answers = db.Column(db.String(60), nullable=False, default='')

    def get_reset_token(self, expires_sec=1800):
        serializer = Serializer(app.config['SECRET_KEY'], expires_sec)
        return serializer.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serializer = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serializer.loads(token)['user_id']
        except:
            return None
        return Club.query.get(user_id)

    def __repr__(self):
        return f"Club(name='{self.name}', answers=[{self.answers}])"