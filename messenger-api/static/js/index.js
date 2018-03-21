'use-strict';

// Connect to Messenger Extensions API
(function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.com/en_US/messenger.Extensions.js";
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
