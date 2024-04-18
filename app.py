from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
import requests
import openai
from openai import OpenAI

app = Flask(__name__)
app.secret_key = b'_53oi3uriq9pifpff;apl'
csrf = CSRFProtect(app)

openai_api_key = 'Your-OPENAI-API-KEY'


client = OpenAI(
    api_key=openai_api_key
)

conversation_history = []

@app.route('/fetch', methods=['POST'])
def fetch():
    if request.method == 'POST':
        input_text = request.form['input']

        conversation_history.append(["You", input_text])

        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": input_text,
                    }
                ],
                model="gpt-3.5-turbo",
            )

            output_text = chat_completion.choices[0].message.content
            conversation_history.append(["Bot", output_text ])

        except KeyError:
            error_message = "Unexpected response from ChatGPT API. Please try again later."
            return render_template('home.html', value=error_message)
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('home.html', value=error_message)

        # Pass the output to the HTML template for rendering
        return render_template('home.html', value = conversation_history)

    return render_template('home.html', value = conversation_history)


@app.route('/')
def home():
    return render_template('home.html', value=conversation_history)



if __name__ == '__main__':
    app.run(debug=True)
