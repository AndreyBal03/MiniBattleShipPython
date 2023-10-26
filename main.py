import time #Esto se usara para generar pausas
import os #Esto nos permitira conocer el sistema operativo de los usuarios
import socket #Indispensable para la conexion online

"""Aqui habra algunas variables mayormente colores que es más facil
Escribir de una vez para evitar repeticiones"""

red = "\033[1;31m"
blue = "\033[1;34m"
green = "\033[1;32m"
white =  "\033[0;m"
#Esta mini seccion genera un diccionario para pasar las coordenadas
# de letras a numeros y poder trabajar con ellas
dicc_coords = {}
for i,j in enumerate("ABCDEFGHIJ"):
    dicc_coords[j] = i

def coords_to_index(coord):
    """Esta utilidad cambiara las coordenadas de 'A2' a
    indices de matriz: [0,2]"""
    if len(coord) < 2:
        return -1

    try:
        coord = coord.upper()
        return (dicc_coords[coord[0]], int(coord[1]))
    except (ValueError, KeyError):
        return -1

class Tablero(): #Esta clase facilita trabajar con 2 tableros
    def __init__(self): 
        self.tabla = [
                [0,0,0,0,0,0,0,0,0,0], #Esto crea una matriz de 10x10 llena de ceros
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0], 
                [0,0,0,0,0,0,0,0,0,0], 
                [0,0,0,0,0,0,0,0,0,0], 
                [0,0,0,0,0,0,0,0,0,0], 
                ]

        """Aqui los barcos seran a forma de diccionario
        por las propiedades de ids con las que cuentan"""
        
        self.boat = {"casillas" : [1,1]} #Size = 2
        self.destroyer = {"casillas" : [1,1,1]}   #Size = 3
        self.crusier = {"casillas" : [1,1,1,1]}  #Size = 4
        self.battleship = {"casillas" : [1,1,1,1,1]}  #Size = 5
        self.aircraft = {"casillas" : [1,1,1,1,1,1]}  #Size = 6



    def start_ships(self):
        """Esta funcion generara los barcos iniciales
        en el caso de que el tablero sea tuyo y no del
        enemigo"""
        size = 2

        while size < 7:
            clear()
            self.show()

            print_cool("""
            Para colocar los barcos debes escribir la posicion, tomando en cuenta
            que el barco crecera hacia abajo o a la derecha.
            Las unicas reglas que deberas tomar en cuenta es que debe de haber al menos
            un cuadro de separación entre cada barco.""",
                       slow_rate = .005,
                       color = green)

            print_cool(f"Tamaño de barco : {size}",color =red)

            coord = input("Introduce las coordenadas del barco, EJEMP: A6\n: ")
            coord = coords_to_index(coord)
            axis = input("Introduce\n0.Para barco horizontal\n1.Para barco vertical\n: ")
            if len(axis) < 1:
                continue

            if axis not in ["0", "1"]:
                continue
            axis = int(axis)

            if coord == -1:
                print_cool("Coordenadas invalidas :(", color = red, slow_rate = .05)
                continue


            """Seccion para validar que el barco sea posible de colocar"""
            valid = 1 #Todos los barcos inician siendo validos  
            #Horizontal
            if axis == 0 and len(self.tabla[0]) < coord[1] + size:
                continue

            if axis == 1 and len(self.tabla[1]) < coord[0] + size:
                continue
            
            if axis == 0:
                for i in range(size):
                    if self.tabla[coord[0]][coord[1] + i] != 0: 
                        valid = -1
                        break

            if axis == 1:
                for i in range(size):
                    if self.tabla[coord[0] + i][coord[1]] !=0 :
                        valid = -1
                        break
            
            if valid == -1:
                print_cool("Barco invalido :(", color = red, slow_rate = .05)
                continue
            
            match size:
                case 2:
                    barco = self.boat["casillas"]
                case 3:
                    barco = self.destroyer["casillas"]
                case 4:
                    barco = self.crusier["casillas"]
                case 5:
                    barco = self.battleship["casillas"]
                case 6:
                    barco = self.aircraft["casillas"]


            if axis == 0:
                """Primero se bloquean las casillas vecinas colocando
                un indice diferente a 0 o 1, en este caso 4"""
                for y_ in [-1,0,1]:
                    if coord[0]+y_ >= 0 and coord[0]+y_ < len(self.tabla):
                        for x_ in range(-1, size + 1):
                            if coord[1]+x_ >= 0 and coord[1]+x_ < len(self.tabla[0]):
                                self.tabla[coord[0] + y_][coord[1] + x_] = 4
                                
                for i in range(size):
                    #Se hace asi con diccionarios para poder saber cuando un
                    #barco completo se elimina
                    self.tabla[coord[0]][coord[1] + i] = barco[i]

                    #print(barco[i])
                    #time.sleep(1)
                    pass

            if axis == 1:
                """Aqui se invierte los y_ con x_ por el cambio de axis"""
                for x_ in [-1, 0, 1]:
                    if coord[1] + x_ >= 0 and coord[1] + x_ < len(self.tabla[0]):
                        for y_ in range(-1, size+1):
                            if coord[0] + y_ >= 0 and coord[0] + y_ < len(self.tabla):
                                self.tabla[coord[0]+ y_][coord[1] + x_] = 4

                for i in range(size):
                    self.tabla[coord[0]+i][coord[1]] = barco[i]

            size+=1
            
        clear()    



    def mark(self, case, indx):
        self.tabla[indx[0]][indx[1]] = case

    def show(self): 
        """Esta funcion permite mostrar el tablero en cualquier momento"""
        print("   ", end="")
        for nums in dicc_coords.values():
            print(f"| {green}{nums} ", end=white)
        print()
        
        letters = list(dicc_coords.keys())
        letter = 0 #Esto solo es el indice para poder imprimir las letras despues
        for row in self.tabla:
            #Para cada linea de la tabla se imprimira:
            print(" -"*22) 
            print(f" {green}{letters[letter]} ", end=white) #Esto imprime la letra
            letter+=1
            
            for column in row:
                
                #Posibles iconos dentro del tablero
                match column:
                    case 0: #No hay nada
                        icon = ' '
                    case 1: #Hay un barco
                        icon = blue +'o'+ white
                    case 2: #Tiro fallido
                        icon = 'x'
                    case 3: #Golpe acertado
                        icon = red + 'x' + white
                    case 4: #Bloqueo de casillas no disponibles
                        #Descomentar la siguiente 
                        #icon = green + "-" + white 
                        icon = ' '
                    case _:
                        #Por defecto se deja en blanco
                        icon = ' '
                
                print(f"| {icon} ", end="")
            
            print("|")
        print(" -"*22)




        

