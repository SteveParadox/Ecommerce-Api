import os


class Config:
    def __init__(self):
        pass

    ENV = 'dev'

    
    if os.path.exists('config.env'):
        print('Importing environment from .env file')
        for line in open('config.env'):
            var = line.strip().split('=')
            if len(var) == 2:
                os.environ[var[0]] = var[1].replace("\"", "")
                if ENV == 'dev':
                    if "SECRET_KEY" in var:
                            SECRET_KEY=var[1]
                    else:
                        pass
                    if "JWT_SECRET_KEY" in var:
                        JWT_SECRET_KEY=var[1]
                    else:
                        pass
                    if "SQLALCHEMY_DATABASE_URI" in var:
                        SQLALCHEMY_DATABASE_URI=var[1]
                    else:
                        pass
                    if "MAIL_SERVER" in var:
                        MAIL_SERVER=var[1]
                    else:
                        pass
                    if "MAIL_PORT" in var:
                        MAIL_PORT=var[1]
                    else:
                        pass
                    if "MAIL_USE_TLS" in var:
                        MAIL_USE_TLS=var[1]
                    else:
                        pass
                    if "MAIL_USE_SSL" in var:
                        MAIL_USE_SSL=var[1]
                    else:
                        pass
                    if "MAIL_USERNAME" in var:
                        MAIL_USERNAME=var[1]
                    else:
                        pass
                    if "MAIL_PASSWORD" in var:
                        MAIL_PASSWORD=var[1]
                    else:
                        pass
                    if "MAIL_DEFAULT_SENDER" in var:
                        MAIL_DEFAULT_SENDER=var[1]
                    else:
                        pass
                    if "MAIL_USE_SSL" in var:
                        MAIL_USE_SSL=var[1]
                    else:
                        pass
                    SQLALCHEMY_TRACK_MODIFICATIONS = False
                    CORS_HEADERS = 'Content-Type'
                    JWT_BLACKLIST_ENABLED=True
                    JWT_BLACKLIST_TOKEN_CHECKS=['access', 'refresh']
                    SECURITY_PASSWORD_SALT = 'my_precious_two'
                else:        
                    if "PROD_SECRET_KEY" in var:
                        SECRET_KEY=var[1]
                    else:
                        pass
                    if "MAIL_SERVER" in var:
                        MAIL_SERVER=var[1]
                    else:
                        pass
                    if "MAIL_PORT" in var:
                        MAIL_PORT=var[1]
                    else:
                        pass
                    if "MAIL_USE_TLS" in var:
                        MAIL_USE_TLS=var[1]
                    else:
                        pass
                    if "MAIL_USE_SSL" in var:
                        MAIL_USE_SSL=var[1]
                    else:
                        pass
                    if "MAIL_USERNAME" in var:
                        MAIL_USERNAME=var[1]
                    else:
                        pass
                    if "MAIL_PASSWORD" in var:
                        MAIL_PASSWORD=var[1]
                    else:
                        pass
                    if "MAIL_DEFAULT_SENDER" in var:
                        MAIL_DEFAULT_SENDER=var[1]
                    else:
                        pass
                    if "MAIL_USE_SSL" in var:
                        MAIL_USE_SSL=var[1]
                    else:
                        pass
                    if "API_KEY" in var:
                        API_KEY=var[1]
                    else:
                        pass
                    SQLALCHEMY_TRACK_MODIFICATIONS = False
                    SQLALCHEMY_DATABASE_URI = ""
        #CORS_HEADERS = 'Access-Control-Allow-Origin'

