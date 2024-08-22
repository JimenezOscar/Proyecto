#Este es un conjunto de pruebas automatizadas para una API de productos utilizando el framework Behave en Python.
# Behave es un framework que permite escribir pruebas de comportamiento en un formato de texto legible y luego ejecutarlas
import requests # Se utiliza para enviar solicitudes HTTP y manejar respuestas en Python. Permite realizar operaciones como enviar GET o POST requests.
from behave import given, when, then #importa los decoradores de behave para que los podamos usar

API_URL = "http://localhost:5000"

# ---------------------------------- Obtener todos los productos---------------------------------------------------
# Given: la API está en funcionamiento
#verificar que la API esté en funcionamiento antes de continuar con otras pruebas. Se hace enviando una solicitud
# HTTP GET a la URL de la API y comprobando que la respuesta tenga un código de estado 200
@given('la API está en funcionamiento')
def verificar_api_funcionando(context):
    response = requests.get(API_URL) #request.get, es el nombre del modulo
    assert response.status_code == 200

# Este paso envía una solicitud a la API para obtener la lista de todos los productos.
# Usa una función para enviar una solicitud de tipo GET a la dirección específica de la API (/products).
# La respuesta de esta solicitud se guarda en context.response
@when('envío una solicitud GET a "/products"')
def enviar_solicitud_get_productos(context):
    context.response = requests.get(f"{API_URL}/products")

# Verifica que la respuesta de la API sea correcta.
# Revisa el "código de estado" de la respuesta. Un código 200 significa que la solicitud fue exitosa y
# que la API respondió correctamente.
@then('el código de estado de la respuesta debe ser 200')
def verificar_codigo_estado_200(context):
    assert context.response.status_code == 200
# Comprueba que la respuesta de la API contenga una lista de productos.
# Convierte la respuesta de la API en formato JSON y verifica que sea una lista (como una lista de productos).
@then('la respuesta debe contener una lista de productos')
def verificar_lista_productos(context):
    assert isinstance(context.response.json(), list)


# -----------------------------------Obtener un producto por ID-----------------------------------------------------
# Envía una solicitud para obtener los detalles de un producto específico usando su ID.
# Utiliza el ID del producto, que se pasa como parte de la URL (/products/{id}), para hacer la
# solicitud GET. La respuesta de esta solicitud se guarda en context.response.
@when('envío una solicitud GET a "/products/{id}"')
def enviar_solicitud_get_producto_por_id(context, id):
    context.response = requests.get(f"{API_URL}/products/{id}")
# Verifica que la respuesta contenga el producto con el ID específico.
# Convierte la respuesta en formato JSON y comprueba que el ID del producto en la respuesta coincide con el ID que se
# solicitó.
@then('la respuesta debe contener el producto con ID {id}')
def verificar_producto_por_id(context, id):
    product = context.response.json()
    assert product['id'] == int(id)

# ------------------------------------Crear un nuevo producto---------------------------------------------------------
# Envía una solicitud para crear un nuevo producto con los datos proporcionados.
# Toma los datos del producto (ID, nombre, precio, stock) de la tabla en el escenario de Gherkin, los organiza en un
# formato adecuado (JSON) y envía una solicitud POST a la API. La respuesta se guarda en context.response.
@when('envío una solicitud POST a "/products" con los siguientes datos')
def enviar_solicitud_post_nuevo_producto(context):
    for row in context.table:
        product_data = {
            "id": int(row['id']),
            "name": row['name'],
            "price": float(row['price']),
            "stock": int(row['stock'])
        }
    context.response = requests.post(f"{API_URL}/products", json=product_data)

@then('el codigo de estado de la respuesta debe ser 200')
def verificar_codigo_estado_200(context):
    assert context.response.status_code == 200

# Verifica que la respuesta de la solicitud POST contiene el nuevo producto con el ID que se ha proporcionado.
# Convierte la respuesta en formato JSON y comprueba que el ID del nuevo producto en la respuesta coincide con el ID
# que se envió en la solicitud.
@then('la respuesta debe contener el nuevo producto con ID {id}')
def verificar_nuevo_producto(context, id):
    product = context.response.json()
    assert product['id'] == int(id)

