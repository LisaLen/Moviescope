'use strict';

$('#moviep_withlist_btn').on('click', function(evt){
    let imdb_id = $('#imdbid').val();
    $.get('/add-to-wishlist', {imdb_id:imdb_id}, function(results){
                if (results === 'OK'){
                alert('Movie was added to your Wish List');
                $('#moviep_withlist_btn').prop("disabled", true);  
                }else{
                    alert('ERROR');
                }
    });
});