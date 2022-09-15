import pydantic


class HourTempData(pydantic.BaseModel):
    hour: int
    temp: int
    condition: str


class ForecastDateData(pydantic.BaseModel):
    date: str
    hours: list[HourTempData]


class LocalityData(pydantic.BaseModel):
    name: str


class GeoObjectData(pydantic.BaseModel):
    locality: LocalityData


class CityTempData(pydantic.BaseModel):
    geo_object: GeoObjectData
    forecasts: list[ForecastDateData]
