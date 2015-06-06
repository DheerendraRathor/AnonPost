/**
 * Created by dheerenr on 6/7/15.
 */

var replies_to_render = [];

function fetchReplies() {
    $.get('/home/get_replies/{0}/'.format(complaint_id), {}, function (data) {
        replies_to_render = data;
        renderReplies();

    }, "json")
        .fail(function () {
            $("#error-alert-content").html("Unable to fetch replies");
            $("#error-alert").show();
        });
};

function renderReplies() {
    $("#reply-content").html("");
    var reply_display = $("#replyTemplate").html();

    $.each(replies_to_render, function (index, reply) {
        var submitter;
        if (reply.user_type == 'A') {
            submitter = 'Admin';
        }
        else {
            submitter = 'Submitter';
        }
        var reply_body = reply_display.format(reply.id, reply.message, submitter);
        $("#reply-content").append(reply_body);
    });
};

$("#reply-form").submit(function(e){
    e.preventDefault();
    $.ajax({
        url : '/home/add_reply/{0}/'.format(complaint_id),
        dataType: 'json',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': Cookies.get('csrftoken'),
            'message': $("#reply-textarea").val(),
        },
        success: function(data){
            replies_to_render.push(data);
            renderReplies();
            $("#reply-form")[0].reset();
        },
        error: function(data){
            console.log(data);
            $("#error-alert-content").html(data.responseText);
            $("#error-alert").show();
        }
    });
});

fetchReplies();