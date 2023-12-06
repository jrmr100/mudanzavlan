txt_vlan_nueva = "migracion_olt_boleita/lista_vlan_nueva.txt"
txt_vlan_vieja = "migracion_olt_boleita/lista_vlan_vieja.txt"
txt_nombres_vlan = "migracion_olt_boleita/lista_nombres_vlan.txt"
txt_salida = "migracion_olt_boleita/salida/salida-"
txt_plantilla_config = "migracion_olt_boleita/plantilla_config.txt"
txt_router_config = "migracion_olt_boleita/router_config.txt"
interface_anterior = "interface Port-channel6."
interface_nueva = "interface Port-channel4."


interface_vieja = """interface TenGigabitEthernet0/3/0.3313
 description LASER-LAS-MERCE;ID:26533
 bandwidth 153600
 encapsulation dot1Q 3313
 ip address 172.23.238.77 255.255.255.252
 service-policy input 150M
 service-policy output 150M"""
rutas_ip = """ip route 190.94.224.72 255.255.255.252 172.23.238.78 name GPON-VL3313-TUNO-LASER-LAS-MERCE"""