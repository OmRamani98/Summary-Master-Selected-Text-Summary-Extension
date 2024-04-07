from flask import Flask, jsonify, request
from flask_cors import CORS
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import pos_tag
from collections import Counter

import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

app = Flask(__name__)
CORS(app)

def preprocess_text(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    words = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return sentences, words

def extract_keywords(text, num_keywords=5):
    words = word_tokenize(text)
    pos_tags = pos_tag(words)
    stopwords_set = set(stopwords.words('english'))
    keywords = [word for word, pos in pos_tags if word.lower() not in stopwords_set and word.isalpha()]

    keyword_counts = Counter(keywords)
    most_common_keywords = keyword_counts.most_common(num_keywords)
    
    return [keyword for keyword, count in most_common_keywords]

def calculate_word_frequencies(words):
    word_frequencies = FreqDist(words)
    return word_frequencies

def calculate_sentence_scores(sentences, word_frequencies):
    sentence_scores = {}

    for i, sentence in enumerate(sentences):
        for word, freq in word_frequencies.items():
            if word in sentence.lower():
                if i not in sentence_scores:
                    sentence_scores[i] = freq
                else:
                    sentence_scores[i] += freq

    return sentence_scores

@app.route('/summary', methods=['POST'])
def generate_summary():
    data = request.get_json()
    text = data['text']
    summary_percentage = float(data['sliderValue'])  # Convert to float

    sentences, words = preprocess_text(text)
    word_frequencies = calculate_word_frequencies(words)
    sentence_scores = calculate_sentence_scores(sentences, word_frequencies)

    total_sentences = len(sentences)
    num_sentences = int(total_sentences * (summary_percentage / 100))

    sorted_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    summary_sentences = [sentences[i] for i, _ in sorted_sentences[:num_sentences]]
    summary = ' '.join(summary_sentences)

    keywords = extract_keywords(summary, num_keywords=6)

    return jsonify({'summary': summary, 'keywords': keywords})

if __name__ == "__main__":
    app.run(debug=True, port=5003)
