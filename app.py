from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

class Paraphraser:
    def __init__(self, api_key, model="llama3-70b-8192"):
        self.client = Groq(api_key=api_key)  # Pass the API key to the Groq client
        self.model = model

    def paraphrase(self, text):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"paraphrase: {text}\n"
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        paraphrased_text = ""
        for chunk in completion:
            paraphrased_text += chunk.choices[0].delta.content or ""

        return paraphrased_text.strip()

# Initialize Flask app
app = Flask(__name__)

# Get API key from environment variables (or you can hardcode it for testing)
API_KEY = os.getenv("GROQ_API_KEY")  # Ensure this is set in the environment

# Initialize the paraphraser with the API key
paraphraser = Paraphraser(api_key="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")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/paraphrase', methods=['POST'])
def paraphrase_text():
    text = request.form.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    paraphrased_text = paraphraser.paraphrase(text)
    return jsonify({'paraphrased_text': paraphrased_text})

if __name__ == "__main__":
    app.run(debug=True)
