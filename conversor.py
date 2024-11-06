from herramientas.log_date import logging
import herramientas.convert as convert
import datos


# Creo mi login del modulo
logger = logging.getLogger(__name__)


try:
    # Crear listas con el contenido de los archivos txt
    logger.info("Iniciando el proceso creando listas con el contenido de los archivos txt")
    with open(datos.txt_plantilla_config, "r") as plantilla_config:
        lista_plantilla_config = plantilla_config.readlines()

    with open(datos.txt_vlan_nueva, "r") as vlan_nueva:
        lista_vlan_nueva = vlan_nueva.readlines()

    with open(datos.txt_vlan_vieja, "r") as vlan_vieja:
        lista_vlan_vieja = vlan_vieja.readlines()

    with open(datos.txt_nombres_vlan, "r") as nombres_vlan:
        lista_nombres_vlan = nombres_vlan.readlines()

    with open(datos.txt_router_config, "r") as router_config:
        lista_router_config = router_config.readlines()
except Exception as e:
    logger.error(e)



# Creo lista con la configuracion vieja del cliente - caso cisco
lista_almacen_configs = []
for linea_vlan in lista_vlan_vieja:
    almacen_router_config = ""
    marcar_int = 0
    for linea_router_config in lista_router_config:
        if datos.interface_anterior + linea_vlan in linea_router_config:
            almacen_router_config = almacen_router_config + linea_router_config
            marcar_int = 1
        elif marcar_int == 1 and "description" in linea_router_config:
            almacen_router_config = almacen_router_config + linea_router_config
        elif marcar_int == 1 and "bandwidth" in linea_router_config:
            almacen_router_config = almacen_router_config + linea_router_config
        elif marcar_int == 1 and "encapsulation" in linea_router_config:
            almacen_router_config = almacen_router_config + linea_router_config
        elif marcar_int == 1 and "ip address" in linea_router_config:
            almacen_router_config = almacen_router_config + linea_router_config
            # aprovecho y busco el nexthop usando la IP
            lista_linea_router_config = linea_router_config.split(" ")
            address_ip = lista_linea_router_config[3]
            octecs_ip = address_ip.split(".")
            last_oct = int(octecs_ip[3]) + 1
            next_hop = octecs_ip[0] + "." + octecs_ip[1] + "." + octecs_ip[2] + "." + str(last_oct)

        elif marcar_int == 1 and "service-policy input" in linea_router_config:
            almacen_router_config = almacen_router_config + linea_router_config
        elif marcar_int == 1 and "service-policy output" in linea_router_config:
            almacen_router_config = almacen_router_config + linea_router_config
        elif marcar_int == 1 and linea_router_config == "!\n":
            # Busco las IP estaticas usando el nexthop
            almacen_route = ""
            for linea_router_router_config2 in lista_router_config:
                if "ip route" == linea_router_router_config2[:8]:
                    lista_linea_router_router_config2 = linea_router_router_config2.split(" ")
                    linea_nexthop = lista_linea_router_router_config2[4] 
                    if next_hop == linea_nexthop:
                        almacen_route = almacen_route + "no " + linea_router_router_config2
            lista_almacen_configs.append(almacen_router_config + "exit\n" + almacen_route)
            marcar_int = 0


# valido que las listas sean del mismo tamaño
if len(lista_nombres_vlan) != len(lista_vlan_vieja) or\
   len(lista_nombres_vlan) != len(lista_vlan_nueva) or\
   len(lista_nombres_vlan) != len(lista_almacen_configs):

    # REVISO CUAL VLAN NO ESTA EN EL ARCHIVO DE CONFIG DEL ROUTER
    lista_vlan_noconfig = []
    for vlan_vieja in lista_vlan_vieja:
        marca = 0
        for linea_router_config in lista_almacen_configs:
            linea_vlan = linea_router_config.split("\n")[0]
            vlan_router_config = linea_vlan.split(".")[1]
            if vlan_vieja[:-1] == vlan_router_config:
                marca = 1
        if marca == 0:
            lista_vlan_noconfig.append(vlan_vieja[:-1])
    logger.error("Error!, Las listas fuentes no tienen el mismo tamaño" + "\n" +
                 "Nombres VLAN = " + str(len(lista_nombres_vlan)) + "\n" +
                 "VLAN VIEJA = " + str(len(lista_vlan_vieja)) + "\n" +
                 "VLAN NUEVA = " + str(len(lista_vlan_nueva)) + "\n" +
                 "ALMACEN ROUTER CONFIG = " + str(len(lista_almacen_configs)) + "\n" +
                 "VLAN no presentes en el archivo del router: " + str(lista_vlan_noconfig) + "\n")

    raise ValueError("Error!, Las listas fuentes no tienen el mismo tamaño, REVISAR EL ARCHIVO LOG")


