# DaDaDump

![alt text](https://i.imgur.com/610nA6U.png)

* DaDaDump es un software de tipo OSINT que permite recabar contraseñas usando un usuario o una contraseña como input.
* Los datos de DaDaDump son recabados de breachdirectory.org y ihavebeenpwned.org, utilizando tecnicas de WebScraping con Selenium y Captcha V3 Bypass
* Este proyecto es for-fun, de fin de semana, pero puede resultar una herramienta bastante util a la hora de realizar pruebas de intrusión en sistemas.

## Instalación

* Para instalar DaDaDump debes de descargar Python 3.8 que puedes consultar aquí -> https://www.python.org/downloads/release/python-380/.
* Posteriormente, clona el repositorio e instala las dependencias del archivo requirements.txt
```bash
  pip install -r requirements.txt
  python run.py
```
    
## Demo

* Para usar el software, ejecute el script run.py
```
python run.py
```

* Posteriormente, el software preguntara por un usuario/correo electrónico


```
    ____        ____        ____
   / __ \____ _/ __ \____ _/ __ \__  ______ ___  ____
  / / / / __ `/ / / / __ `/ / / / / / / __ `__ \/ __ \
 / /_/ / /_/ / /_/ / /_/ / /_/ / /_/ / / / / / / /_/ /
/_____/\__,_/_____/\__,_/_____/\__,_/_/ /_/ /_/ .___/
                                             /_/


[!] + Aviso: Esta herramienta es solo para fines educativos, no me hago responsable del mal uso que se le pueda dar o de los daños que se puedan causar con ella
[!] + En caso de que no funcione, es posible que el sitio web haya cambiado su estructura, en ese caso, por favor, reportalo en el repositorio de github
[!] + Para cualquier duda o sugerencia, puedes contactarme en twitter: @miguelalvrzz02

[!] + Creado por: @malvads

[!] - Introduce el email o el nombre de usuario:

```

* Usted deberá de introducir el correo electrónico / usuario objetivo.
* El software, en caso de que el dato sea un correo electrónico, preguntara si quieres verificar la existencia de breaches en ihavebeenpwned.

```
[!] - Introduce el email o el nombre de usuario: hola@mundo.com
[?] - ¿Quieres verificar si el correo electronico tiene un leak de datos? (s=si, n=no): s
````

* En caso de pulsar s, el software verificará la existencia de breaches en ihavebeenpwned, en caso de existir, continua la ejecución.
* En caso de pulsar n, el software directamente consultará en breachdirectory.org
* Siguiendo con la ejecución, posterior al paso anterior, se devolverán los datos consultados:

```
[!] hola@mundo.com parece lekeado, buscaremos datos....
[!] - Obtenido el Token de ReCaptcha v2 -> 03AII...EmfQg
[!] - Obteniendo datos de breachdirectory.org...
[!] - Parseando datos...
[!] - Se han encontrado 3 datos de hola@mundo.com
[?] - ¿Quieres tratar de obtener las contraseñas de los hashes? (s=si, n=no):
```
* Si en la opción *¿Quieres tratar de obtener las contraseñas de los hashes?* pulsas s, consultará con providers on-line para dehashear los hashes sha1 y devolver la contraseña.
* En caso contrario se devuelve la tabla completa.

```
[?] - ¿Quieres tratar de obtener las contraseñas de los hashes? (s=si, n=no): s
[!] - Tratando de dehashear 19819d38c92e90a7c48f102e5ebda7a7a7f10b23 utilizando un servicio online...
[+] + Buscando en md5decrypt.net...
[!] + Hash no encontrado
[!] - Tratando de dehashear 239f662d924668c1427ccf634c57b8b71c124c12 utilizando un servicio online...
[+] + Buscando en md5decrypt.net...
[!] + Hash no encontrado
[!] - Tratando de dehashear bccdcb8b25c6422c7a65bb205e3e4acc2fe2eb34 utilizando un servicio online...
[+] + Buscando en md5decrypt.net...
[!] + Hash desencriptado: computador

+------------+------------------------------------------+-----------------------------------------------------+-----------------+
| password   | sha1                                     | sha1_dehash_result                                  | sha1_dehashed   |
|------------+------------------------------------------+-----------------------------------------------------+-----------------|
| i3ol**     | 19819d38c92e90a7c48f102e5ebda7a7a7f10b23 | 19819d38c92e90a7c48f102e5ebda7a7a7f10b23            | false           |
| mxcf****   | 239f662d924668c1427ccf634c57b8b71c124c12 | 239f662d924668c1427ccf634c57b8b71c124c12            | false           |
| comp****** | bccdcb8b25c6422c7a65bb205e3e4acc2fe2eb34 | bccdcb8b25c6422c7a65bb205e3e4acc2fe2eb34:computador | true            |
+------------+------------------------------------------+-----------------------------------------------------+-----------------+

```
## MD5_DECRYPT_API

 - El software utiliza actualmente 2 providers para realizar los dehashing en linea, uno concretamente es https://md5decrypt.net/
 * Puedes solicitar una API key de manera gratuita en https://md5decrypt.net/ y editar los archivos de configuración.

 ```
 /Config/config.ini
 ```

 ```
 [HASH]
MD5_DECRYPT_EMAIL=EMAIL_HERE
MD5_DECRYPT_PASSWORD=KEY_HERE
[SOFTWARE]
MAX_TRIES=5
 ```


## Software Build and Unit Testing

* Para correr los tests del software, debe ejecutar lo siguiente:
```
python test/test_breaker.py
```
* Todos los cambios de este software llegan a la rama master posteriormente de su respectivo build usando Travis en una máquina virtual
```
jobs:
  include:
    - name: "Python 3.8.0 on Windows"
      os: windows    
      language: shell
      before_install:
        - choco install python --version 3.8.0
        - python -m pip install --upgrade pip

      env: PATH=/c/Python38:/c/Python38/Scripts:$PATH
install: pip install -r requirements.txt
script: python test/test_breaker.py
```
## Advertencia

- Esta herramienta es solo para fines educativos, no me hago responsable del mal uso que se le pueda dar o de los daños que se puedan causar con ella.
- En caso de que no funcione, es posible que el sitio web haya cambiado su estructura, en ese caso, por favor, reportalo en el repositorio de github
- Este software fue desarrollado con fines de aprendizaje/educativos, Miguel Álvarez (@malvads) no se hace responsable en ningún momento del mal uso que se le pueda dar al mismo.
- Para cualquier duda o sugerencia, puedes contactarme en twitter: @miguelalvrzz02
## Dudas/Contribuir

- En caso de querer contribuir, clona el repositorio y realiza tu propia versión del software, será revisa si usas una pull request.
- En caso de dudas, utilizar el apartado "issues".

## Agradecimientos

- https://haveibeenpwned.com/
- https://breachdirectory.org
- https://md5decrypt.net/
- https://hashes.com/
## License

[MIT](https://choosealicense.com/licenses/mit/)

