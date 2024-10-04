from langchain import OpenAI, LLMChain, Document
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Getting preprocessed data
preprocessed_data  = 'A rose is either a woody perennial flowering plant of the genus Rosa (/ˈroʊzə/),[4] in the family Rosaceae (/roʊˈzeɪsiːˌiː/),[4] or the flower it bears. There are over three hundred species and tens of thousands of cultivars.[5] They form a group of plants that can be erect shrubs, climbing, or trailing, with stems that are often armed with sharp prickles.[6] Their flowers vary in size and shape and are usually large and showy, in colours ranging from white through yellows and reds. Most species are native to Asia, with smaller numbers native to Europe, North America, and Northwest Africa.[6] Species, cultivars and hybrids are all widely grown for their beauty and often are fragrant. Roses have acquired cultural significance in many societies. Rose plants range in size from compact, miniature roses to climbers that can reach seven meters in height.[6] Different species hybridize easily, and this has been used in the development of the wide range of garden roses.'

# Creating a Document object
document = Document(page_content=preprocessed_data)

# Set up the embeddings and vector store
embeddings = OpenAIEmbeddings("OpenAI API")
vector_store = FAISS.from_documents([document], embeddings)

# Set up the RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
   llm = OpenAI("OpenAI API"),
   chain_type="stuff",
   retriever=vector_store.as_retriever()
)

# Ask a question
question = "What is a Rose?"
answer = qa_chain.run(question)

# Print the answer
print("Question:", question)
print("Answer:", answer)
