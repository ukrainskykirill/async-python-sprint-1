from tasks import DataAnalyzingTask, DataAggregationTask

CITIES = {
    "LONDON": "https://code.s3.yandex.net/async-module/london-response.json",
    "BERLIN": "https://code.s3.yandex.net/async-module/berlin-response.json"
}


class TestDataAnalyzingTasks:
    def setup(self):
        self.dan = DataAnalyzingTask()
        self.da = DataAggregationTask()

    def test_analyse(self):
        assert self.dan.analyse(CITIES) == 'Берлин'
