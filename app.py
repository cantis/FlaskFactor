from . import create_app, db

app = create_app()
app.app_context().push()
db.create_all()

if __name__ == '__main__':
    pass
