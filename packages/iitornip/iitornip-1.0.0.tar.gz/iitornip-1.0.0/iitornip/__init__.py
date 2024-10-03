from . import fetch_nodes
import sys
import os


def iitornip(input_ip, node):
    if node == 'all':
        return fetch_nodes.check_node(input_ip, node)
    elif node == 'exit':
        return fetch_nodes.check_node(input_ip, node)
    else:
        return "Invalid node type. Please use all or exit."

    


