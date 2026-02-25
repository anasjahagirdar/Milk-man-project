app.controller("SubscriptionController", function($scope,$http){

$scope.editId=null;
$scope.customersMap={};
$scope.productsMap={};


// LOAD EVERYTHING
function load(){

$http.get("http://127.0.0.1:5000/api/subscriptions/")
.then(function(res){ $scope.subscriptions=res.data; });

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
start_date:$scope.start_date,
quantity:$scope.quantity,
payment_status:$scope.payment_status
};

if($scope.editId){

$http.put(
"http://127.0.0.1:5000/api/subscriptions/"+$scope.editId,
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
"http://127.0.0.1:5000/api/subscriptions/",
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

if(!confirm("Delete subscription?")) return;

$http.delete("http://127.0.0.1:5000/api/subscriptions/"+id)
.then(function(){

alert("Deleted");
load();

});

};


// EDIT
$scope.edit=function(s){

$scope.editId=s.id;

$scope.customer_id=s.customer_id;
$scope.product_id=s.product_id;
$scope.start_date=s.start_date;
$scope.quantity=s.quantity;
$scope.payment_status=s.payment_status;

};

});