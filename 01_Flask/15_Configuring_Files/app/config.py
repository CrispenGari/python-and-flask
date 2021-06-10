class Config:
    DEBUG = False
    TESTING = False
    ENV = "production"
    
class Development(Config):
    DEBUG = True
    ENV = "development"

class Testing(Config):
    TESTING =True
class Production:
    pass
