from flask import *
from Ecommerce import create_app, db, app


script = create_app()

if __name__ == '__main__':
    script.run(debug=True)
    #with script.app_context():
        #db.drop_all()
        #db.create_all()