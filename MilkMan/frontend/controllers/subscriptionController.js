app.controller("SubscriptionController", function ($scope, $http) {
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
    $scope.start_date = "";
    $scope.quantity = 1;
    $scope.frequency = "daily";
    $scope.successMsg = "";
    $scope.errorMsg = "";
  }

  function load() {
    $http.get(apiUrl("/api/subscriptions/")).then(function (res) {
      $scope.subscriptions = res.data;
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
      start_date: $scope.start_date,
      quantity: $scope.quantity,
      frequency: $scope.frequency,
    };

    if ($scope.editId) {
      $http
        .put(apiUrl("/api/subscriptions/" + $scope.editId), data)
        .then(function () {
          $scope.successMsg = "Subscription updated.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to update subscription.";
        });
    } else {
      $http
        .post(apiUrl("/api/subscriptions/"), data)
        .then(function () {
          $scope.successMsg = "Subscription created.";
          resetForm();
          load();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to create subscription.";
        });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this subscription?")) return;

    $scope.successMsg = "";
    $scope.errorMsg = "";
    $http
      .delete(apiUrl("/api/subscriptions/" + id))
      .then(function () {
        $scope.successMsg = "Subscription deleted.";
        load();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to delete subscription.";
      });
  };

  $scope.pause = function (id) {
    $http
      .post(apiUrl("/api/subscriptions/" + id + "/pause"), {})
      .then(function () {
        $scope.successMsg = "Subscription paused.";
        load();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to pause subscription.";
      });
  };

  $scope.resume = function (id) {
    $http
      .post(apiUrl("/api/subscriptions/" + id + "/resume"), {})
      .then(function () {
        $scope.successMsg = "Subscription resumed.";
        load();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to resume subscription.";
      });
  };

  $scope.cancel = function (id) {
    if (!confirm("Cancel this subscription? This cannot be undone.")) return;
    $http
      .post(apiUrl("/api/subscriptions/" + id + "/cancel"), {})
      .then(function () {
        $scope.successMsg = "Subscription cancelled.";
        load();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to cancel subscription.";
      });
  };

  $scope.edit = function (subscription) {
    $scope.editId = subscription.id;
    $scope.customer_id = subscription.customer_id;
    $scope.product_id = subscription.product_id;
    $scope.start_date = subscription.start_date;
    $scope.quantity = subscription.quantity;
    $scope.frequency = subscription.frequency || "daily";
    $scope.successMsg = "";
    $scope.errorMsg = "";
  };
});