'use strict';
function editReview(evt){
      
    let form = $(this).closest('form') // get edit review form object

    let rating =$(this).closest('tr').find('.rating');
    let review =$(this).closest('tr').find('.review');
    let date_review =$(this).closest('tr').find('.date_review');
    console.log(rating);
    console.log(review);
    console.log(date_review);
    console.log(form);
    let movie_id = form["0"]["0"].value;
    let new_rating = form["0"][1].value;
    let new_review = form["0"][2].value;
    console.log(movie_id, new_rating, new_review);

    let new_date_review;


    //update DB with new rating and review
    $.get('/edit-review.json', {movie_id: movie_id,
                           new_rating: new_rating,
                           new_review: new_review },
                             function(results){
                                if (results != 'ERROR'){
                                    date_review['0'].innerText = results['date_review'];
                                    console.log(results['date_review']);
                                    alert('Review and rating have been updated');

                                 } else{
                                    alert('ERROR: CANNOT DELETE MOVIE');
                             }
    });

   
    rating['0'].textContent = new_rating;
    review["0"].outerText = new_review;
 


}

 $(document).on('click','#confirm-edit', editReview);
