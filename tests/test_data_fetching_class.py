import pytest
from data import CityTempData
from tasks import DataFetchingTask
CITIES = {'ABUDHABI': 'https://code.s3.yandex.net/async-module/abudhabi-response.json',
          "PARIS": "https://code.s3.yandex.net/async-module/paris-response.json"}


class TestDataFetchingTask:
    def setup(self):
        self.df = DataFetchingTask()

    def test_get_data_res(self):
        result = self.df.get_data(CITIES)
        assert isinstance(result, list)

    def test_get_data_result(self):
        result = self.df.get_data(CITIES)
        for res in result:
            assert isinstance(res, CityTempData)

    def test_type_error(self):
        with pytest.raises(TypeError):
            self.df.get_data(1)

    def test_exception(self):
        with pytest.raises(Exception):
            self.df.get_data({})
