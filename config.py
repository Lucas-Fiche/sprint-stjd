import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'apito-legal-chave-secreta-2024'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'AIzaSyCAgvlIKULzL6ZepH3ZH6fqJvw6eZeZaPQ'
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}