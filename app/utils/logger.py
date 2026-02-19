import logging
from datetime import datetime, timezone, timedelta

"""
Por lo general uso esta configuración de logs, amena con AWS
y con la hora seteada a Guatemala, aunque en este proyecto no 
puse muchos logs
"""
GT_TZ = timezone(timedelta(hours=-6))

class GuatemalaFormatter(logging.Formatter):
    """
    Formatter personalizado para convertir la hora UTC de Lambda
    a la hora de Guatemala en los logs.
    """
    def formatTime(self, record, datefmt=None):
    
        dt = datetime.fromtimestamp(record.created, tz=GT_TZ)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()

    def format(self, record):
        
        return super().format(record)

def setup_logger():
  
    root_logger = logging.getLogger()

  
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    formatter = GuatemalaFormatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

   
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)


    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO) 

    return root_logger


logger = setup_logger()

