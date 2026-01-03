import os

class Config:
    """
    Configuration class to manage environment URLs.
    Reads 'ENV' environment variable to switch between 'dev', 'staging', etc.
    Default is 'dev'.
    """
    
    ENV = os.getenv("ENV", "dev")

    URLS = {
        "dev": "http://localhost:8080/wp-login.php",
        "staging": "http://staging-example.com/wp-login.php",
        "prod": "http://example.com/wp-login.php"
    }

    @classmethod
    def get_base_url(cls):
        """Returns the base URL for the current environment."""
        if cls.ENV not in cls.URLS:
            raise ValueError(f"Environment '{cls.ENV}' is not supported. Supported: {list(cls.URLS.keys())}")
        return cls.URLS[cls.ENV]
