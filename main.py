# Importamos módulos requeridos
import os
import random

import pygame

# Estados del juego
ESTADO_INICIO = "inicio"
ESTADO_INSTRUCCIONES = "instrucciones"
ESTADO_JUGANDO = "jugando"
ESTADO_DERROTA = "derrota"
ESTADO_VICTORIA = "victoria"

# Rutas a la carpeta de imágenes de pantallas
DIR_PANTALLAS = os.path.join(os.path.dirname(__file__), "data", "pantallas")

# Se específica el nombre del archivo para cada imagen de pantalla.
# El formato de imagen utilizado puede ser PNG, JPG/JPEG, BMP, o GIF.
PANTALLA_INICIO = "menu.png"
PANTALLA_INSTRUCCIONES = "instrucciones.png"
PANTALLA_VICTORIA = "ganar.png"
PANTALLA_DERROTA = "perder.png"

# Para evitar que el jugador se mueva demasiado rápido
RETRASO = 200

# Códigos de cada elemento del tablero
VACIO = 0
OBSTACULO = 1
JUGADOR = 2
MANZANA = 3
PUERTA = 4
PUERTA_ABIERTA= 5
SEGUIDOR = 6
tipos_seguidor_tablero = {} #marca que imagen de seguidor se usa en el espacio
 

# Tamaño del tablero
# Si se cambian estas constantes, se debe modificar la definición
# del tablero que se encuentra en función reiniciar().
FILAS = 13
COLUMNAS = 14
MAX_PASOS = 60
CANTIDAD_MANZANAS = 3
ANCHO_VENTANA = 950
ALTO_VENTANA= 660
LADO_TABLERO = 660
ANCHO_PANEL = ANCHO_VENTANA - LADO_TABLERO

def celdaapixel(column, fila):
    return column * LADO_TABLERO / COLUMNAS, fila * LADO_TABLERO / FILAS

