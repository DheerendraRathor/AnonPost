var complaints_to_render = [];
var get_posts_url;
var add_post_url;
var post_url;

function fetchComplaints() {
    $.get(get_posts_url, {}, function (data) {
        complaints_to_render = data;
        renderComplaints();

    }, "json")
        .fail(function () {
            $("#error-alert-content").html("Unable to fetch complaints");
            $("#error-alert").show();
        });
}

function renderComplaints() {
    $("#complaint_list").html("");
    var complaint_display = $("#complaintTemplate").html();

    $.each(complaints_to_render, function (index, complaint) {
        var complaint_body = complaint_display.format(complaint.id, complaint.title, complaint.message, complaint.reply_count, post_url.format(complaint.id));
        $("#complaint_list").append(complaint_body);
    });
}

fetchComplaints();


$("#add_complaint").submit(function (e) {
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
            complaints_to_render.unshift(data);
            renderComplaints();
            $("#add_complaint")[0].reset();
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