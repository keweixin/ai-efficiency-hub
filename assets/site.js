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
  const links = [["首页", "index.html"], ["文章", "articles.html"], ["校园", "campus.html"], ["求职", "career.html"], ["工具", "tools.html"], ["关于", "about.html"]];
  const current = location.pathname.split("/").pop() || "index.html";
  const section = document.body.dataset.section || "";
  const activeBySection = { campus: "campus.html", career: "career.html", tools: "tools.html", articles: "articles.html" };
  nav.innerHTML = links.map(([label, href]) => {
    const active = current === href || activeBySection[section] === href ? ' aria-current="page"' : "";
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
      <p>${siteConfig.tagline}。本站坚决抵制任何形式的学术越界或违反学术诚信的行为。所有 AI 工具使用方法均旨在辅助思路拆解与学习效率提升，最终成果的真实性与合规性完全由使用者个人负责，请严格遵守所在学校、考试中心和工作单位的守则。</p>
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

async function buildArticleSearch() {
  const target = document.querySelector("[data-article-index]");
  const panel = document.querySelector("[data-search-panel]");
  if (!target || !panel) return;
  let items = [];
  try {
    const response = await fetch(resolvePath("assets/search-index.json"));
    items = await response.json();
  } catch (error) {
    items = Array.from(target.querySelectorAll(".article-card")).map((card) => ({
      title: card.querySelector("h2")?.textContent || "",
      description: card.querySelector("p")?.textContent || "",
      href: card.querySelector("a")?.getAttribute("href") || "#",
      group: card.dataset.group || "",
      tag: card.dataset.tag || "",
      keyword: card.textContent || ""
    }));
  }
  const input = panel.querySelector("#article-search");
  const count = panel.querySelector("[data-search-count]");
  let group = new URLSearchParams(location.search).get("group") || "all";
  let tag = "all";
  const render = () => {
    const q = (input.value || "").trim().toLowerCase();
    const filtered = items.filter((item) => {
      const text = `${item.title} ${item.description} ${item.tag} ${item.keyword}`.toLowerCase();
      return (group === "all" || item.group === group) && (tag === "all" || item.tag === tag) && (!q || text.includes(q));
    });
    target.innerHTML = filtered.map((item) => `<article class="article-card" data-group="${item.group}" data-tag="${item.tag}"><div class="tag-list"><span class="tag free">免费文章</span><span class="tag">${item.tag}</span></div><h2>${item.title}</h2><p>${item.description}</p><a class="card-link" href="${item.href}">阅读文章</a></article>`).join("") || `<p class="empty-state">没有找到匹配文章，可以换一个关键词。</p>`;
    if (count) count.textContent = `共 ${filtered.length} 篇文章`;
  };
  panel.querySelectorAll("[data-filter-group]").forEach((button) => {
    if (button.dataset.filterGroup === group) button.classList.add("is-active");
    button.addEventListener("click", () => {
      group = button.dataset.filterGroup || "all";
      panel.querySelectorAll("[data-filter-group]").forEach((el) => el.classList.toggle("is-active", el === button));
      render();
    });
  });
  panel.querySelectorAll("[data-filter-tag]").forEach((button) => {
    button.addEventListener("click", () => {
      tag = button.dataset.filterTag || "all";
      panel.querySelectorAll("[data-filter-tag]").forEach((el) => el.classList.toggle("is-active", el === button));
      render();
    });
  });
  input?.addEventListener("input", render);
  render();
}

function initCopyButtons() {
  document.querySelectorAll(".copy-button").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const pre = btn.previousElementSibling;
      const code = pre ? (pre.querySelector("code")?.textContent || "") : "";
      try {
        await navigator.clipboard.writeText(code);
        const originalText = btn.textContent || "复制";
        btn.textContent = "已复制！";
        btn.classList.add("copied");
        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove("copied");
        }, 2000);
      } catch (err) {
        console.error("Failed to copy:", err);
      }
    });
  });
}