def transicion_tipo_ppt(screen, duracion=900):
    fade = pygame.Surface(screen.get_size())
    for a in range(0, 256, 15):
        fade.set_alpha(a)
        screen.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(duracion // 18)

def aparecer_aleatorio(tablero, id_elem):
    """
    Coloca un elemento en una casilla vacía aleatoria del tablero.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - id_elem: El número identificador del elemento que queremos colocar.

    Retorna:
        - (columna, fila): Tupla que indica posición en la que se colocó el elemento.
    """

    # Debemos detectar los espacios vacíos, para ello recorremos
    # el tablero y almacenamos tuplas de (columna, fila) las posiciones
    # en las que un elemento "VACIO" (el número 0 en este caso) se encuentre.
    vacios = []

    # Forma vista en clases de recorrer el arreglo multidimensional.
    # Tanto fila como columna son números.
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            # Obtenemos el elemento que se encuentra en esa fila y columna.
            elem_pos = tablero[fila][columna]
            #ahora buscamos si la casilla de al lado esta vacia para que cuando se cargue el mapa, no se encierren ni las manzanas ni el jugador
            if elem_pos == VACIO:
                vecinos_libres = 0
                if fila -1 >= 0 and tablero[fila-1][columna] == VACIO : 
                    vecinos_libres = vecinos_libres + 1
                if fila +1 < FILAS and tablero[fila+1][columna] == VACIO:
                    vecinos_libres = vecinos_libres + 1
                if columna -1 >= 0 and tablero[fila][columna-1] == VACIO:
                    vecinos_libres = vecinos_libres + 1
                if columna +1 < COLUMNAS and tablero[fila][columna+1] == VACIO:
                    vecinos_libres = vecinos_libres + 1
                if fila - 1 >= 0 and columna - 1 >= 0 and tablero[fila-1][columna-1] == VACIO:
                    vecinos_libres += 1
                if fila - 1 >= 0 and columna + 1 < COLUMNAS and tablero[fila-1][columna+1] == VACIO:
                    vecinos_libres += 1
                if fila + 1 < FILAS and columna - 1 >= 0 and tablero[fila+1][columna-1] == VACIO:
                    vecinos_libres += 1 
                if fila + 1 < FILAS and columna + 1 < COLUMNAS and tablero[fila+1][columna+1] == VACIO:
                    vecinos_libres += 1
                if id_elem != MANZANA or vecinos_libres or PUERTA or JUGADOR > 2:
                # Al utilizar los paréntesis () dentro de la función, lo estaremos
                # añadiendo como una tupla con la estructura (columna, fila).
                    vacios.append((columna, fila))

    # También se puede utilizar comprensión de listas para rellenar el arreglo
    # a la vez que lo recorremos:
    #
    # vacios = [
    #     (columna, fila)
    #     for fila in range(FILAS)
    #     for columna in range(COLUMNAS)
    #     if tablero[fila][columna] == VACIO
    # ]

    # Si no hay casillas vacías, retornamos un valor especial.
    if len(vacios) == 0:
        return -1, -1

    # Usando la función random.choice(lista) podremos obtener una tupla
    # aleatoria desde el arreglo "vacios" que definimos anteriormente.
    columna, fila = random.choice(vacios)

    # Finalmente, colocamos el elemento al poner su número en la casilla
    # del tablero correspondiente.
    tablero[fila][columna] = id_elem

    return columna, fila


def poblar_tablero(tablero):
    """
    Coloca un obstáculo y la manzana en el tablero.

    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
    """
    for i in range(1, 40):
        aparecer_aleatorio(tablero, OBSTACULO)
    for i in range(3):
        aparecer_aleatorio(tablero, MANZANA)
    for i in range (4):
        pos = aparecer_aleatorio(tablero, SEGUIDOR)
        tipos_seguidor_tablero[pos] = random.randint(0, 2)
    aparecer_aleatorio(tablero, PUERTA)
def dibujar_panel(screen, fuente, largo, nivel, seg_salvados):
    panel = pygame.Rect(LADO_TABLERO, 0, ANCHO_PANEL, ALTO_VENTANA)
    x= LADO_TABLERO +10
    titulo = fuente.render("SNAKE", True, "white")
    largo_txt = fuente.render(f"Seguidores actuales: {largo -1}", True, "white") 
    screen.blit(largo_txt, (x, 100))
    meta_txt = fuente.render(f"Salida en el nivel {4}", True, "yellow")
    screen.blit(meta_txt, (x, 140))
    nivel_txt = fuente.render(f"Nivel: {nivel}", True, "black")
    screen.blit(nivel_txt, (x, 180))
    salvados_txt = fuente.render(f"Seguidores salvados: {seg_salvados}", True, "green")
    screen.blit(salvados_txt, (x, 220))
   

def refrescar_tablero(screen, tablero, pasos, img_jugador, posiciones_cuerpo, nivel, imgs_seguidores, seg_totales, direccion, tipos_cuerpo, sobreescribe= None):

    """
    Dibuja el estado actual del tablero en la pantalla.

    Parámetros:
        - screen: La pantalla sobre la cual estamos dibujando.
        - tablero: El tablero con sus posiciones actuales.
    """

    # Rellena la pantalla con el color gris, básicamente pintando
    # por encima de lo que estaba anteriormente.
    screen.fill("gray30")
    wall = pygame.image.load ("assets/blocks/daño.png ").convert_alpha ()
    floor = pygame.image.load ("assets/blocks/Bckkk.png ").convert ()
    apple = pygame.image.load ("assets/elements/llave.png").convert_alpha ()
    puerta= pygame.image.load ("assets/blocks/puerta.jpeg").convert_alpha ()
    puerta_abierta = pygame.image.load ("assets/blocks/puerta_abierta.jpeg").convert_alpha()

    


    # Podemos calcular el tamaño en pixeles que tendrá cada
    # casilla al dividir tanto la altura de la pantalla (screen.get_height())
    # como el ancho (screen.get_width()) por la cantidad de filas y columnas respectivamente.
    # Por ejemplo en este caso alto_elem sería 800 / 15 = 53.3, lo que nos indica que la
    # altura de cada elemento es de 53.3 píxeles.
    alto_elem = LADO_TABLERO / FILAS
    ancho_elem = LADO_TABLERO / COLUMNAS
    # Como el jugador es un círculo, se necesita el radio.
    radio = ancho_elem / 2

    # Posición en eje "y" en unidad de píxeles.
    pos_y = 0
  
    for i in range(FILAS):
        # Posición en eje "x" en unidad de píxeles.
        pos_x = 0
        for j in range(COLUMNAS):
            screen.blit(floor, [pos_x, pos_y])
            if tablero[i][j] == OBSTACULO:
                # Dibuja un rectángulo en la posición (pos_x, pos_y) y que sea
                # de tamaño (ancho_elem, alto_elem) y color negro.
                screen.blit(wall, [pos_x, pos_y])
            elif tablero[i][j] == JUGADOR:
                pass
            elif tablero[i][j] == MANZANA:
                screen.blit(apple, [pos_x, pos_y])
            elif tablero[i][j] == PUERTA:
                screen.blit(puerta, [pos_x, pos_y])
            elif tablero[i][j] == PUERTA_ABIERTA:
                screen.blit(puerta_abierta, [pos_x, pos_y])
            elif tablero[i][j] == SEGUIDOR:
                screen.blit(imgs_seguidores[tipos_seguidor_tablero.get((j, i), 0)], [pos_x, pos_y - 25])
            # Estamos recorriendo los píxeles de la pantalla, por lo que
            # debemos sumar el ancho y altura en pixeles de cada elemento que
            # ya hayamos recorrido para avanzar al siguiente.
            pos_x += ancho_elem
        pos_y += alto_elem
        #este comando deberia mostrar los pasos restantes en pantalla
        fuente = pygame.font.Font(None, 36)
        restantes = MAX_PASOS - pasos
        texto = fuente.render(f"Pasos restantes: {restantes}", True, (255, 255, 255))
        screen.blit(texto, (10, 10))
    col_j, fila_j = posiciones_cuerpo [0]
    px_draw, py_draw = sobreescribe if sobreescribe else celdaapixel(col_j, fila_j)
    if direccion == (0,1) : 
        #aqui los seguidores no traspasan al jugador
        for i in range (1, len(posiciones_cuerpo)):
            col_s, fila_s = posiciones_cuerpo[i]
            px_s, py_s = celdaapixel(col_s, fila_s)
            screen.blit(imgs_seguidores[tipos_cuerpo[i]], [px_s, py_s - 25])
        screen.blit(img_jugador, [px_draw, py_draw - 25])    
    elif direccion == (1,0) : 
        #aqui los seguidores no traspasan al jugador
        for i in range (1, len(posiciones_cuerpo)):
            col_s, fila_s = posiciones_cuerpo[i]
            px_s, py_s = celdaapixel(col_s, fila_s)
            screen.blit(imgs_seguidores[tipos_cuerpo[i]], [px_s, py_s - 25])
        screen.blit(img_jugador, [px_draw, py_draw - 25])
    elif direccion == (-1,0) : 
        #aqui los seguidores no traspasan al jugador
        for i in range (1, len(posiciones_cuerpo)):
            col_s, fila_s = posiciones_cuerpo[i]
            px_s, py_s = celdaapixel(col_s, fila_s)
            screen.blit(imgs_seguidores[tipos_cuerpo[i]], [px_s, py_s - 25])
        screen.blit(img_jugador, [px_draw, py_draw - 25])       
        #este codigo se repite 3 veces dado a que al añadir un "or" en el primero toda las imagenes traspasaban al seguidor incluyendo la de subir la cual no queremos que haga eso
    else:
        screen.blit(img_jugador, [px_draw, py_draw - 25])  
        for i in range (1, len(posiciones_cuerpo)):
            col_s, fila_s = posiciones_cuerpo[i]
            px_s, py_s = celdaapixel(col_s, fila_s)
            screen.blit(imgs_seguidores[tipos_cuerpo[i]], [px_s, py_s -25])
    dibujar_panel(screen, fuente, len(posiciones_cuerpo), nivel, seg_totales)
    # Refresca el contenido que se ve en pantalla.
    pygame.display.flip()


def cambiar_direccion(keys, direccion_actual):
    """
    Cambia la dirección del jugador.

    Parámetros:
        - keys: Arreglo de teclas presionadas.
        - direccion_actual: La dirección en la que estaba avanzando justo antes de analizar
            si hubo un cambio de dirección.

    Retorna:
        - direccion_actual: La nueva dirección del jugador.
    """

    # Tecla W
    if keys[pygame.K_w]:
        # La tupla nos indica que horizontalmente (columnas) no hará nada (0) y
        # que verticalmente (filas) disminuirá el índice en el tablero (-1).
        return (0, -1)
        
              

    # Tecla S
    if keys[pygame.K_s]:
        # En este caso avanzará a través de las filas del tablero.
        return (0, 1)
        
    # Tecla A
    if keys[pygame.K_a]:
        # Retrocede por las columnas del tablero.
        return (-1, 0)

    # Tecla D
    if keys[pygame.K_d]:
        # Avanza por las columnas del tablero.
        return (1, 0)

    # Si no se presiona ninguna de las teclas anteriores, la dirección
    # será la misma que la anterior.
    return direccion_actual


def avanzar(tablero, posiciones_cuerpo, tipos_cuerpo, direccion, sonido_manzana, contador_manzanas, bwomp):
    """
    Avanza el jugador un paso en la dirección dada.
    
    Parámetros:
        - tablero: El tablero con sus posiciones actuales.
        - pos_jugador: Tupla con la posición actual (índice con
            estructura (columna, fila)) del jugador en el tablero.
        - direccion: Tupla con la dirección en la que está avanzando actualmente el jugador.

    Retorna:
        - (resultado, nueva_pos_jugador): Retorna el resultado que se obtiene
            al avanzar (derrota, victoria o "ok" (no cambia de pantalla)) y la nueva posición del jugador.
    """
    pincho = pygame.mixer.Sound("assets/sounds/navajazo.mp3")
   
    # Obtenemos los componentes "x" e "y" de cada tupla recibida
    # con información de la dirección y posición del jugador.
    dir_col, dir_fila = direccion
    ind_actual_col, ind_actual_fila = (
        posiciones_cuerpo[0]  # Tupla (columna, fila) que representa los índices en el tablero.
    )

    # Aplicamos la dirección a la posición del jugador.
    ind_nueva_col = ind_actual_col + dir_col
    ind_nueva_fila = ind_actual_fila + dir_fila

    # Verificamos que no haya choque con el borde del tablero.
    if not (0 <= ind_nueva_col < COLUMNAS and 0 <= ind_nueva_fila < FILAS):
        return "ushallnotpass", posiciones_cuerpo, tipos_cuerpo, contador_manzanas

    # Obtenemos el elemento que se encuentre en el tablero en la nueva posición del jugador.
    pos_elem = tablero[ind_nueva_fila][ind_nueva_col]

    if pos_elem == OBSTACULO :
        pincho . play()        
        
        return "derrota", posiciones_cuerpo, tipos_cuerpo, contador_manzanas 
    if pos_elem == MANZANA :
        sonido_manzana . play () # Reproducimos sonido
        contador_manzanas = contador_manzanas + 1 
        if contador_manzanas == CANTIDAD_MANZANAS:
           for f in range (FILAS):
               for c in range(COLUMNAS):
                   if tablero[f][c] == PUERTA:
                       puerta_Se_Abre = pygame.mixer.Sound("assets/sounds/puerta_abierta.mp3")
                       puerta_Se_Abre . play ()
                       tablero[f][c]= PUERTA_ABIERTA
    susvent = pygame.mixer.Sound("assets/sounds/puerta_ruidosa.mp3")
    if pos_elem == PUERTA:
        return "ushallnotpass", posiciones_cuerpo, tipos_cuerpo, contador_manzanas
    if pos_elem == PUERTA_ABIERTA:
        susvent . play()
        return "siguiente_nivel", posiciones_cuerpo, tipos_cuerpo, contador_manzanas
       


    # Movimiento normal, si es que no encontramos manzana ni obstáculo.
    # Guardamos la posición de la cola antes de mover (por si se agrega un seguidor)
    ind_cola_col, ind_cola_fila = posiciones_cuerpo[-1]

    # Movemos cada segmento a la posición del segmento que tiene delante
    for i in range(len(posiciones_cuerpo) - 1, 0, -1):
        posiciones_cuerpo[i] = posiciones_cuerpo[i - 1]

    # Movimiento normal, si es que no encontramos manzana ni obstáculo.
    tablero[ind_actual_fila][ind_actual_col] = VACIO
    tablero[ind_nueva_fila][ind_nueva_col] = JUGADOR
    posiciones_cuerpo[0] = (ind_nueva_col, ind_nueva_fila)

    if pos_elem == SEGUIDOR:
        tipo = tipos_seguidor_tablero.pop((ind_nueva_col, ind_nueva_fila), 0)
        posiciones_cuerpo.append((ind_cola_col, ind_cola_fila))
        tipos_cuerpo.append(tipo)


    return "ok", posiciones_cuerpo, tipos_cuerpo, contador_manzanas


def reiniciar():
    """
    Crea un nuevo tablero y estado para una nueva partida.

    Retorna:
        - (tablero, pos_jugador): Tablero nuevo y la nueva posición aleatoria del jugador.
            pos_jugador corresponda a una tupla (columna, fila) donde columna y fila son índices
            de matriz tablero.
    """
    tipos_seguidor_tablero.clear() #se limpia el contador
    # Si se modifica constante FILAS o COLUMNAS al inicio, también
    # se debe modificar este arreglo de tablero con los valores correspondientes.
    # Esto puede ser mejorado usando dos bucles "for" anidados o comprensión de listas.
    tablero = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        
    ]

    # Usando dos bucles "for" anidados se haría de la siguiente manera:
    # tablero = []
    # for _ in range(FILAS):
    #     fila_tablero = []
    #
    #     for _ in range(COLUMNAS):
    #         fila_tablero.append(VACIO)
    #
    #     tablero.append(fila_tablero)
    # Otra manera usando comprensión de listas:
    # tablero = [[VACIO] * COLUMNAS for _ in range(FILAS)]
    # El _ en el "for" indica que no usamos la variable con la que iteramos.

    poblar_tablero(tablero)
   

    # Colocamos al jugador en una posición aleatoria.
    posiciones_cuerpo = [aparecer_aleatorio(tablero, JUGADOR)]
    tipos_cuerpo = [None] #se inicia lista
    return tablero, posiciones_cuerpo, tipos_cuerpo