def show_load(time_):
    """Funcion para fines esteticos,
    muestra una barra de carga

    La variable time_ dicta el tiempo de la carga en segundos"""

    lap = time_/100

    for i in range(101):
        print("["+"#"*i+"."*(100-i)+"]", end="\r")
        time.sleep(lap)
    print()

def clear():
    """Esta funcion permitira limpiar la pantalla
    sin importar el dispositivo"""
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def print_cool(string, slow_rate = .01, color = ""):
    """Esta funcion tiene un proposito estetico para
    visualizar mejor los prints"""

    print(color,end="") #Esto cambia el color de los strings
    for chars in string:
        print(chars, end="",flush=True)
        time.sleep(slow_rate)

    print(white) #Esto regresa el color original del print

def show_help():
    """Esta funcion sera la encargada del menu de apoyo al 
    usuario"""

    clear() 

    print_cool("""    
    Bienvenido a Sea BattleShip, a continuacion se te
    presentara un menu en el que puedes escoger que parte
    del juego necesitas apoyo.
              
    Pulsa enter para continuar...""",slow_rate = .02, color = green)
    option = input("")

    clear()

    print_cool("""Escribe el numero de tu opción:
    1. Inicio rapido
    2. Multijugador
    3. Salir al menu""", color = green)

    option = input(": ")
    match option:
        case "1":
            print_cool("""
                  Inicio rapido:
                  Los jugadores dispondran de 5 barcos con distintos tamaños,
                  cada barco tendra un determinado numero de casillas ocupadas
                  segun su tamaño, el objetivo principal del juego es hundir los barcos
                  del contrincante, para ello cada jugador podra lanzar un projectil
                  por turno.
                  El primero en derribar todas las naves/barcos del contrincante
                  es el ganador.

                  Projectiles--
                  Para enviar un projectil solo se necesitara esperar a su turno y
                  posteriormente escribir las coordenadas del lugar a donde se quiere
                  disparar.
                  Si el disparo no dio a nada, la casilla sera rellenada con una cruz
                  blanca, en caso de atinar al golpe, la casilla sera rellenada por una
                  cruz roja con relleno

                  Barcos--
                  Colocar barcos es el paso inicial, para el, se mostrara en pantalla
                  un tablero que se ira actualizarlo segun se vayan añadiendo los
                  barcos. El paso inicial es definir las coordenadas de las que va a
                  partir nuetro barco, el barco siempre va a partir de el lado
                  más proximo hacia la esquina superior izquierda, y va a
                  extenderse ya sea a la derecha o hacia abajo, segun seleccionemos
                  posteriormente.
                  Todos los barcos tendran minimo un espacio de separación entre si.

                  """, slow_rate = .01, color = green)
            option = input("¿Quieres conocer más?\n1. Si\nEnter para salir...\n: ")
            if option == "1":
                show_help()

        case "2":
            print_cool("""
                  Multijugador:
                  Este juego requiere de 2 personas en 2 computadoras distintas.""",
                       color = green, slow_rate = .01)
            print_cool("""
                  Ambas personas tienen que estar conectadas a la misma
                  red de wifi""", color = red, slow_rate = .01)
            print_cool("""
                  Una persona tendra que ser definida como el 'host' y otra como
                  el 'invitado', al momento de rellenar los tableros, se mostrara
                  la opcion de ser uno de estos 2.

                  Host--
                  En caso de seleccionar la opcion de host se te mostraran tu
                  dirección IP y el puerto al cual el invitado debe conectarse.

                  Invitado--
                  Si seleccionaste la opcion de invitado, a continuacion se te
                  pedira la direccion IP y el puerto del host con el que quieres
                  jugar.""",color = green, slow_rate = .01)
            print_cool("""
                  Por defecto el host tendra el primer movimiento.
                  """, color = red, slow_rate = .01)
            option = input("¿Quieres conocer más?\n1. Si\nEnter para salir...\n: ")
            if option == "1":
                show_help()

        case "3":
            clear()
            print("Regresando al menu...")
            show_load(2)
            clear()

        case _:
            clear()
            print("Opcion no encontrada :(")
            show_load(3)
            show_help()    

