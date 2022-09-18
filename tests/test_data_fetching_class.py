from pytest import raises
from data import CityTempData
from tasks import DataFetchingTask
CITIES = {'ABUDHABI': 'https://code.s3.yandex.net/async-module/abudhabi-response.json',
          "PARIS": "https://code.s3.yandex.net/async-module/paris-response.json"}


class TestDataFetchingTask:
    def setup(self) -> None:
        self.df = DataFetchingTask()

    def test_get_data_res(self) -> None:
        for city in CITIES:
            result = self.df.get_data(city)
            assert isinstance(result, list)

    def test_get_data_result(self) -> None:
        for city in CITIES:
            result = self.df.get_data(city)
            for res in result:
                assert isinstance(res, CityTempData)

    def test_exception(self):
        with raises(Exception):
            self.df.get_data({})
