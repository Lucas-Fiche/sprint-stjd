import os
from dotenv import load_dotenv

# Carregar variáveis do .env apenas em desenvolvimento
if os.path.exists('.env'):
    load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-dev-key'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}