function addFlashMessage(msg) {
  $(".flash-container").append(
    '<div class="flash-message">' +
      '<div class="flash-message__text">' +
        '<strong>' + msg + '</strong>' +
      '</div>' +
    '</div>'
  );
}

$(function() {
  setTimeout(function() {
    $('.flash-message').remove();
  }, 5000);
});

if (!window.CURRENT_USER) {
  (function() {
    function login(authCode) {
      $.ajax({
        type: 'POST',
        url: '/gconnect',
        processData: false,
        data: JSON.stringify({ auth_code: authCode }),
        contentType: "application/json; charset=utf-8",
        success: function(result, statusText, xhr) {
          if (parseInt(xhr.status / 100) === 2) {
            window.location.href = "/";
          } else {
            addFlashMessage(statusText);
          }
        },
        error: function(err) {
          addFlashMessage(err);
        }
      });
    };

    gapi.load('auth2', function() {
      var auth2 = gapi.auth2.init({
        client_id: '363268690228-pfarn56i8a4oouv0sp6fip95cjll1p97.apps.googleusercontent.com'
      });

      $('#google-login').click(function() {
        auth2.grantOfflineAccess().then(googleSignInCallback).catch(errorTest);
      });
    });

    function errorTest(e) {
      addFlashMessage(e);
    }

    function googleSignInCallback(authResult) {
      if (authResult['code']) {
        login(authResult['code'])
      } else {
        addFlashMessage('Failed');
      }
    }
  })();
}
