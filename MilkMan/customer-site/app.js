(() => {
  const API_BASE =
    window.API_BASE ||
    (window.location.hostname ? "http://127.0.0.1:5000" : "http://127.0.0.1:5000");

  function getCustomerBasePath() {
    const { pathname } = window.location;
    const match = pathname.match(/^(.*\/customer\/)/);

    if (match) {
      return match[1];
    }

    if (pathname.endsWith("/customer")) {
      return `${pathname}/`;
    }

    return "/customer/";
  }

  const CUSTOMER_BASE_PATH = getCustomerBasePath();
  const PRODUCT_ASSET_BASE = `${CUSTOMER_BASE_PATH}assets/images/products/`;
  const PRODUCT_IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "webp", "avif", "svg"];
  const DEFAULT_PRODUCT_IMAGE_NAME = "default-dairy";
  const DEFAULT_PRODUCT_IMAGE = `${PRODUCT_ASSET_BASE}${DEFAULT_PRODUCT_IMAGE_NAME}.jpg`;
  const PRODUCT_IMAGE_MAP = [
    { match: ["milk", "cow milk", "buffalo milk"], file: "milk" },
    { match: ["curd", "yogurt", "dahi"], file: "curd" },
    { match: ["paneer", "cottage cheese"], file: "paneer" },
    { match: ["ghee"], file: "ghee" },
    { match: ["butter"], file: "butter" },
  ];

  function getCookie(name) {
    const match = document.cookie.match(
      new RegExp("(^|;\\s*)" + name.replace(/[-[\]{}()*+?.,\\\\^$|#\\s]/g, "\\$&") + "=([^;]*)")
    );
    return match ? decodeURIComponent(match[2]) : null;
  }

  function getStoredToken() {
    return sessionStorage.getItem("customer_token") || null;
  }

  function setStoredToken(token) {
    if (!token) {
      sessionStorage.removeItem("customer_token");
      return;
    }
    sessionStorage.setItem("customer_token", token);
  }

  function normalizeText(value) {
    return String(value || "")
      .trim()
      .toLowerCase();
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function formatCurrency(value) {
    const amount = Number(value || 0);
    return new Intl.NumberFormat("en-IN", {
      style: "currency",
      currency: "INR",
      maximumFractionDigits: 0,
    }).format(Number.isFinite(amount) ? amount : 0);
  }

  function buildLocalImageCandidates(name) {
    return PRODUCT_IMAGE_EXTENSIONS.map((ext) => `${PRODUCT_ASSET_BASE}${name}.${ext}`);
  }

  function uniqueList(values) {
    return values.filter((value, index) => value && values.indexOf(value) === index);
  }

  function normalizeProductImagePath(candidate) {
    if (typeof candidate !== "string" || !candidate.trim()) {
      return "";
    }

    const cleaned = candidate.trim().replace(/\\/g, "/");

    if (/^(https?:)?\/\//i.test(cleaned) || /^(data|blob):/i.test(cleaned)) {
      return cleaned;
    }

    if (cleaned.startsWith(CUSTOMER_BASE_PATH)) {
      return cleaned;
    }

    if (cleaned.startsWith("/customer/")) {
      return cleaned;
    }

    if (cleaned.startsWith("customer-site/")) {
      return `${CUSTOMER_BASE_PATH}${cleaned.replace(/^customer-site\//, "")}`;
    }

    if (cleaned.startsWith("MilkMan/customer-site/")) {
      return `${CUSTOMER_BASE_PATH}${cleaned.replace(/^MilkMan\/customer-site\//, "")}`;
    }

    if (cleaned.startsWith("./")) {
      return normalizeProductImagePath(cleaned.slice(2));
    }

    if (cleaned.startsWith("assets/")) {
      return `${CUSTOMER_BASE_PATH}${cleaned}`;
    }

    if (cleaned.startsWith("/assets/")) {
      return `${CUSTOMER_BASE_PATH}${cleaned.replace(/^\//, "")}`;
    }

    if (/^[^/]+\.(svg|png|jpe?g|webp|gif|avif)$/i.test(cleaned)) {
      return `${PRODUCT_ASSET_BASE}${cleaned}`;
    }

    if (cleaned.startsWith("/")) {
      return `${API_BASE}${cleaned}`;
    }

    if (/^(uploads|upload|media|static)\//i.test(cleaned)) {
      return `${API_BASE}/${cleaned}`;
    }

    return cleaned;
  }

  function getExplicitProductImage(product) {
    const candidates = [
      product && product.image,
      product && product.image_url,
      product && product.imageUrl,
      product && product.photo,
      product && product.thumbnail,
    ];

    for (const candidate of candidates) {
      const normalized = normalizeProductImagePath(candidate);
      if (normalized) {
        return normalized;
      }
    }

    return "";
  }

  function getMappedProductImages(product) {
    const haystack = [
      product && product.name,
      product && product.description,
      product && product.category,
      product && product.type,
    ]
      .map(normalizeText)
      .join(" ");

    const match = PRODUCT_IMAGE_MAP.find((entry) =>
      entry.match.some((token) => haystack.includes(token))
    );

    if (match) {
      return buildLocalImageCandidates(match.file);
    }

    return buildLocalImageCandidates(DEFAULT_PRODUCT_IMAGE_NAME);
  }

  function getDefaultProductImages() {
    return buildLocalImageCandidates(DEFAULT_PRODUCT_IMAGE_NAME);
  }

  function getMappedProductImage(product) {
    return getMappedProductImages(product)[0] || DEFAULT_PRODUCT_IMAGE;
  }

  function getProductImage(product) {
    return getExplicitProductImage(product) || getMappedProductImage(product);
  }

  function getProductImageSources(product) {
    const explicit = getExplicitProductImage(product);
    const sources = uniqueList([
      explicit,
      ...getMappedProductImages(product),
      ...getDefaultProductImages(),
    ]);

    return {
      primary: sources[0] || DEFAULT_PRODUCT_IMAGE,
      fallbacks: sources.slice(1),
      final: sources[sources.length - 1] || DEFAULT_PRODUCT_IMAGE,
    };
  }

  async function apiFetch(path, options = {}) {
    const url = path.startsWith("http") ? path : `${API_BASE}${path}`;
    const headers = new Headers(options.headers || {});

    if (!headers.has("Content-Type") && options.body !== undefined) {
      headers.set("Content-Type", "application/json");
    }

    const csrf = getCookie("csrf_access_token");
    if (csrf && !headers.has("X-CSRF-TOKEN")) {
      headers.set("X-CSRF-TOKEN", csrf);
    }

    const token = getStoredToken();
    if (token && !headers.has("Authorization")) {
      headers.set("Authorization", `Bearer ${token}`);
    }

    const res = await fetch(url, {
      ...options,
      headers,
      credentials: "include",
    });

    const isJson = (res.headers.get("content-type") || "").includes("application/json");
    const data = isJson ? await res.json().catch(() => null) : await res.text().catch(() => null);

    if (!res.ok) {
      const message =
        (data && typeof data === "object" && (data.error || data.message)) ||
        (typeof data === "string" ? data : "Request failed");
      const err = new Error(message);
      err.status = res.status;
      err.data = data;
      throw err;
    }

    return data;
  }

  async function customerSignup(payload) {
    const data = await apiFetch("/api/auth/customer/signup", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (data && data.token) setStoredToken(data.token);
    return data;
  }

  async function customerLogin(payload) {
    const data = await apiFetch("/api/auth/customer/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (data && data.token) setStoredToken(data.token);
    return data;
  }

  async function customerLogout() {
    try {
      await apiFetch("/api/auth/customer/logout", { method: "POST" });
    } finally {
      setStoredToken(null);
    }
  }

  async function customerMe() {
    return apiFetch("/api/auth/customer/me", { method: "GET" });
  }

  window.MilkMan = {
    API_BASE,
    apiFetch,
    auth: {
      signup: customerSignup,
      login: customerLogin,
      logout: customerLogout,
      me: customerMe,
      getToken: getStoredToken,
    },
    products: {
      assetBase: PRODUCT_ASSET_BASE,
      defaultImage: DEFAULT_PRODUCT_IMAGE,
      imageMap: PRODUCT_IMAGE_MAP,
      getImage: getProductImage,
      getImageSources: getProductImageSources,
    },
    utils: {
      escapeHtml,
      formatCurrency,
    },
  };
})();
