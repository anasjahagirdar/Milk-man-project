app.controller("DashboardController", function($scope,$http){

$scope.stats={};

$http.get("http://127.0.0.1:5000/api/customers/")
.then(res => $scope.stats.customers=(res.data.data||res.data).length);

$http.get("http://127.0.0.1:5000/api/staff/")
.then(res => $scope.stats.staff=res.data.length);

$http.get("http://127.0.0.1:5000/api/products/?active=true")
.then(res => {
$scope.stats.products=res.data.length;
});

$http.get("http://127.0.0.1:5000/api/subscriptions/")
.then(res => $scope.stats.subscriptions=res.data.length);

$http.get("http://127.0.0.1:5000/api/orders/")
.then(res => {
var orders=res.data||[];
$scope.stats.orders=orders.length;
$scope.stats.revenue=orders.reduce(function(sum,o){ return sum + (o.total_price||0); },0);
});

});
