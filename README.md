# realtime-commenting-system
 
The RealTime Commenting System (RTCS) is RESTful API based on Django, Django Rest Framework (DRF) and Django Channels. Its two main entities are Articles and Comments, and it provides the following capabilities:

* Creating, Reading, Updating, Deleting Article objects.
* Creating, Reading, Updating and Deleting an Article's Comments objects.
* Viewing the Comment objects related to an Article object with real-time updates for new comments.

 **Table of contents:**
 - [Installation](#installation)
 - [Authentication and Security](#auth-sec)
    - [Login](#login)
    - [Permissions](#perms)
    - [Article Web Service](#articles)
    - [Comment Web Service](#comments)
 - [Real-time updates with Websockets](#ws)

<a id="installation"></a>
## Installation
The project is setup to work with a MySQL database. The database credentials which can be defined in the rtcs/settings.py file in the project's root directory.

The required libraries for this project are outlined in the 'requirements.txt' file in the project's home directory (rtcs). A dedicated Python virtual environment with these libraries pre-installed is provided. To run the project's development server:

1. Navigate to 'rtcs_venv/Scripts/' from the root directory and call the 'activate' command.
```
    cd 'rtcs_venv/Scripts
    activate
```

2. Navigate back to the root directory and to the project's home directory and use the runserver manage commands to run the development server.
```
    cd ../../rtcs
    python manage.py runserver
```
This will run a Django development server at 127.0.0.1:8000. 


<a id="auth-sec"></a>
## Authentication and Security

The API uses DRF's SessionAuthentication scheme, which is based on the presence of a session cookie (set by the Server on login response) for accessing the API's resources. Once a user is authenticated on the system via the dedicated endpoint (more details below), the login response will return the Session cookie (named 'sessionid') which will allow access to all GET methods of the API. 

Additional CSRF verification is required for usage of 'unsafe' methods that alter the state of the system (POST, PUT, PATCH, DELETE). When a user authenticates successfully on the system, they will receive the 'csrftoken' cookie (set on login response), and will have to include its value as a header named 'X-CSRFToken' on all 'unsafe' API calls. 

<a id="login"></a>
### Login

The authentication entry point for the API is the 'POST /auth/login/' endpoint. It expects a JSON payload with the user's username and password, as shown below:

```
{
    "username": "stelios",
    "password": 123456
}
```

If successful, the Response will return a "Success" JSON response payload and two 'Set-Cookie' response headers that will set the value of the two security cookies 'sessionid' and 'csrftoken' on the browser, where they will be maintained for the duration of the user's browsing session.

***Note that the POST /auth/login/ endpoint is CSRF-exempt, as it is the entry point at which the CSRF cookie is obtained and thus can be accessible by any unauthenticated user.***

<a id="perms"></a>
### Permissions

The API exposes endpoints for managing the Article and Comment entities on the system with CRUD operations.

<a id="articles"></a>
#### Article Web Service

* GET /articles/: Lists all articles from the system's database
* GET /articles/<article_id>: Retrieves a specific article with id 'article_id'
* POST /articles/: Creates a new article on the database.
* PUT /articles/<article_id>: Replaces article with id 'article_id'. 
* PATCH /articles/<article_id>: Modifies article with id 'article_id'.
* DELETE /articles/<article_id>: Deletes article with id 'article_id'

The POST method expects a JSON payload containing a 'title' and 'content' entries, as shown below:

```
{
    "title": "Article title from API",
    "content": "Article content from API"
}
```
The PUT and PATCH methods are concerned with a specific article instance and hence require the article's id to be sent in the payload, in addition to the URL, as shown below:
```
{
    "id": <article_id>,
    "title": "Article title from API",
    "content": "Article content from API"
}
```

In addition to Authentication, the Article Web Service has a custom permission strategy based on the 'DjangoModelPermissions' scheme provided by DRF. DjangoModelPermissions maps the built-in permission objects that are created for the model to the unsafe methods of the API Endpoint. The default implementation has been overriden to apply permission checks to GET endpoints, which are not included by default. The permissions for the Article Web Service are:

| Method   | Permission |
| ---------| -----------|
| GET     | articles.view_article |
| POST     | articles.add_article |
| PUT      | articles.change_article |
| PATCH    | articles.change_article |
| DELETE   | articles.delete_article |

<a id="comments"></a>
#### Comment Web Service
* GET /articles/<article_id>/comments: Lists all comments related to article with id <article_id>
* GET /articles/<article_id>/comments/<comment_id>: Retrieves a specific comment with id <comment_id>, related to article with id <article_id>
* POST /articles/<article_id>/comments: Creates a new comment related to article with id <article_id>
* PUT /articles/<article_id>/comments/<comment_id>: Replaces comment with id <comment_id>, related to article with id <article_id>
* PATCH /articles/<article_id>/comments/<comment_id>: Modifies comment with id <comment_id>, related to article with id <article_id>
* DELETE /articles/<article_id>/comments/<comment_id>: comment with id <comment_id>, from article with id <article_id>

The POST, PUT, and PATCH methods expect a JSON payload containing a 'content' key, as shown below:

```
{
    "content": "This is the 1st comment on article 1. It only needs a 'content' payload key. All other attributes are handled by the server!"
}
```

In addition to the 'content' field, the Comment model contains three other fields which are automatically added by the server upon creation. These are:

* author: The user id of the user that created the comment (caller of the POST method)
* timestamp: Datetime field which is added automatically when a comment is created
* article: The article id that this comment is related to, set based on the <article_id> parameter of the URL.

The Comment Web Service's permission strategy is identical to the Article Web Service mentioned above, and based on a customized version of DjangoModelPermissions. The permissions for the Comment Web Service are:

| Method   | Permission |
| ---------| -----------|
| GET     | articles.view_comment |
| POST     | articles.add_comment |
| PUT      | articles.change_comment |
| PATCH    | articles.change_comment |
| DELETE   | articles.delete_comment |

<a id="ws"></a>
### Real-time updates with Websockets
The RTCS project also exposes a Websocket server from which clients can receive new comments on an Article in real time. This has been developed using Django Channels with an InMemory channel layer for testing and development purposes. 

Websocket consumers (connections) are available for viewing each articles new comments in real-time. Using the ***ws://<server_ip>:<port>/ws/article/<article_id>/comments*** URL, users can receive all new comments for Article with ID <article_id> in real-time. For example, when a user navigates to view an Article's comments using the UI, in addition to GET /articles/<article_id>/comments, which would retrieve all existing comments of that article, a ws/article/<article_id>/comments request will be sent to establish a Websocket connection with the server, over which new comments will be received as soon as they are created with POST /articles/<article_id>/comments.

***Note that establishing a Websocket connection with ws/article/<article_id>/comments requires the 'Origin' header to be set*** Its expected format is http://<server_ip>:<server_port>, and its value in the default development environment is http://127.0.0.1:8000.
