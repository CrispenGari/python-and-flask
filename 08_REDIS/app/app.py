try:
  from connection import client
except Exception as e:
    print(e)
    

# setting values

client.set("name", "python redis")

# getting values
res = client.get("name")
print(res)

# checking if the key exists

exists = client.exists("name")
print(exists)

# setting expiring values

client.expire("name", 2)

# creating the keys and set the expire time at the same time

client.setex("name", 2, "name that expires")

# deleting values

client.delete("name")



if __name__ == "__main__":
    client.close()