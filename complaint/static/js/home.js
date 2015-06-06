var complaints_to_render = [];

function fetchComplaints() {
    $.get('/home/get_complaints/', {}, function (data) {
        complaints_to_render = data;
        renderComplaints();

    }, "json")
        .fail(function () {
            $("#error-alert-content").html("Unable to fetch complaints");
            $("#error-alert").show();
        });
};

function renderComplaints() {
    $("#complaint_list").html("");
    var complaint_display = $("#complaintTemplate").html();

    $.each(complaints_to_render, function (index, complaint) {
        var complaint_body = complaint_display.format(complaint.id, complaint.title, complaint.message, complaint.reply_count);
        $("#complaint_list").append(complaint_body);
    });
};

fetchComplaints();


$("#add_complaint").submit(function (e) {
    e.preventDefault();
    $.ajax({
        url: '/home/add_complaint/',
        data: {
            'title': $("#subject").val(),
            'message': $("#detail").val(),
            'csrfmiddlewaretoken': Cookies.get('csrftoken'),
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
                })
                html += "</ul></ul>";
            })
            $("#error-alert-content").html(html);
            $("#error-alert").show();

        }
    });
});

$("#error-alert").on("close.bs.alert", function (e) {
    e.preventDefault();
    $(this).hide();
});