from flask import Flask, request, jsonify

import antispam

app = Flask(__name__)

@app.route("/check", methods=["POST"])
def check():
    json = request.json
    subject = json['subject']
    content = json['content']

    try:
        is_spam_subject = antispam.is_spam(subject)
    except:
        is_spam_subject = False

    try:
        is_spam_content = antispam.is_spam(content)
    except:
        is_spam_content = False

    is_spam = is_spam_subject or is_spam_content

    return jsonify(is_spam=is_spam)
