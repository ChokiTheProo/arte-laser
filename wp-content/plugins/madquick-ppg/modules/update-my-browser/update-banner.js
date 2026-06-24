(function (window, document) {
  "use strict";

  // Default browser data (fallback if API fails)
  let BROWSER_DATA = {
    chrome: {
      name: "Google Chrome",
      current: "131",
      minimum: "120",
      critical: "110",
      downloadUrl: "https://www.google.com/chrome/",
    },
    firefox: {
      name: "Mozilla Firefox",
      current: "133",
      minimum: "120",
      critical: "110",
      downloadUrl: "https://www.mozilla.org/firefox/",
    },
    safari: {
      name: "Safari",
      current: "18.2",
      minimum: "16.0",
      critical: "15.0",
      downloadUrl: "https://www.apple.com/safari/",
    },
    edge: {
      name: "Microsoft Edge",
      current: "131",
      minimum: "120",
      critical: "110",
      downloadUrl: "https://www.microsoft.com/edge",
    },
    opera: {
      name: "Opera",
      current: "116",
      minimum: "105",
      critical: "95",
      downloadUrl: "https://www.opera.com/",
    },
  };

  // Fetch latest browser versions from API
  const VersionAPI = {
    async fetchLatestVersions() {
      try {
        // Using a public API that provides browser version info
        const response = await fetch('https://api.github.com/repos/Fyrd/caniuse/contents/data.json', {
          headers: { 'Accept': 'application/vnd.github.v3.raw' }
        });

        if (!response.ok) throw new Error('API fetch failed');

        const data = await response.json();

        // Update versions from API data
        if (data.agents) {
          const agents = data.agents;

          if (agents.chrome && agents.chrome.versions) {
            const versions = agents.chrome.versions.filter(v => v !== null);
            BROWSER_DATA.chrome.current = versions[versions.length - 1];
          }

          if (agents.firefox && agents.firefox.versions) {
            const versions = agents.firefox.versions.filter(v => v !== null);
            BROWSER_DATA.firefox.current = versions[versions.length - 1];
          }

          if (agents.safari && agents.safari.versions) {
            const versions = agents.safari.versions.filter(v => v !== null);
            BROWSER_DATA.safari.current = versions[versions.length - 1];
          }

          if (agents.edge && agents.edge.versions) {
            const versions = agents.edge.versions.filter(v => v !== null);
            BROWSER_DATA.edge.current = versions[versions.length - 1];
          }

          if (agents.opera && agents.opera.versions) {
            const versions = agents.opera.versions.filter(v => v !== null);
            BROWSER_DATA.opera.current = versions[versions.length - 1];
          }
        }

        return true;
      } catch (error) {
        console.warn('Browser version API failed, using fallback data:', error);
        return false;
      }
    },
  };

  // UA detection
  const BrowserDetect = {
    init() {
      const ua = navigator.userAgent || "";
      const vendor = (navigator.vendor || "").toLowerCase();
      let m;
      if ((m = ua.match(/\bOPR\/([\d.]+)/))) {
        this.browser = "opera";
        this.version = m[1];
      } else if ((m = ua.match(/\bEdg\/([\d.]+)/))) {
        this.browser = "edge";
        this.version = m[1];
      } else if ((m = ua.match(/\bFirefox\/([\d.]+)/))) {
        this.browser = "firefox";
        this.version = m[1];
      } else if (
        /Safari\//.test(ua) &&
        !/Chrome|CriOS|OPR|Edg/.test(ua) &&
        vendor.includes("apple")
      ) {
        m = ua.match(/\bVersion\/([\d.]+)/);
        this.browser = "safari";
        this.version = (m && m[1]) || "0";
      } else if (
        /Chrome\/[\d.]+/.test(ua) &&
        !/OPR|Edg/.test(ua) &&
        vendor.includes("google")
      ) {
        m = ua.match(/\bChrome\/([\d.]+)/);
        this.browser = "chrome";
        this.version = (m && m[1]) || "0";
      } else {
        this.browser = "unknown";
        this.version = "0";
      }
      return {
        browser: this.browser,
        version: parseFloat(this.version),
        versionFull: this.version,
        isSupported: this.browser !== "unknown",
      };
    },
  };

  // Version status
  const StatusChecker = {
    getStatus(browser, version) {
      const d = BROWSER_DATA[browser];
      if (!d) return "unsupported";
      const cur = parseFloat(d.current),
        min = parseFloat(d.minimum),
        crit = parseFloat(d.critical);
      if (version >= cur) return "latest";
      if (version >= min) return "update";
      if (version >= crit) return "warning";
      return "critical";
    },
  };

  // Cookies
  const CookieManager = {
    set(name, value, days) {
      const expires = new Date(Date.now() + days * 864e5).toUTCString();
      document.cookie = `${name}=${value};expires=${expires};path=/;SameSite=Lax`;
    },
    get(name) {
      const k = name + "=";
      return (
        document.cookie
          .split(";")
          .map((s) => s.trim())
          .find((c) => c.startsWith(k))
          ?.slice(k.length) || null
      );
    },
    exists(name) {
      return !!this.get(name);
    },
  };

  // UI binder with modal
  const NotificationWidget = {
    messageFor(d, versionFull, status) {
      const m = {
        update: `You're using ${d.name} version ${versionFull}. A newer version (${d.current}) is available with improved performance and new features.`,
        warning: `Your ${d.name} (version ${versionFull}) is outdated. Update to version ${d.current} for important security patches.`,
        critical: `Your ${d.name} (version ${versionFull}) is seriously outdated and may have security vulnerabilities. Please update to version ${d.current} immediately.`,
      };
      return m[status] || m.warning;
    },
    show(browser, versionNum, versionFull, status, config = {}) {
      const el = document.getElementById("browser-notify-bar");
      if (!el) return;

      const d = BROWSER_DATA[browser];

      const iconEl = el.querySelector(".bnu-icon");
      const msgEl = el.querySelector(".bnu-message");
      const nameEl = el.querySelector(".bnu-browser-name");
      const linkEl = el.querySelector(".bnu-download-link");

      if (iconEl) {
        const icons = { update: "🔄", warning: "⚠️", critical: "🚨" };
        iconEl.textContent = icons[status] || "🔄";
      }

      if (msgEl) msgEl.textContent = this.messageFor(d, versionFull, status);
      if (nameEl) nameEl.textContent = d.name;

      const perBrowserOverride =
        (config.redirectUrlFor && config.redirectUrlFor[browser]) || null;
      const url = perBrowserOverride || config.redirectUrl || d.downloadUrl;

      if (linkEl) {
        linkEl.href = url;
        linkEl.textContent = `Update ${d.name}`;
      }

      // Close button
      const closeBtn = el.querySelector(".bnu-close");
      if (closeBtn && !closeBtn.dataset.bound) {
        closeBtn.dataset.bound = "1";
        closeBtn.addEventListener("click", (e) => {
          e.preventDefault();
          e.stopPropagation();
          this.hide(true);
        });
      }

      // Show banner with animation
      setTimeout(() => {
        el.style.display = "block";
        requestAnimationFrame(() => {
          el.classList.add("bnu-visible");
          document.body.classList.add("bnu-body-adjusted");
        });
      }, 800);
    },
    hide(persistent = false) {
      const el = document.getElementById("browser-notify-bar");
      if (!el) return;
      el.classList.remove("bnu-visible");
      document.body.classList.remove("bnu-body-adjusted");
      setTimeout(() => {
        el.style.display = "none";
      }, 400);
      if (persistent) CookieManager.set("browser_notify_hidden", "1", 1);
    },
  };

  // Entrypoint
  const BrowserNotify = {
    async init(config = {}) {
      const bar = document.getElementById("browser-notify-bar");
      if (!bar) return;

      if (CookieManager.exists("browser_notify_hidden")) {
        return NotificationWidget.hide();
      }

      if (
        config.showOnMobile !== true &&
        /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
          navigator.userAgent
        )
      ) {
        return NotificationWidget.hide();
      }

      // Fetch latest versions from API
      await VersionAPI.fetchLatestVersions();

      const det = BrowserDetect.init();
      if (!det.isSupported) return NotificationWidget.hide();

      const status = StatusChecker.getStatus(det.browser, det.version);
      if (status === "latest") return NotificationWidget.hide();

      NotificationWidget.show(det.browser, det.version, det.versionFull, status, config);
    },
  };

  // Auto-init
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => BrowserNotify.init());
  } else {
    BrowserNotify.init();
  }

  window.BrowserNotify = BrowserNotify;
})(window, document);
