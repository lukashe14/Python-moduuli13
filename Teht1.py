from flask import Flask, render_template_string

app = Flask(__name__)

def is_prime(number):
    """Tarkistaa, onko annettu luku alkuluku."""
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True

@app.route('/alkuluku/<int:number>', methods=['GET'])
def check_prime(number):
    """Palauttaa tiedon, onko luku alkuluku."""
    result = {
        "Number": number,
        "isPrime": is_prime(number)
    }
    return (result)

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
