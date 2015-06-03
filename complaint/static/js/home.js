if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) { 
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

function fetchComplaints(){
    $.get('/home/get_complaints/', {}, function(data){
        $("#complaint_list").html("");
        var complaint_display = '<div class="panel panel-default">' +
            '<div class="panel-heading panel-accordion" role="tab" id="headingOne" data-toggle="collapse" data-parent="#complaint_list" href="#collapse{0}" >' +
            '<h4 class="panel-title">' +
            '{1}' +
            '</h4>' +
            '</div>' +
            '<div id="collapse{0}" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingOne">' +
            '<div class="panel-body">' +
            '{2}' +
            '</div>' +
            '</div>' +
            '</div>';
        $.each(data, function(index, complaint){
            var complaint_body = complaint_display.format(complaint.id, complaint.title, complaint.message);
            $("#complaint_list").append(complaint_body);
        });
    }, "json")
        .fail(function(){
            $("#error-alert-content").html("Unable to fetch complaints");
            $("#error-alert").show();
        });
};

fetchComplaints();

$("#add_complaint").submit(function(e){
	e.preventDefault();
    $.ajax({
        url : '/home/add_complaint/',
        data: {
            'title': $("#subject").val(),
            'message': $("#detail").val(),
            'csrfmiddlewaretoken': Cookies.get('csrftoken'),
        },
        type: 'POST',
        dataType: 'json',
        success: function(data){
            fetchComplaints();
            $("#add_complaint")[0].reset();
        },
        error: function(data){
            $("#error-alert-content").html(data.responseText);
            $("#error-alert").show();
        }
    });
});

$("#error-alert").on("close.bs.alert", function(e){
	e.preventDefault();
	$(this).hide();
});