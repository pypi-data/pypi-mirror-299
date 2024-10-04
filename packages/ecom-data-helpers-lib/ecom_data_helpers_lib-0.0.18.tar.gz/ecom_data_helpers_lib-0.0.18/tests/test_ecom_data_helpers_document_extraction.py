import pytest
import unittest
import os

from ecom_data_helpers.document_extraction import (
    extract_docx_to_text,
    extract_pdf_to_text,
    check_file_type
)


class TestEcomDataHelpersDocumentExtraction(unittest.TestCase):

    def setUp(self):

        self.ROOT_DIR =  os.path.dirname(os.path.abspath(__file__))

    def test_extract_docx_to_text_with_sucess(self):

        filepath : str = self.ROOT_DIR + "/data/exemplo.docx"
        with open(filepath, 'rb') as file: 
            text : str = extract_docx_to_text(doc_bytes=file.read())

            assert len(text) > 100

    def test_extract_pdf_to_text_with_sucess(self):
        
        filepath : str = self.ROOT_DIR + "/data/exemplo.pdf"

        with open(filepath, 'rb') as file: 
            text,conversion_process = extract_pdf_to_text(doc_bytes=file.read())

            assert len(text) > 100
            assert conversion_process == 'raw_pdf'

    def test_extract_pdf_to_text_with_error(self):

        filepath : str = self.ROOT_DIR + "/data/exemplo_pdf_imagem.pdf"

        with open(filepath, 'rb') as file: 

            with pytest.raises(Exception, match="Can't extract info from .pdf"):
                extract_pdf_to_text(doc_bytes=file.read())

    def test_check_file_type_pdf_with_sucess(self):

        # Arrange
        # filepath_docx : str = self.ROOT_DIR + "/data/exemplo.docx"
        filepath : str = self.ROOT_DIR + "/data/exemplo.pdf"

        # Act
        with open(filepath, 'rb') as file: 
            file_type : str = check_file_type(file_bytes=file.read())

            # Assert
            assert file_type == 'pdf'

    def test_check_file_type_docx_with_sucess(self):

        # Arrange
        filepath : str = self.ROOT_DIR + "/data/exemplo.docx"

        # Act
        with open(filepath, 'rb') as file: 
            file_type : str = check_file_type(file_bytes=file.read())

            # Assert
            assert file_type == 'docx'


        




if __name__ == "__main__":
    unittest.main()