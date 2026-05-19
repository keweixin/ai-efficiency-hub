const siteConfig = {
  name: "AI效率资源站",
  tagline: "面向大学生和职场新人的 AI 学习、求职与工具资源库",
  adPlaceholder: "赞助内容区域：后续展示与学习、求职和效率工具相关的合规推荐",
  featuredResources: [
    { title: "四六级 14 天备考计划", href: "articles/cet-14-day-study-plan.html", category: "校园效率", summary: "把词汇、阅读、听力、作文拆成每天可执行任务。" },
    { title: "自动化测试面试准备路线", href: "articles/automation-test-interview-roadmap.html", category: "求职冲刺", summary: "按接口、UI、数据库、框架和项目复盘准备。" },
    { title: "稳定 Prompt 的四段式公式", href: "articles/prompt-four-part-formula.html", category: "AI 工具", summary: "用角色、目标、材料、输出格式提升回答稳定性。" }
  ]
};

function resolvePath(path) {
  const inArticle = location.pathname.includes("/articles/");
  if (/^https?:/.test(path) || path.startsWith("#")) return path;
  return inArticle ? `../${path}` : path;
}

function buildNav() {
  const nav = document.querySelector("[data-site-nav]");
  if (!nav) return;
  const links = [["首页", "index.html"], ["校园", "campus.html"], ["求职", "career.html"], ["工具", "tools.html"], ["关于", "about.html"]];
  const current = location.pathname.split("/").pop() || "index.html";
  nav.innerHTML = links.map(([label, href]) => {
    const active = current === href ? ' aria-current="page"' : "";
    return `<a href="${resolvePath(href)}"${active}>${label}</a>`;
  }).join("");
}

function buildFooter() {
  const footer = document.querySelector("[data-site-footer]");
  if (!footer) return;
  const year = new Date().getFullYear();
  footer.innerHTML = `
    <div>
      <strong>${siteConfig.name}</strong>
      <p>${siteConfig.tagline}。本站内容用于学习和效率参考，不替代课程要求、考试规则、官方文档或个人判断。</p>
      <p>© ${year} ${siteConfig.name}. All rights reserved.</p>
    </div>
    <nav class="footer-links" aria-label="Footer">
      <a href="${resolvePath("about.html")}">关于本站</a>
      <a href="${resolvePath("privacy.html")}">隐私政策</a>
      <a href="${resolvePath("contact.html")}">联系合作</a>
      <a href="${resolvePath("sitemap.xml")}">站点地图</a>
    </nav>`;
}

function buildAdSlots() {
  document.querySelectorAll("[data-ad-slot]").forEach((slot) => {
    slot.innerHTML = `<div><strong>赞助内容区域</strong><span>${siteConfig.adPlaceholder}</span></div>`;
  });
}

function buildFeaturedResources() {
  const target = document.querySelector("[data-featured-resources]");
  if (!target) return;
  target.innerHTML = siteConfig.featuredResources.map((item) => `
    <article class="resource-card">
      <span class="tag">${item.category}</span>
      <h3>${item.title}</h3>
      <p>${item.summary}</p>
      <a class="card-link" href="${resolvePath(item.href)}">查看资源</a>
    </article>
  `).join("");
}

document.addEventListener("DOMContentLoaded", () => {
  buildNav();
  buildFooter();
  buildAdSlots();
  buildFeaturedResources();
});
