app.controller("OrderController", function($scope,$http){

$scope.editId=null;
$scope.customersMap={};
$scope.productsMap={};


// LOAD EVERYTHING
function load(){

$http.get("http://127.0.0.1:5000/api/orders/")
.then(function(res){ $scope.orders=res.data; });

$http.get("http://127.0.0.1:5000/api/customers/")
.then(function(res){

$scope.customers=res.data.data || res.data;

$scope.customers.forEach(function(c){
$scope.customersMap[c.id]=c.name;
});

});

$http.get("http://127.0.0.1:5000/api/products/")
.then(function(res){

$scope.products=res.data;

res.data.forEach(function(p){
$scope.productsMap[p.id]=p.name;
});

});

}

load();


// ADD / UPDATE
$scope.add=function(){

var data={
customer_id:$scope.customer_id,
product_id:$scope.product_id,
size:$scope.size,
quantity:$scope.quantity
};

if($scope.editId){

$http.put(
"http://127.0.0.1:5000/api/orders/"+$scope.editId,
data
)
.then(function(){

alert("Updated");

$scope.editId=null;
load();

});

}

else{

$http.post(
"http://127.0.0.1:5000/api/orders/",
data
)
.then(function(){

alert("Added");
load();

});

}

};


// DELETE
$scope.remove=function(id){

if(!confirm("Delete order?")) return;

$http.delete("http://127.0.0.1:5000/api/orders/"+id)
.then(function(){

alert("Deleted");
load();

});

};


// EDIT
$scope.edit=function(o){

$scope.editId=o.id;

$scope.customer_id=o.customer_id;
$scope.product_id=o.product_id;
$scope.size=o.size;
$scope.quantity=o.quantity;

};

});