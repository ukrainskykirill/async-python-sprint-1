from tasks import DataCalculationTask, DataFetchingTask, DataAggregationTask
city = {"MOSCOW": "https://code.s3.yandex.net/async-module/moscow-response.json"}
result = {'city': 'Moscow',
          'data': {'avr_t': {'2022-05-26': 17.73,
                             '2022-05-27': 13.09,
                             '2022-05-28': 12.18,
                             '2022-05-29': 12.0,
                             '2022-05-30': None},
                   'c': 2.0,
                   'condition': {'2022-05-26': 7,
                                 '2022-05-27': 0,
                                 '2022-05-28': 0,
                                 '2022-05-29': 1,
                                 '2022-05-30': None},
                   't': 13.75}
          }

city2 = {
    "LONDON": "https://code.s3.yandex.net/async-module/london-response.json",
    "BERLIN": "https://code.s3.yandex.net/async-module/berlin-response.json"
}

result2 = [{'city': 'London',
            'data': {'avr_t': {'2022-05-26': 17.36,
                               '2022-05-27': 16.27,
                               '2022-05-28': 14.64,
                               '2022-05-29': None,
                               '2022-05-30': None},
                     'c': 11.0,
                     'condition': {'2022-05-26': 11,
                                   '2022-05-27': 11,
                                   '2022-05-28': 11,
                                   '2022-05-29': 0,
                                   '2022-05-30': None},
                     'raiting': 2,
                     't': 16.09}},
           {'city': 'Teltow-Fläming',
            'data': {'avr_t': {'2022-05-26': 19.27,
                               '2022-05-27': 16.0,
                               '2022-05-28': 13.64,
                               '2022-05-29': None,
                               '2022-05-30': None},
                     'c': 5.0,
                     'condition': {'2022-05-26': 9,
                                   '2022-05-27': 6,
                                   '2022-05-28': 0,
                                   '2022-05-29': 0,
                                   '2022-05-30': None},
                     'raiting': 1,
                     't': 16.3}}]


class TestDataCalculationTask:
    def setup(self):
        self.dc = DataCalculationTask()
        self.df = DataFetchingTask()
        self.da = DataAggregationTask()

    def test_avrg_temp(self):
        data = self.df.get_data(city)
        for d in data:
            assert self.dc.calculation(d) == result
