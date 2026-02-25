app.controller("CategoryController", function($scope,$http){

function load(){

$http.get("http://127.0.0.1:5000/api/categories/")
.then(function(res){

$scope.categories=res.data;

});

}

load();


$scope.add=function(){

$http.post(
"http://127.0.0.1:5000/api/categories/",
{ name:$scope.name }
)

.then(function(){

alert("Category added");
load();

});

};

});