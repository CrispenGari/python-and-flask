### Redis and Python

In this one we are going to have a look on how we can make our `redis` server communicate with `python` programming language.

### Redis

Redis is an in memory database that stores data as strings in form of `key` and `values` pairs.

<p align="center"><img src="https://docs.redis.com/latest/images/icon_logo/logo-redis-3.svg" width="100%"/></p>

### Project Setup

Assuming that you have redis installed on your computer and you have python version 3 installed you are ready for this quick demonstration.

> Make sure that the redis server is running on your machine in the background, and is ready to accept connections.

We are going to create and activate the virtual environment by running the following command:

```shell
mkdir env && cd env && virtualenv . && cd .. &&  .\env\Scripts\activate
```

We will create a folder called `app`, and in that folder we will create a file named `app.py` and a package called `connection`.

### Redis installation

We are going to use `pip` to install the `redis` package as follows:

```shell
pip install redis
```

In the connection package we are going to have the following code in it:

```py
import redis
client = redis.Redis(
    host="localhost",
    port= 6379,
    password=""
)
```

### Communicating with the redis server

### 1. saving data to the server

We use the `set()` method and pass the `key` and `value` for example:

```py
client.set("name", "python redis")
```

### 2. getting the data from the database

To get the data from the database we use the `get()` method and pass the key to it. Note that if the `key` provided does not exists we will get null values:

```py
res = client.get("name")
print(res)
```

### 3. Checking if the key exists in the database

To check if the `key` exists in the database we use the `exists` method which returns true (1) or false(0).

```py
exists = client.exists("name")
print(exists) # 1 or 0, 1 if it exists and 0 if it does not
```

### 4. Setting the expiration of the key

We can use the `expire` method to set the expiration time of a key. We pass the key and the duration in seconds for example:

```py
client.expire("name", 2)
```

The key `name` will expire in `2seconds`

### Storing a key and set the expiration duration at the same time

For that we use the `setex` method to store the `key` and `value` pair that expires within a given time.

```py
client.setex("name", 2, "name that expires")
```

### Deleting the a key from a database

We use the `delete` method to delete a key from a database by passing the `key` in the delete method for example:

```py
client.delete("name")
```

> For more commands based on your use case you can find them [here](https://redis.io/commands)

To save the data to the redis server we call the `set` method.

### Refs

1. [docs.redis.com](https://docs.redis.com/latest/rs/references/client_references/client_python/)
2. [redis.io](https://redis.io/commands)
