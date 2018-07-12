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

function searchMovieByImdbID(evt){
    // search movie by ImdbID
    evt.preventDefault();
    let title = $('#movietitle').val();
    console.log(title);
    let url = 'http://www.omdbapi.com/?t=' + title + '&apikey=' + API_KEY
    console.log(url);

    $.get(url, showSearchResults)
   
}




function popUpMovieTitle(evt){
    // fetches movie title of checked movie and send movie title to add-new-movie form
    alert('Hi!, I am radio button');
       let imdb_id_val = $('#imdb_id_radio').val();

        console.log(imdb_id_val);



}


$('#imdbsearch').on('click', searchMovieByTitle);

$('table').on('click','#imdb_id_radio', popUpMovieTitle);

  
    
   







// to fetch data for a particular movie
// function showSearchResults(results){
//     let movie = {title: results['Title'],
//                  released: results['Released'],
//                  genre: results['Genre'],
//                  poster_url: results['Poster'],
//                   imdb_rating: results['imdbRating'],
//                  imdb_id: results['imdbID'],
//                  movie_url: results['Website']};

//     console.log(movie);
// }

// // to build API request for a particular movie based on IMDB ID
// function searchMovie(evt){
//     alert('You need to progrma IMBD feature');
//     evt.preventDefault();
//     let title = $('#movietitle').val();
//     console.log(title);
//     let url = 'http://www.omdbapi.com/?t=' + title + '&apikey=' + API_KEY
//     console.log(url);

//     $.get(url, showSearchResults)
   
// }

// $('#imdbsearch').on('click', searchMovie);
