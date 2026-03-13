app.controller("DashboardController", function ($scope, $http) {
  var apiUrl = window.MilkManAdmin.apiUrl;

  $scope.stats = {};

  $http.get(apiUrl("/api/customers/")).then(function (res) {
    $scope.stats.customers = res.data.total || (res.data.data || res.data).length;
  });

  $http.get(apiUrl("/api/staff/")).then((res) => {
    $scope.stats.staff = res.data.length;
  });

  $http.get(apiUrl("/api/products/?active=true")).then((res) => {
    $scope.stats.products = res.data.length;
  });

  $http.get(apiUrl("/api/subscriptions/")).then((res) => {
    $scope.stats.subscriptions = res.data.length;
  });

  $http.get(apiUrl("/api/orders/")).then((res) => {
    var orders = res.data || [];
    $scope.stats.orders = orders.length;
    $scope.stats.revenue = orders.reduce(function (sum, order) {
      return sum + (order.total_price || 0);
    }, 0);
  });
});