app.controller("CustomerController", function ($scope, $http) {
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
    $scope.address = "";
    $scope.successMsg = "";
    $scope.errorMsg = "";
  }

  function load() {
    $http.get(apiUrl("/api/customers/")).then(function (res) {
      $scope.customers = res.data.data || res.data;
    });
  }

  $scope.resetForm = resetForm;

  load();
  resetForm();

  $scope.addCustomer = function () {
    $scope.successMsg = "";
    $scope.errorMsg = "";
    var payload = {
      name: $scope.name,
      email: $scope.email,
      password: $scope.password,
      phone: $scope.phone,
      address: $scope.address,
    };

    if ($scope.editId) {
      if (!payload.password) delete payload.password;
      $http
        .put(apiUrl("/api/customers/" + $scope.editId), payload)
        .then(function () {
          $scope.successMsg = "Customer updated.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to update customer.";
        });
    } else {
      $http
        .post(apiUrl("/api/customers/"), payload)
        .then(function () {
          $scope.successMsg = "Customer added.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to add customer.";
        });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this customer?")) return;

    $scope.successMsg = "";
    $scope.errorMsg = "";
    $http
      .delete(apiUrl("/api/customers/" + id))
      .then(function () {
        $scope.successMsg = "Customer deleted.";
        load();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to delete customer.";
      });
  };

  $scope.edit = function (customer) {
    $scope.editId = customer.id;
    $scope.name = customer.name;
    $scope.email = customer.email;
    $scope.phone = customer.phone;
    $scope.address = customer.address;
    $scope.password = "";
    $scope.successMsg = "";
    $scope.errorMsg = "";
  };
});