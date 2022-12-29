
"""Provide class for ingesting data from different types of files."""
from typing import List
from .models import IngestorInterface
from .models import CSVIngestor, PdfIngestor, DocxIngestor, TextIngestor
from .models import QuoteModel


class Ingestor(IngestorInterface):
    """Ingestor class encapsulates all helper classes for parsing different types of files."""

    importers = [CSVIngestor, PdfIngestor, DocxIngestor, TextIngestor]

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Select appropriate helper class for a given file path, based on the filetype.

        :path: the file path
        :return: the list of qutes objects 'QuoteModel'
        """
        for importer in cls.importers:
            if importer.can_ingest(path):
                return importer.parse(path)
