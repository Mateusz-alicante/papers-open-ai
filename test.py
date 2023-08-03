from index import PdfReader

reader = PdfReader("./docs", "./storage")

reader.read_in_pdf("paper4", "Actual name of paper")
