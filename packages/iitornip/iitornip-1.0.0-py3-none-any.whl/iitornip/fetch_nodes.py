import requests
from . import iitornipu

def fetch_node(node):
    exit_node_url = 'https://www.dan.me.uk/torlist/?exit'
    all_node_url = 'https://www.dan.me.uk/torlist/?full'

    if node == 'all':
        response = requests.get(all_node_url)
        table_name = 'all_nodes'
    elif node == 'exit':
        response = requests.get(exit_node_url)
        table_name = 'exit_nodes'
    
    node_ips = response.text.split('\n')
    
    if response.status_code == 200:
        conn = iitornipu.create_sqlite()
        iitornipu.create_table(conn)
        iitornipu.insert_data(conn, table_name, node_ips)
        conn.close()
        return True
    else:
        return False

def check_node(input_ip, node):
    node_name = 'exit_nodes' if node == 'exit' else 'all_nodes'
    conn = iitornipu.create_sqlite()
    with conn:
        cur = conn.cursor()
        cur.execute(f'SELECT ip FROM {node_name} WHERE ip = ?', (input_ip,))
        response = cur.fetchone()
        return response is not None
