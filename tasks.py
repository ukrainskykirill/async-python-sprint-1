from multiprocessing import Pool, Queue, Pipe
from concurrent.futures import ThreadPoolExecutor
from queue import Empty
import logging
import openpyxl
from data import CityTempData
from utils import YandexWeatherAPI, RU_CITIES, CLOUDLY, CITIES

logging.basicConfig(level='WARNING', filename='mylog.log')
logger = logging.getLogger()


class DataFetchingTask:
    def __init__(self) -> None:
        self.yapi = YandexWeatherAPI()

    def get_data(self, cities: dict) -> list[CityTempData]:
        cities_data = []
        if cities:
            data_result = self.yapi.get_forecasting(cities)
            city_temp = CityTempData.parse_obj(data_result)
            cities_data.append(city_temp)
            logger.warning('We got data from API')
        else:
            logger.warning('Dict is empty')
            raise Exception
        return cities_data


class DataCalculationTask(DataFetchingTask):
    def __init__(self) -> None:
        super().__init__()

    def calculation(self, cityweather: CityTempData) -> dict:
        average_temp = {}
        daily_condition = {}
        average = []
        condition = []
        for forecast in cityweather.forecasts:
            temp = []
            withoutrain = 0
            if forecast.hours:
                for hours in forecast.hours:
                    if 9 <= hours.hour <= 19:
                        temp.append(hours.temp)
                        if hours.condition not in CLOUDLY:
                            withoutrain += 1
                if len(temp) > 0:
                    average_temp[forecast.date] = round((sum(temp) / len(temp)), 2)
                    average.append(round((sum(temp) / len(temp)), 2))
                    daily_condition[forecast.date] = withoutrain
                    condition.append(withoutrain)
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
    def callback(response: dict) -> None:
        q.put(response)


class DataAggregationTask(DataCalculationTask):
    def init(self) -> None:
        super().__init__()

    def get_from_q(self, conn) -> list:
        rate = []
        try:
            while True:
                rate.append(q.get(timeout=1.5))
        except Empty as e:
            logging.warning(f'Queue is empty! Error {e}')

        for index, data in enumerate(sorted(rate, key=lambda x: (x['data']['t'], x['data']['c']),
                                            reverse=True), start=1):
            data['data']['rating'] = index
        conn.send(rate)
        return rate

    def title(self, data_for_writing: list) -> None:
        book = openpyxl.Workbook()
        sheet = book.active
        sheet['A1'] = 'Страна/день'
        sheet['H1'] = 'Среднее'
        sheet['I1'] = 'Рейтинг'
        j = 1
        try:
            for d in data_for_writing:
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

                col = 7
                sheet[row][col].value = d.get('data').get('c')
                j += 2

            col = 2
            for dat in data_for_writing[0].get('data').get('avr_t').keys():
                sheet[1][col].value = dat
                col += 1
        except AttributeError as e:
            logging.warning(f'This attribute does not exist! Error {e}')
        book.save('forecast.xlsx')
        book.close()


class DataAnalyzingTask(DataAggregationTask):
    def __init__(self) -> None:
        super().__init__()

    def analyse(self, anylyse: list) -> list:
        the_best_city = []
        for a in anylyse:
            try:
                if a.get('data').get('rating') == 1:
                    city = RU_CITIES[a.get('city')]
                    the_best_city.append(city)
                    print(f'Наиболее благоприятный город - {city}')
            except AttributeError as e:
                logging.warning(f'This attribute does not exist! Error {e}')
        return the_best_city


if __name__ == "__main__":
    first, second = Pipe()
    q = Queue(15)
    a = DataAnalyzingTask()
    with ThreadPoolExecutor(15) as thread:
        data = thread.map(a.get_data, CITIES)
    with Pool(3) as pool:
        for d in data:
            pool.apply_async(a.calculation, d, callback=a.callback)
        result = a.get_from_q(first)
        a.analyse(second.recv())
        pool.apply_async(a.title, (result,))
        pool.close()
        pool.join()
