from pydantic_settings import SettingsConfigDict, BaseSettings

class Setting(BaseSettings):
    APP_NAME: str = "StauBook"
    DATABSE_URL : str
    
    model_config = SettingsConfigDict(env_file="backend/.env", 
                                      extra="ignore")
    
    
config = Setting()