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
      <p class="contact-line"><code>ghh1125 [at] zjnu [dot] edu [dot] cn</code></p>
      <p class="role-line">PhD Student in Computer Science and Technology</p>
      <p class="affiliation-line">School of Computer Science and Engineering<br>
        Southeast University<br>
        Nanjing, China</p>
      <p class="profile-links">
        <a href="mailto:ghh1125@zjnu.edu.cn">Email</a> |
        <a href="https://scholar.google.com/citations?user=S34GF9wAAAAJ&hl=en">Google Scholar</a> |
        <a href="https://www.researchgate.net/profile/Hanghui-Guo">ResearchGate</a> |
        <a href="https://www.linkedin.com/in/hanghui-guo-b58a03399/">LinkedIn</a> |
        <a href="https://dblp.org/pid/368/0534.html">DBLP</a> |
        <a href="https://github.com/ghh1125">GitHub</a>
      </p>
      <div id="menu">${nav.map(([label, href, key]) =>
        `<div class="${current === key ? "now" : ""}"><a href="${href}">${label}</a></div>`).join("")}</div>
    </div>`;
})();
