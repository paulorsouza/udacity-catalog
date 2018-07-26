if (!window.CURRENT_USER) {
  (function() {
    function login(provider, authCode) {
      console.log(authCode);
      $.ajax({
        type: 'POST',
        url: '/oauth/'+provider,
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
          console.log(err);
          $("#result").html(
            "Failed to make a server-side call. Check your configuration and console."
          );
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
      console.log(e);
    }

    function googleSignInCallback(authResult) {
      console.log(authResult);
      console.log(authResult['code']);
      if (authResult['code']) {
        login('google', authResult['code'])
      } else {
        $("#result").html(
          "Failed to login."
        );
      }
    }

    window.fbAsyncInit = function() {
      FB.init({
        appId: "2153782074868460",
        cookie: true,
        xfbml: true,
        version: "v3.0"
      });
    };

    (function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s);
      js.id = id;
      js.src = "//connect.facebook.net/en_US/sdk.js";
      fjs.parentNode.insertBefore(js, fjs);
    })(document, "script", "facebook-jssdk");


    $('#facebook-login').click(function() {
      FB.login(function(response) {
        if (response.status === 'connected') {
          var accessToken = response.authResponse.accessToken;
          login('facebook', accessToken)
        } else {
          $("#result").html(
            "Failed to login."
          );
        }
      }, {scope: 'public_profile,email'});
    });
  })();
}
