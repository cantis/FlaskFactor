# from app import create_app
# from app.models.item_type import Item_Type, db

# app = None


# def init_db():
#     """ create the database and load in any base lookup values """
#     # Note: the admin user creation script is in create_user.py

#     # Create the Database
#     with app.app_context():
#         db.create_all()

#         # Load lookup values
#         db.session.add(Item_Type(item_type='Ammunition'))
#         db.session.add(Item_Type(item_type='Armour'))
#         db.session.add(Item_Type(item_type='Equipment'))
#         db.session.add(Item_Type(item_type='Melee'))
#         db.session.add(Item_Type(item_type='Misc Magic'))
#         db.session.add(Item_Type(item_type='Potion'))
#         db.session.add(Item_Type(item_type='Ranged'))
#         db.session.add(Item_Type(item_type='Ring'))
#         db.session.add(Item_Type(item_type='Scroll'))
#         db.session.add(Item_Type(item_type='Wand'))
#         db.session.add(Item_Type(item_type='Treasure'))
#         db.session.commit()


# if __name__ == '__main__':
#     app = create_app()
#     init_db()
