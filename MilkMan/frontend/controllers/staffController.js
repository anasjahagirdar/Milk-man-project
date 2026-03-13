app.controller("StaffController", function ($scope, $http) {
  var apiUrl = window.MilkManAdmin.apiUrl;
  $scope.editId = null;
  $scope.successMsg = "";
  $scope.errorMsg = "";

  function resetForm() {
    $scope.editId = null;
    $scope.name = "";
    $scope.email = "";
    $scope.password = "";
    $scope.phone = "";
    $scope.role = "staff";
    $scope.successMsg = "";
    $scope.errorMsg = "";
  }

  function load() {
    $http.get(apiUrl("/api/staff/")).then(function (res) {
      $scope.staff = res.data;
    });
  }

  $scope.resetForm = resetForm;

  load();
  resetForm();

  $scope.add = function () {
    $scope.successMsg = "";
    $scope.errorMsg = "";
    var payload = {
      name: $scope.name,
      email: $scope.email,
      password: $scope.password,
      phone: $scope.phone,
      role: $scope.role,
    };

    if ($scope.editId) {
      // Don't send password on edit unless changed
      if (!payload.password) delete payload.password;
      $http
        .put(apiUrl("/api/staff/" + $scope.editId), payload)
        .then(function () {
          $scope.successMsg = "Staff member updated.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to update staff member.";
        });
    } else {
      $http
        .post(apiUrl("/api/staff/"), payload)
        .then(function () {
          $scope.successMsg = "Staff member added.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to add staff member.";
        });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this staff member?")) return;

    $scope.successMsg = "";
    $scope.errorMsg = "";
    $http
      .delete(apiUrl("/api/staff/" + id))
      .then(function () {
        $scope.successMsg = "Staff member removed.";
        load();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to delete staff member.";
      });
  };

  $scope.edit = function (staff) {
    $scope.editId = staff.id;
    $scope.name = staff.name;
    $scope.email = staff.email;
    $scope.phone = staff.phone;
    $scope.role = staff.role;
    $scope.password = ""; // Clear — only set if changing
    $scope.successMsg = "";
    $scope.errorMsg = "";
  };
});