# create a first user...
# Based on: https://realpython.com/using-flask-login-for-user-management-with-flask/
from app.models.user import User, db
from app.users.users import hash_password

from app import create_app

app = create_app()


def main():
    with app.app_context():
        if User.query.all():
            if input('A user already exists! Create another? (y/n): ') == 'n':
                return

        email = input('Enter email address: ')
        first_name = input('First Name: ')
        last_name = input('Last Name: ')
        password = input('Password: ')

        user = User(
            user_id=email,
            firstname=first_name,
            lastname=last_name,
            password=hash_password(password)
        )
        db.session.add(user)
        db.session.commit()
        print('\r-- User Added')


if __name__ == '__main__':
    main()
