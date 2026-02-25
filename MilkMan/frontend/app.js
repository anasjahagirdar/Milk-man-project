var app = angular.module("milkApp", ["ngRoute"]);

app.run(function($rootScope,$location){

$rootScope.isLoggedIn=!!localStorage.getItem("token");

$rootScope.logout=function(){

localStorage.removeItem("token");
$rootScope.isLoggedIn=false;
$location.path("/");

};

});

app.config(function($routeProvider){

$routeProvider

.when("/",{
templateUrl:"views/login.html",
controller:"AuthController"
})

.when("/dashboard",{
templateUrl:"views/dashboard.html",
controller:"DashboardController"
})

.when("/customers",{templateUrl:"views/customers.html",controller:"CustomerController"})
.when("/staff",{templateUrl:"views/staff.html",controller:"StaffController"})
.when("/categories",{templateUrl:"views/categories.html",controller:"CategoryController"})
.when("/products",{templateUrl:"views/products.html",controller:"ProductController"})
.when("/subscriptions",{templateUrl:"views/subscriptions.html",controller:"SubscriptionController"})
.when("/orders",{templateUrl:"views/orders.html",controller:"OrderController"})

.otherwise({redirectTo:"/"});

});