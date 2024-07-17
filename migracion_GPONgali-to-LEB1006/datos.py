txt_vlan_vieja = "migracion_GPONgali-to-LEB1006/lista_vlan_vieja.txt"
txt_vlan_nueva = "migracion_GPONgali-to-LEB1006/lista_vlan_nueva.txt"
txt_nombres_vlan = "migracion_GPONgali-to-LEB1006/lista_nombres_vlan.txt"
txt_salida = "migracion_GPONgali-to-LEB1006/salida/salida-"
txt_plantilla_config = "migracion_GPONgali-to-LEB1006/plantilla_config.txt"
txt_router_config = "migracion_GPONgali-to-LEB1006/router_config.txt"
interface_anterior = "interface TenGigabitEthernet1/0/3."
interface_nueva = "Po9"


interface_vieja = """interface TenGigabitEthernet0/3/0.3313
 description LASER-LAS-MERCE;ID:26533
 bandwidth 153600
 encapsulation dot1Q 3313
 ip address 172.23.238.77 255.255.255.252
 service-policy input 150M
 service-policy output 150M"""
rutas_ip = """ip route 190.94.224.72 255.255.255.252 172.23.238.78 name GPON-VL3313-TUNO-LASER-LAS-MERCE"""