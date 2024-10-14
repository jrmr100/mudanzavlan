import logging
from datetime import datetime
import datos

# Obtengo la fecha del sistema
now = datetime.now()
today = now.strftime('%d%m%Y')

# Configuro los parametros y formatos del logging
logging.basicConfig(handlers=[logging.FileHandler(filename=datos.working_directory + "conversor-" + today + ".log",
                                                  encoding='utf-8',
                                                  mode='a+')],
                    level=10,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
