app.controller("OrderController", function ($scope, $http) {
  var apiUrl = window.MilkManAdmin.apiUrl;
  $scope.editId = null;
  $scope.customersMap = {};
  $scope.productsMap = {};
  $scope.successMsg = "";
  $scope.errorMsg = "";

  function resetForm() {
    $scope.editId = null;
    $scope.customer_id = "";
    $scope.product_id = "";
    $scope.quantity = 1;
    $scope.status = "pending";
    $scope.successMsg = "";
    $scope.errorMsg = "";
  }

  function load() {
    $http.get(apiUrl("/api/orders/")).then(function (res) {
      $scope.orders = res.data;
    });

    $http.get(apiUrl("/api/customers/")).then(function (res) {
      $scope.customers = res.data.data || res.data;
      $scope.customersMap = {};
      $scope.customers.forEach(function (customer) {
        $scope.customersMap[customer.id] = customer.name;
      });
    });

    $http.get(apiUrl("/api/products/")).then(function (res) {
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
    $scope.successMsg = "";
    $scope.errorMsg = "";
    var data = {
      customer_id: $scope.customer_id,
      product_id: $scope.product_id,
      quantity: $scope.quantity,
      status: $scope.status,
    };

    if ($scope.editId) {
      $http
        .put(apiUrl("/api/orders/" + $scope.editId), data)
        .then(function () {
          $scope.successMsg = "Order updated successfully.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to update order.";
        });
    } else {
      $http
        .post(apiUrl("/api/orders/"), data)
        .then(function () {
          $scope.successMsg = "Order created successfully.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to create order.";
        });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this order?")) return;

    $scope.successMsg = "";
    $scope.errorMsg = "";
    $http
      .delete(apiUrl("/api/orders/" + id))
      .then(function () {
        $scope.successMsg = "Order deleted.";
        load();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to delete order.";
      });
  };

  $scope.updateStatus = function (order, status) {
    $http
      .put(apiUrl("/api/orders/" + order.id), { status: status })
      .then(function () {
        order.status = status;
        $scope.successMsg = "Order status updated to: " + status;
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to update status.";
      });
  };

  $scope.edit = function (order) {
    $scope.editId = order.id;
    $scope.customer_id = order.customer_id;
    $scope.product_id = order.product_id;
    $scope.quantity = order.quantity;
    $scope.status = order.status || "pending";
    $scope.successMsg = "";
    $scope.errorMsg = "";
  };
});