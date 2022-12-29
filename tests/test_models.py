import pathlib
import unittest
import docx

from QuoteEngine.ingestor import CSVIngestor, QuoteModel, PdfIngestor, DocxIngestor, TextIngestor

SOURSE_FOLDER = pathlib.Path(__file__).parent.resolve() / 'utils/'

class TestCSVIngestor(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.file_name =  SOURSE_FOLDER / 'quotesCSV.csv'
    
    def test_parse(self):
        quotes = CSVIngestor.parse(str(self.file_name))
        self.assertEqual(quotes, [QuoteModel('Chase the mailman', 'Skittle'), QuoteModel('When in doubt, go shoe-shopping', 'Mr. Paws')])
        
    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            CSVIngestor.parse('unknownfile.csv')
            
    def test_cannot_ingest(self):
        with self.assertRaises(Exception) as ex:
            CSVIngestor.parse('file.txt')
        self.assertEqual("('Cannot ingest', 'file.txt')", str(ex.exception))


class TestPDFIngestor(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.maxDiff = None
        self.file_name = SOURSE_FOLDER / 'quotesPDF.pdf'

    def test_parse(self):
        quotes = PdfIngestor.parse(str(self.file_name))
        self.assertEqual(quotes, [QuoteModel('Treat yo self', 'Fluffles'),
                                  QuoteModel('Life is like a box of treats', 'Forrest Pup'),
                                  QuoteModel("It's the size of the fight in the dog", 'Bark Twain'),
                                 ])

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            PdfIngestor.parse('unknownfile.pdf')
            
    def test_cannot_ingest(self):
        with self.assertRaises(Exception) as ex:
            PdfIngestor.parse('file.txt')
        self.assertEqual("('Cannot ingest', 'file.txt')", str(ex.exception))

  
class TestDocxIngestor(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.maxDiff = None
        self.file_name = SOURSE_FOLDER / 'quotesDOCX.docx'
    
    def test_parse(self):
        quotes = DocxIngestor.parse(str(self.file_name))
        self.assertEqual(quotes, [QuoteModel('Bark like no one’s listening', 'Rex'),
                                  QuoteModel('RAWRGWAWGGR', 'Chewy'),
                                  QuoteModel('Life is like peanut butter: crunchy', 'Peanut'),
                                  QuoteModel('Channel your inner husky', 'Tiny'),
                                 ])

    def test_file_not_found(self):
        with self.assertRaises(docx.opc.exceptions.PackageNotFoundError):
            DocxIngestor.parse('unknownfile.docx')
            
    def test_cannot_ingest(self):
        with self.assertRaises(Exception) as ex:
            DocxIngestor.parse('file.txt')
        self.assertEqual("('Cannot ingest', 'file.txt')", str(ex.exception))


class TestTxtIngestor(unittest.TestCase):
    @classmethod
    def setUpClass(self) -> None:
        self.maxDiff = None
        self.file_name = SOURSE_FOLDER / 'quotesTXT.txt'
    
    def test_parse(self):
        quotes = TextIngestor.parse(str(self.file_name))
        print(quotes)
        self.assertEqual(quotes, [QuoteModel('To bork or not to bork', 'Bork'),
                                  QuoteModel('He who smelt it...', 'Stinky'),
                                 ])

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            TextIngestor.parse('unknownfile.txt')
            
    def test_cannot_ingest(self):
        with self.assertRaises(Exception) as ex:
            TextIngestor.parse('file.pdf')
        self.assertEqual("('Cannot ingest', 'file.pdf')", str(ex.exception))