# ---------------------------------Crear un producto con datos inválidos------------------------------------------------
# Envía una solicitud para crear un producto, pero con datos que no son válidos.
# Toma los datos del producto (ID, nombre, precio, stock) que se definen como inválidos en la tabla del escenario de
# Gherkin, organiza esos datos en formato JSON, y luego hace una solicitud POST a la API. La respuesta de la API se guarda en context.response.
@when('envío una solicitud POST a "/products" con datos inválidos')
def enviar_solicitud_post_producto_datos_invalidos(context):
    for row in context.table: #se usa un bucle for para recorrer context.table proporcionada por el archivo gherkin
        product_data = {    #crea un diccionario con los productos
            "id": int(row['id']),
            "name": row['name'],
            "price": float(row['price']),
            "stock": int(row['stock'])
        }
    context.response = requests.post(f"{API_URL}/products", json=product_data)

# Verifica que la respuesta de la API tenga el código de estado 422.
# Revisa el código de estado de la respuesta guardada en context.response.
@then('el código de estado de la respuesta debe ser 422')
def verificar_codigo_estado_422(context):
    assert context.response.status_code == 422
# Verifica que la respuesta de la API contenga un mensaje de error.
# Convierte la respuesta en formato JSON y comprueba que el mensaje de error (usualmente bajo la clave 'detail') esté
# presente.
@then('la respuesta debe contener un mensaje de error')
def verificar_mensaje_error(context):
    assert 'detail' in context.response.json()

# -----------------------------------Crear un producto con ID duplicado------------------------------------------------
# Envía una solicitud para crear un nuevo producto, pero con un ID que ya está en uso (duplicado).
# Toma los datos del producto (ID, nombre, precio, stock) que están definidos en la tabla del escenario de Gherkin,
# organiza esos datos en formato JSON, y hace una solicitud POST a la API. La respuesta de la API se guarda en context.response.
@when('envío una solicitud POST a "/products" con ID duplicado')
def enviar_solicitud_post_producto_id_duplicado(context):
    for row in context.table:
        product_data = {
            "id": int(row['id']),
            "name": row['name'],
            "price": float(row['price']),
            "stock": int(row['stock'])
        }
    context.response = requests.post(f"{API_URL}/products", json=product_data)

# Verifica que la respuesta de la API tenga el código de estado 400.
# Revisa el código de estado de la respuesta guardada en context.response.
@then('el código de estado de la respuesta debe ser 400')
def verificar_codigo_estado_400(context):
    assert context.response.status_code == 400

# Verifica que la respuesta de la API contenga un mensaje de error específico.
# Convierte la respuesta en formato JSON y comprueba que el mensaje de error bajo la clave 'detail' sea "El producto
# con este ID ya existe".
@then('la respuesta debe contener un mensaje de error "El producto con este ID ya existe"')
def verificar_mensaje_error_id_duplicado(context):
    assert context.response.json()['detail'] == "El producto con este ID ya existe"

# --------------------------------Actualizar un producto existente----------------------------------------------------
# Toma los datos del producto (ID, nombre, precio, stock) de la tabla en el escenario de Gherkin, organiza esos datos
# en formato JSON, y hace una solicitud PUT a la API con esos datos. La respuesta de la API se guarda en context.response.
# Permite probar si la API puede actualizar correctamente la información de un producto existente con nuevos datos.
@when('envío una solicitud PUT a "/products/{id}" con los siguientes datos')
def enviar_solicitud_put_actualizar_producto(context, id):
    for row in context.table:
        product_data = {
            "id": int(row['id']),
            "name": row['name'],
            "price": float(row['price']),
            "stock": int(row['stock'])
        }
    context.response = requests.put(f"{API_URL}/products/{id}", json=product_data)

# Verifica que la respuesta de la API contenga los datos del producto actualizado.
# Convierte la respuesta de la API en formato JSON y comprueba que el producto tiene el ID que se especificó. Si el
# ID coincide, se asume que el producto se actualizó correctamente.
@then('la respuesta debe contener el producto actualizado con ID {id}')
def verificar_producto_actualizado(context, id):
    product = context.response.json()
    assert product['id'] == int(id)

