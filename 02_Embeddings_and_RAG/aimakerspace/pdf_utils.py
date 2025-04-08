import os
from typing import List
import PyPDF2

class PDFFileLoader:
    """
    Loads PDF files from a given directory or a single PDF file.
    """
    def __init__(self, path: str):
        self.path = path
        self.documents = []

    def load(self):
        if os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path) and self.path.lower().endswith(".pdf"):
            self.load_file(self.path)
        else:
            raise ValueError(
                "Provided path is neither a valid directory nor a .pdf file."
            )

    def load_file(self, file_path: str):
        """Reads a single PDF file and extracts its text."""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            self.documents.append(text)

    def load_directory(self):
        """Walks through a directory, loading all PDF files found."""
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.lower().endswith(".pdf"):
                    self.load_file(os.path.join(root, file))

    def load_documents(self) -> List[str]:
        """Loads the PDF documents and returns their text."""
        self.load()
        return self.documents


class CharacterTextSplitter:
    """
    Splits text into chunks based on a specified chunk size and overlap.
    """
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        if chunk_size <= chunk_overlap:
            raise ValueError("Chunk size must be greater than chunk overlap")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        # Use steps of chunk_size - chunk_overlap to create overlapping chunks
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


def load_pdf_chunks(path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Reads PDF files from a directory (or a single PDF file) located at 'path',
    extracts the text, splits it into chunks, and returns a list of text chunks.

    Args:
        path (str): The directory or file path to the PDF files.
        chunk_size (int, optional): Maximum size of each text chunk. Defaults to 1000.
        chunk_overlap (int, optional): The overlap size between consecutive chunks. Defaults to 200.

    Returns:
        List[str]: A list of text chunks extracted from the PDF documents.
    """
    loader = PDFFileLoader(path)
    documents = loader.load_documents()
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_texts(documents)





if __name__ == "__main__":
    loader = PDFFileLoader("data/pdf")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
