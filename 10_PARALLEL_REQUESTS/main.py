
from flask import Flask, request,  make_response, jsonify


app = Flask(__name__)


def isPrime(number:int):
  factors = list()
  if (number < 1) :return False
  if (number == 1) :return True

  for i in range(2, number):
      if number % i == 0:
          factors.append(i)
  return {
    "number": number,
    "factors": factors,
    "prime": False if len(factors) > 0 else True,
  };


@app.route('/isprime/<int:id>', methods=["GET"])
def _(id):
    return make_response(jsonify(isPrime(id))), 200
    
    
if __name__ == "__main__":
    app.run(debug=True, port=3001) # allow hot reloading