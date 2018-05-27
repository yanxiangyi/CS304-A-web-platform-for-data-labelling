# CS304-A-web-platform-for-data-labelling

## 🔨 Dependency Installation 🔨
`sudo pip install flask`

`sudo pip install mysqlclient`

## 🏗 Server Establishment 🏗

`git clone git@github.com:DNXie/CS304-A-web-platform-for-data-labelling.git`

`cd CS304-A-web-platform-for-data-labelling`

`FLASK_APP=deploy.py flask run --host=0.0.0.0`


## 📝 Webpage Visiting 📝

We currently have three web pages:

[Index](http://47.106.34.103:5000/) 
[Main Page](http://47.106.34.103:5000/mainpage)
[Log in](http://47.106.34.103:5000/login)

[Image Label](http://47.106.34.103:5000/imagelabel.html)
[Publish](http://47.106.34.103:5000/publish.html)
[Text Label](http://47.106.34.103:5000/textlabel.html)


## 🌈 Current API 🌈

### Login API

[/login/username/<user_name>/password/<pass_word>](http://47.106.34.103:5000/login/username/<user_name>/password/<pass_word>)

[/login/email/<user_email>/password/<pass_word>](http://47.106.34.103:5000/login/email/<useremail>/password/<pass_word>)

Success Return:

```json
{
  "code": 0
}
```

Failure Return:

```json
{
  "code": 1,
  "message": "Wrong password!"
}
```

or

```json
{
  "code": 1,
  "message": "User doesn't exist!"
}
```

### Register API

[/register/email/<user_email>/username/<user_name>/password/<pass_word>](http://47.106.34.103:5000/register/email/<user_email>/username/<user_name>/password/<pass_word>)

Success Return:

```json
{
  "code": 0
}
```

Failure Return:

```json
{
  "code": 1, 
  "message": "User already exists!"}
```

or

```json
{
  "code": 1,
  "message": "Register failed! Please try later!"
}
```

### Forget API

[/forget/email/<user_email>](http://47.106.34.103:5000/forget/email/<user_email>)

Success Return:

```json
{
  "code": 0
}
```

Failure Return:

```json
{
  "code": 1, 
  "message": "User doesn't exist!"
}
```

