def user_valida(username):
    query=f'''
    SELECT * FROM usuario where username = '{username}' 
    '''
    return query


def insertar_usuario(username, password):
    query=f'''
    INSERT INTO usuario(username, password)
    values
    ('{username}', '{password}')
    '''
    return query

def obtener_ventas():
    query=f'''
    SELECT * FROM ventas
    '''
    return query

def create_venta(username, venta, venta_producto):
    query=f'''
    INSERT INTO ventas(username_id, venta, ventas_productos)
    values
    ('{username}', '{venta}', '{venta_producto}')
    '''
    return query

def update_venta(id, valor):
    query=f'''
    UPDATE ventas set venta= {valor} where id = {id} 
    '''
    return query

def delete_venta(id):
    query=f'''
    DELETE FROM ventas where id = {id} 
    '''
    return query
