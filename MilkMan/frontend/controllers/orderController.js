app.controller("OrderController", function ($scope, $http) {
  $scope.editId = null;
  $scope.customersMap = {};
  $scope.productsMap = {};

  function resetForm() {
    $scope.editId = null;
    $scope.customer_id = "";
    $scope.product_id = "";
    $scope.size = "1L";
    $scope.quantity = 1;
    $scope.status = "pending";
  }

  function load() {
    $http.get("http://127.0.0.1:5000/api/orders/").then(function (res) {
      $scope.orders = res.data;
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
      size: $scope.size,
      quantity: $scope.quantity,
      status: $scope.status,
    };

    if ($scope.editId) {
      $http.put("http://127.0.0.1:5000/api/orders/" + $scope.editId, data).then(function () {
        alert("Order updated");
        resetForm();
        load();
      });
    } else {
      $http.post("http://127.0.0.1:5000/api/orders/", data).then(function () {
        alert("Order added");
        resetForm();
        load();
      });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this order?")) return;

    $http.delete("http://127.0.0.1:5000/api/orders/" + id).then(function () {
      alert("Order deleted");
      load();
    });
  };

  $scope.edit = function (order) {
    $scope.editId = order.id;
    $scope.customer_id = order.customer_id;
    $scope.product_id = order.product_id;
    $scope.size = order.size;
    $scope.quantity = order.quantity;
    $scope.status = order.status || "pending";
  };
});
