import os

os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"

query = "From the paper in the context, extract the following information: Datasets used for training of the computer vision model presented in the paper, year of release of the Datasets used for training of the computer vision model presented in the paper (This corresponds to the publication year of the citation pointing to the dataset). If there are multiple datasets, include all of them. Generate your response strictly in a csv format, where each entry represents a database and do not include anything else. If there is no information about the release year of the dataset substitute it by null. For example, your response can look like (without the quotes): 'Dataset name 1:null,Dataset name 2:2002'. Here Dataset name 1 has an unknown release date, and Dataset2 is released in 2002. There should be no other text in your response apart from the names of the datasets and the release years. Only include datasets that are specifically mentioned in the paper. Do not include any other datasets."
# query = """
# I want you to extract to extract the databases that are used to train the computer vision model presented in the paper given in the context.
# I also want you to find information in the paper about when the dataset was published. To do this, look through the body of the paper and the references.
# The dataset year matches the publication date of the referrenced dataset paper.
# If there are multiple datasets used in the paper, give me all of them. Only include third-party datasets. Do not include datasets created by the researchers.
# Return the results strictly in the following format:
# For each dataset, add a new line to your response, the line should contain the dataset name, followed by a comma, and then the year in which the dataset was published.
# If you cannot find information about the dataset name, specify the year as null.
# For example, your response could look like this (only what is in between the single quotes):
# '
# Dataset Name 1, 2002
# Dataset Name 2, null
# '
# Here, the paper contains two datasets: Dataset Name 1, which was published in 2002, and Dataset Name 2, for which the publication date is unkonwn.
# It is important that your response strictly follows this format. Do not include any other text besides the dataset names, and the year in which they have been published
# """

from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from csv import writer
import shutil


def removeFromFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


class PdfReader:
    def __init__(self, pdfDir, storageDir="./storage", resultPath="./result.csv"):
        self.pdfDir = pdfDir
        self.storageDir = storageDir
        self.storageDir = storageDir

    def read_in_pdf(self, pdfName, docTitle):
        removeFromFolder(self.storageDir)
        pdf_path = f"{self.pdfDir}/{pdfName}.pdf"
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()

        embeddings = OpenAIEmbeddings()
        vectordb = Chroma.from_documents(
            pages, embedding=embeddings, persist_directory=self.storageDir
        )
        vectordb.persist()
        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        pdf_qa = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(temperature=0.8, model_name="gpt-3.5-turbo"),
            vectordb.as_retriever(),
            memory=memory,
        )

        result = pdf_qa({"question": query})
        print(result["answer"])

        with open(self.storageDir + ".csv", "a") as resultCSV:
            writer_object = writer(resultCSV)
            writer_object.writerow([docTitle] + result["answer"].split(","))
