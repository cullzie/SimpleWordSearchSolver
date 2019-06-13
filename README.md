# SimpleWordSearchSolver
Solves vertical and horizontal word search of files passed in with correct format 

## Getting Started
The word search should be saved to a file with .pzl extension.

Sample structure of the word search in the file would be:
```
CIRN
ADOG
TCIS
KCOW

CAT
DOG
COW
```

Output will be saved to the same directory with .out extenstion:
```
CAT (1, 1) (1, 3) 
DOG (2, 2) (4, 2) 
COW (2, 4) (4, 4) 
```

To call the script pass in the path to the puzzle file:
```
python WordSearch.py farm.pzl
```

### Prerequisites
This project uses the python standard library. 
The only external library added is mock in order to run the tests. This is not available in python 2.7 by default


## Running the tests
To execute the unittests run:
```
python tests/data/tests.py
```

## Built With
* [python](https://www.python.org/downloads/release/python-2714/) - Python version used

## Authors

* **cullzie**

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details



