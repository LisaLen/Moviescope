'use strict';

// ##############ADD MOVIE TO JOURNAL####################################

const API_KEY = '3cea6db4';

// movie_in_db is true id movie already exists in moviescope db
let movie_in_db = false;

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
       
        let tb_row, title, poster, year, imdb_id;
        for (let search_result of search_results){
             title = search_result['Title'];
             
             if(search_result['Poster'] === 'N/A'){
                  poster = 'static/IMG/no_poster.jpg';
            }else{
              poster = search_result['Poster'];
            }
             imdb_id = search_result['imdbID'];
             year = search_result['Year'];
           
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
        
    $('#imdbid').val([results['imdbID']]);
    $('#movietitle').val(results['Title']);
    $('#movietitle').attr('readonly', true);
    $('#imdb_rating').val(results['imdbRating']);
    $('#released').val(results['Released']);
    $('#released').attr('readonly', true);
    $('#genre').val(results['Genre']);
    $('#genre').attr('readonly', true);
    $('#plot').val(results['Plot']);
    $('#plot').attr('readonly', true);
    $('#movie_url').val(results['Website']);
    $('#poster_img').val(results['Poster']);
}

function searchMovieByImdbID(imdb_id_val){
    // searchs movie by ImdbID
 
    let url = 'http://www.omdbapi.com/?i=' + imdb_id_val + '&apikey=' + API_KEY + '&plot=short'
    
    $.get(url, popUpMovieInformation)
    
}

function checkMovieInJournal(evt){
    //checks, if selected movie exists in user's journal

    let tr = $(this).closest('tr');
    let imdb_id_val  = tr.context.value;
    
    $.get('/check-imdbid-in-db', {imdb_id: imdb_id_val}, function(result){
        if (result['movie_in_db'] === true){
            movie_in_db = true;
        }
        if(result['in_journal']=== true){
            alert('This movie is already in your journal. To edit review, use \'Edit\' on Journal page');
            $('#rating').prop("disabled", true);
            $('#review').attr('readonly', true);
            $('#add-movie-btn').prop("disabled", true);
        }else{
            $('#rating').prop("disabled", false);
            $('#review').attr('readonly', false);
            $('#add-movie-btn').prop("disabled", false);
        };

        if(result['in_wishlist']=== true){
            $('#wishlist-btn').prop("disabled", true);  
        }else{
            $('#wishlist-btn').prop("disabled", false);
        };

    searchMovieByImdbID (imdb_id_val);
    })
}

$('#imdbsearch').on('click', searchMovieByTitle);

$(document).on('click', '#imdb_id_radio', checkMovieInJournal);


// ##############WISH LIST####################################

function makeWishListUpdate(imdb_id){
    //sends ajax request to add movie_id into wishlist of current user
    $.get('/add-to-wishlist', {imdb_id: $('#imdbid').val()}, function(movie_in_wishlist){
            if(movie_in_wishlist === 'OK'){
                alert('Movie was added to your Wish List');
                }else{
                    alert('ERROR')
                }
    })

}

function addToWishlist(evt){
    // adding movie into wishlist of current user
            
        let imdb_id = $('#imdbid').val();

        // if movie if not in DB, send ajax request to add movie into DB
        if (movie_in_db === false){
                    
            let new_movie = {imdb_id: imdb_id,
                            movie_title: $('#movietitle').val(),
                            imdb_rating: $('#imdb_rating').val(),
                            released: $('#released').val(),
                            genre: $('#genre').val(),
                            plot:  $('#plot').val(),
                            movie_url: $('#movie_url').val(),
                            poster_img: $('#poster_img').val()};
            $.get('/add-movie-to-db', new_movie, function(new_results){
                
            makeWishListUpdate(imdb_id);
            });
        }else{
            makeWishListUpdate(imdb_id);
        }        
}

$('#wishlist-btn').on('click', addToWishlist);
    
   







