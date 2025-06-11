from langchain_community.document_loaders import PDFPlumberLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, AgentType
# from langchain.agents.agent_toolkits import create_retriever_tool
from langchain.tools import Tool
from services.helper import guardrail_prompt, rules_prompt

import os



class Knowlage:

    def __init__(self, company: str):
        self.company = company
        self.base_path = f"knowlages/{self.company}"

    # Upload knowlage
    # params self
    def upload(self):
        pass


    # Load knowlages
    # params self
    def load_all(self):
        if not os.path.exists(self.base_path):
            raise FileNotFoundError(f"Knowlage not found: {self.base_path}")

        documents = []

        # Loop semua file PDF dalam folder
        for file in os.listdir(self.base_path):
            if file.endswith(".pdf"):
                path = os.path.join(self.base_path, file)
                loader = PDFPlumberLoader(path)
                docs = loader.load()
                documents.extend(docs)  # Gabung semua dokumen

        if not documents:
            raise ValueError("Knowlages not found")

        return documents

    # Load knowlage
    # params self
    def agent(self):
        embeding_model = "models/embedding-001"
        llm_model      = "gemini-1.5-flash"
        knowlages      = self.load_all()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs_split = text_splitter.split_documents(knowlages)

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

        rag_tools = Tool(
            name="retriver_tools",
            description=rules_prompt,
            func=qa_chain.run,
            return_direct=True
        )

        tools = [rag_tools]
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=True,
            verbose=True,
            agent_kwargs={
                "system_message": rules_prompt
            }
        )

        return agent

    # Query
    # params self, query: string
    def query(self, search: str):
        response = self.agent().invoke(search)
        return response