if (!window.CURRENT_USER) {
  (function() {
    function login(provider, token) {
      $.ajax({
        type: 'POST',
        url: '/login/'+provider,
        processData: false,
        data: JSON.stringify({ token: token }),
        contentType: "application/json; charset=utf-8",
        success: function(result, statusText, xhr) {
          if (parseInt(xhr.status / 100) === 2) {
            window.location.href = "/";
          } else {
            console.error(statusText);
            $("#result").html(
              "Failed to make a server-side call. Check your configuration and console."
            );
          }
        },
        error: function(err) {
          console.log(err);
          $("#result").html(
            "Failed to make a server-side call. Check your configuration and console."
          );
        }
      });
    };

    gapi.load('auth2', function() {
      var auth2 = gapi.auth2.init({
        scope: 'openid email',
        client_id: '363268690228-pfarn56i8a4oouv0sp6fip95cjll1p97.apps.googleusercontent.com'
      });

      $('#google-login').click(function() {
        auth2.grantOfflineAccess().then(googleSignInCallback);
      });
    });

    function googleSignInCallback(authResult) {
      if (authResult['code']) {
        login('google', authResult['code'])
      } else {
        $("#result").html(
          "Failed to login."
        );
      }
    }
  })();
}