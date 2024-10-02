import os

from pathlib import Path
from typing import List, Optional

from deeptxt.core.readers import BaseReader
from deeptxt.core.document import Document

from langchain_community.document_loaders.pdf import PyPDFLoader


class PDFReader(BaseReader):
    """PDF reader using PyPDF.

    Args:
        input_file (str): File path to read.
    """

    def __init__(self, input_file: str = None):

        try:
            import pypdf  # noqa: F401
        except ImportError:
            raise ImportError("pypdf package not found, please install it with `pip install pypdf`")

        if not input_file:
            raise ValueError("You must provide a `input_dir` parameter")

        if not os.path.isfile(input_file):
            raise ValueError(f"File `{input_file}` does not exist")

        self.input_file = Path(input_file)

    def load_data(self, extra_info: Optional[dict] = None) -> List[Document]:
        """Loads data from the specified directory."""
        lc_documents = PyPDFLoader(file_path=self.input_file).load()

        return [Document().from_langchain_format(doc=doc) for doc in lc_documents]
