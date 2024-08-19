Feature: API de Productos

  Scenario: Obtener todos los productos
    Given la API está en funcionamiento
    When envío una solicitud GET a "/products"
    Then el código de estado de la respuesta debe ser 200
    And la respuesta debe contener una lista de productos

  Scenario: Obtener un producto por ID
    Given la API está en funcionamiento
    When envío una solicitud GET a "/products/1"
    Then el código de estado de la respuesta debe ser 200
    And la respuesta debe contener el producto con ID 1

  Scenario: Crear un nuevo producto
    Given la API está en funcionamiento
    When envío una solicitud POST a "/products" con los siguientes datos
      | id | name       | price | stock |
      | 4  | Producto 4 | 51    | 11    |
    Then el código de estado de la respuesta debe ser 200
    And la respuesta debe contener el nuevo producto con ID 4

  Scenario: Crear un producto con datos inválidos
    Given la API está en funcionamiento
    When envío una solicitud POST a "/products" con datos inválidos
      | id | name | price | stock |
      | 8  |      | -10   | -5    |
    Then el código de estado de la respuesta debe ser 422
    And la respuesta debe contener un mensaje de error

  Scenario: Crear un producto con ID duplicado
    Given la API está en funcionamiento
    When envío una solicitud POST a "/products" con ID duplicado
      | id | name       | price | stock |
      | 1  | Producto 1 | 100   | 5     |
    Then el código de estado de la respuesta debe ser 400
    And la respuesta debe contener un mensaje de error "Product with this ID already exists"

  #aqui

  Scenario: Actualizar un producto existente
    Given la API está en funcionamiento
    When envío una solicitud PUT a "/products/1" con los siguientes datos
      | id | name       | price | stock |
      | 1  | Producto 1 | 150   | 20    |
    Then el código de estado de la respuesta debe ser 200
    And la respuesta debe contener el producto actualizado con ID 1

 ##
  Scenario: Actualizar un producto con datos inválidos
    Given la API está en funcionamiento
    When envío una solicitud PUT a "/products/1" con datos inválidos
      | name | price | stock |
      |      | -100  | -10   |
    Then el código del estado de la respuesta debe ser 422
    And la respuesta debe contener un mensaje del error

  Scenario: Eliminar un producto existente
    Given la API está en funcionamiento
    When envío una solicitud DELETE a "/products/2"
    Then el código de estado de la respuesta debe ser igual a 200


  Scenario: Eliminar un producto sin ID
    Given la API está en funcionamiento
    When envío una solicitud DELETE a "/products"
    Then el código de estado de la respuesta debe ser 405
    And la respuesta debe contener un mensaje de error "Method Not Allowed"
