app.controller("ProductController", function($scope,$http){

$scope.categoryMap = {};
$scope.categories = [];
$scope.editId = null;
$scope.search = "";
$scope.units = ["L","ml","kg","g","pieces","custom"];


// LOAD CATEGORIES
function loadCategories(){

$http.get("http://127.0.0.1:5000/api/categories/")
.then(function(res){

$scope.categories = res.data;

// build ID → NAME map
res.data.forEach(function(c){
$scope.categoryMap[c.id] = c.name;
});

});

}


// LOAD PRODUCTS
function loadProducts(){

$http.get("http://127.0.0.1:5000/api/products/?active=true")
.then(function(res){
$scope.products = res.data;
});

}


loadCategories();
loadProducts();


// ADD OR UPDATE PRODUCT
$scope.add=function(){

// UPDATE MODE
if($scope.editId){

$http.put(
"http://127.0.0.1:5000/api/products/"+$scope.editId,
{
name:$scope.name,
category_id:$scope.category_id,
size:$scope.size,
unit:$scope.unit,
price:$scope.price,
stock:$scope.stock,
is_active:$scope.is_active
}
)

.then(function(){

alert("Product Updated");

// reset form
$scope.editId=null;
$scope.name="";
$scope.category_id="";
$scope.size="";
$scope.unit="";
$scope.price="";
$scope.stock="";
$scope.is_active=true;

loadProducts();

});

}

// CREATE MODE
else{

$http.post(
"http://127.0.0.1:5000/api/products/",
{
name:$scope.name,
category_id:$scope.category_id,
size:$scope.size,
unit:$scope.unit,
price:$scope.price,
stock:$scope.stock,
is_active:$scope.is_active
}
)

.then(function(){

alert("Product Added");

// reset form
$scope.name="";
$scope.category_id="";
$scope.size="";
$scope.unit="";
$scope.price="";
$scope.stock="";
$scope.is_active=true;

loadProducts();

});

}

};


// DELETE PRODUCT
$scope.remove=function(id){

if(!confirm("Delete this product?")) return;

$http.delete("http://127.0.0.1:5000/api/products/"+id)

.then(function(){

alert("Deleted");
loadProducts();

});

};


// EDIT PRODUCT (fills form)
$scope.edit=function(p){

$scope.editId = p.id;

$scope.name = p.name;
$scope.category_id = p.category_id;
$scope.size = p.size;
$scope.unit = p.unit;
$scope.price = p.price;
$scope.stock = p.stock;
$scope.is_active = p.is_active;

};

// FILTERED LIST
$scope.filtered = function(){
var term = ($scope.search||"").toLowerCase();
if(!term) return $scope.products;
return ($scope.products||[]).filter(function(p){
return (p.name||"").toLowerCase().includes(term) || (p.unit||"").toLowerCase().includes(term);
});
};

});
