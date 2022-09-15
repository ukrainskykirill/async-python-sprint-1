from utils import CITIES
from tasks import DataAnalyzingTask


def forecast_weather(city):
    """
    Анализ погодных условий по городам
    """
    start = DataAnalyzingTask()
    start.analyse(city)


if __name__ == "__main__":
    forecast_weather(CITIES)
