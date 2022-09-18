from tasks import DataAnalyzingTask
data = [{'city': 'London',
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
                    'rating': 2,
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
                    'rating': 1,
                    't': 16.3}}]


class TestDataAnalyzingTasks:
    def setup(self) -> None:
        self.da = DataAnalyzingTask()

    def test_analyse(self) -> None:
        assert self.da.analyse(data) == ['Берлин']

