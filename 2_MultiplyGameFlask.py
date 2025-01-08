from flask import Flask, render_template, request, redirect, url_for
import random

app = Flask(__name__,template_folder='D:/MKR50/IntelJ/Workspace/Python/mkk/pk')

# Route for the home page
@app.route('/',methods=['GET'])
def home():
    # Generate two random numbers for the multiplication question
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return render_template('game.html', num1=num1, num2=num2,score=0,lives=10)

# Route to handle the answer submission
@app.route('/', methods=['POST'])
def check():
    # Get the form data
    num1 = int(request.form['num1'])
    num2 = int(request.form['num2'])
    score = int(request.form['score'])
    lives = int(request.form['lives'])
    user_answer = int(request.form['answer'])
    if lives==0:
        lives=5
        score = 0

    # Calculate the correct answer
    correct_answer = num1 * num2
    if user_answer == correct_answer:
        result = "Correct!"
        score+=1

    else:
        result = f"Wrong! The correct answer was {correct_answer}."
        lives-=1
    # Redirect back to the home page with the result
    return render_template('game.html', num1=random.randint(1, 10), num2=random.randint(1, 10), result=result,lives=lives,score=score)

if __name__ == '__main__':
    app.run(debug=True)