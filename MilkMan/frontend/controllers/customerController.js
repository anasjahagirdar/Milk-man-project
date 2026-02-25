app.controller("CustomerController", function($scope,$http){

$scope.editId=null;

function load(){

$http.get("http://127.0.0.1:5000/api/customers/")
.then(function(res){

$scope.customers=res.data.data || res.data;

});

}

load();


// ADD / UPDATE
$scope.addCustomer=function(){

if($scope.editId){

$http.put(
"http://127.0.0.1:5000/api/customers/"+$scope.editId,
{
name:$scope.name,
email:$scope.email,
password:$scope.password
}
)

.then(function(){

alert("Updated");

$scope.editId=null;
$scope.name="";
$scope.email="";
$scope.password="";

load();

});

}

else{

$http.post(
"http://127.0.0.1:5000/api/customers/",
{
name:$scope.name,
email:$scope.email,
password:$scope.password
}
)

.then(function(){

alert("Added");

$scope.name="";
$scope.email="";
$scope.password="";

load();

});

}

};


// DELETE
$scope.remove=function(id){

if(!confirm("Delete this customer?")) return;

$http.delete("http://127.0.0.1:5000/api/customers/"+id)

.then(function(){

alert("Deleted");
load();

});

};


// EDIT
$scope.edit=function(c){

$scope.editId=c.id;

$scope.name=c.name;
$scope.email=c.email;

};

});