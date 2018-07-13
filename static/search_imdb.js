'use strict';

const API_KEY = '3cea6db4';

function searchMovieByTitle(evt){
    // constract API request to search movies by title
    evt.preventDefault();
    let title = $('#movietitle').val();
    console.log(title);
    let url = 'http://www.omdbapi.com/?s=' + title + '&type=movie&apikey=' + API_KEY
    console.log(url);

   $.get(url, showSearchResults)
}

function showSearchResults(results){
   // fetches API data
    
    let search_results=results['Search'];
    if (search_results){
        $('table').empty();
       console.log(search_results);
        let tb_row;
        let title, poster, year, imdb_id;
        for (let search_result of search_results){
             title = search_result['Title'];
             console.log(title);
             if(search_result['Poster'] === 'N/A'){
                  poster = 'static/no_poster.jpg'
            }else{
              poster = search_result['Poster'];
            }
             imdb_id = search_result['imdbID'];
           console.log(imdb_id);
      
            console.log(poster);
            year = search_result['Year'];
           console.log(year);

            tb_row = `<tr><td><input type='radio' name='imdb_id_radio' id='imdb_id_radio' value=${imdb_id}></td>
                        <td><img src=${poster} width='50' hight='50'></td>
                        <td>${title}</td>
                        <td>${year}</td>
                    </tr>`;
         $('table').append(tb_row);

    }
    }else{
        alert('No movie is found');
     }
}

function popUpMovieInformation(results) {
    console.log(results['Title']);
    $('#movietitle').val(results['Title']);
    console.log($('#movietitle').val())

}



        // let movie = {title: result['Title'],
        //          released: result['Released'],
        //          genre: result['Genre'],
        //          poster_url: result['Poster'],
        //          imdb_rating: result['imdbRating'],
        //          imdb_id: result['imdbID'],
        //          movie_url: result['Website']};

       

function searchMovieByImdbID(evt){
    // search movie by ImdbID

    let imdb_id_val = $('#imdb_id_radio').val();
    console.log(imdb_id_val);
   
    let url = 'http://www.omdbapi.com/?i=' + imdb_id_val + '&apikey=' + API_KEY
    console.log(url);

    $.get(url, popUpMovieInformation)
    
}




$('#imdbsearch').on('click', searchMovieByTitle);

$('table').on('click','#imdb_id_radio', searchMovieByImdbID);

  
    
   







