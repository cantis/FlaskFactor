# Create a first user.
# This file is designed to be run by itself, it asks questions and then creates a user, it isn't really part of the application.
# Based on: https://realpython.com/using-flask-login-for-user-management-with-flask/
from app import create_app
from app.models.user import User, db
from app.users.users import hash_password

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
