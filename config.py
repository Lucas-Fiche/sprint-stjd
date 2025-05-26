import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fallback-key-development-only'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # Não deixar chaves expostas em produção
    if not os.environ.get('SECRET_KEY'):
        raise ValueError("SECRET_KEY deve ser definida em produção")
    if not os.environ.get('GEMINI_API_KEY'):
        raise ValueError("GEMINI_API_KEY deve ser definida em produção")

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}