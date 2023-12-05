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

with open(datos.txt_plantilla_config, "r") as plantilla_config:
    lista_plantilla_config = plantilla_config.readlines()

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
        linea_nueva = linea.replace("DATOS_INTERFACE_VIEJA", datos.interface_vieja)
        return linea_nueva
    elif tipo_valor == 5:
        linea_nueva = linea.replace("DATOS_RUTAS_VIEJA", datos.rutas_ip)
        return linea_nueva


lista_salida = []
size_lista = len(lista_vlan_nueva)  # Declaro el tamaño de la lista
for index_lista in range(size_lista):
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
                almacen_interface = almacen_interface + item_interface + "\n"
        if "DATOS_RUTAS_VIEJA" in linea_plantilla_config:
            tipo_valor = 5
            linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                       datos.rutas_ip,
                                                       linea_plantilla_config)
            almacen_ruta = linea_plantilla_config
        if "DATOS_INTERFACE_NUEVA" in linea_plantilla_config:
            linea_plantilla_config = almacen_interface[:-1]
        if "DATOS_RUTAS_NUEVA" in linea_plantilla_config:
            if "RED1" in almacen_ruta:
                almacen_ruta = almacen_ruta.replace("RED1", "GPON")
            linea_plantilla_config = almacen_ruta.replace("VL" + lista_vlan_vieja[index_lista][:-1], "VL" + lista_vlan_nueva[index_lista][:-1])

        lista_salida.append(linea_plantilla_config)
    string_salida = ""
    for item in lista_salida:
        string_salida = string_salida + item
    with open(datos.txt_salida + lista_nombres_vlan[index_lista][:-1] +
              "-" + lista_vlan_nueva[index_lista][:-1] +
              ".txt", "w") as salida:
        print("procesando archivo " + lista_nombres_vlan[index_lista][:-1] +
              "-" + lista_vlan_nueva[index_lista][:-1])
        salida.write(string_salida)