def mostrar_pantalla(screen, nombre_archivo):
    """
    Carga una imagen y la muestra escalada a la ventana.

    Parámetros:
        - screen: La pantalla donde colocaremos la imagen.
        - nombre_archivo: El nombre del archivo de la imagen.
    """

    ruta = os.path.join(DIR_PANTALLAS, nombre_archivo)

    try:
        imagen = pygame.image.load(ruta)
        imagen = pygame.transform.scale(imagen, screen.get_size())

        # Dibujamos la imagen en la pantalla en la coordenada (0, 0).
        screen.blit(imagen, (0, 0))

        # Refrescamos pantalla.
        pygame.display.flip()
    except FileNotFoundError:
        # Fallback de seguridad en caso de que las imágenes no existan aún
        screen.fill("black")
        pygame.display.flip()
        print(f"Advertencia: No se encontró la imagen {ruta}")


def main():
    pygame.init()

    # Establecemos la resolución de la pantalla.
    screen = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))

    # Establecemos el título de la ventana.
    pygame.display.set_caption("Outcat")
    fuente = pygame.font.Font(None, 36)

    running = True
    posiciones_cuerpo = []
    estado = ESTADO_INICIO
    tablero = []
    direccion = (0, 0)
    tiempo_ultimo_mov = 0
    pasos = 0
    contador_manzanas = 0
    nivel = 1
    animacion = None
    direccion_anterior = (0, 0)
    egg = ""
    seg_totales = 0


    mostrar_pantalla(screen, PANTALLA_INICIO)
    sonido_manzana = pygame.mixer.Sound ("assets/sounds/agarrar_llave.mp3")
    bwomp = pygame.mixer.Sound("assets/sounds/bwomp.mp3")
    tadan = pygame.mixer.Sound("assets/sounds/tadan.mp3")
    susvent = pygame.mixer.Sound("assets/sounds/puerta_ruidosa.mp3")
    puerta_seabre =pygame.mixer.Sound("assets/sounds/puerta_abierta.mp3")
    pincho = pygame.mixer.Sound("assets/sounds/navajazo.mpeg")
    
    pygame.mixer.music.load ("assets/sounds/musicadelterraria.mpeg")
    pygame.mixer.music.play( 0) # Ejecutamos en bucle infinito
    # Este es el bucle principal del juego, todo lo que sucede en el juego
    # está aquí.
    mostrar_pantalla(screen, PANTALLA_INICIO)

    img_arriba= pygame.image.load("assets/elements/Mago_arriba1.png").convert_alpha()
    img_arriba2= pygame.image.load("assets/elements/Mago_arriba2.png").convert_alpha()#parte de la animacion del mago
    img_arriba3= pygame.image.load("assets/elements/Mago_arriba3.png").convert_alpha()#parte de la animacion del mago
    img_abajo= pygame.image.load("assets/elements/Mago_abajo1.png").convert_alpha()
    img_abajo2= pygame.image.load("assets/elements/Mago_abajo2.png").convert_alpha()#parte de la animacion del mago
    img_abajo3= pygame.image.load("assets/elements/Mago_abajo3.png").convert_alpha()#parte de la animacion del mago
    img_izq= pygame.image.load("assets/elements/mago.png").convert_alpha()
    img_izq2= pygame.image.load("assets/elements/Mago_izq2.png").convert_alpha()#parte de la animacion del mago
    img_der= pygame.image.load("assets/elements/magoflip.png").convert_alpha()
    img_der2= pygame.image.load("assets/elements/Mago_izq2flip.png").convert_alpha()#parte de la animacion del mago
    frames_por_direccion = {
        (0, -1): [img_arriba, img_arriba2, img_arriba, img_arriba3],
        (0,  1): [img_abajo, img_abajo2, img_abajo, img_abajo3],
        (-1, 0): [img_izq, img_izq2],
        (1,  0): [img_der, img_der2],
    }
    frame_actual = 0    
    img_actual = img_izq
    #se cargan las imagenes de los seguidores
    img_tipo1  = pygame.image.load("assets/elements/Zorro_abajo1.png").convert_alpha()
    img_tipo2  = pygame.image.load("assets/elements/Paj_abajo1.png").convert_alpha()
    img_tipo3 = pygame.image.load("assets/elements/Cabra_abajo1.png").convert_alpha()
    imgs_seguidores = [img_tipo1, img_tipo2, img_tipo3] #estos se ciclan
    while running:
        # Se analizan los eventos del bucle actual.
        for evento in pygame.event.get():
            # Si es que se quiere cerrar la ventana.
            if evento.type == pygame.QUIT:
                running = False

            # Si es que se presiona alguna tecla.
            if evento.type == pygame.KEYDOWN:
                #si es que el jugador quiere sentirse mas 𝓟𝓵𝓾𝓮𝔂
                if estado == ESTADO_INICIO and evento.unicode.isalpha():
                    egg += evento.unicode.lower()
                    egg = egg[-5:] #cinco letras
                    if egg == "pluey": 
                        splat = pygame.mixer.Sound("assets/sounds/splat.mp3")
                        pygame.mixer.music.load ("assets/sounds/pluey.mp3")
                        splat . play()
                        pygame.mixer.music.play(-1)
                        egg = ""
                if estado == ESTADO_INICIO:
                    if evento.key == pygame.K_SPACE:
                        tablero, posiciones_cuerpo, tipos_cuerpo = reiniciar()
                        direccion = (0, 0)
                        nivel = 1
                        # Obtiene tiempo en milisegundos
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        pasos = 0
                        refrescar_tablero(screen, tablero, pasos, img_actual, posiciones_cuerpo, nivel, imgs_seguidores, seg_totales, direccion, tipos_cuerpo)
                        contador_manzanas = 0
                        pasos = 0
                    elif evento.key == pygame.K_i:
                        estado = ESTADO_INSTRUCCIONES
                        mostrar_pantalla(screen, PANTALLA_INSTRUCCIONES)
                elif estado == ESTADO_INSTRUCCIONES:
                    estado = ESTADO_INICIO
                    mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado in (ESTADO_DERROTA, ESTADO_VICTORIA):
                    if evento.key == pygame.K_SPACE:
                        tablero, posiciones_cuerpo, tipos_cuerpo = reiniciar()
                        
                        pygame.mixer.music.play(0)
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        estado = ESTADO_JUGANDO
                        pasos = 0
                        contador_manzanas = 0
                        nivel = 1
                        seg_totales = 0
                        refrescar_tablero(screen, tablero, pasos, img_actual, posiciones_cuerpo, nivel, imgs_seguidores, seg_totales, direccion, tipos_cuerpo)
                        

                    if evento.key == pygame.K_ESCAPE:
                        estado = ESTADO_INICIO
                        mostrar_pantalla(screen, PANTALLA_INICIO)

                elif estado == ESTADO_JUGANDO:
                    direccion = cambiar_direccion(pygame.key.get_pressed(), direccion)

        if estado == ESTADO_JUGANDO: 
            #esto para que el jugador se mueva de manera fluida
            if animacion:
                ox, oy, dx, dy, t = animacion 
                t = min(t + 0.2, 1.0)
                px = ox + (dx - ox) * t
                py = oy + (dy - oy) * t
                refrescar_tablero(screen, tablero, pasos, img_actual, posiciones_cuerpo, nivel, imgs_seguidores, seg_totales, direccion, tipos_cuerpo, (px, py))
                animacion = (ox, oy, dx, dy, t) if t < 1.0 else None
                if t < 1.0:
                    continue 
            tiempo_actual = pygame.time.get_ticks()  # En milisegundos

            # La variable RETRASO hace que si no han pasado esa cantidad de ticks,
            # entonces no se avanzará en el tablero.
            keys = pygame.key.get_pressed()
            direccion = (0, 0)

            if keys[pygame.K_w]:
                direccion = (0, -1)
            elif keys[pygame.K_s]:
                direccion = (0, 1)
            elif keys[pygame.K_a]:
                direccion = (-1, 0)
            elif keys[pygame.K_d]:
                direccion = (1, 0)

            if direccion != (0, 0) and tiempo_actual - tiempo_ultimo_mov >= RETRASO:
                col_antes, fila_antes = posiciones_cuerpo[0]
                resultado, posiciones_cuerpo, tipos_cuerpo, contador_manzanas = avanzar(tablero, posiciones_cuerpo, tipos_cuerpo, direccion, sonido_manzana, contador_manzanas, bwomp)
                

                if resultado == "derrota":
                    pygame.mixer.music.stop()
                    bwomp . play ()
                    estado = ESTADO_DERROTA
                    
                    mostrar_pantalla(screen, PANTALLA_DERROTA)
                   
                elif resultado == "siguiente_nivel":
                    seg_totales += len(posiciones_cuerpo) -1
                    if nivel >= 4:
                        estado = ESTADO_VICTORIA
                        pygame.mixer.music.stop()
                        tadan . play ()
                        mostrar_pantalla(screen, PANTALLA_VICTORIA)
                    else:
                        transicion_tipo_ppt(screen)
                        nivel = nivel + 1
                        tablero, posiciones_cuerpo, tipos_cuerpo = reiniciar()
                        direccion = (0, 0)
                        tiempo_ultimo_mov = pygame.time.get_ticks()
                        pasos = 0
                        contador_manzanas = 0
                        refrescar_tablero(screen, tablero, pasos, img_actual, posiciones_cuerpo, nivel, imgs_seguidores, seg_totales,direccion, tipos_cuerpo,)
                elif resultado == "ushallnotpass":
                    pass
                else:
                    tiempo_ultimo_mov = tiempo_actual
                    if direccion != direccion_anterior:
                        frame_actual = 0
                    direccion_anterior = direccion
                    if direccion in frames_por_direccion:
                        lista = frames_por_direccion[direccion]
                        frame_actual = (frame_actual + 1) % len(lista)
                        img_actual = lista[frame_actual]
                    pasos +=1
                    restantes=MAX_PASOS - pasos 
                    pygame.display.set_caption(f"Outcat - Pasos restantes: {restantes}")
                    if pasos >= MAX_PASOS:
                        pygame.mixer.music.stop()
                        estado = ESTADO_DERROTA
                        mostrar_pantalla(screen, PANTALLA_DERROTA)
                    else:  
                        animacion = (*celdaapixel(col_antes,fila_antes), *celdaapixel(*posiciones_cuerpo[0]), 0.0)
    pygame.quit()


if __name__ == "__main__":
    main()