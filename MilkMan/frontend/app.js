var routeMeta = {
  "/": {
    templateUrl: "views/login.html",
    controller: "AuthController",
    label: "Sign In",
    eyebrow: "Admin Access",
    short: "IN",
  },
  "/dashboard": {
    templateUrl: "views/dashboard.html",
    controller: "DashboardController",
    requiresAuth: true,
    label: "Dashboard",
    eyebrow: "Operations Overview",
    short: "DB",
  },
  "/customers": {
    templateUrl: "views/customers.html",
    controller: "CustomerController",
    requiresAuth: true,
    label: "Customers",
    eyebrow: "Customer Records",
    short: "CU",
  },
  "/staff": {
    templateUrl: "views/staff.html",
    controller: "StaffController",
    requiresAuth: true,
    label: "Staff",
    eyebrow: "Team Management",
    short: "ST",
  },
  "/categories": {
    templateUrl: "views/categories.html",
    controller: "CategoryController",
    requiresAuth: true,
    label: "Categories",
    eyebrow: "Catalog Structure",
    short: "CA",
  },
  "/products": {
    templateUrl: "views/products.html",
    controller: "ProductController",
    requiresAuth: true,
    label: "Products",
    eyebrow: "Inventory Control",
    short: "PR",
  },
  "/subscriptions": {
    templateUrl: "views/subscriptions.html",
    controller: "SubscriptionController",
    requiresAuth: true,
    label: "Subscriptions",
    eyebrow: "Recurring Delivery Plans",
    short: "SU",
  },
  "/orders": {
    templateUrl: "views/orders.html",
    controller: "OrderController",
    requiresAuth: true,
    label: "Orders",
    eyebrow: "Delivery Requests",
    short: "OR",
  },
};

var navItems = [
  { path: "/dashboard", label: "Dashboard", icon: "bi-grid-1x2-fill" },
  { path: "/customers", label: "Customers", icon: "bi-people-fill" },
  { path: "/staff", label: "Staff", icon: "bi-person-badge-fill" },
  { path: "/categories", label: "Categories", icon: "bi-tags-fill" },
  { path: "/products", label: "Products", icon: "bi-box-seam-fill" },
  { path: "/subscriptions", label: "Subscriptions", icon: "bi-arrow-repeat" },
  { path: "/orders", label: "Orders", icon: "bi-bag-check-fill" },
];

var app = angular.module("milkApp", ["ngRoute"]);

app.run(function ($rootScope, $location) {
  function syncRouteMeta() {
    $rootScope.currentRouteMeta = routeMeta[$location.path()] || routeMeta["/dashboard"];
  }

  $rootScope.navItems = navItems;
  $rootScope.isLoggedIn = !!localStorage.getItem("token");
  $rootScope.adminName = localStorage.getItem("admin_name") || "Administrator";
  $rootScope.sidebarOpen = false;

  $rootScope.isAuthRoute = function () {
    return $location.path() === "/";
  };

  $rootScope.isActive = function (path) {
    return $location.path() === path;
  };

  $rootScope.toggleSidebar = function () {
    $rootScope.sidebarOpen = !$rootScope.sidebarOpen;
  };

  $rootScope.closeSidebar = function () {
    $rootScope.sidebarOpen = false;
  };

  $rootScope.logout = function () {
    localStorage.removeItem("token");
    localStorage.removeItem("admin_name");
    $rootScope.isLoggedIn = false;
    $rootScope.adminName = "Administrator";
    $rootScope.closeSidebar();
    $location.path("/");
  };

  $rootScope.$on("$routeChangeStart", function (event, next) {
    if (next && next.requiresAuth && !localStorage.getItem("token")) {
      event.preventDefault();
      $rootScope.isLoggedIn = false;
      $rootScope.adminName = "Administrator";
      $location.path("/");
    }
  });

  $rootScope.$on("$routeChangeSuccess", function () {
    $rootScope.isLoggedIn = !!localStorage.getItem("token");
    $rootScope.adminName = localStorage.getItem("admin_name") || "Administrator";
    $rootScope.closeSidebar();
    syncRouteMeta();
  });

  syncRouteMeta();
});

app.config(function ($routeProvider, $httpProvider) {
  $httpProvider.interceptors.push(function ($q, $location, $rootScope) {
    return {
      request: function (config) {
        var token = localStorage.getItem("token");
        if (token) {
          config.headers = config.headers || {};
          config.headers.Authorization = "Bearer " + token;
        }
        return config;
      },
      responseError: function (rejection) {
        if (rejection && rejection.status === 401) {
          localStorage.removeItem("token");
          localStorage.removeItem("admin_name");
          $rootScope.isLoggedIn = false;
          $rootScope.adminName = "Administrator";
          $location.path("/");
        }
        return $q.reject(rejection);
      },
    };
  });

  angular.forEach(routeMeta, function (config, path) {
    $routeProvider.when(path, config);
  });

  $routeProvider.otherwise({ redirectTo: "/" });
});
