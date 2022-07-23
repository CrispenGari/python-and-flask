### Parallel Requests

Let's say we want have a function that checks if the number is prime or not. If the number is not prime we want to return the factors of that number in a json response that looks as follows:

```json
{
  "factors": [2, 5],
  "number": 10,
  "prime": false
}
```

The function for doing that looks as follows:

```py

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
```

Then this means that every time we send the get request to `http://127.0.0.1:3001/isprime/<id>` we are going calling the following route:

```py
@app.route('/isprime/<int:id>', methods=["GET"])
def _(id):
    return make_response(jsonify(isPrime(id))), 200
```

Let's take a scenario where the number is very large like `6000000`, this means that the the computation will be huge and it can block other requests to be processed.

> But flask by default allows parallel requests. So we can send multiple request to the server without waiting for others to be finished.