def create_host():
    """Esta funcion junto con la de 'create_client' seran
    las encargadas en crear los usuarios web"""

    IP = socket.gethostbyname(socket.gethostname())
    PORT = 8000

    #Este print permitira a el otro jugador conocer la info
    #para conectarse
    print(f"""
    Datos para la conexión:
    IP = {IP}
    PORT = {PORT}
    Esperando conexión...
    """)

    #Seccion de la creacion de la variable para la conexion
    host = socket.socket()
    host.bind((IP,PORT))
    host.listen(3)
    
    conexion, addr = host.accept()

    """Para evitar conflictos y problemas de orden el host siempre
    sera el primero en dar movimientos, en este caso retornamos
    '0' para posteriormente distinguir quien es el host y el
    invitado"""
    return (conexion, 0)


def create_client():
    """Esta sera la otra parte de la conexion web, la persona
    que use esta funcion sera la segunda en turno"""
    
    #La informacion requerida en este paso es casi la misma
    #solo que aqui el usuario necesita escribir la del host
    IP = input("Introduce la IP del host: ")

    while True:
        try:
            PORT = int(input("Introduce el puerto: "))
            break
        except ValueError:
            print_cool("PORT invalido :(", color = red)
            time.sleep(1)
            clear()
    
    client = socket.socket()
    client.connect((IP,PORT))
    """Aqui se hace algo similar que con el host, pero en este
    caso se deja el indice 1, para saber que es el segundo
    en jugar"""
    return (client, 1)

