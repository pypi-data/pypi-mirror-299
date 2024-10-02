import  os
import docx
import  PyPDF2

class DocumentLoader:
    """
    A class to load and process documents. 

    Supported file types:
    - Text (.txt)
    - Microsoft Word (.docx)
    - PDF (.pdf)

    Parameters:
    - file_path (str): The path to the document file.
    - pdf_mode (str): Mode to handle PDF files, default is "simple" or "complex"  is used to extract data from complex pdfs.


    """
    def __init__(self , file_path,pdf_mode="simple"):
        self.__file_path = file_path
        self.__pdf_mode=pdf_mode 
        self.__file_type = self.__get_file_type(file_path)

    def __get_file_type(self,file_path):
        """ Identify the file extension/type."""
        _,ext = os.path.splitext(file_path)
        return ext.lower()
    
    def load_document(self):
        """Main function to load documents based on file type.
                """
        if self.__file_type == ".pdf":
            return self.__load_pdf()
        elif self.__file_type == ".docx":
            return self.__load_docx()
        elif self.__file_type ==".txt":
            return self.__load_txt()
        else:
            raise ValueError(f"Unsupported file type: {self.__file_type}")

  
    def __load_pdf(self):
        """Load a PDF document and extract its text based on the specified mode.
            - mode (str): "simple" for normal/simple high quality  pdfs. 
            - mode (str): "complex" for complex pdfs with low quality .
            Start with by-default "simple" mode . If accuracy is bad  , then change mode to "complex" """
        
        if self.__pdf_mode == "simple":
            return self.__load_simple_pdf()
        elif self.__pdf_mode == "complex":
            return self.__load_complex_pdf()
        else:
            raise ValueError("Invalid mode. Choose 'simple' or 'complex'.")
    
    def __load_simple_pdf(self):
        """Load a complex pdf document and extract its text.
        Parameters:
            - file_path (str): The path to the pdf file.
            - mode (str): "simple" """
        
        with open(self.__file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
        return text

    def __load_complex_pdf(self):
        """Load a complex pdf document and extract its text.
        Parameters:
            - file_path (str): The path to the pdf file.
            - mode(str) : "complex" """
        # Implement your complex PDF processing code
        

    

    def __load_docx(self):
        """Load a DOCX document and extract its text.
        Parameters:
            - file_path (str): The path to the docx file."""
        
        doc = docx.Document(self.__file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
   
    def __load_txt(self):
        """Load a TXT document and extract its text.
        Parameters:
            - file_path (str): The path to the text file.
        """

        with open(self.__file_path, "r", encoding="utf-8") as file:
            text = file.read()
        return text


