app.controller("StaffController", function ($scope, $http) {
  $scope.editId = null;

  function resetForm() {
    $scope.editId = null;
    $scope.name = "";
    $scope.email = "";
    $scope.password = "";
    $scope.phone = "";
    $scope.role = "";
  }

  function load() {
    $http.get("http://127.0.0.1:5000/api/staff/").then(function (res) {
      $scope.staff = res.data;
    });
  }

  $scope.resetForm = resetForm;

  load();

  $scope.add = function () {
    var payload = {
      name: $scope.name,
      email: $scope.email,
      password: $scope.password,
      phone: $scope.phone,
      role: $scope.role,
    };

    if ($scope.editId) {
      $http.put("http://127.0.0.1:5000/api/staff/" + $scope.editId, payload).then(function () {
        alert("Staff updated");
        resetForm();
        load();
      });
    } else {
      $http.post("http://127.0.0.1:5000/api/staff/", payload).then(function () {
        alert("Staff added");
        resetForm();
        load();
      });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this staff member?")) return;

    $http.delete("http://127.0.0.1:5000/api/staff/" + id).then(function () {
      alert("Staff deleted");
      load();
    });
  };

  $scope.edit = function (staff) {
    $scope.editId = staff.id;
    $scope.name = staff.name;
    $scope.email = staff.email;
    $scope.phone = staff.phone;
    $scope.role = staff.role;
    $scope.password = "";
  };
});
