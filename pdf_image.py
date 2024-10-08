
from ironpdf import *
pdf = PdfDocument.FromFile("hero.pdf")
all_text = pdf.ExtractAllText()
