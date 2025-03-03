import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theunihub.settings')

django.setup()

def populate():

if __name__ == '__main__':
    
    print('Populating TheUniHub database...')
    
    populate()