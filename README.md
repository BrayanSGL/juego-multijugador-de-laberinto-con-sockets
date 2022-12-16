# Mi proyecto 

Este proyecto es una aplicación básica de un modelo cliente servidor con sockets TCP. El video juego es un laberinto en el cual todos los clientes inician a la vez tras el aviso de uno de ellos. Al iniciar la partida el mapa es totalmente negro, pues el ideal es ir descucriendo el mapa. La aparición del jugador es aleatoria. Y para descubrir el mapa basta con tener en cuenta el sistema de movimiento.

- Dirección: a,s,d,w o las flechas del teclado
- Movimiento: Barra espaciadora

Tras encontrar el cofre, el cliente termina el juego y se declara ganador.

## Instalación

1. Descargar el código
2. Verificar la tener python funcionado en la computadora
3. instalar requerimientos: `$ pip install -r requirements.txt`

## Uso
> Asegurarse de estar en los directorios correctos.

1. Ejecutar el servidor desde una terminal `py server.py`
2. Verificar la IP, en la que está corriendo el servidor tras ejecutarlo (**Aparece automáticamente en la terminal**)
3. Colocar la IP del servidor en la clase Network del cliente. (**IMPORTANTE**)
4. Ejecutar `py run.py` (Se recomienda desde VScode)


## Licencia
Este proyecto está licenciado bajo la licencia MIT. 