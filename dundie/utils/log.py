import logging
import os
from logging import handlers

# BOILERPLATE (código que precisa ser repetida muitas vezes)
# mas ele pode ser substituido por uma funcao que faz tudo isso, sem repeticao
# ou mesmo uma lib especifica para isso
# configuração de logs para o programa

LOG_LEVEL = os.getenv("LOG_LEVEL", "WARNING").upper()
log = logging.getLogger("dundie")
fmt = logging.Formatter(  # as variáveis a serem usadas na substituicao estão
    # são documentadas no site da lib
    "%(asctime)s  %(name)s  %(levelname)s "
    "l:%(lineno)d f:%(filename)s: %(message)s"
)


def get_logger(logfile="dundie.log"):
    """Retorna um logger configurado."""
    # ch = logging.StreamHandler()  # Console/terminal/stderr. Pode ser
    # formatado
    # ch.setLevel(LOG_LEVEL)

    fh = handlers.RotatingFileHandler(  # formata a mensagem de log e exporta
        # para um arquivo
        logfile,
        maxBytes=300,  # 10**6
        backupCount=10,  # numero de arquivos de log a serem mantidos (se 1,
        # quando o tamanho máximo for atingido, o informações anteriores serão
        # sobrescritas)
    )
    fh.setLevel(LOG_LEVEL)
    # ch.setFormatter(fmt)
    fh.setFormatter(fmt)
    # log.addHandler(ch)
    log.addHandler(fh)  # o handler "decide" o que fazer com o log
    return log
