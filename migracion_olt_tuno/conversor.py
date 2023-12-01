import datos as datos

ruta_salida = "migracion_olt_tuno/salida/salida-"
ruta_plantilla_config = "migracion_olt_tuno/plantilla_config.txt"


# Crear lista con el contenido de los archivos txt
with open(ruta_plantilla_config, "r") as plantilla_config:
    lista_plantilla_config = plantilla_config.readlines()
    
def reemplazo_valores(tipo_valor, datos, linea):
    linea_nueva = ""
    if tipo_valor == 1:
        linea_nueva = linea.replace("VLAN_NUEVA", datos)
        return linea_nueva
    elif tipo_valor == 2:
        linea_nueva = linea.replace("VLAN_VIEJA", datos)
        return linea_nueva
    elif tipo_valor == 3:
        linea_nueva = linea.replace("NOMBRE_VLAN", datos)
        return linea_nueva
    elif tipo_valor == 4:
        linea_nueva = linea.replace("DATOS_INTERFACE_VIEJA", datos)
        return linea_nueva
    elif tipo_valor == 5:
        linea_nueva = linea.replace("DATOS_RUTAS_VIEJA", datos)
        return linea_nueva


lista_salida = []
for linea_plantilla_config in lista_plantilla_config:
    if "VLAN_NUEVA" in linea_plantilla_config:
        tipo_valor = 1
        linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                   datos.vlan_nueva,
                                                   linea_plantilla_config)
    if "VLAN_VIEJA" in linea_plantilla_config:
        tipo_valor = 2
        linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                   datos.vlan_vieja,
                                                   linea_plantilla_config)
    if "NOMBRE_VLAN" in linea_plantilla_config:
        tipo_valor = 3
        linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                   datos.nombre_vlan,
                                                   linea_plantilla_config)
    if "DATOS_INTERFACE_VIEJA" in linea_plantilla_config:
        tipo_valor = 4
        linea_plantilla_config = reemplazo_valores(tipo_valor,
                                                   datos.interface_vieja,
                                                   linea_plantilla_config)
        lista_linea_interface = linea_plantilla_config.split("\n")
        almacen_interface = ""
        for item_interface in lista_linea_interface[1:]:
            if "encapsulation dot1Q" in item_interface:
                lista_dot1q = item_interface.split(" ")
                item_interface = "encapsulation dot1Q " + datos.vlan_nueva
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
        if "RED1"  in almacen_ruta:
            almacen_ruta = almacen_ruta.replace("RED1", "GPON")
        linea_plantilla_config = almacen_ruta.replace("VL" + datos.vlan_vieja, "VL" + datos.vlan_nueva)
    
    lista_salida.append(linea_plantilla_config)
string_salida = ""
for item in lista_salida:
    string_salida = string_salida + item
with open(ruta_salida + datos.nombre_vlan + "-" + datos.vlan_nueva + ".txt", "w") as salida:
    salida.write(string_salida)