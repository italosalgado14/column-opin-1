/* Carga gráficos Plotly definidos por shortcode {{ chart(id="...") }}.
 * - Lee JSON desde /data/charts/{id}.json
 * - Inyecta paper/plot bg y colores de tema según tema activo (light/dark/auto)
 * - Re-renderiza si el usuario cambia el tema
 */
(function () {
  if (typeof Plotly === "undefined") {
    console.warn("[charts] Plotly no está cargado.");
    return;
  }

  const containers = Array.from(document.querySelectorAll(".chart[data-chart-id]"));
  if (containers.length === 0) return;

  function isDark() {
    const t = document.documentElement.dataset.theme;
    if (t === "dark") return true;
    if (t === "light") return false;
    return window.matchMedia("(prefers-color-scheme: dark)").matches;
  }

  function themeOverlay() {
    const dark = isDark();
    return {
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(0,0,0,0)",
      font: { color: dark ? "#ebe7dc" : "#1a1a1a" },
      title: { font: { color: dark ? "#ebe7dc" : "#1a1a1a" } },
      xaxis: { gridcolor: dark ? "#2e2c25" : "#e2dfd7", zerolinecolor: dark ? "#2e2c25" : "#e2dfd7", color: dark ? "#c4bfb1" : "#4a4a4a" },
      yaxis: { gridcolor: dark ? "#2e2c25" : "#e2dfd7", zerolinecolor: dark ? "#2e2c25" : "#e2dfd7", color: dark ? "#c4bfb1" : "#4a4a4a" },
    };
  }

  async function loadChart(container) {
    const id = container.dataset.chartId;
    const target = container.querySelector(`#chart-${CSS.escape(id)}`);
    const placeholder = target.querySelector(".chart__placeholder");
    // Shortcode emits an absolute URL via Zola get_url; fallback for legacy.
    const url = container.dataset.chartUrl || `${window.location.origin}/data/charts/${id}.json`;

    try {
      const res = await fetch(url, { cache: "no-cache" });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const fig = await res.json();

      if (placeholder) placeholder.remove();

      const layout = Object.assign({}, fig.layout || {}, themeOverlay());
      // Merge xaxis/yaxis carefully (themeOverlay clobbers full axis)
      if (fig.layout?.xaxis) layout.xaxis = Object.assign({}, fig.layout.xaxis, themeOverlay().xaxis);
      if (fig.layout?.yaxis) layout.yaxis = Object.assign({}, fig.layout.yaxis, themeOverlay().yaxis);

      const config = {
        responsive: true,
        displaylogo: false,
        locale: "es",
        modeBarButtonsToRemove: ["lasso2d", "select2d", "autoScale2d"],
        toImageButtonOptions: { format: "png", filename: id, scale: 2 },
      };

      Plotly.newPlot(target, fig.data, layout, config);
      container.dataset.loaded = "true";
    } catch (err) {
      console.error(`[charts] error cargando ${id}:`, err);
      if (placeholder) {
        placeholder.textContent = `Error cargando gráfico: ${err.message}`;
        placeholder.classList.add("chart__placeholder--error");
      }
    }
  }

  // Carga inicial
  containers.forEach(loadChart);

  // Re-render al cambiar tema
  const observer = new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.attributeName === "data-theme") {
        containers.forEach((c) => {
          if (c.dataset.loaded !== "true") return;
          const target = c.querySelector(".chart__plot");
          Plotly.relayout(target, themeOverlay()).catch(() => {});
        });
      }
    }
  });
  observer.observe(document.documentElement, { attributes: true });
})();
