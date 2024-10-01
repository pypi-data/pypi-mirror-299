# Alex Frame: Python Web Framework built for learning purposes

![purpose](https://img.shields.io/badge/purpose-learning-green.svg)
![PyPI](https://img.shields.io/pypi/v/alexgalt_framework.svg)

Alex Frame is a Python web framework built for learning purposes.

It's a WSGI framework and can be used with any WSGI application server such as Gunicorn.

## Installation

```shell
pip install alexgalt-framework
```


## How to use it

### Basic usage:

```python
from alexgalt_framework.api import API

app = API()


@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route("/book")
class BooksResource:
    def get(self, req, resp):
        resp.text = "Books Page"

    def post(self, req, resp):
        resp.text = "Endpoint to create a book"


@app.route("/template")
def template_handler(req, resp):
    resp.body = app.template(
        "index.html", context={"name": "Frame", "title": "Best Framework"}).encode()
```

### Unit Tests

The recommended way of writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). There are two built in fixtures
that you may want to use when writing unit tests with alexgalt_framework. The first one is `app` which is an instance of the main `API` class:

```python
def test_route_overlap_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."

    with pytest.raises(AssertionError):
        @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."
```

The other one is `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](https://requests.readthedocs.io/) and it should feel very familiar:

```python
def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(req, resp, name):
        resp.text = f"hey {name}"

    assert client.get("http://testserver/matthew").text == "hey matthew"
```

## Templates

The default folder for templates is `templates`. You can change it when initializing the main `API()` class:

```python
app = API(templates_dir="templates_dir_name")
```

Then you can use HTML files in that folder like so in a handler:

```python
@app.route("/show/template")
def handler_with_template(req, resp):
    resp.html = app.template(
        "example.html", context={"title": "Awesome Framework", "body": "welcome to the future!"})
```

## Static Files

Just like templates, the default folder for static files is `static` and you can override it:

```python
app = API(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>{{title}}</title>

  <link href="/static/main.css" rel="stylesheet" type="text/css">
</head>

<body>
    <h1>{{body}}</h1>
    <p>This is a paragraph</p>
</body>
</html>
```

### Middleware

You can create custom middleware classes by inheriting from the `alexgalt_framework.middleware.Middleware` class and overriding its two methods
that are called before and after each request:

```python
from alexgalt_framework.api import API
from alexgalt_framework.middleware import Middleware


app = API()


class SimpleCustomMiddleware(Middleware):
    def process_request(self, req):
        print("Before dispatch", req.url)

    def process_response(self, req, res):
        print("After dispatch", req.url)


app.add_middleware(SimpleCustomMiddleware)
```


### ORM

Here's how it will connect to the database:
```python
from alexgalt_framework.orm import Database

db = Database("./test.db")
```
How it will define tables:

```python
from alexgalt_framework.orm import Table, Column, ForeignKey

...

class Author(Table):
    name = Column(str)
    age = Column(int)


class Book(Table):
    title = Column(str)
    published = Column(bool)
    author = ForeignKey(Author)
```
How it will create tables:

```python
db.create(Author)
db.create(Book)
```

How it will create an instance and insert a row:

```python
greg = Author(name="George", age=13)
db.save(greg)
```

How it will fetch all rows:

```python
authors = db.all(Author)
```

How it will get a specific row:

```python
author = db.get(Author, 47)
```
How it will save an object with a foreign key reference:
```python
book = Book(title="Building an ORM", published=True, author=greg)
db.save(book)
```
How it will fetch an object with a foreign key:
```python
print(Book.get(55).author.name)
```
How it will update an object:

```python
book.title = "How to build an ORM"
db.update(book)
```
And finally, how it will delete an object:

```python
db.delete(Book, id=book.id)
```
Now that the API is settled, we're ready to start writing the ORM. But before you do, keep in mind that it all comes down to one idea: In order to write an ORM, you need to convert Python functions into SQL statements and the results of those SQL statements into Python objects. For example, the db.get(Author, 47) function should be translated into the following SQL statement:
```sql
SELECT * FROM author WHERE ID=47;
```
And its result, which is a row, should be converted into a Python object such that you can access the data of that row as properties of that object:

```python
author = db.get(Author, 47)
print(author.name)
print(author.age)
```