# RUN
you can run directed:
```shell
pip install --no-cache-dir -r requirements.txt
python main.py 80
```
or simple way by docker
```shell
docker build -t rasa_wx .
docker run -d -p 80:80 rasa_wx
```

# Dependence
```shell
web.py==0.62
requests==2.25.1
```

# REST
REST channel: POST
http://<host>:<port>/webhooks/rest/webhook,
format:
{
  "sender": "test_user",  // sender ID of the user sending the message
  "message": "Hi there!"
}

The response from Rasa Open Source will be a JSON body of bot responses,
for example:
[
  {"text": "Hey Rasa!"}, {"image": "http://example.com/image.jpg"}
]


# Visit
local host to visit: 127.0.0.1:80
