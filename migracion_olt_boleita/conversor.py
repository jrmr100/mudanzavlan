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
                if "ip route" in linea_router_router_config2 and\
                     next_hop in linea_router_router_config2:
                    almacen_route = almacen_route + linea_router_router_config2
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
                elif "ip route" in item_interface:
                    if "RED1" in item_interface:
                        item_interface = item_interface.replace("RED1", "GPON")
                    if "VL" + lista_vlan_vieja[index_lista][:-1] in item_interface:
                        item_interface = item_interface.replace("VL" + lista_vlan_vieja[index_lista][:-1], "VL" + lista_vlan_nueva[index_lista][:-1])
                almacen_interface = almacen_interface + item_interface + "\n"
        if "DATOS_INTERFACE_NUEVA" in linea_plantilla_config:
            linea_plantilla_config = almacen_interface[:-1]

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
