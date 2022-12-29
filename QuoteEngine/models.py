"""Provide classes for ingesting data from different types of files.

Module contains abstract class with two methods 'can_ingest', 'parse' and
then realizes this class with several different classes:
CSVIngestor, PdfIngestor, DocxIngestor and TextIngestor.

Each class knows the strategy how to parse the file of relevant type.
"""
from typing import List
import csv
import os
import logging
import subprocess
from abc import ABC, abstractmethod
from docx import Document
import docx
import random
from string import whitespace

from .constants import QUOTE_AUTHOR_SEPARATOR


class QuoteModel:
    """QuoteModel with two fields: 'body' and 'author'."""

    def __init__(self, body, author):
        """Construct a new `QuoteModel` from quote and the author.

        :param body: A 2-argument predicates quote body.
        :param author: The author value to whom quot belongs to.
        """
        self.body = body
        self.author = author
    
    def __eq__(self, __o: object) -> bool:
        """Compare two objects by comparing thier properties.
        
        :param __o: the object to compare
        :return: the result of comparing
        """
        return self.body == __o.body and self.author == __o.author
    
    def __hash__(self):
        """Hash object.
        
        :return: the object address
        """
        return id(self)
    
    def __repr__(self):
        """Define object representation for the output."""
        return f'{self.body} - {self.author}'


class IngestorInterface(ABC):
    """A general superclass for ingestors from different types of files.

    An 'IngestorInterface' represents the parsing method for some text
    in the file and turing it into the object .

    It is used as class object with calling the parse method.

    Concrete subclasses can override the `parse` classmethod to provide custom
    behavior to be able to ingest data from the file.
    """

    type_ = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Define if the file can be processed by ingestor.

        :param path: the file path on the disk.
        """
        parts = path.split('.')
        ext = parts[-1]
        return ext in cls.type_

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse text from file and turn it into the list of models 'QuoteModel'.

        Concrete subclasses must override this method to be able to
        parse the text from file based on filetype.

        :param path: the file path on the disk.
        """
        pass


class CSVIngestor(IngestorInterface):
    """A sublass for IngestorInterface superclass for dealing with csv file."""

    type_ = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse text from csv file and turn it into the list of models 'QuoteModel'.

        :param path: the file path on the disk.
        :return: the sequence of 'QuoteModel'
        """
        if not cls.can_ingest(path):
            logging.error(f'Cannot ingest {path}')
            raise Exception('Cannot ingest', path)

        quotes = []
        try:
            with open(path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    quotes.append(QuoteModel(row['body'], row['author']))
        except KeyError:
            logging.error('Csv file has wrong header names')
            raise
        except FileNotFoundError:
            logging.error(f'Cannot open file {path}')
            raise
        return quotes


class PdfIngestor(IngestorInterface):
    """A sublass for IngestorInterface superclass for dealing with pdf file."""

    type_ = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse text from pdf file and turn it into the list of models 'QuoteModel'.

        :param path: the filepath on the disk.
        :return: the sequence of 'QuoteModel'
        """
        if not cls.can_ingest(path):
            raise Exception('Cannot ingest', path)

        tmp = f'./{random.randint(0,100000000)}.txt'
        call = subprocess.call(['pdftotext', path, tmp])

        file_ref = open(tmp, 'r')
        quotes = []

        try:
            for line in file_ref:
                items = line.strip().split(' "')
                for item in items:
                    parsed_item = item.split(QUOTE_AUTHOR_SEPARATOR)
                    if len(parsed_item) >= 2:
                        quotes.append(
                            QuoteModel(parsed_item[0].strip(whitespace + '"'), parsed_item[1].strip(whitespace + '"'))
                        )
        except FileNotFoundError:
            logging.error(f'Cannot open file {path}')
            raise
        except IndexError:
            logging.error(f'Pdf file {path} has wrongly built data.')
            raise
        file_ref.close()
        os.remove(tmp)
        return quotes


class DocxIngestor(IngestorInterface):
    """A sublass for IngestorInterface superclass for dealing with docx file."""

    type_ = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse text from docx file and turn it into the list of models 'QuoteModel'.

        :param path: the filepath on the disk.
        :return: the sequence of 'QuoteModel'
        """
        if not cls.can_ingest(path):
            logging.error(f'Cannot ingest {path}')
            raise Exception('Cannot ingest', path)

        quotes = []
        try:
            doc = Document(path)
        except docx.opc.exceptions.PackageNotFoundError:
            logging.error(f'Cannot open file {path}')
            raise

        for el in doc.paragraphs:
            if el.text != "":
                info_line = el.text.split(QUOTE_AUTHOR_SEPARATOR)
                if len(info_line) < 2:
                        continue
                quotes.append(
                    QuoteModel(info_line[0].strip(whitespace + '"'), info_line[1].strip(whitespace + '"'))
                )
        return quotes


class TextIngestor(IngestorInterface):
    """A sublass for IngestorInterface superclass for dealing with txt file."""

    type_ = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse text from txt file and turn it into the list of models 'QuoteModel'.

        :param path: the filepath on the disk.
        :return: the sequence of 'QuoteModel'
        """
        if not cls.can_ingest(path):
            logging.error(f'Cannot ingest {path}')
            raise Exception('Cannot ingest', path)

        quotes = []
        try:
            with open(path) as f:
                for line in f:
                    info_line = line.split(QUOTE_AUTHOR_SEPARATOR)
                    if len(info_line) < 2:
                        continue
                    quotes.append(
                        QuoteModel(info_line[0].strip(whitespace + '"'), info_line[1].strip(whitespace + '"'))
                    )
        except FileNotFoundError:
            logging.error(f'Cannot open file {path}')
            raise
        except IndexError:
            logging.error(f'Txt file {path} has wrongly built data.')
            raise
        return quotes
