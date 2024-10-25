# config.py
import logging

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "12345678"

LOG_FILE="chatbot/log_file/chatbot.log"

def setup_logging(log_file=LOG_FILE,level=logging.INFO):
    """
    Bu fonksiyon, loglama ayarlarını yapılandırır.

    Parametreler:
        log_file: Logların kaydedileceği dosyanın yolu (varsayılan config.LOG_FILE).
        level: Loglama seviyesi (varsayılan INFO).

    Yaptığı İşlemler:
        1. Loglama ayarlarını yapılandırır (log dosyası, seviye, format vb.).
    
    """
    logging.basicConfig(
        filename=log_file,
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S", 
    )
    