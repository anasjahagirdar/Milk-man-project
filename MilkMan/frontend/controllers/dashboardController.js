app.controller("DashboardController", function($scope,$http){

$scope.stats={};

$http.get("http://127.0.0.1:5000/api/customers/")
.then(res => $scope.stats.customers=(res.data.data||res.data).length);

$http.get("http://127.0.0.1:5000/api/staff/")
.then(res => $scope.stats.staff=res.data.length);

$http.get("http://127.0.0.1:5000/api/products/")
.then(res => $scope.stats.products=res.data.length);

$http.get("http://127.0.0.1:5000/api/subscriptions/")
.then(res => $scope.stats.subscriptions=res.data.length);

$http.get("http://127.0.0.1:5000/api/orders/")
.then(res => $scope.stats.orders=res.data.length);

});