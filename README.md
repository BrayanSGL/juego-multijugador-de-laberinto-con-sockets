#Código Servidor

Este código crea un servidor de sockets que escucha conexiones en un puerto específico y, cuando se conecta un cliente, crea un hilo para atender a ese cliente. Cuando el cliente envía datos, el servidor los recibe, los decodifica y los envía de vuelta al cliente.

La lógica del servidor se encuentra en la función threaded_client, que se llama cada vez que se conecta un cliente. Esta función se encarga de enviar al cliente la configuración inicial del juego, y luego se queda en un bucle infinito esperando datos del cliente, procesándolos y enviándolos de vuelta.


