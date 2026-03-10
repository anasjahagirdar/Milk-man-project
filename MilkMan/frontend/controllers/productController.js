app.controller("ProductController", function ($scope, $http) {
  $scope.categoryMap = {};
  $scope.categories = [];
  $scope.editId = null;
  $scope.search = "";
  $scope.units = ["L", "ml", "kg", "g", "pieces", "custom"];

  function resetForm() {
    $scope.editId = null;
    $scope.name = "";
    $scope.category_id = "";
    $scope.size = "";
    $scope.unit = "";
    $scope.price = "";
    $scope.stock = "";
    $scope.description = "";
    $scope.is_active = true;
  }

  function loadCategories() {
    $http.get("http://127.0.0.1:5000/api/categories/").then(function (res) {
      $scope.categories = res.data;
      $scope.categoryMap = {};
      res.data.forEach(function (category) {
        $scope.categoryMap[category.id] = category.name;
      });
    });
  }

  function loadProducts() {
    $http.get("http://127.0.0.1:5000/api/products/").then(function (res) {
      $scope.products = res.data;
    });
  }

  $scope.resetForm = resetForm;

  loadCategories();
  loadProducts();
  resetForm();

  $scope.add = function () {
    var payload = {
      name: $scope.name,
      category_id: $scope.category_id,
      size: $scope.size,
      unit: $scope.unit,
      price: $scope.price,
      stock: $scope.stock,
      description: $scope.description,
      is_active: $scope.is_active,
    };

    if ($scope.editId) {
      $http
        .put("http://127.0.0.1:5000/api/products/" + $scope.editId, payload)
        .then(function () {
          alert("Product updated");
          resetForm();
          loadProducts();
        });
    } else {
      $http.post("http://127.0.0.1:5000/api/products/", payload).then(function () {
        alert("Product added");
        resetForm();
        loadProducts();
      });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this product?")) return;

    $http.delete("http://127.0.0.1:5000/api/products/" + id).then(function () {
      alert("Product deleted");
      loadProducts();
    });
  };

  $scope.edit = function (product) {
    $scope.editId = product.id;
    $scope.name = product.name;
    $scope.category_id = product.category_id;
    $scope.size = product.size;
    $scope.unit = product.unit;
    $scope.price = product.price;
    $scope.stock = product.stock;
    $scope.description = product.description;
    $scope.is_active = product.is_active;
  };

  $scope.filtered = function () {
    var term = ($scope.search || "").toLowerCase();
    if (!term) return $scope.products;
    return ($scope.products || []).filter(function (product) {
      return (
        (product.name || "").toLowerCase().includes(term) ||
        (product.unit || "").toLowerCase().includes(term) ||
        (($scope.categoryMap[product.category_id] || "").toLowerCase().includes(term))
      );
    });
  };
});
