if (!window.CURRENT_USER) {
  (function() {
    function login(authCode) {
      console.log(authCode);
      $.ajax({
        type: 'POST',
        url: '/g-plus-auth',
        processData: false,
        data: JSON.stringify({ auth_code: authCode }),
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
          /* TODO implement flash message */
          console.log(err);
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
      /* TODO implement flash message */
      console.log(e);
    }

    function googleSignInCallback(authResult) {
      if (authResult['code']) {
        login(authResult['code'])
      } else {
        /* TODO implement flash message */
        console.log("Failed");
      }
    }
  })();
}
