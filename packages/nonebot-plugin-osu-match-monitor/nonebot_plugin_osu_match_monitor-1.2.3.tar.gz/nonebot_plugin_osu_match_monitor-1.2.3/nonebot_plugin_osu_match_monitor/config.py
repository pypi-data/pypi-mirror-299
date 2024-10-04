from pydantic import BaseModel

class Config(BaseModel):
    osu_api_key: str = ""
    osu_refresh_interval: int = 2