size_lista = len(lista_vlan_nueva)  # Declaro el tamaño de la lista
for index_lista in range(size_lista):
    lista_salida = []
    for linea_plantilla_config in lista_plantilla_config:
        if "VLAN_NUEVA" in linea_plantilla_config:
            tipo_valor = 1
            linea_plantilla_config = convert.reemplazo_valores(tipo_valor, index_lista, linea_plantilla_config,
                                                               lista_vlan_nueva, lista_vlan_vieja, lista_nombres_vlan,
                                                               lista_almacen_configs)
        if "VLAN_VIEJA" in linea_plantilla_config:
            tipo_valor = 2
            linea_plantilla_config = convert.reemplazo_valores(tipo_valor, index_lista, linea_plantilla_config,
                                                               lista_vlan_nueva, lista_vlan_vieja, lista_nombres_vlan,
                                                               lista_almacen_configs)
        if "NOMBRE_VLAN" in linea_plantilla_config:
            tipo_valor = 3
            linea_plantilla_config = convert.reemplazo_valores(tipo_valor, index_lista, linea_plantilla_config,
                                                               lista_vlan_nueva, lista_vlan_vieja, lista_nombres_vlan,
                                                               lista_almacen_configs)
        if "DATOS_INTERFACE_VIEJA" in linea_plantilla_config:
            tipo_valor = 4
            linea_plantilla_config = convert.reemplazo_valores(tipo_valor, index_lista, linea_plantilla_config,
                                                               lista_vlan_nueva, lista_vlan_vieja, lista_nombres_vlan,
                                                               lista_almacen_configs)
            lista_linea_interface = linea_plantilla_config.split("\n")
            almacen_interface = ""
            for item_interface in lista_linea_interface[1:]:
                if "encapsulation dot1Q" in item_interface:
                    lista_dot1q = item_interface.split(" ")
                    item_interface = "encapsulation dot1Q " + lista_vlan_nueva[index_lista][:-1]
                elif "ip address" in item_interface:
                    list_item_interface = item_interface.split(" ")
                    ip_address = list_item_interface[3]
                    mask_dec = list_item_interface[4]
                    
                    mask_bit = convert.convertir_mask(mask_dec)

                    IP_ADDRESS_BIT = ip_address + mask_bit

                elif "ip route" in item_interface:
                    if "RED1" in item_interface:
                        item_interface = item_interface.replace("RED1", "GPON")
                    if "VL" + lista_vlan_vieja[index_lista][:-1] in item_interface:
                        item_interface = item_interface.replace("VL" + lista_vlan_vieja[index_lista][:-1], "VL" + lista_vlan_nueva[index_lista][:-1])
                    item_interface = item_interface[3:]
                almacen_interface = almacen_interface + item_interface + "\n"
        if "DATOS_INTERFACE_NUEVA" in linea_plantilla_config:
            linea_plantilla_config = almacen_interface[:-1]
        if "IP_ADDRESS_BIT" in linea_plantilla_config:
            linea_plantilla_config = linea_plantilla_config.replace("IP_ADDRESS_BIT", IP_ADDRESS_BIT)
        if "RUTAS_ESTATICAS_JUN" in linea_plantilla_config:
            rutas_jun = ""
            if "ip route" in almacen_interface:
                list_almacen_interface = almacen_interface.split("\n")
                for item_almacen_interface in list_almacen_interface:
                    if "ip route" in item_almacen_interface:
                        list_item_almacen_interface = item_almacen_interface.split(" ")
                        mask_bit = convert.convertir_mask(list_item_almacen_interface[4])
                        rutas_jun = rutas_jun + "set routing-options static route " + list_item_almacen_interface[3] + mask_bit + " next-hop " + list_item_almacen_interface[5] + "\n"
                linea_plantilla_config = linea_plantilla_config.replace("RUTAS_ESTATICAS_JUN", rutas_jun)
            else:
                linea_plantilla_config = linea_plantilla_config.replace("RUTAS_ESTATICAS_JUN", "NO TIENE ESTATICAS")
        if "NEXTHOP" in linea_plantilla_config:
            if "ip route" in almacen_interface:
                list_almacen_interface = almacen_interface.split("\n")
                for item_almacen_interface in list_almacen_interface:
                    if "ip route" in item_almacen_interface:
                        list_item_almacen_interface = item_almacen_interface.split(" ")
                        nexthop = list_item_almacen_interface[4]
                        
                linea_plantilla_config = linea_plantilla_config.replace("NEXTHOP", nexthop)
            
        lista_salida.append(linea_plantilla_config)  
    string_salida = ""
    for item in lista_salida:
        string_salida = string_salida + item
    with open(datos.txt_salida + lista_nombres_vlan[index_lista][:-1] +
              "-" + lista_vlan_vieja[index_lista][:-1] +
              "-" + lista_vlan_nueva[index_lista][:-1] +
              ".txt", "w") as salida:
        print("procesando archivo " + lista_nombres_vlan[index_lista][:-1] +
              "-" + lista_vlan_vieja[index_lista][:-1] +
              "-" + lista_vlan_nueva[index_lista][:-1])
        salida.write(string_salida)
        logger.info("procesando archivo " + lista_nombres_vlan[index_lista][:-1] +
              "-" + lista_vlan_vieja[index_lista][:-1] +
              "-" + lista_vlan_nueva[index_lista][:-1])
