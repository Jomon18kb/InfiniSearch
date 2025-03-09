from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

class SearchEngine:
    def __init__(self, api_key, model="llama3-70b-8192"):
        self.client = Groq(api_key=api_key)  
        self.model = model

    def search(self, query):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Search: {query}\n"
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        search_results = ""
        for chunk in completion:
            search_results += chunk.choices[0].delta.content or ""

        return search_results.strip()


app = Flask(__name__)


API_KEY = os.getenv("GROQ_API_KEY")


search_engine = SearchEngine(api_key=API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if not query:
        return jsonify({'error': 'No search query provided'}), 400

    search_results = search_engine.search(query)
    return jsonify({'results': search_results})

if __name__ == "__main__":
    app.run(debug=True)
