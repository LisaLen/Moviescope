const API_KEY = '3cea6db4'
function showSearchResults(results){
    let movie = {title: results['Title'],
                 released: results['Released'],
                 genre: results['Genre'],
                 poster_url: results['Poster'],
                  imdb_rating: results['imdbRating'],
                 imdb_id: results['imdbID'],
                 movie_url: results['Website']};

    console.log(movie);
}


function searchMovie(evt){
    alert('You need to progrma IMBD feature');
    evt.preventDefault();
    let title = $('#movietitle').val();
    console.log(title);
    let url = 'http://www.omdbapi.com/?t=' + title + '&apikey=' + API_KEY
    console.log(url);

    $.get(url, showSearchResults)
   
}

$('#imdbsearch').on('click', searchMovie);
