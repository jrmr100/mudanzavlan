def reemplazo_valores(tipo_valor, index_lista, linea, lista_vlan_nueva,
                      lista_vlan_vieja, lista_nombres_vlan, lista_almacen_configs):
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