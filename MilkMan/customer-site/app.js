(() => {
  const API_BASE =
    ((window.MILKMAN_RUNTIME && window.MILKMAN_RUNTIME.apiBaseUrl) || window.API_BASE || "").replace(/\/+$/, "") ||
    `${window.location.protocol}//${window.location.hostname}:5000`;

  // ── Image system ──────────────────────────────────────────────────────────

  function getCustomerBasePath() {
    const { pathname } = window.location;
    const match = pathname.match(/^(.*\/customer\/)/);
    if (match) return match[1];
    if (pathname.endsWith("/customer")) return `${pathname}/`;
    return "/";
  }

  const CUSTOMER_BASE_PATH = getCustomerBasePath();
  const PRODUCT_ASSET_BASE = `${CUSTOMER_BASE_PATH}assets/images/products/`;
  const DEFAULT_PRODUCT_IMAGE = `${PRODUCT_ASSET_BASE}default-dairy.png`;
  const PRODUCT_IMAGE_MAP = [
    { match: ["milk", "cow milk", "buffalo milk", "full cream"], file: "milk" },
    { match: ["curd", "yogurt", "dahi"], file: "curd" },
    { match: ["paneer", "cottage cheese"], file: "paneer" },
    { match: ["ghee"], file: "ghee" },
    { match: ["butter"], file: "butter" },
  ];
  const PRODUCT_IMAGE_EXTENSIONS = ["avif", "jpg", "jpeg", "png", "webp", "svg"];

  function normalizeText(value) {
    return String(value || "").trim().toLowerCase();
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

  /**
   * Resolve any image path to a full URL.
   * Paths starting with /static/ are served by Flask, so prepend API_BASE.
   */
  function resolveImageUrl(path) {
    if (typeof path !== "string" || !path.trim()) return "";
    const cleaned = path.trim().replace(/\\/g, "/");
    // Already absolute URL — return as-is
    if (/^(https?:)?\/\//i.test(cleaned) || /^(data|blob):/i.test(cleaned)) return cleaned;
    // Flask-served static assets — prepend API_BASE
    if (cleaned.startsWith("/static/")) return `${API_BASE}${cleaned}`;
    return cleaned;
  }

  function normalizeProductImagePath(candidate) {
    if (typeof candidate !== "string" || !candidate.trim()) return "";
    const cleaned = candidate.trim().replace(/\\/g, "/");
    if (/^(https?:)?\/\//i.test(cleaned) || /^(data|blob):/i.test(cleaned)) return cleaned;
    // Flask static assets — prepend API_BASE so browser can reach them
    if (cleaned.startsWith("/static/")) return `${API_BASE}${cleaned}`;
    if (cleaned.startsWith("/assets/")) return cleaned;
    if (cleaned.startsWith("assets/")) return `/${cleaned}`;
    if (/^[^/]+\.(svg|png|jpe?g|webp|gif|avif)$/i.test(cleaned)) return `${PRODUCT_ASSET_BASE}${cleaned}`;
    if (cleaned.startsWith("/")) return cleaned;
    return cleaned;
  }

  function getExplicitProductImage(product) {
    const candidates = [
      product && product.image_url,
      product && product.image,
      product && product.imageUrl,
      product && product.photo,
    ];
    for (const candidate of candidates) {
      const normalized = normalizeProductImagePath(candidate);
      if (normalized) return normalized;
    }
    return "";
  }

  function getMappedProductImages(product) {
    const haystack = [product && product.name, product && product.description, product && product.category]
      .map(normalizeText)
      .join(" ");
    const match = PRODUCT_IMAGE_MAP.find(entry => entry.match.some(token => haystack.includes(token)));
    const baseName = match ? match.file : "default-dairy";
    return PRODUCT_IMAGE_EXTENSIONS.map(ext => `${PRODUCT_ASSET_BASE}${baseName}.${ext}`);
  }

  function getProductImageSources(product) {
    const explicit = getExplicitProductImage(product);
    const mapped = getMappedProductImages(product);
    const sources = [explicit, ...mapped].filter((v, i, a) => v && a.indexOf(v) === i);
    return {
      primary: sources[0] || DEFAULT_PRODUCT_IMAGE,
      fallbacks: sources.slice(1),
      final: sources[sources.length - 1] || DEFAULT_PRODUCT_IMAGE,
    };
  }

  function getProductImage(product) {
    return getExplicitProductImage(product) || getMappedProductImages(product)[0] || DEFAULT_PRODUCT_IMAGE;
  }

  // ── Toast system ──────────────────────────────────────────────────────────

  function showToast(message, type = "success") {
    let container = document.getElementById("mm-toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "mm-toast-container";
      container.style.cssText = "position:fixed;bottom:2rem;right:2rem;z-index:99999;display:flex;flex-direction:column;gap:0.75rem;";
      document.body.appendChild(container);
    }

    const colors = {
      success: { bg: "#eef5ec", border: "#7cb87a", icon: "✅" },
      error:   { bg: "#fdf0ec", border: "#d4856a", icon: "❌" },
      danger:  { bg: "#fdf0ec", border: "#d4856a", icon: "❌" },
      info:    { bg: "#fdf8f0", border: "#e8a838", icon: "ℹ️" },
    };
    const c = colors[type] || colors.info;

    const toast = document.createElement("div");
    toast.style.cssText = `
      background:${c.bg};border-left:4px solid ${c.border};border-radius:12px;
      padding:1rem 1.5rem;min-width:280px;max-width:400px;
      box-shadow:0 4px 24px rgba(124,100,60,0.12);
      display:flex;align-items:center;gap:0.75rem;
      font-family:'Plus Jakarta Sans',sans-serif;font-size:0.9rem;
      color:#2c2416;opacity:0;transform:translateY(12px);
      transition:all 0.3s cubic-bezier(0.16,1,0.3,1);
    `;
    toast.innerHTML = `<span style="font-size:1.2rem">${c.icon}</span><span>${escapeHtml(message)}</span>`;
    container.appendChild(toast);

    requestAnimationFrame(() => {
      toast.style.opacity = "1";
      toast.style.transform = "translateY(0)";
    });

    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateY(-8px)";
      setTimeout(() => toast.remove(), 350);
    }, 4000);
  }

  // ── Auth storage ──────────────────────────────────────────────────────────

  function getStoredToken() {
    return sessionStorage.getItem("customer_token") || null;
  }

  function setStoredToken(token) {
    if (!token) {
      sessionStorage.removeItem("customer_token");
    } else {
      sessionStorage.setItem("customer_token", token);
    }
  }

  function setStoredUser(user) {
    if (!user) {
      sessionStorage.removeItem("customer_user");
      sessionStorage.removeItem("customer_role");
    } else {
      sessionStorage.setItem("customer_user", JSON.stringify(user));
    }
  }

  function setStoredRole(role) {
    if (!role) {
      sessionStorage.removeItem("customer_role");
    } else {
      sessionStorage.setItem("customer_role", role);
    }
  }

  function getStoredUser() {
    try {
      const raw = sessionStorage.getItem("customer_user");
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  function isLoggedIn() {
    return !!getStoredToken();
  }

  // ── Cookie helpers (for CSRF) ─────────────────────────────────────────────

  function getCookie(name) {
    const match = document.cookie.match(
      new RegExp("(^|;\\s*)" + name.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&") + "=([^;]*)")
    );
    return match ? decodeURIComponent(match[2]) : null;
  }

  // ── API fetch ─────────────────────────────────────────────────────────────

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

    const res = await fetch(url, { ...options, headers, credentials: "include" });

    const isJson = (res.headers.get("content-type") || "").includes("application/json");
    const data = isJson ? await res.json().catch(() => null) : await res.text().catch(() => null);

    if (res.status === 401) {
      // Token expired — clear and redirect to login
      setStoredToken(null);
      setStoredUser(null);
      setStoredRole(null);
      if (!window.location.pathname.endsWith("login.html")) {
        window.location.href = "login.html";
      }
      return null;
    }

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

  // ── Auth functions ────────────────────────────────────────────────────────

  async function customerLogin(payload) {
    const data = await apiFetch("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (data) {
      // Reject non-customers
      if (data.role && data.role !== "customer") {
        throw new Error("Please use the admin panel to log in.");
      }
      const token = data.access_token || data.token;
      if (token) setStoredToken(token);
      if (data.user) setStoredUser(data.user);
      if (data.role) setStoredRole(data.role);
    }
    return data;
  }

  async function customerSignup(payload) {
    const data = await apiFetch("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(payload),
    });
    if (data) {
      const token = data.access_token || data.token;
      if (token) setStoredToken(token);
      if (data.user) setStoredUser(data.user);
      if (data.role) setStoredRole(data.role);
    }
    return data;
  }

  async function customerLogout() {
    try {
      await apiFetch("/api/auth/customer/logout", { method: "POST" });
    } catch {}
    setStoredToken(null);
    setStoredUser(null);
    setStoredRole(null);
    window.location.href = "login.html";
  }

  async function customerMe() {
    // IMPORTANT: this function MUST throw when not authenticated.
    // Every caller uses try/catch — returning null silently breaks all auth guards.

    // Fast path: no token stored → definitely not logged in
    const token = getStoredToken();
    if (!token) {
      setStoredUser(null);
      setStoredRole(null);
      throw new Error("Not authenticated");
    }

    // Validate token with the live API (catches expired tokens)
    let data;
    try {
      data = await apiFetch("/api/auth/customer/me", { method: "GET" });
    } catch (err) {
      // Network or API error — clear stale data and propagate
      setStoredToken(null);
      setStoredUser(null);
      setStoredRole(null);
      throw err;
    }

    if (!data) {
      // apiFetch returned null — 401 was already handled (storage cleared, redirect queued)
      // Still throw so callers' catch blocks can run their own redirect logic
      throw new Error("Not authenticated");
    }

    // Success — refresh cached profile
    setStoredUser(data);
    return data;
  }


  // ── Celebrate overlay ─────────────────────────────────────────────────────

  function celebrate() {
    const overlay = document.createElement("div");
    overlay.style.cssText =
      "position:fixed;inset:0;background:rgba(253,250,245,0.95);backdrop-filter:blur(10px);" +
      "display:grid;place-items:center;z-index:20000;opacity:0;transition:opacity 0.4s ease;";
    overlay.innerHTML = `
      <div style="text-align:center">
        <div style="font-size:5rem;margin-bottom:1.5rem;animation:bounce 0.6s ease">🎉</div>
        <h2 style="font-family:'Syne',sans-serif;font-size:2.5rem;font-weight:800;color:#2c2416;margin-bottom:0.75rem">Subscribed!</h2>
        <p style="color:#6b5b45;font-size:1.1rem">Your fresh dairy journey begins tomorrow morning 🥛</p>
      </div>`;
    document.body.appendChild(overlay);
    requestAnimationFrame(() => (overlay.style.opacity = "1"));
    setTimeout(() => {
      overlay.style.opacity = "0";
      setTimeout(() => overlay.remove(), 400);
    }, 2500);
  }

  // ── Custom cursor ─────────────────────────────────────────────────────────

  function initCursor() {
    if (window.innerWidth < 768) return;
    const cursor = document.createElement("div");
    cursor.id = "mm-cursor";
    const follower = document.createElement("div");
    follower.id = "mm-cursor-follower";
    document.body.appendChild(cursor);
    document.body.appendChild(follower);

    let mouseX = 0, mouseY = 0, followerX = 0, followerY = 0;
    window.addEventListener("mousemove", e => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      cursor.style.left = mouseX + "px";
      cursor.style.top = mouseY + "px";
    });
    (function animateFollower() {
      followerX += (mouseX - followerX) * 0.15;
      followerY += (mouseY - followerY) * 0.15;
      follower.style.left = followerX + "px";
      follower.style.top = followerY + "px";
      requestAnimationFrame(animateFollower);
    })();

    document.addEventListener("mouseover", e => {
      if (e.target.closest("a, button, input, textarea, [role=button], .mm-card")) {
        document.body.classList.add("cursor-hover");
      }
    });
    document.addEventListener("mouseout", e => {
      if (e.target.closest("a, button, input, textarea, [role=button], .mm-card")) {
        document.body.classList.remove("cursor-hover");
      }
    });
  }

  function initMagnetic() {
    if (window.innerWidth < 768) return;
    document.querySelectorAll(".mm-magnetic").forEach(mag => {
      mag.addEventListener("mousemove", e => {
        const rect = mag.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        mag.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px) scale(1.05)`;
      });
      mag.addEventListener("mouseleave", () => (mag.style.transform = ""));
    });
  }

  function getProductEmoji(name = "", category = "") {
    const n = (name + " " + category).toLowerCase();
    if (n.includes("milk")) return "🥛";
    if (n.includes("ghee")) return "🫙";
    if (n.includes("butter")) return "🧈";
    if (n.includes("paneer")) return "🧀";
    if (n.includes("curd") || n.includes("yogurt")) return "🥣";
    return "🌿";
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => { initCursor(); initMagnetic(); });
  } else {
    initCursor();
    initMagnetic();
  }

  // ── Public API ────────────────────────────────────────────────────────────

  window.MilkMan = {
    API_BASE,
    apiFetch,
    auth: {
      login: customerLogin,
      signup: customerSignup,
      logout: customerLogout,
      me: customerMe,
      getToken: getStoredToken,
      getUser: getStoredUser,
      isLoggedIn,
    },
    products: {
      assetBase: PRODUCT_ASSET_BASE,
      defaultImage: DEFAULT_PRODUCT_IMAGE,
      imageMap: PRODUCT_IMAGE_MAP,
      getImage: getProductImage,
      getImageSources: getProductImageSources,
      getEmoji: getProductEmoji,
    },
    utils: {
      escapeHtml,
      formatCurrency,
      showToast,
      celebrate,
      initMagnetic,
      resolveImageUrl,
    },
    toast: {
      success: msg => showToast(msg, "success"),
      error: msg => showToast(msg, "error"),
      info: msg => showToast(msg, "info"),
    },
  };
})();
