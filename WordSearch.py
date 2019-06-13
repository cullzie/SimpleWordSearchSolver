import os
import sys
import logging
import functools

from collections import OrderedDict


logging.basicConfig()
logger = logging.getLogger(__name__)


def check_prerequisites(func):
    @functools.wraps(func)
    def wrap(self, *args, **kwargs):
        if func.__name__ == 'write':
            if not self.results:
                raise WordSearchException('There are no results to write.')
        elif func.__name__ == 'solve':
            if not self.puzzle:
                raise WordSearchException('No puzzle has been loaded.')
        return func(self, *args, **kwargs)

    return wrap


class WordSearchException(Exception):
    """
    Exception class for custom handling of errors in the WordSearch class

    """
    def __init__(self, message):
        super(WordSearchException, self).__init__(message)


class WordSearch(object):
    def __init__(self, puzzle_file_location):
        self.path_to_puzzle = puzzle_file_location
        self.file_name = puzzle_file_location.split('.')[0]

        self.puzzle = list()
        self.words_to_search = list()
        self.results = OrderedDict()

    def _solve_horizontal(self, word, word_reversed):
        """
        Finds any matches in rows of the wordsearch

        :param str word: Word to find in the row of the wordsearch
        :param str word_reversed: Word in reverse order to find in the row of the wordsearch
        :return: None
        """
        solved = False
        for x_coordinate, row in enumerate(self.puzzle):
            word_found = word.upper() in row.upper()
            reversed_word_found = word_reversed.upper() in row.upper()

            if word_found:
                start = row.find(word) + 1
                end = row.find(word) + len(word)
            elif reversed_word_found:
                start = row.find(word_reversed) + len(word_reversed)
                end = row.find(word_reversed) + 1

            if word_found or reversed_word_found:
                actual_row = x_coordinate + 1
                self.results[word] = [(start, actual_row), (end, actual_row)]
                solved = True
                return solved
        return solved

    def _solve_vertical(self, word, word_reversed):
        """
        Finds any matches in columns of the wordsearch


        :param str word: Word to find in the row of the wordsearch
        :param str word_reversed: Word in reverse order to find in the row of the wordsearch
        :return: None
        """
        solved = False
        for x_coordinate in range(len(self.puzzle)):
            column = ''
            for y_coordinate, row in enumerate(self.puzzle):
                column = column + row[x_coordinate]
                actual_column = x_coordinate + 1

                word_found = word.upper() in column.upper()
                reversed_word_found = word_reversed.upper() in column.upper()

                if word_found:
                    start = column.find(word) + 1
                    end = column.find(word) + len(word)
                elif reversed_word_found:
                    start = column.find(word_reversed) + len(word_reversed)
                    end = column.find(word_reversed) + 1

                if word_found or reversed_word_found:
                    self.results[word] = [(actual_column, start), (actual_column, end)]
                    solved = True
                    return solved
        return solved

    @check_prerequisites
    def solve(self):
        """
        Solves the wordSearch and adds the result to self.result OrderedDict

        :return: None
        """

        for word in self.words_to_search:
            word_reversed = word[::-1]

            if not self._solve_horizontal(word, word_reversed) and not self._solve_vertical(word, word_reversed):
                self.results[word] = 'Not Found'

    @check_prerequisites
    def read(self):
        """
        Reads the WordSearch file into the object
        puzzle attribute contains the wordsearch
        words_to_search attribute contains list of words to find

        :return: None
        """
        try:
            with open(self.path_to_puzzle, 'r') as f:
                lines = f.readlines()
                if lines:
                    split_data = ''.join(lines).split(os.linesep + os.linesep)
                    self.puzzle = split_data[0].split(os.linesep)
                    self.words_to_search = split_data[1].split(os.linesep)
                else:
                    raise WordSearchException('Puzzle file is empty: {0}'.format(self.path_to_puzzle))
        except IOError as e:
            raise WordSearchException('The file name passed in does not exist: {0}'.format(self.path_to_puzzle))
        except Exception as e:
            logger.error('Error reading file: {0}'.format(str(e)))
            raise WordSearchException('Error occurred while reading the file: {0}'.format(self.path_to_puzzle))

    @check_prerequisites
    def write(self):
        """
        Writes the result file in the correct format to the same directory as the puzzle file.
        Has .out file extension

        :return: None
        """

        try:
            with open(self.file_name + '.out', 'w+') as w:
                for k, v in self.results.items():
                    if isinstance(v, str):
                        w.write('{0} {1} {2}'.format(k, v, os.linesep))
                    else:
                        w.write('{0} {1} {2} {3}'.format(k, v[0], v[1], os.linesep))
        except Exception as e:
            logger.error('Error writing file: {0}'.format(str(e)))


def run(args):
    try:
        if len(args) == 2:
            path_to_puzzle = args[1]
            word_search = WordSearch(path_to_puzzle)
            word_search.read()
            word_search.solve()
            word_search.write()
        elif len(args) < 2:
            logger.warn('Too few arguments passed')
            logger.warn('Please run with the following format: python WordSearch.py <file_name>')
        elif len(args) > 2:
            logger.warn('Too many arguments passed')
            logger.warn('Please run with the following format: python WordSearch.py <file_name>')
    except WordSearchException as exc:
        logger.error('Exception occurred while running the program: {0}'.format(exc.message))
    except Exception as exc:
        logger.error('An Un-handled Exception occured while running the program: {0}'.format(exc.message))


if __name__ == '__main__':
    run(sys.argv)
