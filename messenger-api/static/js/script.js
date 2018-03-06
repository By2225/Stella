'use-strict';

// Submits form to Java Stellar API
$(document).ready(function() {
    var form = $("form");

    form.submit((event) => {
        event.preventDefault();
        console.log(form.serialize());
        $.ajax({
            type: "POST",
            data: form.serialize(),
            url: "http://stellarapi.herokuapp.com/send",
            success: function(resp, status, fullRespObj) {
                console.log(resp);
                console.log(status);
                console.log(fullRespObj);
                if ($("form").length > 0) {
                    $("form").replaceWith("<h1> Transaction completed <h1>");
                }
            },
            error: function(resp, status, error) {

                if ($("form").length > 0) {
                    $("form").replaceWith("<h1> Transaction failed <h1>");
                }
                console.log(resp);
                console.log(status);
                console.log(error);
            }
        })
    });
});

// Connect to Messenger Extensions API
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement(s);
    js.id = id;
    js.src = "https://connect.facebook.com/en_US/messenger.Extensions.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'Messenger'));

// The Messenger Extensions JS SDK is done loading
window.extAsyncInit = function() {}
MessengerExtensions.requestCloseBrowser(function success() {
    // webview closed
}, function error(err) {
    // an error occurred
    console.log(err);
});
