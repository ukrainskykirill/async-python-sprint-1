from tasks import DataCalculationTask, DataFetchingTask, DataAggregationTask
cities = {"MOSCOW": "https://code.s3.yandex.net/async-module/moscow-response.json"}
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


class TestDataCalculationTask:
    def setup(self) -> None:
        self.dc = DataCalculationTask()
        self.df = DataFetchingTask()
        self.da = DataAggregationTask()

    def test_calculation(self) -> None:
        for city in cities:
            data = self.df.get_data(city)
        for d in data:
            assert self.dc.calculation(d) == result

