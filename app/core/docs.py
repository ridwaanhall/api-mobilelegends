from __future__ import annotations

from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse


SWAGGER_AUTH_STORAGE_KEY = "mlbb.swagger.auth"
SWAGGER_AUTH_STORAGE_TTL_SECONDS = 60 * 60 * 24


def build_swagger_ui_html(*, openapi_url: str, title: str, swagger_js_url: str, swagger_css_url: str) -> HTMLResponse:
    response = get_swagger_ui_html(
        openapi_url=openapi_url,
        title=title,
        swagger_js_url=swagger_js_url,
        swagger_css_url=swagger_css_url,
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "displayRequestDuration": True,
        },
    )

    script_tag = '<script src="/api/docs/auth.js"></script>'
    content = response.body.decode("utf-8").replace("</body>", f"{script_tag}</body>")
    return HTMLResponse(content=content, status_code=response.status_code)


def swagger_auth_script() -> str:
    return f"""
(function () {{
  const STORAGE_KEY = "{SWAGGER_AUTH_STORAGE_KEY}";
  const TTL_MS = {SWAGGER_AUTH_STORAGE_TTL_SECONDS} * 1000;
  const LOGOUT_PATH = "/api/user/auth/logout";

  function now() {{
    return Date.now();
  }}

  function loadStoredToken() {{
    try {{
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      const data = JSON.parse(raw);
      if (!data || !data.token || !data.expiresAt || data.expiresAt <= now()) {{
        localStorage.removeItem(STORAGE_KEY);
        return null;
      }}
      return data.token;
    }} catch (_) {{
      localStorage.removeItem(STORAGE_KEY);
      return null;
    }}
  }}

  function saveStoredToken(token) {{
    if (!token) return;
    localStorage.setItem(STORAGE_KEY, JSON.stringify({{
      token: token,
      expiresAt: now() + TTL_MS
    }}));
  }}

  function clearStoredToken() {{
    localStorage.removeItem(STORAGE_KEY);
  }}

  function normalizeToken(value) {{
    if (!value) return "";
    const trimmed = String(value).trim();
    return trimmed.toLowerCase().startsWith("bearer ")
      ? trimmed.slice(7).trim()
      : trimmed;
  }}

  const intervalId = setInterval(function () {{
    if (!window.ui || !window.ui.authActions || !window.ui.specSelectors) return;
    clearInterval(intervalId);

    const originalAuthorize = window.ui.authActions.authorize;
    const originalLogout = window.ui.authActions.logout;

    window.ui.authActions.authorize = function (payload) {{
      const result = originalAuthorize(payload);
      try {{
        const auth = payload && payload.HTTPBearer;
        const token = normalizeToken(auth && auth.value);
        if (token) {{
          saveStoredToken(token);
        }}
      }} catch (_) {{}}
      return result;
    }};

    window.ui.authActions.logout = function () {{
      clearStoredToken();
      return originalLogout.apply(this, arguments);
    }};

    const storedToken = loadStoredToken();
    if (storedToken && window.ui.preauthorizeApiKey) {{
      window.ui.preauthorizeApiKey("HTTPBearer", storedToken);
    }}

    const currentRequestInterceptor = window.ui.getConfigs().requestInterceptor;
    window.ui.getConfigs().requestInterceptor = function (request) {{
      if (request && request.url && request.url.indexOf(LOGOUT_PATH) !== -1) {{
        clearStoredToken();
        if (window.ui.authActions && window.ui.authActions.logout) {{
          originalLogout.call(window.ui.authActions, ["HTTPBearer"]);
        }}
      }}
      if (typeof currentRequestInterceptor === "function") {{
        return currentRequestInterceptor(request);
      }}
      return request;
    }};
  }}, 100);
}})();
""".strip()
