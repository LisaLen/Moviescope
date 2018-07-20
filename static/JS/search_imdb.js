'use strict';

const API_KEY = '3cea6db4';

function searchMovieByTitle(evt){
    // constract API request to search movies by title
    evt.preventDefault();
    let title = $('#movietitleIMDb').val();
    let url = 'http://www.omdbapi.com/?s=' + title + '&type=movie&apikey=' + API_KEY
    
   $.get(url, showSearchResults)
}

function showSearchResults(results){
   // fetches API data
    
    let search_results=results['Search'];
    if (search_results){
        $('#movie_search').empty();
       console.log(search_results);
        let tb_row;
        let title, poster, year, imdb_id;
        for (let search_result of search_results){
             title = search_result['Title'];
             console.log(title);
             if(search_result['Poster'] === 'N/A'){
                  poster = 'static/IMG/no_poster.jpg'
            }else{
              poster = search_result['Poster'];
            }
             imdb_id = search_result['imdbID'];
           console.log(imdb_id);
      
            console.log(poster);
            year = search_result['Year'];
           console.log(year);

            tb_row = `<tr><td><input type='radio' name='imdb_id_radio' id='imdb_id_radio' value=${imdb_id} ></td>
                        <td><img src=${poster} width='50' hight='70'></td>
                        <td>${title}</td>
                        <td>${year}</td>
                    </tr>`;
         $('#movie_search').append(tb_row);

    }
    }else{
        alert('No movie is found');
     }
}

function popUpMovieInformation(results) {
    //sends selected movie informain to add-new-moview form
    
    // to check if imdb_id is in journal or not  


    $('#imdbid').val([results['imdbID']]);
    console.log(results['Title']);
    $('#movietitle').val(results['Title']);
    console.log($('#movietitle').val());

    $('#imdb_rating').val(results['imdbRating']);
    $('#released').val(results['Released']);
    $('#genre').val(results['Genre']);
    $('#plot').val(results['Plot']);
    $('#movie_url').val([results['Website']]);
    $('#poster_img').val(results['Poster']);
    console.log($('#movie_url').val());
    console.log($('#poster_img').val());


}


function searchMovieByImdbID(imdb_id_val){
    // search movie by ImdbID

     
    console.log(imdb_id_val);

    // let imdb_id_val = $('#imdb_id_radio').val();
    let url = 'http://www.omdbapi.com/?i=' + imdb_id_val + '&apikey=' + API_KEY
    console.log(url);

    $.get(url, popUpMovieInformation)
    
}

function checkMovieInJournal(evt){
    //checks, if selected movie exists in user's journal

  
    console.log('hi')
    let tr = $(this).closest('tr');
    console.log(tr)
    let imdb_id_val  = tr.context.value

    console.log(imdb_id_val);


    $.get('/check-imdbid-indb', {imdb_id: imdb_id_val}, function(results){
        if(results==='True'){
            console.log(results);
            alert('This movie is already in your journal. To edit review, use \'Edit\' on Journal page');
        }else{
            searchMovieByImdbID (imdb_id_val);
        }
    } )
}

$('#imdbsearch').on('click', searchMovieByTitle);

$(document).on('click', '#imdb_id_radio', checkMovieInJournal);



  
    
   







