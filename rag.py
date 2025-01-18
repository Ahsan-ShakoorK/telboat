import openai
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAGSystem:
    def __init__(self, openai_api_key, data):
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.data = data
        self._setup_faiss_index()

    def _setup_faiss_index(self):
        data_texts = [item["text"] for item in self.data]
        data_embeddings = self.embedding_model.encode(data_texts)
        dimension = data_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(data_embeddings)

    def retrieve_relevant_data(self, query, top_k=5):
        query_embedding = self.embedding_model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        relevant_data = [self.data[i] for i in indices[0]]
        return relevant_data

    def generate_response(self, query):
        if "who are you" in query.lower():
            return "I'm the LATOKEN bot! I can help you learn about LATOKEN, the Hackathon, and the Culture Deck. 😊"

        relevant_data = self.retrieve_relevant_data(query)
        if not relevant_data:
            return "I don't have information on that topic. Please check LATOKEN's official website for more details. 😊"

        context = "\n".join([item["text"] for item in relevant_data])

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant based on the provided context."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ],
                max_tokens=100,
                temperature=0.3,
            )
            bot_response = response.choices[0].message.content
        except Exception as e:
            bot_response = context

        return bot_response

    def ask_follow_up_question(self):
        follow_up_questions = [
            "Why does LATOKEN help people learn about and buy assets?",
            "What is the purpose of the Sugar Cookie Test?",
            "Why is a Wartime CEO necessary?",
            "In what situations is stress beneficial, and in what situations is it harmful?"
        ]
        # Cycle through the questions or select based on the context
        return follow_up_questions[0]