**Sistema de recomendación de productos para comercio electrónico**

Se utilizo un modelo de recomendación basado en similitud de usuarios y productos. Implementamos este sistema en una API usando Flask, con una interfaz web sencilla para que los usuarios puedan solicitar recomendaciones.

El conjunto de datos es un archivo CSV titulado Year 2009-2010.csv, que contiene registros de transacciones, incluyendo campos como:

Customer ID: Identificación única de cada cliente.
StockCode: Código del producto.
Quantity: Cantidad comprada.
Description: Descripción del producto.
InvoiceDate: Fecha de la transacción.
UnitPrice: Precio por unidad.
Country: País del cliente.
