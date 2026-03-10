app.controller("AuthController", function ($scope, $http, $location, $rootScope) {
  $scope.error = "";
  $scope.isSubmitting = false;

  $scope.login = function () {
    $scope.error = "";
    $scope.isSubmitting = true;

    $http
      .post("http://127.0.0.1:5000/api/auth/admin/login", {
        email: $scope.email,
        password: $scope.password,
      })
      .then(function (response) {
        localStorage.setItem("token", response.data.token);
        localStorage.setItem(
          "admin_name",
          (response.data.user && response.data.user.name) || "Administrator"
        );
        $rootScope.isLoggedIn = true;
        $rootScope.adminName = localStorage.getItem("admin_name");
        $location.path("/dashboard");
      })
      .catch(function (err) {
        $scope.error =
          (err && err.data && (err.data.error || err.data.message)) || "Invalid login credentials.";
      })
      .finally(function () {
        $scope.isSubmitting = false;
      });
  };
});
