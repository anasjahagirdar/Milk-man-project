app.controller("ProductController", function ($scope, $http) {
  var apiUrl = window.MilkManAdmin.apiUrl;
  $scope.categoryMap = {};
  $scope.categories = [];
  $scope.editId = null;
  $scope.search = "";
  $scope.successMsg = "";
  $scope.errorMsg = "";
  $scope.units = ["500ml", "1L", "200g", "250g", "400g", "500g", "custom"];

  function resetForm() {
    $scope.editId = null;
    $scope.name = "";
    $scope.category_id = "";
    $scope.unit = "";
    $scope.price = "";
    $scope.stock = "";
    $scope.description = "";
    $scope.image_url = "";
    $scope.is_active = true;
    $scope.successMsg = "";
    $scope.errorMsg = "";
  }

  function loadCategories() {
    $http.get(apiUrl("/api/categories/")).then(function (res) {
      $scope.categories = res.data;
      $scope.categoryMap = {};
      res.data.forEach(function (category) {
        $scope.categoryMap[category.id] = category.name;
      });
    });
  }

  function loadProducts() {
    $http
      .get(apiUrl("/api/products/?active=false"))
      .then(function (res) {
        $scope.products = res.data;
      })
      .catch(function () {
        // Fallback to default active-only list
        $http.get(apiUrl("/api/products/")).then(function (res) {
          $scope.products = res.data;
        });
      });
  }

  $scope.resetForm = resetForm;

  loadCategories();
  loadProducts();
  resetForm();

  $scope.add = function () {
    $scope.successMsg = "";
    $scope.errorMsg = "";
    var payload = {
      name: $scope.name,
      category_id: $scope.category_id,
      unit: $scope.unit,
      price: $scope.price,
      stock: $scope.stock,
      description: $scope.description,
      image_url: $scope.image_url || null,
      is_active: $scope.is_active,
    };

    if ($scope.editId) {
      $http
        .put(apiUrl("/api/products/" + $scope.editId), payload)
        .then(function () {
          $scope.successMsg = "Product updated successfully.";
          resetForm();
          loadProducts();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to update product.";
        });
    } else {
      $http
        .post(apiUrl("/api/products/"), payload)
        .then(function () {
          $scope.successMsg = "Product added successfully.";
          resetForm();
          loadProducts();
        })
        .catch(function (err) {
          $scope.errorMsg =
            (err && err.data && (err.data.error || err.data.message)) ||
            "Failed to add product.";
        });
    }
  };

  $scope.deactivate = function (id) {
    if (!confirm("Deactivate this product? It will be hidden from the store.")) return;

    $scope.successMsg = "";
    $scope.errorMsg = "";
    $http
      .delete(apiUrl("/api/products/" + id))
      .then(function () {
        $scope.successMsg = "Product deactivated.";
        loadProducts();
      })
      .catch(function (err) {
        $scope.errorMsg =
          (err && err.data && (err.data.error || err.data.message)) ||
          "Failed to deactivate product.";
      });
  };

  // Alias for template compatibility
  $scope.remove = $scope.deactivate;

  $scope.edit = function (product) {
    $scope.editId = product.id;
    $scope.name = product.name;
    $scope.category_id = product.category_id;
    $scope.unit = product.unit;
    $scope.price = product.price;
    $scope.stock = product.stock;
    $scope.description = product.description;
    $scope.image_url = product.image_url || "";
    $scope.is_active = product.is_active;
    $scope.successMsg = "";
    $scope.errorMsg = "";
  };

  $scope.filtered = function () {
    var term = ($scope.search || "").toLowerCase();
    if (!term) return $scope.products;
    return ($scope.products || []).filter(function (product) {
      return (
        (product.name || "").toLowerCase().includes(term) ||
        (product.unit || "").toLowerCase().includes(term) ||
        ($scope.categoryMap[product.category_id] || "").toLowerCase().includes(term)
      );
    });
  };
});