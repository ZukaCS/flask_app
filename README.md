# CS50x Final Project

#### Video Demo: <https://www.youtube.com/watch?v=wIWTBwRMRHE>


This is a final project for **CS50's Introduction to Computer Science**

# Description

This is a website where users can search for a desired country and get basic stats on it. 

The site was built using [HTML](https://en.wikipedia.org/wiki/HTML), [CSS](https://en.wikipedia.org/wiki/CSS), [Javascript](https://en.wikipedia.org/wiki/Javascript) and [Python](https://en.wikipedia.org/wiki/Python)

## Features
1. Register and Login
2. Search for a desired country's stats
   - Users can input the name of the country that they want to get stats of in lowercase or uppercase letters. They can also choose a specific country from the dropdown 
   menu. After clicking 'search', the website displays the flag, name, capital, region, area, population, and independence status.
3. Add a country to the favorites
   - Users can add a preferred country to favorites with a single click on the heart icon.
4. Remove a country from the favorites
   - Users can remove a preferred country from favorites with a single click on the heart icon or from the favorites page.
5. See your favorite countries on Favourites Page
   - Countries' flags and names that were added to favorites are listed on the favorites page
6. Report a bug
   - Users can report a bug by describing them. I receive those reports in my email.

## Technologies used
There were a lot of technologies that I found useful to make this website:
1. Backend
   - [Flask](https://flask.palletsprojects.com/en/2.2.x/) in Python
   - [Rest Countries](https://restcountries.com/) API
   - [SQLite3](https://sqlite.org/index.html) database

Using them was very important to make different parts of the website's components function. By using [Rest Countries](https://restcountries.com/) API, the code gathers stats about all countries in the world. Python file processes that information and then displays it to the user. In addition, I wrote codes to hash passwords, report if a website is not behaving as it should, add and remove countries from favorites, Register/Login, Log out, store all of the information needed in the [SQLite3](https://sqlite.org/index.html) database, etc. All thanks to [Flask](https://flask.palletsprojects.com/en/2.2.x/) in Python.

2. Frontend
   - [Ajax](https://ka.wikipedia.org/wiki/Ajax) in Javascript
   - [SweetAlert2](https://sweetalert2.github.io/) in Javascript
   - [Font Awesome](https://fontawesome.com/) in Javascript

By using Javascript I made the website more interactive. When I started making this website using flask, I didn't like that exchanging the information with the server required a page refresh. That is why I used Ajax in this project. It allows us to exchange data asynchronously with a web server/backend, therefore, in some cases, page refresh is not required to send or receive data from the backend making the webpage more dynamic instead of static. [SweetAlert2](https://sweetalert2.github.io/) allowed me to have beautiful pop-up boxes on the page and finally, I used a heart icon from [Font Awesome](https://fontawesome.com/).

 

 
## Files and Directories
- **flask_app**
   - `templates` - contains all html files
   - `static` - contains all static files
      - `styles` - contains all css files
      - `images` - contains all images that website uses
      - **database.db** - database file
   - **app.py** - flask application
   - **requirements.txt** - project dependencies


## The end

This is my final project for CS50x. I learned a lot in the process of making the project. 

I am very glad that I took this course. The journey had its ups and downs however in the end, I made it.

**This was CS50.**
