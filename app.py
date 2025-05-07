from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from transformers import pipeline
import warnings

warnings.filterwarnings("ignore", message="Some weights of the model checkpoint...")

qa_pipeline = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")

app = Flask(__name__)

qa_dict = {}
with open('qa.txt', 'r') as file:
    for line in file:
        question, answer = line.strip().split('|')
        qa_dict[question.lower()] = answer

recognizer = sr.Recognizer()
def extract_answer_from_text(text, question):
    complete_answer = ""

    chunk_size = 100000
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i + chunk_size]
        answer = qa_pipeline(question=question, context=chunk)
        complete_answer += answer['answer']

    return complete_answer

with open("text1.txt", "r", encoding="utf-8") as file:
    text1_contents = file.read()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('input')
    user_input = user_input.lower()
    bot_response = ""

    if user_input in qa_dict:
        bot_response = qa_dict[user_input]
    else:
        bot_response = find_best_match(user_input, qa_dict)

    if bot_response is None:
        bot_response = extract_answer_from_text(text1_contents, user_input)

    if not bot_response:
        bot_response = "I'm not sure how to answer that question."    

    return jsonify({'response': bot_response})

def find_best_match(question, qa_data):
    best_match = None
    best_score = 0

    for q, a in qa_data.items():
        q_tokens = set(q.split())
        question_tokens = set(question.split())
        common_tokens = q_tokens.intersection(question_tokens)
        score = len (common_tokens)

        if score > best_score:
            best_match = a
            best_score = score

    return best_match

@app.route('/voice_input', methods=['POST'])
def voice_input():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            recognized_speech = recognizer.recognize_google(audio)
            return jsonify({'input': recognized_speech})
    except sr.WaitTimeoutError:
        return jsonify({'input': ""})
    except sr.UnknownValueError:
        return jsonify({'input': ""})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
