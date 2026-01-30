import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql, OperationalError, Error


class PostgresHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PostgresHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, dbname=None, user=None, password=None, host=None, port=None):
        if hasattr(self, "_initialized") and self._initialized:
            return

        dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.env'))
        load_dotenv(dotenv_path)

        dbname = dbname or os.getenv('DB_NAME')
        user = user or os.getenv('DB_USER')
        password = password or os.getenv('DB_PASSWORD')
        host = host or os.getenv('DB_HOST', 'localhost')
        port = port or int(os.getenv('DB_PORT', 5432))

        self.connection_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }

        self.conn = None
        self.cursor = None
        self._initialized = True  # Flag to prevent re-initialization

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor()
            print("Connected to the database.")
        except OperationalError as e:
            print(f"Failed to connect to the database: {e}")
            raise

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            print("Connection closed.")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            print("Query executed successfully.")
        except Error as e:
            self.conn.rollback()
            print(f"Error executing query: {e}")
            raise

    def fetch_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"Error fetching query: {e}")
            raise

    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching one row: {e}")
            raise

    def __del__(self):
        print("Destroying PostgresHandler instance...")
        try:
            self.close()
        except Exception as e:
            print(f"Error during destructor cleanup: {e}")
        PostgresHandler._instance = None