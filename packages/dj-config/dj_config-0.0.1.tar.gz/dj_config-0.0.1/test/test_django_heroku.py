import sys
import os
import importlib

import pytest
from dotenv import load_dotenv

load_dotenv()
import testproject.settings as config

def test_databases():
    importlib.reload(config)
    print(config.DATABASES)
    
    assert 'postgres' in config.DATABASES['default']['ENGINE']

# def test_test_runner():
#     # Mock CI environment.
#     os.environ['CI'] = '1'
#     importlib.reload(config)
    
#     assert 'heroku' in config.TEST_RUNNER.lower()
    
#     # Cleanup environment for further tests. 
#     del os.environ['CI']
    
def test_staticfiles():
    importlib.reload(config)
    
    assert config.STATIC_URL == '/static/'
    assert 'whitenoise' in config.MIDDLEWARE[0].lower()
    

def test_allowed_hosts():
    importlib.reload(config)
    
    assert config.ALLOWED_HOSTS == ['*']
    
    
def test_logging():
    importlib.reload(config)
    
    assert 'console' in config.LOGGING['handlers']
    
    
def test_secret_key():

    importlib.reload(config)
    assert config.SECRET_KEY == 'supersecretkey'
