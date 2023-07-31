from flask import Flask, render_template, request
from spell_checker_model import spell_checker
from manage_word import add_new_word

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        input_text = request.form['input_text']
        result = spell_checker(input_text)
        words = [ x['word'] for x in result['result'] ]
        return render_template('result.html', input_text=input_text, result=result, words=words)
    
@app.route('/addToDict')
def addToDict():
    new_word = request.args.get('new_word')
    if new_word:
        success = add_new_word(new_word)
        return render_template('addToDict.html', new_word=new_word, success=success)
    else:
        return render_template('addToDict.html')  # No input, so render the template without showing the alert

if __name__ == '__main__':
    app.run(debug=True)