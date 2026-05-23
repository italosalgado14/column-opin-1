(function () {
  const KEY = "columna-theme";
  const root = document.documentElement;
  const stored = localStorage.getItem(KEY);
  if (stored === "dark" || stored === "light") {
    root.dataset.theme = stored;
  }

  const btn = document.getElementById("theme-toggle");
  if (!btn) return;

  btn.addEventListener("click", () => {
    const current = root.dataset.theme;
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    let next;
    if (current === "auto" || !current) {
      next = prefersDark ? "light" : "dark";
    } else if (current === "dark") {
      next = "light";
    } else {
      next = "dark";
    }
    root.dataset.theme = next;
    localStorage.setItem(KEY, next);
  });
})();
