from .db import next_menu_id, next_order_id

def get_next_menu_id():
    global next_menu_id
    val = next_menu_id
    next_menu_id += 1
    return val

def get_next_order_id():
    global next_order_id
    val = next_order_id
    next_order_id += 1
    return val
