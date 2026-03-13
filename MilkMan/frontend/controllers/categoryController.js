app.controller("CategoryController", function ($scope, $http) {
  var apiUrl = window.MilkManAdmin.apiUrl;
  $scope.editId = null;

  function resetForm() {
    $scope.editId = null;
    $scope.name = "";
    $scope.description = "";
  }

  function load() {
    $http.get(apiUrl("/api/categories/")).then(function (res) {
      $scope.categories = res.data;
    });
  }

  $scope.resetForm = resetForm;

  load();

  $scope.add = function () {
    var payload = {
      name: $scope.name,
      description: $scope.description,
    };

    if ($scope.editId) {
      $http
        .put(apiUrl("/api/categories/" + $scope.editId), payload)
        .then(function () {
          alert("Category updated");
          resetForm();
          load();
        });
    } else {
      $http.post(apiUrl("/api/categories/"), payload).then(function () {
        alert("Category added");
        resetForm();
        load();
      });
    }
  };

  $scope.remove = function (id) {
    if (!confirm("Delete this category?")) return;

    $http.delete(apiUrl("/api/categories/" + id)).then(function () {
      alert("Category deleted");
      load();
    });
  };

  $scope.edit = function (category) {
    $scope.editId = category.id;
    $scope.name = category.name;
    $scope.description = category.description;
  };
});