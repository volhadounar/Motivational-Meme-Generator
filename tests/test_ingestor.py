import unittest
import pathlib
from functools import reduce

from QuoteEngine.ingestor import Ingestor


class TestIngestor(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.maxDiff = None
        self.source_files = [pathlib.Path(__file__).parent.resolve() / 'utils/' / 'quotesTXT.txt',
                             pathlib.Path(__file__).parent.resolve() / 'utils/' / 'quotesDOCX.docx',
                             pathlib.Path(__file__).parent.resolve() / 'utils/' / 'quotesPDF.pdf',
                           ]

    def test_parse(self):
        unique_results = set()
        for file in self.source_files:
            quotes = Ingestor.parse(str(file))
            unique_results.update(quotes)
        all_quotes_as_str = reduce(lambda prev, next: prev + next.body + next.author, unique_results, '')
        for result in ['To bork or not to bork', 'Bork', 'He who smelt it...', 'Stinky', 'RAWRGWAWGGR', 'Chewy', 'Bark like no one’s listening', 'Rex', 'Life is like peanut butter: crunchy', 'Peanut',
                       'Channel your inner husky', 'Tiny', 'Treat yo self', 'Fluffles', 'Life is like a box of treats', 'Forrest Pup', "It's the size of the fight in the dog", 'Bark Twain']:
            self.assertIn(result, all_quotes_as_str)
