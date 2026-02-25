app.controller("ProductController", function($scope,$http){

$scope.categoryMap = {};
$scope.categories = [];
$scope.editId = null;


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

$http.get("http://127.0.0.1:5000/api/products/")
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
price:$scope.price,
stock:$scope.stock
}
)

.then(function(){

alert("Product Updated");

// reset form
$scope.editId=null;
$scope.name="";
$scope.category_id="";
$scope.size="";
$scope.price="";
$scope.stock="";

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
price:$scope.price,
stock:$scope.stock
}
)

.then(function(){

alert("Product Added");

// reset form
$scope.name="";
$scope.category_id="";
$scope.size="";
$scope.price="";
$scope.stock="";

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
$scope.price = p.price;
$scope.stock = p.stock;

};

});