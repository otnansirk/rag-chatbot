from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from services.helper import prompt_agent_rules, guardrail_prompt
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from services.tools.check_stock import check_stock
from langchain.tools import Tool, StructuredTool
from langchain.agents import create_react_agent
from langchain.prompts import PromptTemplate
from langchain.agents import AgentExecutor
from langchain.chains import RetrievalQA

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

        # Loop all pdf files in folder
        for file in os.listdir(self.base_path):
            if file.endswith(".pdf"):
                path = os.path.join(self.base_path, file)
                loader = PDFPlumberLoader(path)
                docs = loader.load()
                documents.extend(docs)  # Join all documents

        if not documents:
            raise ValueError("Knowlages not found")

        return documents

    # Agent
    # params self
    def agent(self):
        embeding_model = "models/embedding-001"
        llm_model      = "gemini-1.5-flash"
        knowlages      = self.load_all()

        llm = ChatGoogleGenerativeAI(model=llm_model, temperature=0.3)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs_split = text_splitter.split_documents(knowlages)

        embeddings = GoogleGenerativeAIEmbeddings(model=embeding_model)
        vectorstore = FAISS.from_documents(docs_split, embeddings)

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        qa_chain_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=guardrail_prompt,
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": qa_chain_prompt}
        )

        rag_tool = Tool(
            name="retriver_tools",
            description="Untuk menjawab pertanyaan tentang inestasi",
            func=qa_chain.run
        )
        check_stock_tool = StructuredTool.from_function(
            name="check_stock",
            description=(
            "Gunakan ini untuk menjawab pertanyaan tentang ketersediaan, stok, jumlah barang. "),
            func=check_stock
        )

        tools = [rag_tool, check_stock_tool]

        # Definisikan prompt
        prompt = PromptTemplate.from_template(prompt_agent_rules)
        agent = create_react_agent(llm, tools, prompt)

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True
        )
        return agent_executor

    # Query
    # params self, query: string
    def query(self, search: str):
        response = self.agent().invoke({"input": search})
        return response