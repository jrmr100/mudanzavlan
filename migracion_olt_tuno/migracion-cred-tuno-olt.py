# OJETIVO:
# Migrar los clientes desde credicard a la nueva OLT de TUNO

from migracion_olt_tuno import datos


ruta_vlan_vieja = "migracion_olt_tuno/lista_vlan_vieja.txt"
ruta_vlan_nueva = "migracion_olt_tuno/lista_vlan_nueva.txt"
ruta_nombres_vlan = "migracion_olt_tuno/lista_nombres_vlan.txt"
ruta_plantilla_config = "migracion_olt_tuno/plantilla_config.txt"
ruta_salida = "migracion_olt_tuno/salida.txt"

# Crear lista con el contenido de los archivos txt
with open(ruta_vlan_vieja, "r") as vlan_vieja:
    lista_vlan_vieja = vlan_vieja.readlines()

with open(ruta_vlan_nueva, "r") as vlan_nueva:
    lista_vlan_nueva = vlan_nueva.readlines()

with open(ruta_nombres_vlan, "r") as nombres_vlan:
    lista_nombres_vlan = nombres_vlan.readlines()

with open(ruta_plantilla_config, "r") as plantilla_config:
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


# Cargo los valores de las listas
lista_salida = []
index_lista = 0
for vlan_nueva in lista_vlan_nueva:
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

        lista_salida.append(linea_plantilla_config)
        
        print(lista_salida)
    index_lista = index_lista + 1


with open(ruta_salida, "w") as salida:
        salida.write(linea_plantilla_config)

