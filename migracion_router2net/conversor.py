import datos

# Crear listas con el contenido de los archivos txt
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


def reemplazo_valores(tipo_valor, index_lista, linea):
    linea_nueva = ""
    if tipo_valor == 1:
        linea_nueva = linea.replace("VLAN_NUEVA", lista_vlan_nueva[index_lista][:-1])
        return linea_nueva
    elif tipo_valor == 2:
        linea_nueva = linea.replace("VLAN_VIEJA", lista_vlan_vieja[index_lista][:-1])
        return linea_nueva
    elif tipo_valor == 3:
        linea_nueva = linea.replace("NOMBRE_VLAN", lista_nombres_vlan[index_lista][:-1])
        return linea_nueva
    elif tipo_valor == 4:
        linea_nueva = linea.replace("DATOS_INTERFACE_VIEJA", lista_almacen_configs[index_lista][:-1])
        return linea_nueva


def convertir_mask(mask):
    dicc_mask = {"255.255.255.255": "/32",
                 "255.255.255.254": "/31",
                 "255.255.255.252": "/30",
                 "255.255.255.248": "/29",
                 "255.255.255.240": "/28",
                 "255.255.255.224": "/27",
                 "255.255.255.192": "/26",
                 "255.255.255.128": "/25",
                 "255.255.255.0": "/24",
                 "255.255.254.0": "/23",
                 "255.255.252.0": "/22",
                 "255.255.248.0": "/21",
                 "255.255.240.0": "/20",
                 "255.255.224.0": "/19",
                 "255.255.192.0": "/18",
                 "255.255.128.0": "/17",
                 "255.255.0.0": "/16",
                 "255.254.0.0": "/15",
                 "255.252.0.0": "/14",
                 "255.248.0.0": "/13",
                 "255.240.0.0": "/12",
                 "255.224.0.0": "/11",
                 "255.192.0.0": "/10",
                 "255.128.0.0": "/9",
                 "255.0.0.0": "/8",
                 "254.0.0.0": "/7",
                 "252.0.0.0": "/6",
                 "248.0.0.0": "/5",
                 "240.0.0.0": "/4",
                 "224.0.0.0": "/3",
                 "192.0.0.0": "/2",
                 "128.0.0.0": "/1",
                 "0.0.0.0": "/0"
                 }
    mask_bit = dicc_mask.get(mask)
    return mask_bit


# creo archivo con la configuracion vieja del cliente
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
    raise ValueError("Error!, Las listas fuentes no tienen el mismo tamaño")


size_lista = len(lista_vlan_nueva)  # Declaro el tamaño de la lista
for index_lista in range(size_lista):
    lista_salida = []
    for linea_plantilla_config in lista_plantilla_config:
        if "VLAN_NUEVA" in linea_plantilla_config:
            tipo_valor = 1
            linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                       index_lista,
                                                       linea_plantilla_config)
        if "VLAN_VIEJA" in linea_plantilla_config:
            tipo_valor = 2
            linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                       index_lista,
                                                       linea_plantilla_config)
        if "NOMBRE_VLAN" in linea_plantilla_config:
            tipo_valor = 3
            linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                       index_lista,
                                                       linea_plantilla_config)
        if "DATOS_INTERFACE_VIEJA" in linea_plantilla_config:
            tipo_valor = 4
            linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                       index_lista,
                                                       linea_plantilla_config)
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
                    
                    mask_bit = convertir_mask(mask_dec)

                    IP_ADDRESS_BIT = ip_address + mask_bit

                elif "ip route" in item_interface:
                    if "RED1" in item_interface:
                        item_interface = item_interface.replace("RED1", "GPON")
                    if "VL" + lista_vlan_vieja[index_lista][:-1] in item_interface:
                        item_interface = item_interface.replace("VL" + lista_vlan_vieja[index_lista][:-1], "VL" + lista_vlan_nueva[index_lista][:-1])
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
                        mask_bit = convertir_mask(list_item_almacen_interface[4])
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
                        nexthop = list_item_almacen_interface[5]
                        
                linea_plantilla_config = linea_plantilla_config.replace("NEXTHOP", nexthop)
            
        lista_salida.append(linea_plantilla_config)  
    string_salida = ""
    for item in lista_salida:
        string_salida = string_salida + item
    with open(datos.txt_salida + lista_nombres_vlan[index_lista][:-1] +
              "-" + lista_vlan_nueva[index_lista][:-1] +
              "-" + lista_vlan_vieja[index_lista][:-1] +
              ".txt", "w") as salida:
        print("procesando archivo " + lista_nombres_vlan[index_lista][:-1] +
              "-" + lista_vlan_nueva[index_lista][:-1] +
              "-" + lista_vlan_vieja[index_lista][:-1])
        salida.write(string_salida)
