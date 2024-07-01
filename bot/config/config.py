from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8')

    """Wigwam Drum Game botunun ayarları."""

    API_ID: int  # Telegram API ID'niz.
    API_HASH: str  # Telegram API Hash değeri.

    API_BASE_URL: str = "https://drumapi.wigwam.app/api"  # Wigwam API'sinin temel URL'si.

    CLAIM_FARM_INTERVAL: int = 4 * 60 * 60  # Çiftlik ödüllerinin toplanma aralığı (saniye). Varsayılan: 4 saat.
    TAP_INTERVAL: int = 60  # Dokunma (tap) işlemi aralığı (saniye). Varsayılan: 1 dakika.
    USE_PROXY: bool = False  # Proxy kullanılıp kullanılmayacağı. Varsayılan: False.
    PROXY_URL: str = None  # Proxy adresi (eğer kullanılıyorsa).

settings = Settings()  # Ayarları yükle