def play(conexion, turno, tablero):
    """Debido a que los metodos para el host y el cliente en
    sockets son iguales, simplemente usamos la variable conexion
    para trabajar"""

    barcos_propios = 20
    restantes = 20
    clear()
    tab_contrario = Tablero()

    res = None #Esta variable recibe las respuestas del otro jugador

    if turno != 0: #En caso de no ser el primer jugador
        print("Tu tablero: ")
        tablero.show()
        print("Tablero enemigo: ")
        tab_contrario.show()
        print(f"Casillas de barcos enemigos: {restantes}")
        print(f"Casillas de flota propia: {barcos_propios}")
        print_cool("Esperando respuesta enemiga...", color = red, slow_rate = .05)
        res = conexion.recv(64).decode("utf-8") #Aqui se recibe la respuesta
        res = coords_to_index(res) #Obtenemos nuestros indices
        
        while tablero.tabla[res[0]][res[1]] == 1:
            #En caso de golpear a un barco
            clear()
            tablero.mark(3, res)
            barcos_propios -=1
            conexion.send("3".encode("utf-8"))
            if barcos_propios == 0:
                break

            print("Tu tablero: ")
            tablero.show()
            print("Tablero enemigo: ")
            tab_contrario.show()
            print(f"Casillas de barcos enemigos: {restantes}")
            print(f"Casillas de flota propia: {barcos_propios}")
            print_cool("Esperando respuesta enemiga...", color = red, slow_rate = .05)
            res = conexion.recv(64).decode("utf-8") #Aqui se recibe la respuesta
            res = coords_to_index(res) #Obtenemos nuestros indices

        if barcos_propios == 0:
            clear()
            print_cool("Juego terminado, suerte a la proxima :(...", color = red)
            return 0

        tablero.mark(2, res)
        conexion.send("2".encode("utf-8"))

    while True:
        #Este es el bucle del juego principal
        clear() 
        print("Tu tablero: ")
        tablero.show()
        print("Tablero enemigo: ")
        tab_contrario.show()
        print(f"Casillas de barcos enemigos: {restantes}")
        print(f"Casillas de flota propia: {barcos_propios}")

        launch = input("Introduce las coordenadas del lanzamiento: ")
        if coords_to_index(launch) != -1:
            conexion.send(launch.encode("utf-8"))
        else: 
            print_cool("Coordenadas invalidas :(",color = red, slow_rate = .05)
            continue

        res = conexion.recv(64).decode("utf-8")
        while res == "3": #Mientras hayas golpeado
            tab_contrario.mark(int(res),coords_to_index(launch))
            restantes -= 1
            if restantes == 0:
                break
            clear() 
            print("Tu tablero: ")
            tablero.show()
            print("Tablero enemigo: ")
            tab_contrario.show()
            print(f"Casillas de barcos enemigos: {restantes}")
            print(f"Casillas de flota propia: {barcos_propios}")
    
            launch = input("Introduce las coordenadas del lanzamiento: ")
            if coords_to_index(launch) != -1:
                conexion.send(launch.encode("utf-8"))
            else: 
                print_cool("Coordenadas invalidas :(",color = red, slow_rate = .05)
                continue
            res = conexion.recv(64).decode("utf-8")



        if restantes == 0:
            clear()
            print_cool("Juego terminado GANASTE!!",color = green)
            break
        
        clear()
        print("Tu tablero: ")
        tablero.show()
        print("Tablero enemigo: ")
        tab_contrario.show()
        print(f"Casillas de barcos enemigos: {restantes}")
        print(f"Casillas de flota propia: {barcos_propios}")


        print_cool("Esperando respuesta enemiga...", color = red, slow_rate = .05)
        res = conexion.recv(64).decode("utf-8")
        res = coords_to_index(res)

        while tablero.tabla[res[0]][res[1]] == 1:
            #En caso de golpear a un barco 
            clear()
            tablero.mark(3, res)
            conexion.send("3".encode("utf-8"))
            barcos_propios -= 1

            if barcos_propios == 0:
                break

            print("Tu tablero: ")
            tablero.show()
            print("Tablero enemigo: ")
            tab_contrario.show()
            print(f"Casillas de barcos enemigos: {restantes}")
            print(f"Casillas de flota propia: {barcos_propios}")
            print_cool("Esperando respuesta enemiga...", color = red, slow_rate = .05)
            res = conexion.recv(64).decode("utf-8") #Aqui se recibe la respuesta
            res = coords_to_index(res) #Obtenemos nuestros indices

        if barcos_propios == 0:
            clear()
            print_cool("Juego terminado, suerte a la proxima :(...", color = red)
            break
        else:
            tablero.mark(2, res)
            conexion.send("2".encode("utf-8"))

    

    

def main():
    """Esta sera la funcion de la que partiremos y encendera todo"""

    clear() #Esto es por si el usuario tenia algo ya en pantalla

    print_cool("Bienvenido a Sea Battle Ship")

    while True:
        print_cool("Selecciona una opción")
        print_cool("""
        1. Se jugar
        2. Quiero conocer el juego""", color = blue)

        #Esto es como un elif para las opciones del usuario
        option = input("-> ")
        match option:
            case "1":
                break
            case "2":
                show_help()
            case _:
                print_cool("Opcion invalida :(", color = red)
                time.sleep(1)
                clear()

    tab = Tablero()
    tab.start_ships()
    tab.show()

    #Seccion para iniciar el Multijugador

    print_cool("""¿Seras el host o el invitado del juego?
    1. Host
    2. Invitado""", color  = green)

    while True:
        option = input("-> ")

        match option:
            case "1":
                user, turno = create_host()
                break
            case "2":
                user, turno = create_client()
                break
            case _:
                print("Opcion invalida  :(")

    play(user, turno, tab)


if __name__ == '__main__':
    main()
