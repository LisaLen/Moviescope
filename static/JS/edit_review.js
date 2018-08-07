'use strict';
function editReview(evt){
      
    let form = $(this).closest('form') // get edited review
    let rating =$(this).closest('tr').find('.rating');
    let review =$(this).closest('tr').find('.review');
    console.log(review)
    let date_review =$(this).closest('tr').find('.date_review');
    let movie_id = form["0"]["0"].value;
    let new_review = form["0"][1].value;
    let new_rating = form["0"][2].value;
   
    let new_date_review;

    //update DB with new rating and review
    $.get('/edit-review.json', {movie_id: movie_id,
                                new_rating: new_rating,
                                new_review: new_review },
                            function(results){
                                if (results != 'ERROR'){
                                    date_review['0'].innerText = results['date_review'];
                                    alert('Review and rating have been updated');
                                }else{
                                    alert('ERROR: CANNOT UPDATE REVIEW');
                                }
    });

    rating.empty();
    
    let rating_star = '';
    
    for (let i = 0; i < new_rating; i++){
        rating_star += '<span><i class="text-warning fas fa-star" style="font-size:7px"></i></span>';
    };

    rating.append(rating_star);
    
    review.empty();
    review.append(new_review)


    // review["0"].outerText = new_review;
}

$(document).on('click','#confirm-edit', editReview);