#------------------------------- Actualizar un producto con datos inválidos-------------------------------------------
# Envía una solicitud para actualizar un producto con datos que no son válidos (por ejemplo, valores negativos o campos faltantes).
# Toma los datos inválidos del producto de la tabla en el escenario de Gherkin, organiza esos datos en formato JSON,
# y hace una solicitud PUT a la API con esos datos. La respuesta de la API se guarda en context.response.
@when('envío una solicitud PUT a "/products/{id}" con datos inválidos')
def enviar_solicitud_put_producto_datos_invalidos(context, id):
    for row in context.table:
        product_data = {
            "name": row['name'],
            "price": float(row['price']),
            "stock": int(row['stock'])
        }
    context.response = requests.put(f"{API_URL}/products/{id}", json=product_data)

# Verifica que la respuesta de la API tenga el código de estado 422.
# Revisa el código de estado de la respuesta guardada en context.response.
@then('el código del estado de la respuesta debe ser 422')
def verificar_codigo_estado_422_actualizacion(context):
    assert context.response.status_code == 422

# Verifica que la respuesta de la API incluya un mensaje de error.
# Convierte la respuesta de la API en formato JSON y comprueba que contiene una clave llamada 'detail',
# que generalmente contiene el mensaje de error.
@then('la respuesta debe contener un mensaje del error')
def verificar_mensaje_error_actualizacion(context):
    assert 'detail' in context.response.json()

#----------------------------------- Eliminar un producto existente-------------------------------------------------
# Envía una solicitud para eliminar un producto específico de la API.
# Utiliza el método HTTP DELETE para enviar una solicitud a la URL del producto que se desea eliminar, donde {id} es
# el identificador del producto. La respuesta de la API se guarda en context.response.
@when('envío una solicitud DELETE a "/products/{id}"')
def enviar_solicitud_delete_producto(context, id):
    context.response = requests.delete(f"{API_URL}/products/{id}")

# Verifica que la respuesta de la API tenga el código de estado 200.
# Revisa el código de estado de la respuesta almacenada en context.response.
@then('el código de estado de la respuesta debe ser igual a 200')
def verificar_codigo_estado_200_eliminacion(context):
    assert context.response.status_code == 200

# -----------------------------------Eliminar un producto sin ID------------------------------------------------------
# Envía una solicitud DELETE a la URL de la API sin especificar un ID de producto.
# Utiliza el método HTTP DELETE para hacer una solicitud a la URL base de los productos (/products), en lugar de una
# URL específica para un producto.
@when('envío una solicitud DELETE a "/products"')
def enviar_solicitud_delete_producto_sin_id(context):
    context.response = requests.delete(f"{API_URL}/products")

# Verifica que la respuesta de la API tenga el código de estado 405.
# Revisa el código de estado de la respuesta almacenada en context.response.
@then('el código de estado de la respuesta debe ser 405')
def verificar_codigo_estado_405(context):
    assert context.response.status_code == 405

# Verifica que la respuesta de la API incluya un mensaje de error que explique por qué la solicitud no es permitida.
# Convierte la respuesta de la API en formato JSON y comprueba que contenga un mensaje de error con el texto "Method
# Not Allowed".
@then('la respuesta debe contener un mensaje de error "Method Not Allowed"')
def verificar_mensaje_error_metodo_no_permitido(context):
    assert context.response.json()['detail'] == "Method Not Allowed"

#----------------------------Reiniciar los productos a su estado inicial----------------------------------------------
# Envía una solicitud para reiniciar todos los productos en la API a su estado inicial.
# Utiliza el método HTTP POST para enviar una solicitud a la URL /reset.
@when('envío una solicitud POST a "/reset"')
def enviar_solicitud_post_reset(context):
    context.response = requests.post(f"{API_URL}/reset")

# Verifica que la respuesta de la API tenga el código de estado 200.
# Comprueba el código de estado de la respuesta almacenada en context.response.
@then('el código de estado es igual a 200')
def verificar_codigo_estado_200(context):
    assert context.response.status_code == 200

# Verifica que los productos han sido reiniciados a su estado inicial.
# Envía una solicitud GET a la URL /products para obtener la lista de productos actuales. Luego, comprueba que la
# respuesta contiene datos, indicando que los productos están en el estado esperado después del reinicio.
@then('los productos deben ser reiniciados a su estado inicial')
def verificar_productos_reiniciados(context):
    response = requests.get(f"{API_URL}/products")
    response_data = response.json()
    assert response_data