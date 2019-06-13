import os
import unittest
import mock

from collections import OrderedDict
from WordSearch import WordSearch, WordSearchException, run


class TestWordSearchIntegration(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        # Removes any generated output files
        data_dir = os.path.join(os.getcwd(), 'data')
        for f in os.listdir(data_dir):
            if f.endswith(".out"):
                os.remove(os.path.join(data_dir, f))

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail()
        except Exception as inst:
            self.assertEqual(inst.message, msg)

    def test_read_valid_file(self):
        expected_puzzle = ['GXWRVZNZXVAXBXN', 'LOOFIDSEOJAATMW', 'CFKDIZWOKRLMGMN', 'UOVXRNPTUCGDZIG',
                           'OJEUZMDMIMIGVLX', 'AWOCYQWQHXPHJLD', 'BEJNKRFDPKNYCFT', 'EGWFTZKRNFEFMWZ',
                           'WPTXSMWLNEYCBFD', 'AGZZZDJWMKLJJYN', 'BJTUPFCLWSVXREE', 'QFINRMZMYDNNLKB',
                           'HYLLWPTYNLCPKCH', 'TCAUNJVTWOQKXUF', 'JFPVOPYTFYIPAPB']
        expected_words = ['CHICKEN', 'COW', 'PIG']
        ws = WordSearch('data/farm.pzl')
        ws.read()
        self.assertEqual(expected_words, ws.words_to_search)
        self.assertEqual(expected_puzzle, ws.puzzle)

    @mock.patch('WordSearch.logger')
    def test_read_empty_file(self, mock_logger):
        ws = WordSearch('data/empty.pzl')
        self.assertRaises(WordSearchException, ws.read)
        self.assertEquals(mock_logger.error.call_count, 1)
        mock_logger.error.assert_called_with('Error reading file: Puzzle file is empty: data/empty.pzl')

    def test_read_missing_file(self):
        ws = WordSearch('data/no_such_file.pzl')
        self.assertRaises(WordSearchException, ws.read)

    def test_solve_valid_data(self):
        expected_results = OrderedDict()
        expected_results['DICTIONARY'] = [(1, 5), (1, 14)]
        expected_results['INTEGER'] = 'Not Found'
        expected_results['LIST'] = 'Not Found'
        expected_results['PIP'] = [(6, 10), (8, 10)]
        expected_results['PYTHON'] = [(15, 14), (10, 14)]
        expected_results['STRING'] = 'Not Found'
        expected_results['TUPLE'] = [(8, 6), (8, 2)]

        ws = WordSearch('data/python.pzl')
        ws.read()
        ws.solve()
        self.assertEquals(ws.results, expected_results)

    def test_solve_vertical_valid(self):
        expected_results = OrderedDict()
        expected_results['HEART'] = [(5, 7), (5, 3)]

        ws = WordSearch('data/suits.pzl')
        ws.read()
        for word in ws.words_to_search:
            word_reversed = word[::-1]
            ws._solve_vertical(word, word_reversed)
        self.assertEqual(ws.results, expected_results)

    def test_solve_horizontal_valid(self):
        expected_results = OrderedDict()
        expected_results['DIAMOND'] = [(7, 1), (1, 1)]

        ws = WordSearch('data/suits.pzl')
        ws.read()
        for word in ws.words_to_search:
            word_reversed = word[::-1]
            ws._solve_horizontal(word, word_reversed)
        self.assertEqual(ws.results, expected_results)

    def test_write_results_valid(self):
        expected_results = ['CHICKEN Not Found \n', 'COW (4, 6) (2, 6) \n', 'PIG (11, 6) (11, 4) \n']

        ws = WordSearch('data/farm.pzl')
        ws.read()
        ws.solve()
        ws.write()

        with open(ws.file_name + '.out', 'rw') as f:
            data = f.readlines()
            self.assertEquals(data, expected_results)

    @mock.patch('WordSearch.logger')
    def test_write_results_failure(self, mock_logger):
        expected_results = OrderedDict()
        expected_results['DIAMOND'] = [(7, 1), (1, 1)]

        ws = WordSearch('data/farm.pzl')
        ws.read()
        ws.solve()
        ws.write()

    def test_call_solve_before_read(self):
        ws = WordSearch('data/farm.pzl')
        self.assertRaisesWithMessage('No puzzle has been loaded.', ws.solve)

    def test_call_write_before_solve(self):
        ws = WordSearch('data/farm.pzl')
        self.assertRaisesWithMessage('There are no results to write.', ws.write)

    @mock.patch('WordSearch.WordSearch')
    def test_run_valid(self, mock_wordsearch):
        run(['WordSearch.py', 'data/farm.pzl'])
        self.assertEquals(mock_wordsearch.return_value.read.call_count, 1)
        self.assertEquals(mock_wordsearch.return_value.solve.call_count, 1)
        self.assertEquals(mock_wordsearch.return_value.write.call_count, 1)

    @mock.patch('WordSearch.logger')
    def test_run_too_many_arguments(self, mock_logger):
        run(['WordSearch.py', 'data/farm.pzl', 'typed to much'])
        self.assertEquals(mock_logger.warn.call_count, 2)
        self.assertTrue(mock_logger.warn.mock_calls == [mock.call('Too many arguments passed'),
                                                        mock.call(
                                                            'Please run with the following format: python WordSearch.py <file_name>')])

    @mock.patch('WordSearch.logger')
    def test_run_too_few_arguments(self, mock_logger):
        run(['WordSearch.py'])
        self.assertEquals(mock_logger.warn.call_count, 2)
        self.assertTrue(mock_logger.warn.mock_calls == [mock.call('Too few arguments passed'),
                                                        mock.call(
                                                            'Please run with the following format: python WordSearch.py <file_name>')])


if __name__ == '__main__':
    unittest.main()
