from multiprocessing import Pool, Queue
from concurrent.futures import ThreadPoolExecutor
from queue import Empty
from typing import Optional, List, Dict
import logging
import openpyxl
from data import *
from utils import YandexWeatherAPI, RU_CITIES, CLOUDLY

logging.basicConfig(level='WARNING', filename='mylog.log')
logger = logging.getLogger()
q = Queue()


class DataFetchingTask:
    def __init__(self) -> None:
        self.yapi = YandexWeatherAPI()

    def get_data(self, cities: dict) -> List[CityTempData]:
        cities_data = []
        if len(cities) > 0:
            with ThreadPoolExecutor(max_workers=5) as thread:
                try:
                    result = thread.map(self.yapi.get_forecasting, cities)
                    logger.warning('We got data from API')
                except TypeError as e:
                    logging.warning(f'Function got the wrong type! Error {e}')
                for data in thread.map(CityTempData.parse_obj, result):
                    cities_data.append(data)
                return cities_data
        else:
            logging.warning(f'Dictionary is empty! Error {Exception}')
            raise Exception


class DataCalculationTask(DataFetchingTask):
    def __init__(self) -> None:
        super().__init__()

    def calculation(self, cityweather: CityTempData) -> Dict:
        average_temp = {}
        daily_condition = {}
        average = []
        condition = []
        for forecast in cityweather.forecasts:
            temp = []
            withoutrain = 0
            if len(forecast.hours) > 0:
                for hours in forecast.hours:
                    if 9 <= hours.hour <= 19:
                        temp.append(hours.temp)
                        if hours.condition not in CLOUDLY:
                            withoutrain += 1
                daily_condition[forecast.date] = withoutrain
                condition.append(withoutrain)
                if len(temp) > 0:
                    average_temp[forecast.date] = round((sum(temp) / len(temp)), 2)
                    average.append(round((sum(temp) / len(temp)), 2))
                else:
                    average_temp[forecast.date] = None
            else:
                average_temp[forecast.date] = None
                daily_condition[forecast.date] = None
        t = round(sum(average) / len(average), 2)
        c = round(sum(condition) / len(condition), 2)
        data = {'avr_t': average_temp, 'condition': daily_condition, 't': t, 'c': c}
        dic = {'city': cityweather.geo_object.locality.name, 'data': data}
        return dic

    @staticmethod
    def callback(response: Optional) -> None:
        q.put(response)

    def aggregation(self, cities: Dict) -> None:
        cities_data = self.get_data(cities)
        with Pool(2) as pool:
            for data in cities_data:
                pool.apply_async(self.calculation, args=(data,), callback=DataCalculationTask.callback)
            pool.close()
            pool.join()


class DataAggregationTask(DataCalculationTask):
    def init(self) -> None:
        super().__init__()

    def get_from_q(self, city: Dict) -> List:
        rate = []
        self.aggregation(city)
        for i in range(len(city)):
            try:
                data = q.get(timeout=1)
                rate.append(data)
            except Empty as e:
                logging.warning(f'Queue is empty! Error {e}')

        for index, data in enumerate(sorted(rate, key=lambda x: (x['data']['t'], x['data']['c']),
                                            reverse=True), start=1):
            data['data']['rating'] = index

        return rate

    def title(self, city: dict) -> list:
        book = openpyxl.Workbook()
        sheet = book.active
        data = self.get_from_q(city)
        sheet['A1'] = 'Страна/день'
        sheet['H1'] = 'Среднее'
        sheet['I1'] = 'Рейтинг'
        j = 1
        try:
            for d in data:
                try:
                    sheet[j + 1][0].value = RU_CITIES[d.get('city')]
                except AttributeError as e:
                    logging.warning(f'This attribute does not exist! Error {e}')
                sheet[j + 1][1].value = 'Температура, среднее'
                sheet[j + 2][1].value = 'Без осадков, часов'
                row = j + 1
                col = 2

                for temp in d.get('data').get('avr_t').values():
                    sheet[row][col].value = temp
                    col += 1
                sheet[row][col].value = d.get('data').get('t')
                sheet[row][col + 1].value = d.get('data').get('rating')

                row = j + 2
                col = 2
                for hours in d.get('data').get('condition').values():
                    sheet[row][col].value = hours
                    col += 1
                sheet[row][col].value = d.get('data').get('c')
                j += 2

            col = 2
            for dat in data[0].get('data').get('avr_t').keys():
                sheet[1][col].value = dat
                col += 1
        except AttributeError as e:
            logging.warning(f'This attribute does not exist! Error {e}')

        book.save('forecast.xlsx')
        book.close()
        return data


class DataAnalyzingTask(DataAggregationTask):
    def __init__(self) -> None:
        super().__init__()

    def analyse(self, city: dict) -> None:
        data = self.title(city)
        try:
            for d in data:
                if d.get('data').get('rating') == 1:
                    city = RU_CITIES[d.get('city')]
                    print(f'Наиболее благоприятный город - {city}')
        except AttributeError as e:
            logging.warning(f'This attribute does not exist! Error {e}')
