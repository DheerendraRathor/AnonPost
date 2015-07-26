var posts_to_render = [];
var get_posts_url;
var add_post_url;
var post_url;

function fetchPosts() {
    $.get(get_posts_url, {}, function (data) {
        posts_to_render = data;
        renderPosts();

    }, "json")
        .fail(function () {
            $("#error-alert-content").html("Unable to fetch posts");
            $("#error-alert").show();
        });
}

function renderPosts() {
    $("#post_list").html("");
    var post_display = $("#postTemplate").html();

    $.each(posts_to_render, function (index, post) {
        var post_body = post_display.format(post.id, post.title, post.message, post.reply_count, post_url.format(post.id));
        $("#post_list").append(post_body);
    });
}

fetchPosts();


$("#add_post").submit(function (e) {
    e.preventDefault();
    $.ajax({
        url: add_post_url,
        data: {
            'title': $("#subject").val(),
            'message': $("#detail").val(),
            'csrfmiddlewaretoken': Cookies.get('csrftoken')
        },
        type: 'POST',
        dataType: 'json',
        success: function (data) {
            posts_to_render.unshift(data);
            renderPosts();
            $("#add_post")[0].reset();
        },
        error: function (data) {
            data = JSON.parse(data.responseText);
            var html = "";
            $.each(data, function (key, value) {
                html += "<ul><b>{0}</b><ul>".format(key);
                $.each(value, function (index, val) {
                    html += "<li>{0}</li>".format(val.message);
                });
                html += "</ul></ul>";
            });
            $("#error-alert-content").html(html);
            $("#error-alert").show();

        }
    });
});