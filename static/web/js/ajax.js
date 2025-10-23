// var isLoading = false;

// $(document).on("submit", "form.ajax", function (e) {
//     e.preventDefault();
//     var $this = $(this),
//         data = new FormData(this),
//         action_url = $this.attr("action"),
//         reset = $this.hasClass("reset"),
//         reload = $this.hasClass("reload"),
//         redirect = $this.hasClass("redirect"),
//         redirect_url = $this.attr("data-redirect");

//     if (!isLoading) {
//         isLoading = true;
//         $.ajax({
//             url: action_url,
//             type: "POST",
//             data: data,
//             cache: false,
//             contentType: false,
//             processData: false,
//             dataType: "json",
//             success: function (data) {
//                 var status = data.status;
//                 var title = data.title;
//                 var message = data.message;
//                 var pk = data.pk;
//                 if (status == "true") {
//                     title = title || "Success";
//                     Swal.fire({
//                         title: title,
//                         html: message,
//                         icon: "success",
//                     }).then(function () {
//                         if (redirect) {
//                             window.location.href = redirect_url;
//                         } else if (reload) {
//                             window.location.reload();
//                         } else if (reset) {
//                             $this[0].reset();
//                         }
//                     });
//                 } else {
//                     title = title || "An Error Occurred";
//                     Swal.fire({
//                         title: title,
//                         html: message,
//                         icon: "error",
//                     });
//                     isLoading = false; // Reset isLoading flag in the error block
//                 }
//             },
//             error: function () {
//                 var title = "An error occurred";
//                 var message = "Something went wrong";
//                 Swal.fire({
//                     title: title,
//                     html: message,
//                     icon: "error",
//                 });
//                 isLoading = false; // Reset isLoading flag in the error block
//             }
//         });
//     }
// });
var isLoading = false;

$(document).on("submit", "form.ajax", function (e) {
    e.preventDefault();
    var $this = $(this),
        data = new FormData(this),
        action_url = $this.attr("action"),
        reset = $this.hasClass("reset"),
        reload = $this.hasClass("reload"),
        redirect = $this.hasClass("redirect"),
        redirect_url = $this.attr("data-redirect");

    if (!isLoading) {
        isLoading = true;
        $.ajax({
            url: action_url,
            type: "POST",
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            dataType: "json",
            success: function (data) {
                var status = data.status;
                var title = data.title;
                var message = data.message;
                var pk = data.pk;
                if (status == "true") {
                    title = title || "Success";
                    Swal.fire({
                        title: title,
                        html: message,
                        icon: "success",
                    }).then(function () {
                        if (redirect) {
                            window.location.href = redirect_url;
                        } else if (reload) {
                            window.location.reload();
                        } else if (reset) {
                            $this[0].reset();
                        }
                    });
                } else {
                   
                    isLoading = false; // Reset isLoading flag in the error block
                }
            },
            error: function () {
                isLoading = false; // Reset isLoading flag in the error block
            }
        });
    }
});

// delete

var isLoading = false;
$(document).on("submit", "form.delete-ajax", function (e) {
    e.preventDefault();
    var $this = $(this),
        data = new FormData(this),
        action_url = $this.attr("action");

    if (!isLoading) {
        // Show SweetAlert confirmation dialog specifically for deletion
        Swal.fire({
            title: "Are you sure?",
            text: "Do you really want to delete this? This action cannot be undone.",
            icon: "warning",
            showCancelButton: true,  // Show "Yes" and "No" buttons
            confirmButtonText: "Yes, delete it!",
            cancelButtonText: "No, cancel!",
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {
                // If "Yes" is clicked, proceed with the AJAX request for deletion
                isLoading = true;
                $.ajax({
                    url: action_url,
                    type: "POST",
                    data: data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    dataType: "json",
                    success: function (data) {
                        var status = data.status;
                        var title = data.title;
                        var message = data.message;
                        if (status == "true") {
                            Swal.fire({
                                title: title || "Success",
                                html: message,
                                icon: "success",
                            }).then(function () {
                                window.location.reload();  // Reload the page to reflect the deletion
                            });
                        } else {
                            Swal.fire({
                                title: title || "An Error Occurred",
                                html: message,
                                icon: "error",
                            });
                        }
                    },
                    error: function (data) {
                        Swal.fire({
                            title: "An error occurred",
                            html: "Something went wrong",
                            icon: "error",
                        });
                        isLoading = false;
                    }
                }).then(function () {
                    isLoading = false;
                });
            } else if (result.dismiss === Swal.DismissReason.cancel) {
                // If "No" is clicked, do nothing
                Swal.fire({
                    title: "Cancelled",
                    text: "Your delete request was cancelled.",
                    icon: "info",
                });
            }
        });
    }
});

