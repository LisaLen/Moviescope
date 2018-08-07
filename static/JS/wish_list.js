'use strict';

$(document).on('click','#confirm-add_movie', function(evt){
   //checks, if selected movie exists in user's journal
    let form = $(this).closest('form'); // get edited review
    let imdb_id = form["0"]["0"].value;
    let review = form["0"][1].value;
    let rating = form["0"][2].value;
    let new_date_review;

    //update DB with new rating and review
    $.get('/add-movie-to-journal', {imdbid: imdb_id,
                                    rating: rating,
                                    review: review },
                             function(results){
                                if (results != 'ERROR'){
                                   alert('Review and rating have been updated');

                                 }else{
                                    alert('ERROR: CANNOT DELETE MOVIE');
                                  }  
                             
    });

})

function deleteFromWishList(evt){
    // Delete movie from page and sends movie_id to server

    let movie_id = $(this).closest("tr").context.value;
    
   $(this).closest("tr").remove();

   $.get('/delete-from-wishlist.json', {movie_id: movie_id}, 
                function(results){
                  if (results === 'confirmed'){
                      alert('Movie has been deleted from your Wishlist')
                  }else{
                      alert('ERROR: CANNOT DELETE MOVIE')
                  }
    })
}

$(document).on('click',"#deletefrom_wishlist_btn", deleteFromWishList)
   
   
