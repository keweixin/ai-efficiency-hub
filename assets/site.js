(() => {
  const site = {
    name: "跨境运费避坑工具箱",
    description: "面向外贸员、跨境电商卖家、独立站卖家和 FBA 新手的体积重、CBM、计费重与渠道复核静态工具站。",
    nav: [{"href": "index.html", "label": "首页", "key": "home"}, {"href": "articles.html", "label": "文章", "key": "articles"}, {"href": "volume.html", "label": "体积重", "key": "volume"}, {"href": "channels.html", "label": "渠道", "key": "channels"}, {"href": "packing.html", "label": "包装", "key": "packing"}, {"href": "tools.html", "label": "工具", "key": "tools"}, {"href": "smoke-test.html", "label": "内测", "key": "smoke"}]
  };

  function resolvePrefix() {
    return location.pathname.includes('/articles/') ? '../' : '';
  }

  function initNav() {
    const prefix = resolvePrefix();
    const active = document.body.dataset.active || '';
    document.querySelectorAll('[data-site-nav]').forEach((nav) => {
      nav.innerHTML = site.nav.map((item) => {
        const cls = active === item.key ? ' class="is-active"' : '';
        return `<a${cls} href="${prefix}${item.href}">${item.label}</a>`;
      }).join('');
    });
  }

  function initTheme() {
    const root = document.documentElement;
    const saved = localStorage.getItem('shipping-theme');
    if (saved === 'dark') root.classList.add('dark-theme');
    if (saved === 'light') root.classList.add('light-theme');
    document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
      button.addEventListener('click', () => {
        const isDark = root.classList.toggle('dark-theme');
        root.classList.remove('light-theme');
        localStorage.setItem('shipping-theme', isDark ? 'dark' : 'light');
      });
    });
  }

  function initAdSlots() {
    document.querySelectorAll('[data-ad-slot]').forEach((slot) => {
      slot.innerHTML = '<strong>赞助内容区域</strong><span>预留给合规广告或渠道服务说明。当前不加载第三方广告脚本。</span>';
    });
  }

  function initArticleFilter() {
    const root = document.querySelector('[data-article-filter]');
    const list = document.querySelector('[data-article-list]');
    if (!root || !list) return;
    const input = root.querySelector('[data-search-input]');
    const chips = Array.from(root.querySelectorAll('[data-filter]'));
    const cards = Array.from(list.querySelectorAll('[data-card-group]'));
    const empty = document.querySelector('[data-empty-state]');
    let activeGroup = new URLSearchParams(location.search).get('group') || 'all';

    function apply() {
      const q = (input.value || '').trim().toLowerCase();
      let visible = 0;
      chips.forEach((chip) => chip.classList.toggle('is-active', chip.dataset.filter === activeGroup));
      cards.forEach((card) => {
        const groupOk = activeGroup === 'all' || card.dataset.cardGroup === activeGroup;
        const textOk = !q || card.textContent.toLowerCase().includes(q);
        const show = groupOk && textOk;
        card.hidden = !show;
        if (show) visible += 1;
      });
      if (empty) empty.hidden = visible !== 0;
    }

    chips.forEach((chip) => chip.addEventListener('click', () => {
      activeGroup = chip.dataset.filter || 'all';
      apply();
    }));
    input.addEventListener('input', apply);
    apply();
  }

  function initCopyButtons() {
    document.querySelectorAll('pre').forEach((pre) => {
      if (pre.parentElement && pre.parentElement.classList.contains('code-block-wrapper')) return;
      const wrapper = document.createElement('div');
      wrapper.className = 'code-block-wrapper';
      pre.parentNode.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'copy-button';
      button.textContent = '复制';
      wrapper.appendChild(button);
      button.addEventListener('click', async () => {
        const text = pre.textContent || '';
        try {
          await navigator.clipboard.writeText(text);
          button.textContent = '已复制';
          button.classList.add('copied');
          setTimeout(() => {
            button.textContent = '复制';
            button.classList.remove('copied');
          }, 1600);
        } catch (error) {
          button.textContent = '复制失败';
          setTimeout(() => button.textContent = '复制', 1600);
        }
      });
    });
  }

  function round(value, digits = 2) {
    if (!Number.isFinite(value)) return 0;
    const factor = Math.pow(10, digits);
    return Math.round(value * factor) / factor;
  }

  function initCalculator() {
    const root = document.querySelector('[data-logistics-calculator]');
    if (!root) return;
    const rowsBody = root.querySelector('[data-sku-rows]');
    const customDivisor = root.querySelector('[data-custom-divisor]');
    const totalActual = root.querySelector('[data-total-actual]');
    const totalCbm = root.querySelector('[data-total-cbm]');
    const longSide = root.querySelector('[data-long-side]');
    const channelResults = root.querySelector('[data-channel-results]');
    const suggestion = root.querySelector('[data-suggestion]');
    let rowId = 0;

    const channels = [
      ['DHL 官方常见口径', 5000],
      ['EMS 复核口径', 6000],
      ['标准空运模拟', 6000],
      ['自定义分母', 'custom']
    ];

    function rowTemplate(data = {}) {
      rowId += 1;
      const id = rowId;
      const defaults = Object.assign({ name: '', qty: 1, l: '', w: '', h: '', kg: '' }, data);
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><label class="sr-only" for="sku-name-${id}">SKU 或箱型</label><input id="sku-name-${id}" type="text" value="${defaults.name}" placeholder="如 自拍杆 A 箱" data-field="name"></td>
        <td><label class="sr-only" for="sku-qty-${id}">箱数</label><input id="sku-qty-${id}" type="number" min="1" step="1" value="${defaults.qty}" data-field="qty"></td>
        <td><label class="sr-only" for="sku-l-${id}">长厘米</label><input id="sku-l-${id}" type="number" min="0" step="0.1" value="${defaults.l}" data-field="l"></td>
        <td><label class="sr-only" for="sku-w-${id}">宽厘米</label><input id="sku-w-${id}" type="number" min="0" step="0.1" value="${defaults.w}" data-field="w"></td>
        <td><label class="sr-only" for="sku-h-${id}">高厘米</label><input id="sku-h-${id}" type="number" min="0" step="0.1" value="${defaults.h}" data-field="h"></td>
        <td><label class="sr-only" for="sku-kg-${id}">单箱实重千克</label><input id="sku-kg-${id}" type="number" min="0" step="0.01" value="${defaults.kg}" data-field="kg"></td>
        <td><button class="icon-button" type="button" aria-label="删除这一行" data-remove-row>删</button></td>
      `;
      rowsBody.appendChild(tr);
      tr.querySelectorAll('input').forEach((input) => input.addEventListener('input', calculate));
      tr.querySelector('[data-remove-row]').addEventListener('click', () => {
        tr.remove();
        if (!rowsBody.children.length) addRow();
        calculate();
      });
      calculate();
    }

    function getRows() {
      return Array.from(rowsBody.querySelectorAll('tr')).map((tr) => {
        const value = (field) => {
          const node = tr.querySelector(`[data-field="${field}"]`);
          return node ? node.value : '';
        };
        return {
          name: value('name'),
          qty: Math.max(0, Number(value('qty')) || 0),
          l: Math.max(0, Number(value('l')) || 0),
          w: Math.max(0, Number(value('w')) || 0),
          h: Math.max(0, Number(value('h')) || 0),
          kg: Math.max(0, Number(value('kg')) || 0)
        };
      }).filter((row) => row.qty && row.l && row.w && row.h);
    }

    function channelCalc(rows, divisor) {
      let volume = 0;
      let chargeable = 0;
      rows.forEach((row) => {
        const volumePer = row.l * row.w * row.h / divisor;
        const actualPer = row.kg || 0;
        volume += volumePer * row.qty;
        chargeable += Math.max(volumePer, actualPer) * row.qty;
      });
      return { volume: round(volume), chargeable: round(chargeable) };
    }

    function calculate() {
      const rows = getRows();
      const actual = rows.reduce((sum, row) => sum + row.kg * row.qty, 0);
      const cbm = rows.reduce((sum, row) => sum + (row.l * row.w * row.h / 1000000) * row.qty, 0);
      const longest = rows.reduce((max, row) => Math.max(max, row.l, row.w, row.h), 0);
      totalActual.textContent = `${round(actual)} kg`;
      totalCbm.textContent = `${round(cbm, 4)} CBM`;
      longSide.textContent = longest ? `${round(longest, 1)} cm${longest >= 40 ? '，需复核' : ''}` : '待录入';

      const custom = Math.max(1000, Number(customDivisor.value) || 6000);
      channelResults.innerHTML = channels.map(([name, divisor]) => {
        const realDivisor = divisor === 'custom' ? custom : divisor;
        const result = channelCalc(rows, realDivisor);
        return `<tr><td>${name}</td><td>${realDivisor}</td><td>${result.volume} kg</td><td><strong>${result.chargeable} kg</strong></td></tr>`;
      }).join('');

      if (!rows.length) {
        suggestion.textContent = '录入箱规后显示复核提示。';
        return;
      }
      const dhl = channelCalc(rows, 5000).chargeable;
      const ems = channelCalc(rows, 6000).chargeable;
      const diff = round(Math.abs(dhl - ems));
      const warnings = [];
      if (longest >= 40) warnings.push('存在最长边达到 40cm 口径的箱子，EMS 等渠道需要单独复核。');
      if (diff > 0) warnings.push(`DHL 5000 与 6000 分母模拟差异约 ${diff} kg，建议不要只比较每千克单价。`);
      const density = cbm ? actual / cbm : 0;
      if (density && density < 120) warnings.push(`当前密度约 ${round(density)} kg/CBM，偏轻泡，建议重点复核体积重。`);
      if (!warnings.length) warnings.push('当前样本未出现明显长边或轻泡提醒，但仍需确认渠道分母、进位和附加项。');
      suggestion.textContent = warnings.join(' ');
    }

    function addRow(data) {
      rowTemplate(data);
    }

    root.querySelector('[data-add-row]').addEventListener('click', () => addRow());
    root.querySelector('[data-load-sample]').addEventListener('click', () => {
      rowsBody.innerHTML = '';
      rowId = 0;
      addRow({ name: '自拍杆长条箱', qty: 4, l: 75, w: 35, h: 28, kg: 8 });
      addRow({ name: '配件重货箱', qty: 3, l: 42, w: 30, h: 24, kg: 14 });
      calculate();
    });
    root.querySelector('[data-reset-rows]').addEventListener('click', () => {
      rowsBody.innerHTML = '';
      rowId = 0;
      addRow();
      calculate();
    });
    customDivisor.addEventListener('input', calculate);
    addRow({ name: '示例轻泡箱', qty: 2, l: 60, w: 45, h: 40, kg: 8 });
    addRow({ name: '示例重货箱', qty: 1, l: 38, w: 28, h: 22, kg: 12 });
    calculate();
  }

  initNav();
  initTheme();
  initAdSlots();
  initArticleFilter();
  initCopyButtons();
  initCalculator();
})();
