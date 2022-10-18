# [!] - Script que automatiza el proceso de busqueda de datos de una persona en la web proveniente de leaks de datos
# Esta herramienta es solo para fines educativos, no me hago responsable del mal uso que se le pueda dar o de los daños que se puedan causar con ella
# Creado por: @malvads

import warnings
from xml.etree.ElementInclude import include
warnings.simplefilter('ignore')
from pypasser import reCaptchaV3
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from tabulate import tabulate
import time, requests
import os
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

#Esta clase se encarga de manejar la configuracion del software
class ConfigReader:
    def __init__(self):
        self.MAX_TRIES = 5 # Numero maximo de intentos por defecto
        self.MD5_DECRYPT_EMAIL = "" # Email para desencriptar MD5 por defecto
        self.MD5_DECRYPT_PASSWORD = "" # API Key por defecto
        self.read_config()
    def read_config(self):
        import configparser
        config = configparser.ConfigParser()
        print("[*] - Leyendo archivo de configuracion")
        import os
        print("[*] - Directorio actual: " + os.getcwd())
        import os.path        
        CURRENT_PATH_CONFIG = os.path.join(CURRENT_PATH, "../../Config/config.ini")
        print(CURRENT_PATH_CONFIG)
        config_path = os.path.join(os.getcwd(), CURRENT_PATH_CONFIG)
        config.read(config_path)
        self.MAX_TRIES = config['SOFTWARE']['MAX_TRIES']
        self.MD5_DECRYPT_EMAIL = config['HASH']['MD5_DECRYPT_EMAIL']
        self.MD5_DECRYPT_PASSWORD = config['HASH']['MD5_DECRYPT_PASSWORD']
        #hide MD5_DECRYPT_PASSWORD AND MD5_DECRYPT_EMAIL
        print("[!] - Configuracion cargada correctamente")
        HIDED_MD5_DECRYPT_EMAIL = self.MD5_DECRYPT_EMAIL[0] + "*" * (len(self.MD5_DECRYPT_EMAIL) - 2) + self.MD5_DECRYPT_EMAIL[-1]
        HIDED_MD5_DECRYPT_PASSWORD = self.MD5_DECRYPT_PASSWORD[0] + "*" * (len(self.MD5_DECRYPT_PASSWORD) - 2) + self.MD5_DECRYPT_PASSWORD[-1]
        print("[!] - MAX_TRIES: " + self.MAX_TRIES)
        print("[!] - MD5_DECRYPT_EMAIL: " + HIDED_MD5_DECRYPT_EMAIL)
        print("[!] - MD5_DECRYPT_PASSWORD: " + HIDED_MD5_DECRYPT_PASSWORD)

SOFTWARE_CONFIG = ConfigReader()

#clase que maneja la busqueda de hashes desencriptados en la web
class Hashes:
    @staticmethod
    def decrypt_using_md5decrypt(hash):
        print("[+] + Buscando en md5decrypt.net...")
        try:
            url = "https://md5decrypt.net/en/Api/api.php?hash=" + hash + "&hash_type=sha1&email=" + SOFTWARE_CONFIG.MD5_DECRYPT_EMAIL + "&code=" + SOFTWARE_CONFIG.MD5_DECRYPT_PASSWORD + "&decode=Decrypt"
            r = requests.get(url)
            if r.status_code == 200:
                if r.text == "":
                    print("[!] + Hash no encontrado")
                    return hash
                else:
                    print("[!] + Hash desencriptado: " + r.text)
                    return hash + ':' + r.text
            else:
                print("[!] + Error al buscar en md5decrypt.net")
            return hash
        except:
            print("[!] + Error al buscar en md5decrypt.net")
            return hash
    #obtenemos el csrf token de la web para poder hacer la peticion
    @staticmethod
    def get_csrf_token():
        url = 'https://hashes.com/en/decrypt/hash'
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        token = soup.find('input', {'name': 'csrf_token'}).get('value')
        return token
    #consultamos la web con el hash y el csrf token para obtener el resultado
    @staticmethod
    def dehash(hash, do_decrypt):
        if do_decrypt == 's':
            try:
                url = 'https://hashes.com/en/decrypt/hash'
                data = {}
                data['hashes'] = hash
                data['csrf_token'] = Hashes.get_csrf_token()
                data['knn'] = 64
                data['submitted'] = 'true'
                cookies = {
                    'csrf_cookie': Hashes.get_csrf_token()
                }
                r = requests.post(url, data=data, cookies=cookies)
                soup = BeautifulSoup(r.text, 'html.parser')
                real_hash = hash
                hash = soup.find('pre', {'class': 'mb-0 border-success text-success'}).text
                print ("[+] + Hash desencriptado: " + hash)
                return hash
            except:
                return Hashes.decrypt_using_md5decrypt(hash)
        else:
            print('[!] Retornando hash original: ' + hash)
            return hash

