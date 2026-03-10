app.controller("SubscriptionController", function ($scope, $http) {
  $scope.editId = null;
  $scope.customersMap = {};
  $scope.productsMap = {};

  function resetForm() {
    $scope.editId = null;
    $scope.customer_id = "";
    $scope.product_id = "";
    $scope.start_date = "";
    $scope.quantity = 1;
    $scope.frequency = "daily";
    $scope.payment_status = "pending";
  }

  function load() {
    $http.get("http://127.0.0.1:5000/api/subscriptions/").then(function (res) {
      $scope.subscriptions = res.data;
    });

    $http.get("http://127.0.0.1:5000/api/customers/").then(function (res) {
      $scope.customers = res.data.data || res.data;
      $scope.customersMap = {};
      $scope.customers.forEach(function (customer) {
        $scope.customersMap[customer.id] = customer.name;
      });
    });

    $http.get("http://127.0.0.1:5000/api/products/").then(function (res) {
      $scope.products = res.data;
      $scope.productsMap = {};
      res.data.forEach(function (product) {
        $scope.productsMap[product.id] = product.name;
      });
    });
  }

  $scope.resetForm = resetForm;

  load();
  resetForm();

  $scope.add = function () {
    var data = {
      customer_id: $scope.customer_id,
      product_id: $scope.product_id,
      start_date: $scope.start_date,
      quantity: $scope.quantity,
      frequency: $scope.frequency,
      payment_status: $scope.payment_status,
    };

    if ($scope.editId) {
      $http
        .put("http://127.0.0.1:5000/api/subscriptions/" + $scope.editId, data)
        .then(function () {
          alert("Subscription updated");
          resetForm();
          load();
        });
    } else {
      $http.post("http://127.0.0.1:5000/api/subscriptions/", data).then(function () {
        alert("Subscription added");
        resetForm();
        load();
      });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this subscription?")) return;

    $http.delete("http://127.0.0.1:5000/api/subscriptions/" + id).then(function () {
      alert("Subscription deleted");
      load();
    });
  };

  $scope.edit = function (subscription) {
    $scope.editId = subscription.id;
    $scope.customer_id = subscription.customer_id;
    $scope.product_id = subscription.product_id;
    $scope.start_date = subscription.start_date;
    $scope.quantity = subscription.quantity;
    $scope.frequency = subscription.frequency || "daily";
    $scope.payment_status = subscription.payment_status || "pending";
  };
});
