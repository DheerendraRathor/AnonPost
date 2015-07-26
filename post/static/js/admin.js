/**
 * Created by dheerenr on 6/7/15.
 */

var posts_to_render = [];
var get_all_posts;
var post_url;

function fetchPosts() {
    $.ajax({
        url: get_all_posts.format(currentOffset),
        dataType: 'json',
        type: 'GET',
        async: false,
        success: function (data) {
            posts_to_render = data;
            renderPosts();
        },
        error: function () {
            $("#error-alert-content").html("Unable to fetch posts");
            $("#error-alert").show();
        }
    });
};

function renderPosts() {
    $("#post_list").html("");
    var post_display = $("#postTemplate").html();

    $.each(posts_to_render, function (index, post) {
        var post_body = post_display.format(post.id, post.title, post.message, post.reply_count, post_url.format(post.id));
        $("#post_list").append(post_body);
    });
};

fetchPosts();

$("#previous-page").click(function (e) {
    e.preventDefault();
    if (currentOffset == 0) {
        return false;
    }
    currentOffset -= 10;
    fetchPosts();
    $("#next-page").removeClass('disabled');
    if (currentOffset == 0) {
        $("#previous-page").addClass('disabled');
    }
});

$("#next-page").click(function (e) {
    e.preventDefault();
    currentOffset += 10;
    fetchPosts();
    $("#previous-page").removeClass('disabled');
    if (posts_to_render.length != 10) {
        $("#next-page").addClass('disabled');
    }
});