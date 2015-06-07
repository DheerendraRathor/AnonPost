/**
 * Created by dheerenr on 6/7/15.
 */

var complaints_to_render = [];

function fetchComplaints() {
    $.ajax({
        url: '/home/get_all_complaints/{0}'.format(currentOffset),
        dataType: 'json',
        type: 'GET',
        async: false,
        success: function (data) {
            complaints_to_render = data;
            renderComplaints();
        },
        error: function () {
            $("#error-alert-content").html("Unable to fetch complaints");
            $("#error-alert").show();
        }
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

$("#previous-page").click(function (e) {
    e.preventDefault();
    if (currentOffset == 0) {
        return false;
    }
    currentOffset -= 10;
    fetchComplaints();
    $("#next-page").removeClass('disabled');
    if (currentOffset == 0) {
        $("#previous-page").addClass('disabled');
    }
});

$("#next-page").click(function (e) {
    e.preventDefault();
    currentOffset += 10;
    fetchComplaints();
    $("#previous-page").removeClass('disabled');
    if (complaints_to_render.length != 10) {
        $("#next-page").addClass('disabled');
    }
});