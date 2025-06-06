from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from services.helper import guardrail_prompt


class Knowlage():

    # Upload knowlage
    # params self
    def upload(self):
        pass

    # Load knowlage
    # params self
    def load(self):
        knowlages       = "panduan_investasi.pdf"
        embeding_model  = "models/embedding-001"
        llm_model       = "gemini-1.5-flash"

        loader = PDFPlumberLoader(knowlages)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs_split = text_splitter.split_documents(documents)

        embeddings = GoogleGenerativeAIEmbeddings(model=embeding_model)
        vectorstore = FAISS.from_documents(docs_split, embeddings)

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        llm = ChatGoogleGenerativeAI(model=llm_model, temperature=0.3)
        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=guardrail_prompt,
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt}
        )

        return qa_chain
    
    # Query
    # params self, query: string
    def query(self, search: str):
        response = self.load().invoke(search)
        return response