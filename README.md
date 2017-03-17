# About

This project is a part of Full Stack Developer Nanodegree from [Udacity](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004).  
It's a multi user blog where users can sign in and post blog posts as well as 'Like' and 'Comment' on other posts made on the blog. It has an authentication system for users to be able to register and sign in and then create blog posts!


## Before you begin

  - Install [Python 2.7](https://www.python.org/downloads).
  - Create a new Cloud Platform Console project or retrieve the project ID of an existing project from the Google Cloud Platform Console: [GO TO THE PROJECTS PAGE](https://console.cloud.google.com/project?_ga=1.242911424.31039787.1489322140)
  - Install and then initialize the [Google Cloud SDK](https://cloud.google.com/sdk/docs/).


## Cloning the project from GitHub

  - Clone this repository to your local machine:
    ```
    git clone https://github.com/minghua1991/multi-user-blog.git
    ```
  - Go to the directory that contains all code of this repository:
    ```
    cd multi-user-blog
    ```


## Building and running locally

To build and run the project locally:
  - Start the local development web server by running the following command from the multi-user-blog directory:
    ```
    dev_appserver.py ./
    ```  
    The development web server runs, listening for requests on port 8080.
  - Visit http://localhost:8080/ in your web browser to view the app.  

    Click Login, then sign in with any email address. The development server accepts any email you supply, valid or not. This same code requires a valid Google Account and email when deployed to production.
    
  - Stop the development server by pressing Control+C.
 

## Demo

  - You can also visit the [Live Demo](https://udacity-nanodegree-p3.appspot.com/).

## Todos

 - Use [Bleach](https://pypi.python.org/pypi/bleach) to escape or strip markup and attributes, such as script tag!!!

License
----

MIT
