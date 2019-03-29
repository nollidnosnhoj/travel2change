$(".delete_photo").click(function() {
    console.log("CLICKED!")
    var button = $(this);
    if (confirm("Are you sure you want to delete this photo?")) {
        $.ajax({
            type: "DELETE",
            url: $(this).data('url'),
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function() {
                button.parent().parent().fadeOut(1000);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) { 
                alert("Status: " + textStatus); alert("Error: " + errorThrown); 
            }
        });
    }
});