app.controller("CustomerController", function ($scope, $http) {
  $scope.editId = null;

  function resetForm() {
    $scope.editId = null;
    $scope.name = "";
    $scope.email = "";
    $scope.password = "";
    $scope.phone = "";
    $scope.address = "";
  }

  function load() {
    $http.get("http://127.0.0.1:5000/api/customers/").then(function (res) {
      $scope.customers = res.data.data || res.data;
    });
  }

  $scope.resetForm = resetForm;

  load();

  $scope.addCustomer = function () {
    var payload = {
      name: $scope.name,
      email: $scope.email,
      password: $scope.password,
      phone: $scope.phone,
      address: $scope.address,
    };

    if ($scope.editId) {
      $http
        .put("http://127.0.0.1:5000/api/customers/" + $scope.editId, payload)
        .then(function () {
          alert("Customer updated");
          resetForm();
          load();
        });
    } else {
      $http.post("http://127.0.0.1:5000/api/customers/", payload).then(function () {
        alert("Customer added");
        resetForm();
        load();
      });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this customer?")) return;

    $http.delete("http://127.0.0.1:5000/api/customers/" + id).then(function () {
      alert("Customer deleted");
      load();
    });
  };

  $scope.edit = function (customer) {
    $scope.editId = customer.id;
    $scope.name = customer.name;
    $scope.email = customer.email;
    $scope.phone = customer.phone;
    $scope.address = customer.address;
    $scope.password = "";
  };
});
