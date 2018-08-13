# Moviescope

Moviescope is a personal movie journal, which helps users to track films they have watched or want to watch in the future. A user can search for a movie by title, add reviews and ratings, and store it in a personal journal. Also, Moviescope provides a list of recommendations matching the user’s taste. A user can compile a wishlist of films and find watch options on streaming services and in theaters.


## Contents
  * [Technology Stack](https://github.com/LisaLen/Moviescope/new/master?readme=1#technology-stack)
  * [Features](https://github.com/LisaLen/Moviescope/new/master?readme=1#features)
  * [Installation](https://github.com/LisaLen/Moviescope/new/master?readme=1#installation)

---
### Technology Stack:

Backend: Python, Flask, PostgreSQL, SQLAlchemy  
Frontend: JavaScript, jQuery, AJAX, JASON, Jinja2, Bootstrap, HTML5, CSS3  
APIs: OMDB, Recombee, JustWatch  
Dataset: MovieLens  

---
### Features
  * On ‘Add Movie’ page  user may search movie by title in IMDB, add movie to wishlist, rate it, write a review and store in personal journal 
 ![alt text](https://github.com/LisaLen/Moviescope/blob/master/readme_img/search.jpg)
  * One 'movie journal' page user may navigate through saved movies by scrolling the table, see movie information,
  personal ratings and reviews, delete movie from journal or edit review.
  ![alt text](https://github.com/LisaLen/Moviescope/blob/master/readme_img/journal.jpg)
  
   * To change a review or rating, click ‘Edit’ button. This form shows the most recent rating and review. 
   When user clicks 'confirm', the changes are saved on the server and journal table is updated dynamically. 
   ![alt text](https://github.com/LisaLen/Moviescope/blob/master/readme_img/edit.jpg)
   
   * On Homepage page user may see personalized movie recommendations. 
       ![alt text](https://github.com/LisaLen/Moviescope/blob/master/readme_img/recom1.jpg)  
          Recommendations on the Movie page consider the currently selected movie as well as the user's general movie preferences.  
        ![alt text](https://github.com/LisaLen/Moviescope/blob/master/readme_img/recom2.jpg)  
   * Wishlist page collects movies user saved to watch in the future. User may rate movie and add to personal journal, find watch options or delete movie from this list  
   ![alt text](https://github.com/LisaLen/Moviescope/blob/master/readme_img/wishlist.PNG)  
   * On Watch It page user may see offers from three most popular providers or link to showtimes in theaters.
    ![alt text](https://github.com/LisaLen/Moviescope/blob/master/readme_img/watchit.jpg) 

---
### Installation
To use Moviescope:
  * Install PostgreSQL (Mac OSX)

Clone or fork this repo:  
```sh
https://github.com/LisaLen/Moviescope.git
```
