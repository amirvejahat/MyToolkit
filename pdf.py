from PyPDF2 import PdfFileReader, PdfFileWriter

class PDF:
    

    def __init__(self,pdf_path):
        self.pdf_path = pdf_path
        self._read = PdfFileReader(open(self.pdf_path,"rb"))
        self._writer = None

    def read_page(self,page_number):
        return self._read.getPage(page_number)
    
    def _get_writer(self):
        if self._writer:
            return self._writer
        return PdfFileWriter()

    def _get_new_writer(self):
        del self._writer
        self._writer = PdfFileWriter()


    @property
    def number_of_pages(self):
        return self._read.getNumPages()
    
    
    @staticmethod
    def merge(pdfs_dir,output):
        import glob
        files = sorted(glob.glob("/".join([pdfs_dir,"*.pdf"])))
        pdf_writer = PdfFileWriter()
        for file in files:
            pdf_reader = PdfFileReader(file)
            
            for page in range(pdf_reader.getNumPages()):
                
                pdf_writer.addPage(pdf_reader.getPage(page))
        
        with open(output,"wb") as f:
            pdf_writer.write(f)   


    def split(self,page_per_pdf):
       
        page_number = 0
        self._writer = self._get_writer()
        for page_number in range(self._read.getNumPages()):
            
            self._writer.addPage(self.read_page(page_number))
            page_number += 1
            
            if page_number == page_per_pdf:

                output = self.pdf_path[:-3] + str(page_number +1 ) + ".pdf"
                with open(output,"ab") as f:
                    self._writer.write(f)
                page_number = 0
                self._get_new_writer()
        
        if page_number > 0:
            output = self.pdf_path[:-3] + str(page_number + 1 ) + ".pdf"
            with open(output,"ab") as f:
                self._writer.write(f)
    
    def rotate(self,dst_path,degree):
        
        self._writer = self._get_writer()
        for page_number in range(self.number_of_pages):
            
            tmp_page = self.read_page(page_number).rotateClockwise(degree)
            self._writer.addPage(tmp_page)
        with open(dst_path,"wb") as f:
            self._writer.write(f)

    def __repr__(self):

        self.info = self._read.getDocumentInfo()
        return f"""

            Author: {self.info.author}
            Creator: {self.info.creator}
            Subject: {self.info.subject}
            Title: {self.info.title}
            Number of pages: {self.number_of_pages}

        """
    


pdfs_dir = "/home/csr/Downloads"
pdf_path = "/home/csr/Downloads/rebin.pdf"


pdf = PDF(pdf_path)
pdf.rotate("/home/csr/Downloads/output.pdf",90)
pdf.split(5)


PDF.merge(pdfs_dir,"output.pdf")
