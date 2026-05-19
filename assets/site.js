const siteConfig = {
  name: "AI效率资源站",
  tagline: "面向大学生和职场新人的 AI 学习、求职与工具资源库",
  adPlaceholder: "赞助内容区域：后续展示与学习、求职和效率工具相关的合规推荐",
  sections: [
    {
      title: "校园效率区",
      href: "campus.html",
      accent: "accent-green",
      description: "四六级备考、期末作业结构化、活动策划模板，强调辅助学习而不是代写。"
    },
    {
      title: "求职冲刺区",
      href: "career.html",
      accent: "accent-blue",
      description: "自动化测试、简历优化、面试准备和项目表达，帮助新人把能力讲清楚。"
    },
    {
      title: "AI 工具箱",
      href: "tools.html",
      accent: "accent-amber",
      description: "GPT、Claude、提示词和账号安全基础，用合规方式提升效率。"
    }
  ],
  featuredResources: [
    {
      title: "四六级 AI 备考清单",
      href: "articles/cet-ai-study.html",
      category: "校园效率",
      summary: "把词汇、阅读、作文和听力拆成 14 天执行表。"
    },
    {
      title: "自动化测试面试题路线",
      href: "articles/automation-test-interview.html",
      category: "求职冲刺",
      summary: "从接口、UI 自动化、数据库到项目复盘的回答框架。"
    },
    {
      title: "提示词模板库入门",
      href: "articles/prompt-library.html",
      category: "AI 工具",
      summary: "用角色、目标、约束、输出格式四段式写出稳定 Prompt。"
    }
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

  const links = [
    ["首页", "index.html"],
    ["校园", "campus.html"],
    ["求职", "career.html"],
    ["工具", "tools.html"],
    ["关于", "about.html"]
  ];

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
      <p>${siteConfig.tagline}。本站内容用于学习和效率参考，不提供代写、作弊、绕过平台限制或规避风控服务。</p>
      <p>© ${year} ${siteConfig.name}. All rights reserved.</p>
    </div>
    <nav class="footer-links" aria-label="Footer">
      <a href="${resolvePath("about.html")}">关于本站</a>
      <a href="${resolvePath("privacy.html")}">隐私政策</a>
      <a href="${resolvePath("contact.html")}">联系合作</a>
      <a href="${resolvePath("sitemap.xml")}">站点地图</a>
    </nav>
  `;
}

function buildAdSlots() {
  document.querySelectorAll("[data-ad-slot]").forEach((slot) => {
    slot.innerHTML = `<div><strong>广告位</strong><span>${siteConfig.adPlaceholder}</span></div>`;
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
