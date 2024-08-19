import requests
from behave import given, when, then

API_URL = "http://localhost:5000"

# Given: la API está en funcionamiento
@given('la API está en funcionamiento') #entonces y given es el decorador que se usa para asociar una funcion con
# un paso
# especifico en los escenarios definidos en el example.feature, la cadena "la API está en funcionamiento" hace
# referencia al paso que debe buscar behave para ejecutar, por lo cual debe ser igual al que aparece en el gherkin.
def verificar_api_funcionando(context): # este es el nombre de la funcion que se ejecuta cuando el behave encuentra el "la API está en funcionamiento"
    # y el context almacena el correcto funcionamiento del given
    response = requests.get(API_URL) # esto lo que hace es enviarme una solicitud GET pasandole los parametros ya
    # definidos anteriormente, requests.get es una funcion de la biblioteca request muy util para enviar peticiones,
    # REQUEST.GET
    # ES un  METODO
    assert response.status_code == 200 #Es un atributo del objeto Response que almacena el código de estado HTTP. Debes acceder a él para obtener el valor del código de estado.
    # status_code: Es el nombre específico para el atributo en la clase Response de requests

# Obtener todos los productos
@when('envío una solicitud GET a "/products"') #el when hace el llamado al gherkin buscando el parametro que tiene
# dentro de los parentesis
def enviar_solicitud_get_productos(context): # luego se ejecuta la funcion la cual contiene dentro de (context) la
    # respueta obtenia por el 'envío una solicitud GET a "/products"'
    context.response = requests.get(f"{API_URL}/products") #luego creamos una variable context.response lo cual
    # indica que es igual a la peticion HTTP que hace el request.get pasandole como parametro la url y / products

@then('el código de estado de la respuesta debe ser 200') #el then se refiere a entonces lo que va a pasar,
# por lo cual debemos recibir 'el código de estado de la respuesta debe ser 200' el cual viene de la peticion
# request.get
def verificar_codigo_estado_200(context): # aqui se ejecuta la funcion verificar_codigo_estado_200 la cual guarda la
    # informacion obtenida en 'el código de estado de la respuesta debe ser 200' dentro de (context)
    assert context.response.status_code == 200 # aqui enviamos un assert el cual da el ok si se cumple la condicion
    # la cual es que context.response que contiene la respuesta enviada por requests.get(f"{API_URL}/products") se le
    # pasa el atributo status_code el cual obtiene el status de la peticion y debe ser igual a 200 para que el assert
    # de ok

@then('la respuesta debe contener una lista de productos') # entonces aqui el then busca la coincidencia de 'la
# respuesta debe contener una lista de productos' la cual debe ser igual al del gherkin
def verificar_lista_productos(context): # aqui se ejecuta la funcion verificar_lista_productos la cual guarda la
    # informacion obtenida de el then en (context)
    assert isinstance(context.response.json(), list) # aqui el ISINSTANCE nos verifica que el objeto sea una lista,
    # y el context.response.json(),list, nos convierte el resultado en una lista

# Obtener un producto por ID
@when('envío una solicitud GET a "/products/{id}"') # cuando se envie la solicitud debemos el when debe buscar envío
# una solicitud GET a "/products/{id}"
def enviar_solicitud_get_producto_por_id(context, id): # aqui se ejecuta la funcion
    # enviar_solicitud_get_producto_por_id la cual obtiene el resultado de envío una solicitud GET a "/products/{id}"
    # y lo guarda dentro de context, y id
    context.response = requests.get(f"{API_URL}/products/{id}") # luego creamos una variable llamada context.response
    # la cual va a ser igual a la peticion que se envia con request.get donde se le pasa el API_URL/products/{id}

@then('la respuesta debe contener el producto con ID {id}') # aqui debemos recibir el resultado esperado el cual debe
# ser 'la respuesta debe contener el producto con ID {id}'
def verificar_producto_por_id(context, id):# al recibir la respuesta anterior se ejecuta la funcion
    # verificar_producto_por_id la cual guarda la informacion obtenida en el then dentro del context , id
    product = context.response.json() # aqui creamos una variable llamada product = donde se va a guardar el
    # resultado de context.response.json() el cual debe convertir la respuesta obtenida en por el then en formato json
    assert product['id'] == int(id) # aqui accedemos desde procuct['id'] a la propiedad id y se indica que debe ser
    # igual a el id que ya fue previamente guardado en (context,id)

# Crear un nuevo producto
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

@then('la respuesta debe contener el nuevo producto con ID {id}')
def verificar_nuevo_producto(context, id):
    product = context.response.json()
    assert product['id'] == int(id)

# Crear un producto con datos inválidos
@when('envío una solicitud POST a "/products" con datos inválidos')
def enviar_solicitud_post_producto_datos_invalidos(context):
    for row in context.table:
        product_data = {
            "id": int(row['id']),
            "name": row['name'],
            "price": float(row['price']),
            "stock": int(row['stock'])
        }
    context.response = requests.post(f"{API_URL}/products", json=product_data)

@then('el código de estado de la respuesta debe ser 422')
def verificar_codigo_estado_422(context):
    assert context.response.status_code == 422

@then('la respuesta debe contener un mensaje de error')
def verificar_mensaje_error(context):
    assert 'detail' in context.response.json()

# Crear un producto con ID duplicado
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

@then('el código de estado de la respuesta debe ser 400')
def verificar_codigo_estado_400(context):
    assert context.response.status_code == 400

@then('la respuesta debe contener un mensaje de error "Product with this ID already exists"')
def verificar_mensaje_error_id_duplicado(context):
    assert context.response.json()['detail'] == "Product with this ID already exists"

# Actualizar un producto existente
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

@then('la respuesta debe contener el producto actualizado con ID {id}')
def verificar_producto_actualizado(context, id):
    product = context.response.json()
    assert product['id'] == int(id)

# Actualizar un producto con datos inválidos
@when('envío una solicitud PUT a "/products/{id}" con datos inválidos')
def enviar_solicitud_put_producto_datos_invalidos(context, id):
    for row in context.table:
        product_data = {
            "name": row['name'],
            "price": float(row['price']),
            "stock": int(row['stock'])
        }
    context.response = requests.put(f"{API_URL}/products/{id}", json=product_data)

@then('el código del estado de la respuesta debe ser 422')
def verificar_codigo_estado_422_actualizacion(context):
    assert context.response.status_code == 422

@then('la respuesta debe contener un mensaje del error')
def verificar_mensaje_error_actualizacion(context):
    assert 'detail' in context.response.json()

# Eliminar un producto existente
@when('envío una solicitud DELETE a "/products/{id}"')
def enviar_solicitud_delete_producto(context, id):
    context.response = requests.delete(f"{API_URL}/products/{id}")

@then('el código de estado de la respuesta debe ser igual a 200')
def verificar_codigo_estado_200_eliminacion(context):
    assert context.response.status_code == 200

# Eliminar un producto sin ID
@when('envío una solicitud DELETE a "/products"')
def enviar_solicitud_delete_producto_sin_id(context):
    context.response = requests.delete(f"{API_URL}/products")

@then('el código de estado de la respuesta debe ser 405')
def verificar_codigo_estado_405(context):
    assert context.response.status_code == 405

@then('la respuesta debe contener un mensaje de error "Method Not Allowed"')
def verificar_mensaje_error_metodo_no_permitido(context):
    assert context.response.json()['detail'] == "Method Not Allowed"
