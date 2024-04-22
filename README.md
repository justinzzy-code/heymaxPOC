# Description

This is a POC for Peer-to-Peer (P2P) Book Exchange Platform. This web application will facilitate the easy listing, searching, and exchanging of books among users. The current product is unfinished and only features the only the **backend's main features using Django REST API and Python**.


# Version Requirements

Django 4.2.6

Python 3.9.7


# Setup: 
Navigate to backend folder and run `python ./manage.py makemigrations` followed by `python ./manage.py migrate`

To create a user: py manage.py createsuperuser. [Follow this tutorial](https://www.w3schools.com/django/django_admin_create_user.php)

# To Run: 

Navigate to backend folder and run `python ./manage.py runserver`


# Tips to Explore Project:

Create a one user and have them add and list various books.

Create a second user and them add and list various (different) books.

Now both users can make exchange requests and comments on the other's listed books. Two such users have been pre-created for convenience. You can also create your own under the endpoint: `accounts/register/`

Explore the various API endpoints.

Premade User 1:  `Username: a, Password: a` 

Premade User 2: `Username: b, Password: b`


# Overview of POC Project

Due to time constraints, only main features of the backend were completed. These features include: 

**User Profile**: Registering/Creating user, Login, Logout, Viewing Profile and Updating Profile

**Book Features**: Creating/Updating/Deleting user's books, viewing all books created, viewing all books USER created, listing created books for exchange, viewing/creating/deleting book exchange requests and responding to other users's book exchange requests. The books can be filtered and searched by name, genre and id. 

**Comment Features**: Creating/Updating/Delete user's comments on a book, viewing comments about a book, viewing all user's comments, viewing all comments on all books. 

For more detail, I created a pdf on a more detailed description on some of the API endpoints. 


# Decisions 

Due to time constraints, I elected to do some main features of the backend for the Book Exchange Platform. I chose to focus on more crucial features such as User Profile, Book Filter/Listing/Search, Exchange Mechanisms and some Community Engagement (allowing comments).

# Project Plan + Milestone for future extension

**Back-end**: Include mechanisms for storing messages between users. Create mechanisms for users to communicate via text (messaging system).

**Front-end**: Create a frontend website for the Book Exchange Platform. Intend to use **React.js, Javascript, HTML/CSS** for the frontend. Frontend for forum/social media site.

**Community Engagement**: Improve community engagement features. Right now only basic comments are done. Should create a forum/social_media site for better community engagement. Use recommendation systems to recommend users with similar taste. 

**AI-Enhanced Features**: Create recommendation systems using AI. We could collect user data about user's reading preferences to recommend books for similar genre/taste. Personalized recommendation systems. Allow feedback loop systems so user can tailor their preferences. Consider using NLP to extract text from books to get data about the book's setting, genre, theme, writing style, etc, which can be used for the recommendation system. The system can also recommend users/community that share the same taste as the user. 

