from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Plant
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='test user')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='test_user', email='test_user@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         '7bf5596ef7494cf0fa365afac9a5314e'
                                         '?d=identicon&s=128'))

    def test_owned_plants(self):
        user1 = User(username='test_user1', email='test_user1@example.com')
        user2 = User(username='test_user2', email='test_user2susan@example.com')
        db.session.add_all([user1, user2])

        now = datetime.utcnow()
        u1_plant1 = Plant(plant_name="Plant 1", owner=user1,
                  last_watering_timestamp=now + timedelta(seconds=1))
        u2_plant1 = Plant(plant_name="Plant 2", owner=user2,
                  last_watering_timestamp=now + timedelta(seconds=4))
        u1_plant2 = Plant(plant_name="Plant 3", owner=user1,
                  last_watering_timestamp=now + timedelta(seconds=3))

        db.session.add_all([u1_plant1, u1_plant2, u2_plant1])
        db.session.commit()

        # check owned plants
        user1_plants = user1.owned_plants().all()
        user2_plants = user2.owned_plants().all()
        self.assertEqual(user1_plants, [u1_plant2, u1_plant1])
        self.assertEqual(user2_plants, [u2_plant1])




if __name__ == '__main__':
    unittest.main(verbosity=2)