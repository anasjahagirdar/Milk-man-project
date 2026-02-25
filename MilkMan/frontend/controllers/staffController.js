app.controller("StaffController", function($scope,$http){

$scope.editId=null;

function load(){

$http.get("http://127.0.0.1:5000/api/staff/")
.then(function(res){
$scope.staff=res.data;
});

}

load();


// ADD OR UPDATE
$scope.add=function(){

if($scope.editId){

$http.put(
"http://127.0.0.1:5000/api/staff/"+$scope.editId,
{
name:$scope.name,
email:$scope.email,
password:$scope.password,
role:$scope.role
}
)

.then(function(){

alert("Updated");

$scope.editId=null;
$scope.name="";
$scope.email="";
$scope.password="";
$scope.role="";

load();

});

}

else{

$http.post(
"http://127.0.0.1:5000/api/staff/",
{
name:$scope.name,
email:$scope.email,
password:$scope.password,
role:$scope.role
}
)

.then(function(){

alert("Added");

$scope.name="";
$scope.email="";
$scope.password="";
$scope.role="";

load();

});

}

};


// DELETE
$scope.remove=function(id){

if(!confirm("Delete this staff?")) return;

$http.delete("http://127.0.0.1:5000/api/staff/"+id)

.then(function(){

alert("Deleted");
load();

});

};


// EDIT
$scope.edit=function(s){

$scope.editId=s.id;

$scope.name=s.name;
$scope.email=s.email;
$scope.role=s.role;

};

});