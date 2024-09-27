


from rich import print as print
import flet as ft
import pathlib

from manejo_texto.procesar_etiquetas import Etiquetas, guardar_archivo, etiquetas2texto, separar_etiquetas

from manejo_imagenes.verificar_dimensiones import dimensiones_imagen

from sistema_archivos.buscar_extension import buscar_imagenes, listar_directorios

from componentes.galeria_imagenes import Galeria, Contenedor, ContenedorImagen, imagen_clave,indice_clave, ContImag

from componentes.filas_botones import FilasBotonesEtiquetas

from estilos.estilos_contenedores import estilos_seleccion, estilos_galeria, Estilos

from componentes.lista_desplegable import crear_lista_desplegable,opciones_lista_desplegable, convertir_dimensiones_opencv, extraer_numeros, tupla_resoluciones

from componentes.galeria_estados import Contenedor_Etiquetado, actualizar_estilo_estado
from componentes.galeria_estados import GaleriaEstados

from componentes.clasificador import filtrar_dimensiones, filtrar_etiquetas, leer_imagenes_etiquetadas

from componentes.dialogo_alerta import DialogoAlerta

from vistas.etiquetador.dialogos import dialogo_dataset, dialogo_directorio, dialogo_guardado_tags

from vistas.etiquetador.columna_etiquetas import entrada_tags_agregar,entrada_tags_quitar
from vistas.etiquetador.columna_etiquetas import entrada_tags_buscar
from vistas.etiquetador.columna_etiquetas import filas_filtrado, columna_etiquetas, texto_contador_tags
from vistas.etiquetador.columna_etiquetas import boton_reset_tags, boton_guardar_dataset, boton_reordenar_tags
from vistas.etiquetador.columna_etiquetas import estadisticas

from vistas.etiquetador.columna_seleccion import texto_imagen, texto_ruta_data,texto_ruta_titulo,texto_tags_data,texto_tags_titulo
from vistas.etiquetador.columna_seleccion import columna_seleccion, contenedor_seleccion
from vistas.etiquetador.columna_seleccion import imagen_seleccion

from vistas.etiquetador.clasificador import clasificador_imagenes

from vistas.etiquetador.menu_etiquetador import boton_carpeta, boton_filtrar_dimensiones, boton_dataset, tooltip_carpeta, ayuda_emergente
from vistas.etiquetador.menu_etiquetador import fila_controles, lista_dimensiones_desplegable, lista_estados_desplegable
from vistas.etiquetador.menu_etiquetador import actualizar_lista_dimensiones

from vistas.etiquetador.columna_etiquetador import etiquetador_imagen, crear_botones_etiquetador

from constantes.constantes import Tab, Percentil, Estados, tupla_estados

lista_imagenes = clasificador_imagenes


galeria_etiquetador = GaleriaEstados( estilos_galeria )

imagenes_tags = []



