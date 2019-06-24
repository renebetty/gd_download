import logging
from os.path import join, dirname
from dotenv import load_dotenv
from map_zoning import MapZoning

dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)

if __name__ == '__main__':
    try:
        MapZoning('深圳市').zoning()
    except Exception as ex:
        logging.error(ex)