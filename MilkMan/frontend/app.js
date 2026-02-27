var app = angular.module("milkApp", ["ngRoute"]);

app.run(function($rootScope,$location){

$rootScope.isLoggedIn=!!localStorage.getItem("token");

$rootScope.$on("$routeChangeStart",function(event,next){
if(next && next.requiresAuth && !localStorage.getItem("token")){
event.preventDefault();
$rootScope.isLoggedIn=false;
$location.path("/");
}
});

$rootScope.logout=function(){

localStorage.removeItem("token");
$rootScope.isLoggedIn=false;
$location.path("/");

};

});

app.config(function($routeProvider,$httpProvider){

$httpProvider.interceptors.push(function($q,$location,$rootScope){
return {
request:function(config){
var token=localStorage.getItem("token");
if(token){
config.headers=config.headers || {};
config.headers.Authorization="Bearer "+token;
}
return config;
},
responseError:function(rejection){
if(rejection && rejection.status===401){
localStorage.removeItem("token");
$rootScope.isLoggedIn=false;
$location.path("/");
}
return $q.reject(rejection);
}
};
});

$routeProvider

.when("/",{
templateUrl:"views/login.html",
controller:"AuthController"
})

.when("/dashboard",{
templateUrl:"views/dashboard.html",
controller:"DashboardController",
requiresAuth:true
})

.when("/customers",{templateUrl:"views/customers.html",controller:"CustomerController",requiresAuth:true})
.when("/staff",{templateUrl:"views/staff.html",controller:"StaffController",requiresAuth:true})
.when("/categories",{templateUrl:"views/categories.html",controller:"CategoryController",requiresAuth:true})
.when("/products",{templateUrl:"views/products.html",controller:"ProductController",requiresAuth:true})
.when("/subscriptions",{templateUrl:"views/subscriptions.html",controller:"SubscriptionController",requiresAuth:true})
.when("/orders",{templateUrl:"views/orders.html",controller:"OrderController",requiresAuth:true})

.otherwise({redirectTo:"/"});

});