function initInteractiveTools() {
  // --- Tab Switcher Logic ---
  const tabButtons = document.querySelectorAll(".tool-tab-btn");
  const tabContents = document.querySelectorAll(".tool-tab-content");
  if (tabButtons.length > 0) {
    tabButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const tabId = btn.dataset.tab;
        tabButtons.forEach((b) => {
          b.classList.toggle("active", b === btn);
          b.setAttribute("aria-selected", b === btn ? "true" : "false");
        });
        tabContents.forEach((content) => {
          if (content.id === `${tabId}-panel`) {
            content.style.display = "block";
            content.classList.add("active");
          } else {
            content.style.display = "none";
            content.classList.remove("active");
          }
        });
      });
    });
  }

  // --- GPA Calculator Logic ---
  const container = document.getElementById("course-rows-container");
  const addBtn = document.getElementById("add-course-btn");
  const resetBtn = document.getElementById("reset-gpa-btn");
  const gpaValDisplay = document.getElementById("gpa-val-display");
  const weightedScoreDisplay = document.getElementById("weighted-score-display");
  const totalCreditsDisplay = document.getElementById("total-credits-display");
  const gpa5Display = document.getElementById("gpa-5-display");
  const gpaProgressRing = document.getElementById("gpa-progress-ring");
  const gpaEvaluationText = document.getElementById("gpa-evaluation-text");

  let courseCount = 0;

  function scoreToGpa4(score) {
    if (score >= 90) return 4.0;
    if (score >= 85) return 3.7;
    if (score >= 82) return 3.3;
    if (score >= 78) return 3.0;
    if (score >= 75) return 2.7;
    if (score >= 72) return 2.3;
    if (score >= 68) return 2.0;
    if (score >= 64) return 1.5;
    if (score >= 60) return 1.0;
    return 0.0;
  }

  function scoreToGpa5(score) {
    if (score < 60) return 0.0;
    return parseFloat(((score - 50) / 10).toFixed(2));
  }

  function createCourseRow(name = "", credits = 3.0, score = 90) {
    courseCount++;
    const row = document.createElement("div");
    row.className = "course-row";
    row.id = `course-row-${courseCount}`;
    const nameId = `course-name-${courseCount}`;
    const creditId = `course-credit-${courseCount}`;
    const scoreId = `course-score-${courseCount}`;
    row.innerHTML = `
      <div class="row-field name-field">
        <label class="sr-only" for="${nameId}">第 ${courseCount} 门课程名称</label>
        <input id="${nameId}" type="text" class="course-name-input" placeholder="课程名称（可选）" value="${name}">
      </div>
      <div class="row-field credit-field">
        <label class="sr-only" for="${creditId}">第 ${courseCount} 门课程学分</label>
        <input id="${creditId}" type="number" class="course-credit-input" min="0.5" max="10" step="0.5" placeholder="学分" value="${credits}">
      </div>
      <div class="row-field score-field">
        <label class="sr-only" for="${scoreId}">第 ${courseCount} 门课程百分制成绩</label>
        <input id="${scoreId}" type="number" class="course-score-input" min="0" max="100" placeholder="成绩" value="${score}">
      </div>
      <button class="btn-remove-row" type="button" title="删除此行" aria-label="删除第 ${courseCount} 门课程">
        <svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
      </button>
    `;

    row.querySelectorAll("input").forEach((input) => {
      input.addEventListener("input", calculateGpa);
    });

    row.querySelector(".btn-remove-row").addEventListener("click", () => {
      row.remove();
      calculateGpa();
    });

    container.appendChild(row);
  }

  function calculateGpa() {
    const rows = container.querySelectorAll(".course-row");
    let totalWeightedScore = 0;
    let totalWeightedGpa4 = 0;
    let totalWeightedGpa5 = 0;
    let totalCredits = 0;

    rows.forEach((row) => {
      const creditInput = row.querySelector(".course-credit-input");
      const scoreInput = row.querySelector(".course-score-input");

      const credits = parseFloat(creditInput.value) || 0;
      const score = parseFloat(scoreInput.value) || 0;

      if (credits > 0) {
        totalCredits += credits;
        totalWeightedScore += score * credits;
        totalWeightedGpa4 += scoreToGpa4(score) * credits;
        totalWeightedGpa5 += scoreToGpa5(score) * credits;
      }
    });

    if (totalCredits > 0) {
      const avgScore = totalWeightedScore / totalCredits;
      const avgGpa4 = totalWeightedGpa4 / totalCredits;
      const avgGpa5 = totalWeightedGpa5 / totalCredits;

      weightedScoreDisplay.textContent = avgScore.toFixed(1);
      gpaValDisplay.textContent = avgGpa4.toFixed(2);
      gpa5Display.textContent = avgGpa5.toFixed(2);
      totalCreditsDisplay.textContent = totalCredits.toFixed(1);

      if (gpaProgressRing) {
        const percent = avgGpa4 / 4.0;
        const offset = 314.159 - (percent * 314.159);
        gpaProgressRing.style.strokeDashoffset = offset;
      }

      let evalText = "";
      if (avgGpa4 >= 3.8) {
        evalText = "当前绩点非常优秀，适合继续整理课程成果、项目经历和后续申请材料。";
      } else if (avgGpa4 >= 3.5) {
        evalText = "当前绩点表现稳定，建议保持优势课程，同时针对薄弱科目做阶段复盘。";
      } else if (avgGpa4 >= 3.0) {
        evalText = "当前绩点处于良好区间，可以优先提升高学分课程的复习效率。";
      } else if (avgGpa4 >= 2.0) {
        evalText = "当前绩点还有提升空间，建议先定位低分高学分课程，再制定复习计划。";
      } else {
        evalText = "当前绩点偏低，建议尽快核对课程要求，并为重点科目安排更明确的补强计划。";
      }
      gpaEvaluationText.textContent = evalText;
    } else {
      weightedScoreDisplay.textContent = "0.0";
      gpaValDisplay.textContent = "0.00";
      gpa5Display.textContent = "0.00";
      totalCreditsDisplay.textContent = "0.0";
      if (gpaProgressRing) {
        gpaProgressRing.style.strokeDashoffset = 314.159;
      }
      gpaEvaluationText.textContent = "录入你的学分与百分制成绩，看看你的成绩处于什么水平吧！";
    }
  }

  const presets = {
    freshman: [
      { name: "高等数学 I", credits: 5.0, score: 92 },
      { name: "大学英语 I", credits: 3.0, score: 88 },
      { name: "计算机导论", credits: 3.0, score: 95 },
      { name: "思想道德与法治", credits: 2.0, score: 85 },
      { name: "大学体育 I", credits: 1.0, score: 90 }
    ],
    sophomore: [
      { name: "数据结构与算法", credits: 4.0, score: 94 },
      { name: "操作系统", credits: 4.0, score: 89 },
      { name: "计算机网络", credits: 3.0, score: 91 },
      { name: "软件工程导论", credits: 3.0, score: 87 },
      { name: "数据库系统设计", credits: 3.0, score: 90 }
    ]
  };

  document.querySelectorAll("[data-preset]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const type = btn.dataset.preset;
      container.innerHTML = "";
      if (presets[type]) {
        presets[type].forEach((c) => createCourseRow(c.name, c.credits, c.score));
      }
      calculateGpa();
    });
  });

  addBtn?.addEventListener("click", () => {
    createCourseRow("", 3.0, 85);
    calculateGpa();
  });

  resetBtn?.addEventListener("click", () => {
    container.innerHTML = "";
    createCourseRow("高等数学", 5.0, 90);
    createCourseRow("大学英语", 3.0, 85);
    calculateGpa();
  });

  // --- Resume STAR Generator Logic ---
  const starS = document.getElementById("star-s");
  const starT = document.getElementById("star-t");
  const starA = document.getElementById("star-a");
  const starR = document.getElementById("star-r");
  const starStyle = document.getElementById("star-style");
  const starOutputCode = document.getElementById("star-output-code");
  const copyStarBtn = document.getElementById("copy-star-btn");

  const starPresets = {
    frontend: {
      s: "随着业务功能叠加，某高频交易列表页的首次内容渲染时间（FCP）恶化至 4.2 秒，导致用户流失率显著上升，移动端首屏出现明显白屏卡顿。",
      t: "我负责主导该核心列表页的性能调优工作，目标是在两周内将 FCP 缩短至 1.8 秒以内，并在弱网环境下实现平滑加载，挽回潜在交易用户。",
      a: "采用 Chrome DevTools Performance 深度分析，定位到多处大图阻塞、非核心 JS 未按需加载等问题；实施了路由级首屏代码分割（Code Splitting），引入 CSS 骨架屏（Skeleton Screen），并将全站静态资源通过 WebP 压缩接入 Edge CDN，同时对列表图片实施了 Lazy Loading。",
      r: "首屏 FCP 从 4.2 秒暴降至 1.45 秒（提效 65.5%），在 3G 弱网环境下白屏时长减少了 70%，上线后列表页交易转化率提升了 14.8%，流失率大幅回落。"
    },
    qa: {
      s: "原有项目回归测试阶段过度依赖手工测试，500+ 个功能点全量回归耗时超过 2.5 天，且由于人工漏测频发，导致线上生产环境偶发性报错，沟通与排查成本极高。",
      t: "我承担起搭建全新自动化测试框架的职责，要求在 1 个月内实现核心链路 100% 覆盖，并将自动化回归执行时长压缩至 30 分钟内。",
      a: "基于 pytest 框架搭建了 Page Object Model (POM) 自动化测试架构，利用 Python Selenium/Playwright 编写了 150+ 个并发执行的测试用例；引入并发机制及智能显式等待（Explicit Waits），并在 CI/CD Pipeline 中集成 Webhook 通知，实现代码提交即刻自动触发冒烟与全量测试。",
      r: "回归测试总耗时从 2.5 天暴缩至 22 分钟（提效 98% 以上），测试覆盖率由零跃升至 88%，上线两个月来拦截了 14 次严重阻塞性缺陷，线上发布事故率直降为 0。"
    },
    event: {
      s: "学院一年一度的极客文化科技节参与人数逐年下滑，上届活动实际签到人数不足 120 人，学生社团预算面临被缩减的窘境，亟需探索新型宣传路径以挽回人气。",
      t: "作为本届科技节总负责人，我制定了“签到人数翻倍”的目标，要求在 5000 元有限经费内吸引至少 300 名学生到场深度体验，并实现跨院系传播。",
      a: "重构策划方案，增设了“AI 效率小工具盲盒”与“现场提示词对抗赛”等高交互环节；通过微信公众号、小红书社群矩阵进行裂变海报推广，设计了“邀请 3 人组队即赠送大厂面试指南”的机制，并在全校 8 个主要宿区进行定向海报投放与社群接龙。",
      r: "现场实际参与人数达到 430+ 人，相比上届极增 258%，创下学院近五年活动人数最高纪录；最终以 4200 元超预期省下 16% 预算，社团因此荣获年度“十佳精品活动”称号。"
    }
  };

  function updateStarPreview() {
    if (!starS || !starT || !starA || !starR || !starOutputCode) return;
    const sVal = starS.value.trim();
    const tVal = starT.value.trim();
    const aVal = starA.value.trim();
    const rVal = starR.value.trim();

    if (!sVal && !tVal && !aVal && !rVal) {
      starOutputCode.textContent = "在左侧输入框输入内容，或选择上方预设，将实时生成排版完美的 STAR 简历文本！";
      return;
    }

    const s = sVal || "（未填写情境描述）";
    const t = tVal || "（未填写任务职责）";
    const a = aVal || "（未填写行动步骤）";
    const r = rVal || "（未填写最终结果）";

    const style = starStyle ? starStyle.value : "hardcore";
    let formatted = "";

    if (style === "hardcore") {
      formatted = `* **[项目背景 (Situation)]** ${s}
* **[核心职责 (Task)]** ${t}
* **[技术攻坚 (Action)]** ${a}
* **[业务成效 (Result)]** ${r}`;
    } else if (style === "general") {
      formatted = `* **项目背景**：${s}
* **工作职责**：${t}
* **具体行动**：${a}
* **最终成效**：${r}`;
    } else {
      formatted = `* 【项目背景】${s} 针对此目标，本人【明确任务】${t}。
* 【实施行动】在行动上，${a}。
* 【量化结果】最终实现${r}。`;
    }

    starOutputCode.textContent = formatted;

    starOutputCode.classList.add("updating");
    if (starOutputCode._updateTimeout) clearTimeout(starOutputCode._updateTimeout);
    starOutputCode._updateTimeout = setTimeout(() => {
      starOutputCode.classList.remove("updating");
    }, 200);
  }

  document.querySelectorAll("[data-star-preset]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const type = btn.dataset.starPreset;
      if (starPresets[type]) {
        starS.value = starPresets[type].s;
        starT.value = starPresets[type].t;
        starA.value = starPresets[type].a;
        starR.value = starPresets[type].r;
        updateStarPreview();
      }
    });
  });

  [starS, starT, starA, starR].forEach((textarea) => {
    textarea?.addEventListener("input", updateStarPreview);
  });
  starStyle?.addEventListener("change", updateStarPreview);

  copyStarBtn?.addEventListener("click", async () => {
    const code = starOutputCode ? starOutputCode.textContent : "";
    if (!code || code.startsWith("在左侧输入框") || code.startsWith("在等待输入")) return;
    try {
      await navigator.clipboard.writeText(code);
      const originalText = copyStarBtn.textContent || "一键复制排版";
      copyStarBtn.textContent = "已复制到剪贴板！";
      copyStarBtn.classList.add("copied");
      setTimeout(() => {
        copyStarBtn.textContent = originalText;
        copyStarBtn.classList.remove("copied");
      }, 2000);
    } catch (err) {
      console.error("Failed to copy STAR text:", err);
    }
  });

  if (container) {
    createCourseRow("高等数学", 5.0, 90);
    createCourseRow("大学英语", 3.0, 85);
    calculateGpa();
  }
  updateStarPreview();
}


document.addEventListener("DOMContentLoaded", () => {
  buildNav();
  buildFooter();
  buildAdSlots();
  buildFeaturedResources();
  buildArticleSearch();
  initCopyButtons();
  initInteractiveTools();
});
