app.controller("AuthController", function($scope,$http,$location,$rootScope){

$scope.login=function(){

$http.post(
"http://127.0.0.1:5000/api/auth/admin/login",
{
email:$scope.email,
password:$scope.password
}
)

.then(function(response){

console.log("LOGIN RESPONSE:",response.data);

// save token
localStorage.setItem("token",response.data.token);

// ⭐ IMPORTANT — mark logged in
$rootScope.isLoggedIn=true;

alert("Login success");

// go to dashboard
$location.path("/dashboard");

})

.catch(function(err){

console.log("LOGIN ERROR:",err);
alert("Invalid login");

});

};

});