#Clase que verifica si un correo electronico tiene un leak de datos en internet
class CheckPwned:
    @staticmethod
    def check_pwned(email):
        options = webdriver.ChromeOptions()
        options.add_argument('log-level=3')
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        browser.get('https://haveibeenpwned.com/unifiedsearch/' + email)
        time.sleep(5)
        html_response = browser.page_source
        body = BeautifulSoup(html_response, 'html.parser').body
        #check if body can be parsed into json
        try:
            import json
            json.loads(body.text)
            return True
        except:
            return False

#Esta clase maneja la busqueda de datos en la web
class Fetcher:
    #Inicializamos la clase con el patron de busqueda
    def __init__(self, pattern, under_unit_test=False):
        self.source = 'https://breachdirectory.org/usersearch.php?term='
        self.google_anchor_url = 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6LcdcfIUAAAAACF6YXBGfZeWvtOz3BbZB667xkj8&co=aHR0cHM6Ly9icmVhY2hkaXJlY3Rvcnkub3JnOjQ0Mw..&hl=es&v=vP4jQKq0YJFzU6e21-BGy3GP&size=invisible&cb=jtbjuddi4p5c'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://breachdirectory.org',
            'Connection': 'keep-alive',
            'Referer': 'https://breachdirectory.org/'
        }
        self.response = None
        self.google_token = None
        self.pattern = pattern
        self.max_tries = int(SOFTWARE_CONFIG.MAX_TRIES)
        self.current_tries = 0
        self.already_dumped_on_console = False
        if not under_unit_test:
            self.check_pwned()
    def check_tries(self):
        if self.current_tries >= self.max_tries:
            print('[!] - Error, maximos intentos alcanzados')
            exit()
        else :
            self.current_tries += 1
    def check_pwned(self):
        self.check_email = input("[?] - ¿Quieres verificar si el correo electronico tiene un leak de datos? (s=si, n=no): ")
        if self.check_email == 's':
            self.check_email = True
            self.request_token()
        elif self.check_email == 'n':
            self.check_email = False
            self.request_token()
        else:
            print("[!] - Opcion no valida")
            self.check_pwned()
    def request_token(self):
        #Verificamos si es un correo electronico o no
        if self.pattern.find('@') != -1 and self.check_email:
            if CheckPwned.check_pwned(self.pattern):
                print('\033[92m' + '[!] ' + self.pattern + ' parece lekeado, buscaremos datos....' + '\033[0m')
                #Obtenemos el token de google para poder hacer la peticion a breachdirectory.org
                self.google_token = reCaptchaV3(self.google_anchor_url)
                print_token = self.google_token[:5] + '...' + self.google_token[-5:]
                print ('[!] - Obtenido el Token de ReCaptcha v2 -> ' + print_token)
                self.request()
            else:
                #En caso de que no este en ningun leak de datos, se muestra un mensaje de que no se encontro nada
                print('\033[91m' + '[!] ' +  self.pattern + ' no parece estar lekeado, saliendo...' + '\033[0m')
                exit()
        #Si no es un correo electronico, se obtiene el token de google para poder hacer la peticion a breachdirectory.org
        #Debido a que un dato que no sea un correo electronico puede estar en la base de datos de breachdirectory.org
        else:
            #Obtenemos el token de google para poder hacer la peticion a breachdirectory.org
            self.google_token = reCaptchaV3(self.google_anchor_url)
            print_token = self.google_token[:5] + '...' + self.google_token[-5:]
            print ('[!] - Obtenido el Token de ReCaptcha v3 -> ' + print_token)
            self.request()
    def request(self):
        #Hacemos la peticion a la web con el token de google y el dato a buscar para obtener los resultados de breachdirectory.org
        print('[!] - Obteniendo datos de breachdirectory.org...')
        self.response = requests.get(self.source + self.pattern + '&response=' + self.google_token)
        self.parse_bs4()
    #Parseamos la respuesta de la web para obtener los datos
    def parse_bs4(self):
        if self.already_dumped_on_console:
            exit()
        print('[!] - Parseando datos...')
        self.check_tries()
        #Intentamos parsear la respuesta de la web
        try:
            soup = BeautifulSoup(self.response.text, 'html.parser')
            parsed = {}
            parsed['data'] = []
            #Obtenemos los datos de la tabla
            for row in soup.find('table', {'id': 'passwords'}).find('tbody').find_all('tr'):
                #Agregamos los datos a un diccionario
                parsed['data'].append({
                    'password': row.find_all('td')[0].text,
                    'sha1': row.find_all('td')[1].text
                })
            print('[!] - Se han encontrado ' + str(len(parsed['data'])) + ' datos de ' + self.pattern)
            #Si la longitud del diccionario es mayor a 0, significa que se encontraron datos, intentamos obtener el hash de la contraseña
            if len(parsed['data']) > 0:
                do_hash = input("[?] - ¿Quieres tratar de obtener las contraseñas de los hashes? (s=si, n=no): ")
                for item in parsed['data']:
                    yellow_colored_hash = '\033[93m' + item['sha1'] + '\033[0m'
                    if do_hash == 's':
                        print ('[!] - Tratando de dehashear ' + yellow_colored_hash + ' utilizando un servicio online...')
                    #Obtenemos el hash de la contraseña
                    dehashed = Hashes.dehash(item['sha1'], do_hash)
                    item['sha1_dehash_result'] = dehashed
                    true_json = 'true'
                    false_json = 'false'
                    #Si el hash de la contraseña es igual a true, significa que se encontro la contraseña
                    item['sha1_dehashed'] = true_json if dehashed != item['sha1'] else false_json

                #Recorremos el diccionario para que los datos se vean de una manera mas ordenada y estetica
                for item in parsed['data']:
                    if item['sha1_dehashed'] == 'true':
                        item['sha1_dehashed'] = '\033[92m' + item['sha1_dehashed'] + '\033[0m'
                    else:
                        item['sha1_dehashed'] = '\033[91m' + item['sha1_dehashed'] + '\033[0m'
                #Generamos la tabla con los datos obtenidos
                print('')
                print(tabulate(parsed['data'], headers='keys', tablefmt='psql'))
                self.already_dumped_on_console = True
                exit()
            #En caso de que no se encuentren datos, se muestra un mensaje de que no se encontro nada y reiniciamos el script
            #Esto debido a que en ocasinones, la web no muestra los datos y se debe reiniciar el script para que funcione correctamente
            else:
                if self.already_dumped_on_console:
                    exit()
                print('\033[91m' + '[!] - No se encontraron datos, reiniciando...' + '\033[0m')
                self.request_token()
        #En caso de error, se muestra un mensaje de error y se reinicia el script
        except:
            if self.already_dumped_on_console:
                exit()
            print ('[!] - Error mientras se parseaba la respuesta de la web, reiniciando...')
            self.request_token()
