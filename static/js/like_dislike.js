$(document).ready(function() {
    $('#like_btn').click(function(){
        var categoryIdVar;
        categoryIdVar = $(this).attr("data-categoryid");
        articleIdVar = $(this).attr("data-articleid");

        $.get('/main/like_category/', {category_id: categoryIdVar}, function(data){
            $('#point_count').html(data);
            $('#like_btn').hide();
        });

        $.get('/main/like_article/', {article_id: articleIdVar}, function(data){
            $('#point_count').html(data);
            $('#like_btn').hide();
        });
    });

    $('#dislike_btn').click(function(){
        var categoryIdVar;
        categoryIdVar = $(this).attr("data-categoryid");
        articleIdVar = $(this).attr("data-articleid");

        $.get('/main/dislike_category/', {category_id: categoryIdVar}, function(data){
            $('#point_count').html(data);
            $('#dislike_btn').hide();
        });

        $.get('/main/dislike_article/', {article_id: articleIdVar}, function(data){
            $('#point_count').html(data);
            $('#dislike_btn').hide();
        });
    });
});