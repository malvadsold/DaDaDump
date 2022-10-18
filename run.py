import sys
sys.path.append('./src')
import Breaker
import pyfiglet

#comprobamos si se llama al script desde la terminal
if __name__ == '__main__':
    #texto de bienvenida
    result = pyfiglet.figlet_format("DaDaDump", font = "slant" )
    print(result)
    #Mostramos mensaje de advertencia
    def warning():
        print('\033[93m')
        print("[!] + Aviso: Esta herramienta es solo para fines educativos, no me hago responsable del mal uso que se le pueda dar o de los daños que se puedan causar con ella")
        print("[!] + En caso de que no funcione, es posible que el sitio web haya cambiado su estructura, en ese caso, por favor, reportalo en el repositorio de github")
        print("[!] + Para cualquier duda o sugerencia, puedes contactarme en twitter: @miguelalvrzz02")
        print('\033[0m')
        print("[!] + Creado por: " + '\033[92m' + "@malvads" + '\033[0m')
        print("")

    #Llamamos a la función de advertencia
    warning()
    #Llamamos al script
    input_pattern = input('[!] - Introduce el email o el nombre de usuario: ')
    if input_pattern != '':
        Breaker.Fetcher(input_pattern)
    else:
        print('\033[91m' + '[!] - No has introducido nada, saliendo...' + '\033[0m')
        exit()