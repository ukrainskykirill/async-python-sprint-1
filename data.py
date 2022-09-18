from pydantic import BaseModel
from enum import Enum


class Extra(str, Enum):
    ignore = 'ignore'


class HourTempData(BaseModel):
    hour: int
    temp: int
    condition: str

    class Config:
        extra = Extra.ignore


class ForecastDateData(BaseModel):
    date: str
    hours: list[HourTempData]

    class Config:
        extra = Extra.ignore


class LocalityData(BaseModel):
    name: str

    class Config:
        extra = Extra.ignore


class GeoObjectData(BaseModel):
    locality: LocalityData

    class Config:
        extra = Extra.ignore


class CityTempData(BaseModel):
    geo_object: GeoObjectData
    forecasts: list[ForecastDateData]

    class Config:
        extra = Extra.ignore
