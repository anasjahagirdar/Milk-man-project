app.controller("AuthController", function ($scope, $http, $location, $rootScope) {
  var apiUrl = window.MilkManAdmin.apiUrl;
  $scope.error = "";
  $scope.isSubmitting = false;

  $scope.login = function () {
    $scope.error = "";
    $scope.isSubmitting = true;

    $http
      .post(apiUrl("/api/auth/login"), {
        email: $scope.email,
        password: $scope.password,
      })
      .then(function (response) {
        var role = response.data.role;
        if (role !== "admin" && role !== "staff") {
          $scope.error = "Access denied. Please use the customer site to log in.";
          $scope.isSubmitting = false;
          return;
        }
        // Prefer access_token, fall back to legacy token key
        var token = response.data.access_token || response.data.token;
        localStorage.setItem("token", token);
        localStorage.setItem("role", role);
        localStorage.setItem(
          "admin_name",
          (response.data.user && response.data.user.name) || "Administrator"
        );
        $rootScope.isLoggedIn = true;
        $rootScope.adminName = localStorage.getItem("admin_name");
        $rootScope.userRole = role;
        $location.path("/dashboard");
      })
      .catch(function (err) {
        $scope.error =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Invalid login credentials.";
      })
      .finally(function () {
        $scope.isSubmitting = false;
      });
  };
});