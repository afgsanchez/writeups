## Los 40 Ladrones
### Plataforma: Dockerlabs
### Nivel: Fácil
### url: https://dockerlabs.es/

#### Reconocimiento

Imagen 1 y 2:

Comienza con una exploración inicial utilizando nmap para identificar los servicios y puertos abiertos.

Resultado: Se identifican un servicio HTTP.

![image](https://github.com/afgsanchez/writeups/assets/167230621/9975f066-b55c-4901-b16f-8ca1cd566959)
![image](https://github.com/afgsanchez/writeups/assets/167230621/2a79ba9a-2bf1-4d3f-a5ed-fbe45d3b2fa8)

#### Enumeración de HTTP

Imagen 3 y 4:

Se utiliza dirbuster para buscar directorios ocultos en el servidor web.

Resultado: Se encuentra un archivo interesante: qdefense.txt.
![image](https://github.com/afgsanchez/writeups/assets/167230621/28986bbe-56ef-46d1-bc94-f337ceb76b5f)
![image](https://github.com/afgsanchez/writeups/assets/167230621/402b1f05-4680-4dc7-b7d9-653ae5a2c5ec)

### Explotación

Imagen 5:

Se utiliza knockd usando la secuencia hallada en el archivo oculto en el servidor web.

![image](https://github.com/afgsanchez/writeups/assets/167230621/44ff8bb9-ad0e-4ef0-886a-49e50cb66b36)

#### Reconocimiento

Imagen 6:

Re-Exploración utilizando nmap para identificar si los servicios y puertos han cambiado.

Resultado: Se identifican un nuevo servicio SSH.

![image](https://github.com/afgsanchez/writeups/assets/167230621/af45fde2-f24f-44f8-9f04-56bd29c69c86)

#### Explotación

Imagen 7:

Utilizando hydra para tratar de descubrir el password del usuario "toctoc" dado como dato filtrado en el archivo qtdefense.txt.

Resultado: Se identifican una contraseña válida para el servicio SSH.

![image](https://github.com/afgsanchez/writeups/assets/167230621/36e27929-206c-4c2f-9f81-3017ec0e786e)

#### Explotación

Imagen 8:

Iniciamos sesion en el servicio SSH usando las credenciales conseguidas.
![image](https://github.com/afgsanchez/writeups/assets/167230621/9399c744-f55c-4cf9-8eee-dbd741be5463)

#### Escalada de privilegios

Imagen 9 y 10:

Intentamos el comando sudo -l y verificamos que podemos ejecutar como sudo y sin usar password el comando /opt/bash. Lo que nos lleva a conseguir la escalada de privilegios al usuario root.

![image](https://github.com/afgsanchez/writeups/assets/167230621/4e63aee1-7788-4f97-853b-e25d511aca57)

![image](https://github.com/afgsanchez/writeups/assets/167230621/8534e8ec-9fa1-4e45-92e1-01c3bd9eb5bd)

#### Pwned!!