def main(pagina: ft.Page):

    # estructura con data global
    dataset = Etiquetas("") 

    tags_teclado = Etiquetas("") 

    ############# COMPONENTES GRAFICOS ######################## 

    boton_guardar = ft.FloatingActionButton(
        icon=ft.icons.SAVE, bgcolor=ft.colors.YELLOW_600, tooltip="Guardar todas las etiquetas cambiadas."
    )


    #############  MAQUETADO ############################

    galeria_etiquetador.expand = 1

    fila_galeria_etiquetas = ft.Row(
        [galeria_etiquetador, ft.VerticalDivider(), columna_etiquetas],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        vertical_alignment=ft.CrossAxisAlignment.START,
        wrap = False,
        expand=True,
        )

    pagina.add(fila_controles)  
    pagina.add(ft.Divider(height=7, thickness=1))

    #pestaña de galeria
    tab_galeria = ft.Tab(
        text="Galeria",
        content=fila_galeria_etiquetas,
        visible=True,
        # icon=ft.icons.GRID_VIEW_ROUNDED,
        icon=ft.icons.PHOTO_ROUNDED
        )

    columna_seleccion.visible = False

    # pestaña de etiquetado y navegacion de imagenes
    altura_tab_etiquetado = 800
    fila_etiquetado_navegacion = ft.Row(
        controls = [ 
            columna_seleccion,  
            ft.VerticalDivider(),
            etiquetador_imagen
            ], 
        spacing = 10, 
        height = altura_tab_etiquetado
    ) 
    tab_etiquetado = ft.Tab(
        text="Etiquetado",
        content=fila_etiquetado_navegacion,
        visible=True,    
        icon = ft.icons.TAG_OUTLINED,
    )

    # organizacion en pestañas
    pestanias = ft.Tabs(
        selected_index=Tab.TAB_GALERIA.value,
        animation_duration=500,
        tabs=[
            tab_galeria   ,
            tab_etiquetado,
            # tab_global
        ],
        expand=1,
    )

    # Añadido componentes (todos juntos)
    pagina.add(pestanias)
    # boton para guardar cambios 
    pagina.floating_action_button = boton_guardar

    ############## HANDLERS ##################################

    def buscar_tags_seleccion(e):

        # texto = e.control.value
        texto = entrada_tags_buscar.value
        # descarte de entradas vacias
        if len(texto) == 0:
            return

        # actualizacion de las etiquetas encontradas
        estadisticas()
        filas_filtrado.evento_click(filtrar_todas_etiquetas)
        columna_etiquetas.update()


    def agregar_tags_seleccion(e):
        # texto = e.control.value
        texto = entrada_tags_agregar.value

        # conversion a lista de etiquetas
        texto = separar_etiquetas([texto])
        # descarte de entradas vacias
        if len(texto)== 0:
            return

        tags_teclado.agregar_tags(texto ,sobreescribir=True)
        lista_tags = tags_teclado.tags

        # agregado de tags a imagenes            
        for imagen in lista_imagenes.seleccion:

            imagen.agregar_tags(lista_tags)

            # actualizacion bordes galeria
            imagen.verificar_imagen(lista_imagenes.dimensiones_elegidas)
            imagen.verificar_guardado()
            imagen.actualizar_estilo_estado()

        # actualizacion grafica de todos los componentes
        actualizar_componentes() 
            
        # renovar lista de etiquetas
        estadisticas()
        filas_filtrado.evento_click(filtrar_todas_etiquetas)
        columna_etiquetas.update()


    def quitar_tags_seleccion(e):
        # texto = e.control.value
        texto = entrada_tags_quitar.value

        # conversion a lista de etiquetas
        texto = separar_etiquetas([texto])
        # descarte de entradas vacias
        if len(texto)== 0:
            return

        tags_teclado.agregar_tags(texto ,sobreescribir=True)
        lista_tags = tags_teclado.tags

        # quita de tags a imagenes        
        for imagen in lista_imagenes.seleccion:

            imagen.quitar_tags(lista_tags)

            # actualizacion bordes galeria
            imagen.verificar_imagen(lista_imagenes.dimensiones_elegidas)
            imagen.verificar_guardado()
            imagen.actualizar_estilo_estado()

        # actualizacion grafica de todos los componentes
        actualizar_componentes() 
            
        # renovar lista de etiquetas
        estadisticas()
        filas_filtrado.evento_click(filtrar_todas_etiquetas)
        columna_etiquetas.update()


    def click_botones_tags(e: ft.ControlEvent ):
        """Habilita el accionamiento solidario de los botones de etiquetas repetidas. Tambien llama al handler de actualizaciones."""
        tag = e.control.text
        estado = e.control.estado

        # Se transfieren los tags de la botonera a las imagenes 
        etiquetas_botones = etiquetador_imagen.leer_botones()

        # caso de deseleccion de etiquetas -> botones repetidos actualizados
        if estado==False:
            # extraccion de etiqueta actual
            set_actual = set(etiquetas_botones)
            set_resta = set([tag])
            set_tags = set_actual.difference(set_resta)
            etiquetas_botones = list(set_tags)
  
        etiquetador_imagen.agregar_tags(etiquetas_botones, sobreescribir=True)
        # transferencias y actualizaciones graficas de imagenes
        click_botones_etiquetador(None)


    def click_botones_etiquetador( e: ft.ControlEvent | None ):
        """Actualiza etiquetas, estado, estadisticas y estilo de bordes de las imagenes en base al boton del etiquetador accionado."""

        clave = lista_imagenes.clave_actual

        ## FIX
        ## BUG: Si la clave no está en la seleccion se produce un cambio de tags descontrolado

        if len(lista_imagenes.seleccion)>0:
            # prevencion de errores por posible clave inexistente
            # (suele pasar al cambiar las condiciones de filtrado de imagenes)

            indice = indice_clave(clave, lista_imagenes.seleccion)
            # si la clave actual existe se transfiere la informacion de la botonera la imagen
            if indice != None:
                imagen_seleccionada = imagen_clave(clave, lista_imagenes.seleccion) 

                # Se transfieren los tags de la botonera a las imagenes 
                etiquetas_botones = etiquetador_imagen.leer_botones()
                imagen_seleccionada.agregar_tags(etiquetas_botones, sobreescribir=True)

                # actualizacion bordes galeria
                imagen_seleccionada.verificar_imagen(lista_imagenes.dimensiones_elegidas)
                imagen_seleccionada.verificar_guardado()
                imagen_seleccionada.actualizar_estilo_estado()

            # si dicha clave no se encuentra entonces se elige la primera calve de la lista actual
            else:
                
                print(f"[bold green]Imagen '[bold yellow]{clave}' [bold green]no disponible en galeria")
                clave = lista_imagenes.seleccion[0].clave
                lista_imagenes.clave_actual = clave
                print(f"[bold green]Imagen '[bold yellow]{clave}' [bold green]como sustituto\n")


        # actualizacion grafica de todos los componentes
        actualizar_componentes() 
            
        # renovar lista de etiquetas
        estadisticas()
        filas_filtrado.evento_click(filtrar_todas_etiquetas)
        columna_etiquetas.update()
   

    # Funcion de apertura de directorio
    def resultado_directorio(e: ft.FilePickerResultEvent):
        """Carga las imagenes del proyecto."""
        if e.path:
            # acceso a elementos globales
            global imagenes_tags

            # busqueda 
            lista_imagenes.ruta_directorio =  e.path
            directorio = lista_imagenes.ruta_directorio

            ventana_emergente(pagina, f"Buscando imágenes...\nRuta: {directorio} ")
            rutas_imagen = buscar_imagenes(directorio)
        
            # lectura de imagenes del directorio
            imagenes_etiquetadas = leer_imagenes_etiquetadas(rutas_imagen)
            lista_imagenes.cargar_imagenes(imagenes_etiquetadas)

            # reinicio de las listas de imagenes
            imagenes_tags = lista_imagenes.todas
            lista_imagenes.seleccion = lista_imagenes.todas

            # asignacion de la primera imagen de la galeria 
            clave = lista_imagenes.clave_actual
            if len(lista_imagenes.seleccion)>0:         
                clave = lista_imagenes.seleccion[0].clave
                etiquetador_imagen.setear_salida(lista_imagenes.seleccion[0]) # Previene falsas modificaciones al cambiar de carpeta
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes abierto.\nRuta: {directorio} \nNº imágenes: {len(lista_imagenes.seleccion)}")
 
            else:
                clave = ""
                # reporte por snackbar
                ventana_emergente(pagina, f"Directorio de imagenes vacío.\nRuta: {directorio} ")


            lista_imagenes.clave_actual = clave
            # se descartan los tamaños de imagen no disponibles
            actualizar_lista_dimensiones() 
            lista_dimensiones_desplegable.update()
            # relectura del archivo dataset (puede no existir)
            dataset.ruta = lista_imagenes.ruta_dataset
            dataset.leer_archivo()
            # actualizacion de la app
            cargar_galeria_componentes()


    # Funcion de apertura de archivo con etiquetas (dataset)
    def resultado_dataset(e: ft.FilePickerResultEvent):
        """Carga el archivo de texto con las etiquetas del proyecto."""
        if e.files:
            archivo = e.files[0]    
            # lectura del archivo de dataset               
            ruta_dataset = archivo.path
            lista_imagenes.ruta_dataset = ruta_dataset
            dataset.ruta = ruta_dataset
            dataset.leer_archivo()
            cargar_galeria_componentes()
            # reporte por snackbar
            ventana_emergente(pagina, f"Archivo de  dataset abierto\nNombre archivo: {ruta_dataset}")


    def cargar_galeria_componentes(  e: ft.ControlEvent | None = None ):
        """Muestra las imagenes encontradas y las asigna a los componentes de seleccion y etiquetado. Si no hay imágenes que mostra oculta y/o inhabilita componentes."""
        
        # si se encuentran imagenes se visibilizan y configuran los controles
        filtrar_dimensiones_estados()   
        # agregado de todas las etiquetas al editor
        crear_botones_etiquetador(dataset)  

        #  Asignacion de eventos de los botones internos
        etiquetador_imagen.evento_click(
            funcion_etiquetas   = click_botones_tags,
            funcion_grupo       = click_botones_etiquetador,
            funcion_comando     = click_botones_etiquetador
            )

        # actualizar galeria
        actualizar_estilo_estado( lista_imagenes.seleccion, estilos_galeria )
        # actualizacion grafica
        actualizar_componentes()


    # Eventos galeria
    def click_imagen_galeria(e: ft.ControlEvent):
        """Este handler permite elegir una imagen desde la galeria y pasarla al selector de imagenes al tiempo que carga las etiquetas de archivo."""
        
        # print("click_imagen_galeria")
        contenedor = e.control
        lista_imagenes.clave_actual = contenedor.clave
        # asigna imagen y estilo de bordes a la pestaña de etiquetado
        actualizar_componentes()
        #cambio de pestaña
        pestanias.selected_index = Tab.TAB_SELECCION.value
        # actualizacion grafica
        pagina.update()


    # Funcion para el click sobre la imagen seleccionada
    def click_imagen_seleccion( e: ft.ControlEvent):
        """Esta funcion regresa a la galería de imagenes cerca de la imagen seleccionada."""
        apuntar_galeria( lista_imagenes.clave_actual)   
        #cambio de pestaña
        pestanias.selected_index = Tab.TAB_GALERIA.value
        pagina.update()


    def filtrar_dimensiones_estados( e: ft.ControlEvent | None = None):
        """Selecciona solamente aquellas imagenes que cumplan con el tamaño y estado especificados."""

        # conversion de texto a tupla numerica de dimensiones de imagen elegida
        opcion = lista_dimensiones_desplegable.value
        dimensiones_elegidas = convertir_dimensiones_opencv(str(opcion))

        lista_imagenes.dimensiones_elegidas = dimensiones_elegidas

        # Filtrado en base a las dimensiones de imagen
        dimensiones = dimensiones_elegidas if boton_filtrar_dimensiones.estado else None
        lista_imagenes.seleccion = filtrar_dimensiones(lista_imagenes.todas, dimensiones)

        # Filtrado en base a los estados de las imagenes
        estado = lista_estados_desplegable.value
        lista_imagenes.seleccionar_estado( estado )

        # reporte por snackbar 
        if len(lista_imagenes.todas) > 0 and estado != None:
            ventana_emergente(pagina, f"Filtrado por dimensiones y estado - {len(lista_imagenes.seleccion)} imagenes seleccionadas.")
        # actualizacion de las etiquetas encontradas
        estadisticas()
        filas_filtrado.evento_click(filtrar_todas_etiquetas)
        columna_etiquetas.update()

        # respaldo para que funcione el filtro de etiquetas
        global imagenes_tags
        imagenes_tags = lista_imagenes.seleccion


    def guardar_cambios(e:ft.ControlEvent | None = None):
        """Guarda las etiquetas en archivo de todas las imagenes modificadas. También actualiza estados y graficas."""

        if len(lista_imagenes.seleccion) == 0 : 
            ventana_emergente(pagina,f"Galería vacía - sin cambios")
            return
        imagen: Contenedor_Etiquetado
        i = 0
        for imagen in lista_imagenes.seleccion:  #
            guardado = imagen.guardar_archivo()
            if guardado :
                i += 1 
        for imagen in lista_imagenes.seleccion:
            imagen.verificar_guardado()
        # reporte por snackbar
        if i == 0:
            ventana_emergente(pagina,f"Etiquetas sin cambios")
        else:
            ventana_emergente(pagina,f"¡Etiquetas guardadas! - {i} archivos modificados")
        # actualizacion grafica
        actualizar_componentes(e)    

        entrada_tags_quitar.value = ""
        entrada_tags_quitar.update()
        entrada_tags_agregar.value = ""
        entrada_tags_agregar.update()





    def abrir_dialogo_guardado(e:ft.ControlEvent | None = None):

        # conteo imagenes con cambios sin guardar
        lista_imagenes.clasificar_estados()
        j = len(lista_imagenes.modificadas) 

        # si no hay modificaciones realizadas se cierra la alerta    
        if j == 0:
            # se ignora (nada que hacer)
            ventana_emergente(pagina, "Sin cambios para guardar.")
            return
        else:
            # en caso contrario se lanza la alerta de guardado
            dialogo_guardado_imagenes = DialogoAlerta(
                pagina,
                "¿Guardar cambios?", 
                f"Hay {j} imágenes modificadas."
                )

            dialogo_guardado_imagenes.funcion_confirmacion = guardar_cambios
            dialogo_guardado_imagenes.abrir_alerta() 


    def confirmar_cierre_programa(e:ft.ControlEvent):

        if e.data == "close":
            # conteo imagenes con cambios sin guardar
            lista_imagenes.clasificar_estados()
            j = len(lista_imagenes.modificadas) 
            # si no hay modificaciones realizadas se cierra el programa
            if j==0:
                # cerrar_programa(e)
                pagina.window_destroy()
            # en caso contrario se lanza la alerta de cierre
            else:
                dialogo_cierre_programa = DialogoAlerta(
                    pagina,
                    "¿Descartar cambios?", 
                    f"Hay {j} modificaciones sin guardar."
                    )

                dialogo_cierre_programa.funcion_confirmacion = pagina.window_destroy
                dialogo_cierre_programa.abrir_alerta()



    def ventana_emergente(pagina:ft.Page, texto: str):
        # show_snack_bar obsoleta desde la v0.23 
        pagina.show_snack_bar(
        # pagina.open(
            ft.SnackBar(ft.Text(texto), open=True, show_close_icon=True)
        )


    def actualizar_componentes( e: ft.ControlEvent | None = None):
        """Asigna la imagen actual a los componentes de seleccion y etiquetado en base a la 'clave' global.
        Si ésta no se encuentra en la galeria actual busca la primera imagen disponible y actualiza la clave.
        Tambien carga las imagenes disponibles a la galeria gráfica.
        Si la galeria queda vacia se ocultan los componentes graficos.
        """
        clave = lista_imagenes.clave_actual
        # actualizar galeria
        galeria_etiquetador.cargar_imagenes( lista_imagenes.seleccion )
        galeria_etiquetador.eventos(click = click_imagen_galeria)
        galeria_etiquetador.update()

        if len(lista_imagenes.seleccion)>0:
            # busqueda imagen
            indice = indice_clave(clave, lista_imagenes.seleccion)
            # si la clave actual no se encuentra se toma la primera imagen disponible
            if indice == None:

                print(f"[bold magenta]Imagen '[bold yellow]{clave}' [bold magenta]no disponible en galeria")
                clave = lista_imagenes.seleccion[0].clave
                lista_imagenes.clave_actual = clave
                print(f"[bold magenta]Imagen '[bold yellow]{clave}' [bold magenta]como sustituto\n")


            # seleccion imagen
            imagen_elegida = imagen_clave(clave, lista_imagenes.seleccion)

            etiquetador_imagen.setear_salida(imagen_elegida) # original
            imagen_seleccion(imagen_elegida)

            columna_seleccion.visible = True
            columna_seleccion.update()
            etiquetador_imagen.habilitado = True
            etiquetador_imagen.update()

        else:
            # ocultamiento de componentes graficos
            # columna_etiquetas.visible = False   # FIX
            columna_etiquetas.visible = True
            columna_etiquetas.update()
            # columna_seleccion.visible = False   # FIX
            columna_seleccion.visible = True
            columna_seleccion.update()
            etiquetador_imagen.habilitado = False
            etiquetador_imagen.update()


    def filtrar_todas_etiquetas( e: ft.ControlEvent ):
        """Selecciona las imagenes con al menos una de las etiquetas activadas en la pestaña de estadisticas."""
    
        global imagenes_tags

        if True:
            # lectura de tags seleccionados
            set_etiquetas = set()
            tags_conteo = filas_filtrado.leer_botones()
            for tag in tags_conteo:
                # extraccion del numero de repeticiones
                texto = tag.split("(")[0].strip()
                set_etiquetas.add(texto)

            # inicializacion previa al filtrado
            lista_imagenes.seleccion = imagenes_tags


            # filtrado - si no hay etiquetas de entrada devuelve todo
            lista_imagenes.seleccion = filtrar_etiquetas(lista_imagenes.seleccion, list(set_etiquetas))


            imagenes_galeria = lista_imagenes.seleccion 


            # foco en la galeria
            pestanias.selected_index = Tab.TAB_GALERIA.value
            pestanias.update()

            # reporte por snackbar (CORREGIR: es informativo pero molesto)   FIX
            renglon1 = f"Filtrado por etiquetas habilitado"
            renglon2 = f" - {len(set_etiquetas)} de {len(tags_conteo)} etiquetas seleccionadas;"
            renglon3 = f" - {len(imagenes_galeria)}  de {len(imagenes_tags)} imagenes seleccionadas."
            ventana_emergente(pagina, 
                f"{renglon1}\n{renglon2}\n{renglon3}")
            columna_etiquetas.visible = True
            columna_etiquetas.update()
        else:
            ventana_emergente(pagina, f"Filtrado por etiquetas deshabilitado.")
            # columna_etiquetas.visible = False
            columna_etiquetas.visible = True
            columna_etiquetas.update()

        # actualizacion grafica
        actualizar_componentes() # incluye prevencion de errores por clave inexistente


    # manejador del teclado
    def desplazamiento_teclado(e: ft.KeyboardEvent):
        """Permite el desplazamiento rapido de imagenes con teclas del teclado predefinidas"""
        tecla = e.key   

        numero_imagenes = len(lista_imagenes.seleccion)
        if numero_imagenes > 0:
            # prevencion de errores por posible clave inexistente
            indice = indice_clave(lista_imagenes.clave_actual, lista_imagenes.seleccion)
            if indice == None:
                lista_imagenes.clave_actual = lista_imagenes.seleccion[0].clave

            imagen = imagen_clave(lista_imagenes.clave_actual, lista_imagenes.seleccion)
            indice = lista_imagenes.seleccion.index(imagen)
            # cambio de imagen seleccionada
            cambiar_imagen = False
            # avanzar
            if tecla == "A" or tecla =="Page Up":
                indice -= 1 
                indice = indice if indice>0 else 0
                cambiar_imagen = True
            # retroceder
            elif tecla == "D" or tecla=="Page Down":
                indice += 1 
                indice = indice if indice<numero_imagenes else numero_imagenes-1
                cambiar_imagen = True
            # ir al inicio
            elif tecla == "Home":
                indice = 0
                cambiar_imagen = True
            # ir al final
            elif tecla == "End":
                indice = numero_imagenes - 1
                cambiar_imagen = True
            # restaurar imagen actual
            elif tecla == " ":  #  barra espaciadora
                etiquetador_imagen.restablecer_etiquetas("")
            # guardar imagen actual
            elif tecla == "W": 
                etiquetador_imagen.guardar_etiquetas("")
            
            if cambiar_imagen:
                imagen: Contenedor_Etiquetado
                # actualizacion de parametros
                imagen = lista_imagenes.seleccion[indice]
                lista_imagenes.clave_actual= imagen.clave 
                # carga de imagen
                actualizar_componentes()
                apuntar_galeria(lista_imagenes.clave_actual)


    def cambio_pestanias(e):
        if len(lista_imagenes.seleccion)>0:
            if pestanias.selected_index == Tab.TAB_GALERIA.value:
                apuntar_galeria(lista_imagenes.clave_actual)


    def reset_tags_filtros(e: ft.ControlEvent):
        """Restaura todos los botones de filtrado."""
        filas_filtrado.agregar_tags([], True)
        filtrar_todas_etiquetas(e)


    def guardar_tags_archivo(e: ft.FilePickerResultEvent):
        if e.path :
            ruta = e.path
            texto=f"Guardado de etiquetas en archivo\nRuta: {ruta}"

            # creación / borrado de archivo
            guardar_archivo(ruta,"",modo="w" )
            # escritura de archivo,un renglon por grupo
            tags_grupos = dataset.tags_grupos
            for lista in tags_grupos:
                texto = etiquetas2texto(lista) + "\n"
                guardar_archivo(ruta,texto,modo="a" )

        else :
            texto=f"Guardado cancelado"
        # etiquetador_imagen.guardar_dataset(INCOMPLETO)
        ventana_emergente(pagina, texto)


    def cambiar_orden_tags(e: ft.ControlEvent|None = None):
        """Reordena los botones de filtrado correspondientes a cada etiqueta detectada. """

        # Cambio de orden en caso de pulsarse el boton pertinente
        if e != None:

            if boton_reordenar_tags.valor == True:

                boton_reordenar_tags.valor = False
                boton_reordenar_tags.text = f"Orden por percentiles"
                boton_reordenar_tags.bgcolor = ft.colors.GREEN_ACCENT_700
                boton_reordenar_tags.update()

            else:

                boton_reordenar_tags.valor = True
                boton_reordenar_tags.text = f"Orden alfabético"
                boton_reordenar_tags.bgcolor = ft.colors.GREEN_800
                boton_reordenar_tags.update()

        estadisticas()
        filas_filtrado.evento_click(filtrar_todas_etiquetas)
        columna_etiquetas.update()


    def redimensionar_controles(e: ft.ControlEvent | None):

        # redimensionado etiquetador:
        etiquetador_imagen.base   = int(pagina.width/2)
        etiquetador_imagen.altura = pagina.height - 180
        # filas_filtrado.altura = pagina.height - 240
        filas_filtrado.altura = pagina.height - 400
        # columna_etiquetas.height = pagina.height - 180
        columna_etiquetas.height = pagina.height 
        columna_etiquetas.update()
        etiquetador_imagen.update()
        fila_controles.width = pagina.width 
        fila_controles.update() 


    ###########  FUNCIONES LOCALES #################


    def apuntar_galeria(clave: str):
        """Funcion auxiliar para buscar y mostrar la imagen requerida en base a su clave ('key')."""
        galeria_etiquetador.scroll_to(key=clave, duration=500)


    ###########  ASIGNACION HANDLERS #################

    entrada_tags_agregar.on_submit = agregar_tags_seleccion
    entrada_tags_quitar.on_submit  = quitar_tags_seleccion

    entrada_tags_buscar.on_submit = buscar_tags_seleccion
    entrada_tags_buscar.on_change = buscar_tags_seleccion

    pagina.on_resized = redimensionar_controles
    
    # prevencion decierre directo de aplicacion
    pagina.window_prevent_close = True
    pagina.on_window_event = confirmar_cierre_programa
    # pagina.on_window_event = dialogo_cierre_programa.abrir_alerta

    lista_dimensiones_desplegable.on_change = cargar_galeria_componentes    
    lista_estados_desplegable.on_change = cargar_galeria_componentes     
    boton_filtrar_dimensiones.click_boton = cargar_galeria_componentes   
    boton_reset_tags.on_click = reset_tags_filtros
    
    boton_reordenar_tags.on_click = cambiar_orden_tags

    # inicializacion opciones
    boton_filtrar_dimensiones.estado = False

    # propiedad de pagina: handler del teclado elegido
    pagina.on_keyboard_event = desplazamiento_teclado

    pestanias.on_change = cambio_pestanias

    # Clase para manejar dialogos de archivo y de carpeta
    dialogo_directorio   .on_result = resultado_directorio 
    dialogo_dataset      .on_result = resultado_dataset
    dialogo_guardado_tags.on_result = guardar_tags_archivo


    # Añadido de diálogos a la página
    pagina.overlay.extend([
            dialogo_directorio, dialogo_dataset, dialogo_guardado_tags
        ])

    boton_guardar.on_click = abrir_dialogo_guardado

    contenedor_seleccion.on_click = click_imagen_seleccion

    ############## CONFIGURACIONES GRAFICAS ################     
     
    ancho_pagina = 1400

    galeria_etiquetador.ancho = ancho_pagina 
    fila_controles.width = ancho_pagina 

    etiquetador_imagen.altura = altura_tab_etiquetado
    etiquetador_imagen.base = 500
    etiquetador_imagen.expand = True
    etiquetador_imagen.habilitado = False

    # Propiedades pagina 
    pagina.title = "Etiquetador Imágenes"
    pagina.window_width  = ancho_pagina
    pagina.window_min_width  = 1024
    pagina.window_height = 900
    # pagina.theme_mode = ft.ThemeMode.DARK
    pagina.theme_mode = ft.ThemeMode.LIGHT
    pagina.window_maximizable = True
    pagina.window_minimizable = True
    pagina.window_maximized   = False
    pagina.update()
    


if __name__ == "__main__":
    ft.app(target=main)