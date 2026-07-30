(function () {
  const nav = [
    ["About", "index.html", "about"],
    ["Publications", "research.html", "publications"],
    ["Group", "group.html", "group"],
    ["Openings", "getinvolved.html", "opening"]
  ];
  const current = document.body.dataset.page || "about";
  const header = document.getElementById("site-header");
  if (!header) return;
  header.innerHTML = `
    <div class="mini-intro">
      <img class="avatar" src="img/hanghui-guo.jpg" alt="Hanghui Guo">
      <h1 id="hanghui-guo">Hanghui Guo</h1>
      <p class="role-line">PhD Student</p>
      <p class="affiliation-line">School of Computer Science and Engineering<br>
        Southeast University<br>
        Nanjing, China</p>
      <p class="profile-links">
        <a href="https://scholar.google.com/citations?user=S34GF9wAAAAJ&hl=en">Google Scholar</a> |
        <a href="https://www.researchgate.net/profile/Hanghui-Guo">ResearchGate</a> |
        <a href="https://www.linkedin.com/in/hanghui-guo-b58a03399/">LinkedIn</a> |
        <a href="https://dblp.org/pid/368/0534.html">DBLP</a> |
        <a href="https://github.com/ghh1125">GitHub</a> |
        <a href="https://www.semanticscholar.org/author/Hanghui-Guo/2283536492">Semantic Scholar</a>
      </p>
      <div id="menu">${nav.map(([label, href, key]) =>
        `<div class="${current === key ? "now" : ""}"><a href="${href}">${label}</a></div>`).join("")}</div>
    </div>`;
})();

(function () {
  const metrics = document.getElementById("scholar-metrics");
  if (!metrics) return;

  const cacheBuster = Date.now();
  const sources = [
    `https://raw.githubusercontent.com/ghh1125/ghh1125.github.io/google-scholar-stats/gs_data.json?ts=${cacheBuster}`,
    `scholar-metrics.json?ts=${cacheBuster}`
  ];

  const applyMetrics = (data) => {
    if (!data) return;
    const fields = {
      "scholar-citations": data.citedby ?? data.citations,
      "scholar-h-index": data.hindex ?? data.h_index,
      "scholar-i10-index": data.i10index ?? data.i10_index,
      "scholar-updated": data.updated
    };
    Object.entries(fields).forEach(([id, value]) => {
      if (value !== undefined && value !== null) {
        const element = document.getElementById(id);
        if (element) element.textContent = value;
      }
    });
  };

  const fetchSource = (index) => {
    if (index >= sources.length) return Promise.resolve();
    return fetch(sources[index], { cache: "no-store" })
      .then((response) => {
        if (!response.ok) throw new Error("Scholar data unavailable");
        return response.json();
      })
      .then(applyMetrics)
      .catch(() => fetchSource(index + 1));
  };

  fetchSource(0);
})();
