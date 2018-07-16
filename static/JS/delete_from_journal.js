'use strict';

function deleteFromJournal(evt){
    // Delete movie from page and sends movie_id to server

    let movie_id = $(this).closest("tr").context.value;

   $(this).closest("tr").remove();

   $.get('/delete-from-joural', {movie_id: movie_id}, function(results){
    if (results == 'confirmed'){
        alert('Movie has been deleted from your journal')
    }else{
        alert('ERROR: CANNOT DELETE MOVIE')
    }
})



}


$("#deleteMovie").on("click", deleteFromJournal)
   
   

