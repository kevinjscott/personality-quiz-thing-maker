from flask import Flask, request, jsonify, render_template
from user_summary import summarize_user_responses
from generate_image import generate_image
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questions', methods=['GET'])
def quiz_questions():
    with open('static/js/quiz_questions.json', 'r') as file:
        questions = json.load(file)
    return jsonify(questions)


@app.route('/quiz', methods=['POST'])
def quiz():
    answers = request.json['answers']
    questions = load_questions()
    paired_responses = [(questions[i]['question'], answer) for i, answer in enumerate(answers)]
    summary = summarize_user_responses(paired_responses)
    return jsonify({'summary': summary})

@app.route('/generate-image', methods=['POST'])
def generate_image_route():
    data = request.json
    image_url = generate_image(data['summary'], data['paired_responses'], "dall-e-3", data['itemType'])
    return jsonify({'image_url': image_url})

@app.route('/questions', methods=['GET'])
def get_questions():
    questions = load_questions()
    return jsonify({'questions': questions})

def load_questions():
    with open('static/js/quiz_questions.json', 'r') as file:
        questions = json.load(file)['questions']
    return questions

if __name__ == "__main__":
    app.run(debug=True, port=3000)
