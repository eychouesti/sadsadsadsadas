# bot/utils.py

import logging
from datetime import datetime

# Logger'ı yapılandırma
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Loglama fonksiyonu
def log(message):
    logger.info(message)

# Diğer yardımcı fonksiyonlar (örnek):

def format_time(seconds):
    """Saniye cinsinden verilen süreyi saat, dakika ve saniye olarak biçimlendirir."""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
