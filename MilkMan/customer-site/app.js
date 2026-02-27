(() => {
  const API_BASE =
    window.API_BASE ||
    (window.location.hostname ? "http://127.0.0.1:5000" : "http://127.0.0.1:5000");

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
  };
})();
