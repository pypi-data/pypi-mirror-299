from . import fetch_nodes
import sqlite3


def create_sqlite():
    sqlite_db = sqlite3.connect('iitornip/iitornip.db')
    return sqlite_db

def create_table(sqlite_db):
    with sqlite_db:
        sqlite_db.execute('''
            CREATE TABLE IF NOT EXISTS all_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                ip TEXT NOT NULL
            );
        ''')
        sqlite_db.execute('''
            CREATE TABLE IF NOT EXISTS exit_nodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                ip TEXT NOT NULL
            );
        ''')
def insert_data(sqlite_db, node, data):
    with sqlite_db:
        for node_ip in data:
            if node_ip:
                sqlite_db.execute(f'INSERT INTO {node} (ip) VALUES (?);', (node_ip,))


def update_db():
    update_all = fetch_nodes.fetch_node('all')
    update_exit = fetch_nodes.fetch_node('exit')
    all = True if update_all == True else False
    exit = True if update_exit == True else False
    return all and exit
