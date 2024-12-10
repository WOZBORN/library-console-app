import configparser

config = configparser.ConfigParser()
config.read("../config/config.ini")

# Путь к файлу данных
DATA_FILE = config.get("LIBRARY", "data_file", fallback="../test_library.json")

# Поля для поиска
SEARCH_FIELDS = config.get("LIBRARY", "search_fields", fallback="id,title,author,year").split(",")