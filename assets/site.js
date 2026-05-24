(() => {
  const site = {
    name: "跨境运费避坑工具箱",
    description: "面向外贸员、跨境电商卖家、独立站卖家和 FBA 新手的体积重、CBM、计费重与渠道复核静态工具站。",
    nav: [{"href": "index.html", "label": "首页", "labelEn": "Home", "key": "home"}, {"href": "articles.html", "label": "文章", "labelEn": "Articles", "key": "articles"}, {"href": "volume.html", "label": "体积重", "labelEn": "Volumetric", "key": "volume"}, {"href": "channels.html", "label": "渠道", "labelEn": "Channels", "key": "channels"}, {"href": "packing.html", "label": "包装", "labelEn": "Packing", "key": "packing"}, {"href": "tools.html", "label": "工具", "labelEn": "Tools", "key": "tools"}, {"href": "smoke-test.html", "label": "内测", "labelEn": "Beta", "key": "smoke"}]
  };

  const JSPDF_SRC = 'https://cdn.jsdelivr.net/npm/jspdf@4.2.1/dist/jspdf.umd.min.js';

  const i18n = {
    zh: {
      siteName: '跨境运费避坑工具箱',
      skip: '跳到正文',
      brandAria: '跨境运费避坑工具箱首页',
      mainNav: '主导航',
      themeToggle: '切换深浅色',
      footerDesc: '用于发货前复核体积重、CBM、计费重和渠道口径。规则会变化，具体发货请以官方报价和承运商确认为准。',
      footerArticles: '文章索引',
      footerTools: '计算工具',
      footerSmoke: '内测说明',
      footerPrivacy: '隐私政策',
      footerContact: '联系',
      copyright: '© 2026 跨境运费避坑工具箱. 本站不提供承运商报价承诺。',
      toolsEyebrow: 'Calculator',
      toolsH1: '多 SKU 体积重 / CBM / 计费重计算器',
      toolsLead: '录入每类货物的箱数、外箱尺寸和实重，本地计算 DHL 5000、EMS 6000、标准空运 6000 和自定义分母下的计费重，并提示长边复核项。',
      startCalc: '开始计算',
      formulaLink: '先看公式说明',
      visualCaption: '站内生成插图：用于表示体积重、CBM 和计费重核算。',
      localTool: 'Local Tool',
      calcTitle: '发货前复核表',
      calcLead: '数据只在浏览器内计算，并自动保存在当前浏览器本地，不会上传。默认 EMS 长边提醒按超过 40cm 标记，实际规则请以官方报价和收寄确认为准。',
      addSku: '添加 SKU',
      loadSample: '载入示例',
      resetRows: '清空',
      exportPdf: '导出 PDF 报告',
      saveReady: '已自动保存到当前浏览器。',
      saveRestored: '已恢复上次在本浏览器保存的录入内容。',
      saveCleared: '已清空本地保存的录入内容。',
      saveUnavailable: '当前浏览器未允许本地保存，本次录入仅保留在页面内。',
      thSku: 'SKU / 箱型',
      thQty: '箱数',
      thLength: '长 cm',
      thWidth: '宽 cm',
      thHeight: '高 cm',
      thWeight: '单箱实重 kg',
      thAction: '操作',
      customDivisor: '自定义分母',
      metricActual: '总实重',
      metricCbm: '总 CBM',
      metricLongSide: '最长边提醒',
      channel: '渠道',
      divisor: '分母',
      volumeWeight: '体积重',
      chargeableWeight: '计费重',
      howToRead: 'How to Read',
      readTitle: '工具输出怎么看',
      readCard1Title: '计费重不是最终报价',
      readCard1Text: '它只是报价复核入口。还要确认进位、附加项、目的地限制和服务类型。',
      readCard2Title: '长边提醒不是拦截规则',
      readCard2Text: '默认按 EMS 超过 40cm 口径提醒，目的是提示你回到官方页面或客服确认。',
      readCard3Title: '拆分建议只做复核',
      readCard3Text: '工具只提示可能需要复核，不承诺某个方案一定更优。',
      langButton: 'EN',
      skuPlaceholder: '如 自拍杆 A 箱',
      deleteShort: '删',
      deleteRow: '删除这一行',
      pending: '待录入',
      needReview: '，需复核',
      emptySuggestion: '录入箱规后显示复核提示。',
      longSideWarning: '存在最长边超过 40cm 口径的箱子，EMS 等渠道需要单独复核。',
      divisorWarning: 'DHL 5000 与标准空运 6000 的整票计费重差异约 {diff} kg，建议不要只比较每千克单价。',
      emsPieceWarning: 'EMS 逐箱长边复核与标准空运整票 6000 模拟差异约 {diff} kg，建议把长边箱单独发给承运商确认。',
      emsNoDimWarning: 'EMS 未触发长边计泡时可能按实重模拟，与标准空运整票 6000 差异约 {diff} kg，建议确认对应产品和目的地口径。',
      densityWarning: '当前密度约 {density} kg/CBM，偏轻泡，建议重点复核体积重。',
      normalWarning: '当前样本未出现明显长边或轻泡提醒，但仍需确认渠道分母、进位和附加项。',
      dhlChannel: 'DHL 官方常见口径',
      emsChannel: 'EMS 复核口径',
      airChannel: '标准空运模拟',
      customChannel: '自定义分母',
      exportReady: 'PDF 报告已生成。',
      exportLoading: '正在生成 PDF 报告...',
      exportEmpty: '请先录入至少一行完整箱规。',
      exportFailed: 'PDF 生成失败，请稍后重试。',
      reportTitle: '货柜装载与计费重复核报告',
      reportSubtitle: '本报告由浏览器本地生成，不上传数据；结果仅用于发货前复核。',
      reportGenerated: '生成时间',
      reportSummary: '汇总指标',
      reportSku: 'SKU / 箱型明细',
      reportChannels: '渠道计费重对比',
      reportNotes: '复核提醒',
      reportDisclaimer: '说明：本报告不替代承运商报价、收寄确认、进位规则和附加项确认。'
    },
    en: {
      siteName: 'Cross-border Freight Review Toolbox',
      skip: 'Skip to content',
      brandAria: 'Cross-border Freight Review Toolbox home',
      mainNav: 'Main navigation',
      themeToggle: 'Toggle color theme',
      footerDesc: 'Review volumetric weight, CBM, chargeable weight and channel assumptions before shipment. Rules change, so final shipment decisions should follow carrier quotes and confirmation.',
      footerArticles: 'Articles',
      footerTools: 'Calculator',
      footerSmoke: 'Beta notes',
      footerPrivacy: 'Privacy',
      footerContact: 'Contact',
      copyright: '© 2026 Cross-border Freight Review Toolbox. This site does not promise carrier quotes.',
      toolsEyebrow: 'Calculator',
      toolsH1: 'Multi-SKU Volumetric Weight / CBM / Chargeable Weight Calculator',
      toolsLead: 'Enter carton counts, outer dimensions and actual weight. The browser compares DHL 5000, EMS 6000, standard air 6000 and a custom divisor, then flags long-side review points.',
      startCalc: 'Start calculating',
      formulaLink: 'Read the formula guide',
      visualCaption: 'Site-generated illustration for volumetric weight, CBM and chargeable weight review.',
      localTool: 'Local Tool',
      calcTitle: 'Pre-shipment Review Sheet',
      calcLead: 'All calculations run locally in your browser and autosave on this device only. Nothing is uploaded. The EMS long-side reminder uses above 40cm as a review point; final rules should follow official quotes and acceptance confirmation.',
      addSku: 'Add SKU',
      loadSample: 'Load sample',
      resetRows: 'Clear',
      exportPdf: 'Export PDF report',
      saveReady: 'Autosaved in this browser.',
      saveRestored: 'Restored the last saved entries from this browser.',
      saveCleared: 'Cleared locally saved calculator entries.',
      saveUnavailable: 'Local saving is not available in this browser; entries only stay on the page.',
      thSku: 'SKU / carton',
      thQty: 'Cartons',
      thLength: 'L cm',
      thWidth: 'W cm',
      thHeight: 'H cm',
      thWeight: 'Actual kg / carton',
      thAction: 'Action',
      customDivisor: 'Custom divisor',
      metricActual: 'Total actual weight',
      metricCbm: 'Total CBM',
      metricLongSide: 'Longest side',
      channel: 'Channel',
      divisor: 'Divisor',
      volumeWeight: 'Volumetric weight',
      chargeableWeight: 'Chargeable weight',
      howToRead: 'How to Read',
      readTitle: 'How to interpret the output',
      readCard1Title: 'Chargeable weight is not the final quote',
      readCard1Text: 'It is the starting point for review. Rounding, surcharges, destination limits and service type still need confirmation.',
      readCard2Title: 'Long-side reminders are review prompts',
      readCard2Text: 'The default EMS above-40cm reminder is meant to prompt official-page or support confirmation.',
      readCard3Title: 'Split suggestions only indicate review points',
      readCard3Text: 'The tool flags items worth checking; it does not guarantee one route is always better.',
      langButton: '中文',
      skuPlaceholder: 'e.g. selfie stick carton A',
      deleteShort: 'Del',
      deleteRow: 'Delete this row',
      pending: 'Pending',
      needReview: ', review needed',
      emptySuggestion: 'Enter carton data to see review notes.',
      longSideWarning: 'At least one carton is above the 40cm long-side review point; EMS and similar routes need separate confirmation.',
      divisorWarning: 'The shipment-level DHL 5000 vs standard air 6000 chargeable-weight difference is about {diff} kg. Do not compare only the per-kg rate.',
      emsPieceWarning: 'The EMS piece-level long-side review vs standard air shipment-level 6000 simulation differs by about {diff} kg. Send long-side cartons to the carrier for confirmation.',
      emsNoDimWarning: 'When EMS long-side volumetric review is not triggered, EMS may simulate on actual weight. The difference from standard air shipment-level 6000 is about {diff} kg; confirm product and destination rules.',
      densityWarning: 'Current density is about {density} kg/CBM, which looks light and bulky. Prioritize volumetric-weight review.',
      normalWarning: 'No obvious long-side or light-bulky signal appears in this sample, but divisor, rounding and surcharges still need confirmation.',
      dhlChannel: 'DHL common official basis',
      emsChannel: 'EMS review basis',
      airChannel: 'Standard air simulation',
      customChannel: 'Custom divisor',
      exportReady: 'PDF report generated.',
      exportLoading: 'Generating PDF report...',
      exportEmpty: 'Enter at least one complete carton row first.',
      exportFailed: 'PDF generation failed. Please try again later.',
      reportTitle: 'Container Loading and Chargeable Weight Review Report',
      reportSubtitle: 'Generated locally in the browser. No data is uploaded; use the result for pre-shipment review only.',
      reportGenerated: 'Generated at',
      reportSummary: 'Summary',
      reportSku: 'SKU / carton details',
      reportChannels: 'Channel comparison',
      reportNotes: 'Review notes',
      reportDisclaimer: 'Note: this report does not replace carrier quotes, acceptance confirmation, rounding rules or surcharge checks.'
    }
  };

  function resolvePrefix() {
    return location.pathname.includes('/articles/') ? '../' : '';
  }

  function storageGet(key) {
    try {
      return window.localStorage.getItem(key);
    } catch (error) {
      return null;
    }
  }

  function storageSet(key, value) {
    try {
      window.localStorage.setItem(key, value);
      return true;
    } catch (error) {
      return false;
    }
  }

  function storageRemove(key) {
    try {
      window.localStorage.removeItem(key);
      return true;
    } catch (error) {
      return false;
    }
  }

  function currentLang() {
    return storageGet('shipping-lang') === 'en' ? 'en' : 'zh';
  }

  function t(key) {
    const lang = currentLang();
    return (i18n[lang] && i18n[lang][key]) || i18n.zh[key] || key;
  }

  function initNav() {
    const prefix = resolvePrefix();
    const active = document.body.dataset.active || '';
    const lang = currentLang();
    document.querySelectorAll('[data-site-nav]').forEach((nav) => {
      nav.innerHTML = site.nav.map((item) => {
        const cls = active === item.key ? ' class="is-active"' : '';
        const label = lang === 'en' ? item.labelEn : item.label;
        return `<a${cls} href="${prefix}${item.href}">${label}</a>`;
      }).join('');
    });
  }

  function applyLanguage() {
    const lang = currentLang();
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    document.querySelectorAll('[data-i18n]').forEach((node) => {
      node.textContent = t(node.dataset.i18n);
    });
    document.querySelectorAll('[data-i18n-aria]').forEach((node) => {
      node.setAttribute('aria-label', t(node.dataset.i18nAria));
    });
    document.querySelectorAll('[data-i18n-placeholder]').forEach((node) => {
      node.setAttribute('placeholder', t(node.dataset.i18nPlaceholder));
    });
    document.querySelectorAll('[data-lang-toggle]').forEach((button) => {
      button.setAttribute('aria-pressed', String(lang === 'en'));
    });
    document.querySelectorAll('[data-lang-current]').forEach((node) => {
      node.textContent = t('langButton');
    });
    initNav();
    document.dispatchEvent(new CustomEvent('shipping:languagechange', { detail: { lang } }));
  }

  function initLanguage() {
    document.querySelectorAll('[data-lang-toggle]').forEach((button) => {
      button.addEventListener('click', () => {
        storageSet('shipping-lang', currentLang() === 'en' ? 'zh' : 'en');
        applyLanguage();
      });
    });
    applyLanguage();
  }

  function initTheme() {
    const root = document.documentElement;
    const saved = storageGet('shipping-theme');
    if (saved === 'dark') root.classList.add('dark-theme');
    if (saved === 'light') root.classList.add('light-theme');
    document.querySelectorAll('[data-theme-toggle]').forEach((button) => {
      button.addEventListener('click', () => {
        const isDark = root.classList.toggle('dark-theme');
        root.classList.remove('light-theme');
        storageSet('shipping-theme', isDark ? 'dark' : 'light');
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
    const params = new URLSearchParams(location.search);
    let activeGroup = params.get('group') || 'all';
    if (!chips.some((chip) => chip.dataset.filter === activeGroup)) activeGroup = 'all';
    const initialQuery = params.get('q') || '';
    if (initialQuery) input.value = initialQuery;

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
    const exportButton = root.querySelector('[data-export-report]');
    const exportStatus = root.querySelector('[data-export-status]');
    const saveStatus = root.querySelector('[data-save-status]');
    const storageKey = 'shipping-calculator-state-v1';
    let rowId = 0;
    let lastReport = null;
    let restoreReady = false;
    let saveTimer = 0;

    const channels = [
      { key: 'dhlChannel', divisor: 5000, mode: 'shipment' },
      { key: 'emsChannel', divisor: 6000, mode: 'ems-piece' },
      { key: 'airChannel', divisor: 6000, mode: 'shipment' },
      { key: 'customChannel', divisor: 'custom', mode: 'shipment' }
    ];

    function setSaveStatus(key, delay = 2200) {
      if (!saveStatus) return;
      saveStatus.textContent = key ? t(key) : '';
      if (key && delay) {
        window.clearTimeout(saveStatus.dataset.timer || 0);
        const timer = window.setTimeout(() => {
          if (saveStatus.textContent === t(key)) saveStatus.textContent = '';
        }, delay);
        saveStatus.dataset.timer = String(timer);
      }
    }

    function getRawRows() {
      return Array.from(rowsBody.querySelectorAll('tr')).map((tr) => {
        const value = (field) => {
          const node = tr.querySelector(`[data-field="${field}"]`);
          return node ? String(node.value || '').trim() : '';
        };
        return {
          name: value('name').slice(0, 120),
          qty: value('qty'),
          l: value('l'),
          w: value('w'),
          h: value('h'),
          kg: value('kg')
        };
      }).filter((row) => Object.values(row).some(Boolean));
    }

    function sanitizeStoredRows(rows) {
      if (!Array.isArray(rows)) return [];
      return rows.slice(0, 300).map((row) => {
        const safe = row && typeof row === 'object' ? row : {};
        return {
          name: String(safe.name || '').slice(0, 120),
          qty: String(safe.qty || ''),
          l: String(safe.l || ''),
          w: String(safe.w || ''),
          h: String(safe.h || ''),
          kg: String(safe.kg || '')
        };
      }).filter((row) => Object.values(row).some(Boolean));
    }

    function readSavedState() {
      const raw = storageGet(storageKey);
      if (!raw) return null;
      try {
        const parsed = JSON.parse(raw);
        if (!parsed || parsed.version !== 1) throw new Error('Unsupported calculator state');
        const rows = sanitizeStoredRows(parsed.rows);
        const custom = Math.max(1000, Number(parsed.customDivisor) || 6000);
        return { rows, customDivisor: String(custom) };
      } catch (error) {
        storageRemove(storageKey);
        return null;
      }
    }

    function saveStateNow(statusKey = 'saveReady') {
      if (!restoreReady) return;
      const payload = {
        version: 1,
        savedAt: new Date().toISOString(),
        customDivisor: String(customDivisor.value || '6000'),
        rows: getRawRows()
      };
      if (storageSet(storageKey, JSON.stringify(payload))) {
        setSaveStatus(statusKey);
      } else {
        setSaveStatus('saveUnavailable', 3600);
      }
    }

    function scheduleSave() {
      if (!restoreReady) return;
      window.clearTimeout(saveTimer);
      saveTimer = window.setTimeout(() => saveStateNow(), 350);
    }

    function clearSavedState() {
      window.clearTimeout(saveTimer);
      storageRemove(storageKey);
      setSaveStatus('saveCleared');
    }

    function rowTemplate(data = {}) {
      rowId += 1;
      const id = rowId;
      const defaults = Object.assign({ name: '', qty: 1, l: '', w: '', h: '', kg: '' }, data);
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><label class="sr-only" for="sku-name-${id}" data-row-label="thSku">${t('thSku')}</label><input id="sku-name-${id}" type="text" placeholder="${t('skuPlaceholder')}" data-field="name"></td>
        <td><label class="sr-only" for="sku-qty-${id}" data-row-label="thQty">${t('thQty')}</label><input id="sku-qty-${id}" type="number" min="1" step="1" data-field="qty"></td>
        <td><label class="sr-only" for="sku-l-${id}" data-row-label="thLength">${t('thLength')}</label><input id="sku-l-${id}" type="number" min="0" step="0.1" data-field="l"></td>
        <td><label class="sr-only" for="sku-w-${id}" data-row-label="thWidth">${t('thWidth')}</label><input id="sku-w-${id}" type="number" min="0" step="0.1" data-field="w"></td>
        <td><label class="sr-only" for="sku-h-${id}" data-row-label="thHeight">${t('thHeight')}</label><input id="sku-h-${id}" type="number" min="0" step="0.1" data-field="h"></td>
        <td><label class="sr-only" for="sku-kg-${id}" data-row-label="thWeight">${t('thWeight')}</label><input id="sku-kg-${id}" type="number" min="0" step="0.01" data-field="kg"></td>
        <td><button class="icon-button" type="button" aria-label="${t('deleteRow')}" data-remove-row>${t('deleteShort')}</button></td>
      `;
      rowsBody.appendChild(tr);
      ['name', 'qty', 'l', 'w', 'h', 'kg'].forEach((field) => {
        const input = tr.querySelector(`[data-field="${field}"]`);
        if (input) input.value = defaults[field] ?? '';
      });
      tr.querySelectorAll('input').forEach((input) => input.addEventListener('input', () => {
        calculate();
        scheduleSave();
      }));
      tr.querySelector('[data-remove-row]').addEventListener('click', () => {
        tr.remove();
        if (!rowsBody.children.length) addRow();
        calculate();
        scheduleSave();
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

    function shipmentCalc(rows, actual, divisor) {
      const volume = rows.reduce((sum, row) => {
        return sum + (row.l * row.w * row.h / divisor) * row.qty;
      }, 0);
      return { volume: round(volume), chargeable: round(Math.max(actual, volume)) };
    }

    function emsPieceCalc(rows) {
      let volume = 0;
      let chargeable = 0;
      rows.forEach((row) => {
        const volumePer = row.l * row.w * row.h / 6000;
        const actualPer = row.kg || 0;
        const hasLongSide = row.l > 40 || row.w > 40 || row.h > 40;
        volume += volumePer * row.qty;
        chargeable += (hasLongSide ? Math.max(volumePer, actualPer) : actualPer) * row.qty;
      });
      return { volume: round(volume), chargeable: round(chargeable) };
    }

    function calcChannel(rows, actual, channel, customDivisorValue) {
      const divisor = channel.divisor === 'custom' ? customDivisorValue : channel.divisor;
      const result = channel.mode === 'ems-piece'
        ? emsPieceCalc(rows)
        : shipmentCalc(rows, actual, divisor);
      return {
        key: channel.key,
        name: t(channel.key),
        divisor,
        volume: result.volume,
        chargeable: result.chargeable
      };
    }

    function translateRows() {
      rowsBody.querySelectorAll('[data-row-label]').forEach((label) => {
        label.textContent = t(label.dataset.rowLabel);
      });
      rowsBody.querySelectorAll('[data-field="name"]').forEach((input) => {
        input.setAttribute('placeholder', t('skuPlaceholder'));
      });
      rowsBody.querySelectorAll('[data-remove-row]').forEach((button) => {
        button.textContent = t('deleteShort');
        button.setAttribute('aria-label', t('deleteRow'));
      });
    }

    function calculate() {
      const rows = getRows();
      const actual = rows.reduce((sum, row) => sum + row.kg * row.qty, 0);
      const cbm = rows.reduce((sum, row) => sum + (row.l * row.w * row.h / 1000000) * row.qty, 0);
      const longest = rows.reduce((max, row) => Math.max(max, row.l, row.w, row.h), 0);
      totalActual.textContent = `${round(actual)} kg`;
      totalCbm.textContent = `${round(cbm, 4)} CBM`;
      longSide.textContent = longest ? `${round(longest, 1)} cm${longest > 40 ? t('needReview') : ''}` : t('pending');

      const custom = Math.max(1000, Number(customDivisor.value) || 6000);
      const channelData = channels.map((channel) => calcChannel(rows, actual, channel, custom));
      channelResults.innerHTML = channelData.map((item) => {
        return `<tr><td>${item.name}</td><td>${item.divisor}</td><td>${item.volume} kg</td><td><strong>${item.chargeable} kg</strong></td></tr>`;
      }).join('');

      if (!rows.length) {
        suggestion.textContent = t('emptySuggestion');
        lastReport = { rows, actual, cbm, longest, channelData, warnings: [] };
        return;
      }
      const dhl = channelData.find((item) => item.key === 'dhlChannel')?.chargeable || 0;
      const ems = channelData.find((item) => item.key === 'emsChannel')?.chargeable || 0;
      const air = channelData.find((item) => item.key === 'airChannel')?.chargeable || 0;
      const divisorDiff = round(Math.abs(dhl - air));
      const emsDiff = round(Math.abs(ems - air));
      const warnings = [];
      if (longest > 40) warnings.push(t('longSideWarning'));
      if (divisorDiff > 0) warnings.push(t('divisorWarning').replace('{diff}', divisorDiff));
      if (emsDiff > 0) warnings.push(t(longest > 40 ? 'emsPieceWarning' : 'emsNoDimWarning').replace('{diff}', emsDiff));
      const density = cbm ? actual / cbm : 0;
      if (density && density < 120) warnings.push(t('densityWarning').replace('{density}', round(density)));
      if (!warnings.length) warnings.push(t('normalWarning'));
      suggestion.textContent = warnings.join(' ');
      lastReport = { rows, actual: round(actual), cbm: round(cbm, 4), longest: round(longest, 1), channelData, warnings };
    }

    function loadJsPdf() {
      if (window.jspdf && window.jspdf.jsPDF) return Promise.resolve(window.jspdf.jsPDF);
      return new Promise((resolve, reject) => {
        const existing = document.querySelector('script[data-jspdf]');
        if (existing) {
          existing.addEventListener('load', () => resolve(window.jspdf.jsPDF), { once: true });
          existing.addEventListener('error', reject, { once: true });
          return;
        }
        const script = document.createElement('script');
        script.src = JSPDF_SRC;
        script.async = true;
        script.defer = true;
        script.dataset.jspdf = 'true';
        script.onload = () => resolve(window.jspdf.jsPDF);
        script.onerror = reject;
        document.head.appendChild(script);
      });
    }

    function wrapText(ctx, text, x, y, maxWidth, lineHeight) {
      const chars = Array.from(String(text || ''));
      let line = '';
      let cursorY = y;
      chars.forEach((char) => {
        const test = line + char;
        if (ctx.measureText(test).width > maxWidth && line) {
          ctx.fillText(line, x, cursorY);
          line = char.trimStart();
          cursorY += lineHeight;
        } else {
          line = test;
        }
      });
      if (line) ctx.fillText(line, x, cursorY);
      return cursorY + lineHeight;
    }

    function drawTable(ctx, title, headers, rows, x, y, widths) {
      const rowHeight = 42;
      ctx.fillStyle = '#20252b';
      ctx.font = '700 26px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      ctx.fillText(title, x, y);
      y += 22;
      ctx.fillStyle = '#eef3f7';
      ctx.fillRect(x, y, widths.reduce((sum, width) => sum + width, 0), rowHeight);
      ctx.strokeStyle = '#d8e0ea';
      ctx.lineWidth = 2;
      let cursorX = x;
      ctx.font = '700 18px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      ctx.fillStyle = '#20252b';
      headers.forEach((header, index) => {
        ctx.strokeRect(cursorX, y, widths[index], rowHeight);
        ctx.fillText(header, cursorX + 12, y + 27);
        cursorX += widths[index];
      });
      y += rowHeight;
      ctx.font = '18px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      rows.forEach((row, rowIndex) => {
        cursorX = x;
        ctx.fillStyle = rowIndex % 2 ? '#fbfcfd' : '#ffffff';
        ctx.fillRect(x, y, widths.reduce((sum, width) => sum + width, 0), rowHeight);
        ctx.fillStyle = '#20252b';
        row.forEach((cell, index) => {
          ctx.strokeRect(cursorX, y, widths[index], rowHeight);
          ctx.fillText(String(cell), cursorX + 12, y + 27);
          cursorX += widths[index];
        });
        y += rowHeight;
      });
      return y + 34;
    }

    function createReportCanvas(report) {
      const width = 1240;
      const rowCount = report.rows.length + report.channelData.length + report.warnings.length;
      const height = Math.max(980, 760 + rowCount * 54);
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#f6f8fb';
      ctx.fillRect(0, 0, width, height);
      ctx.fillStyle = '#19705a';
      ctx.fillRect(0, 0, width, 14);
      ctx.fillStyle = '#ffffff';
      ctx.fillRect(68, 72, width - 136, height - 144);
      ctx.strokeStyle = '#d8e0ea';
      ctx.lineWidth = 2;
      ctx.strokeRect(68, 72, width - 136, height - 144);

      let y = 132;
      ctx.fillStyle = '#20252b';
      ctx.font = '700 38px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      ctx.fillText(t('reportTitle'), 104, y);
      y += 42;
      ctx.fillStyle = '#5f6874';
      ctx.font = '20px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      y = wrapText(ctx, t('reportSubtitle'), 104, y, 920, 28);
      ctx.fillText(t('reportGenerated') + ': ' + new Date().toLocaleString(), 104, y + 10);
      y += 68;

      const summaryRows = [
        [t('metricActual'), round(report.actual) + ' kg'],
        [t('metricCbm'), report.cbm + ' CBM'],
        [t('metricLongSide'), report.longest ? report.longest + ' cm' : t('pending')]
      ];
      y = drawTable(ctx, t('reportSummary'), [t('channel'), t('chargeableWeight')], summaryRows, 104, y, [360, 300]);

      const skuRows = report.rows.map((row) => [
        row.name || '-',
        row.qty,
        row.l + ' x ' + row.w + ' x ' + row.h,
        row.kg + ' kg'
      ]);
      y = drawTable(ctx, t('reportSku'), [t('thSku'), t('thQty'), 'L x W x H cm', t('thWeight')], skuRows, 104, y, [360, 130, 270, 220]);

      const channelRows = report.channelData.map((item) => [
        item.name,
        item.divisor,
        item.volume + ' kg',
        item.chargeable + ' kg'
      ]);
      y = drawTable(ctx, t('reportChannels'), [t('channel'), t('divisor'), t('volumeWeight'), t('chargeableWeight')], channelRows, 104, y, [360, 150, 220, 240]);

      ctx.fillStyle = '#20252b';
      ctx.font = '700 26px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      ctx.fillText(t('reportNotes'), 104, y);
      y += 36;
      ctx.font = '20px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      ctx.fillStyle = '#3f4853';
      (report.warnings.length ? report.warnings : [t('normalWarning')]).forEach((note) => {
        y = wrapText(ctx, '• ' + note, 124, y, 920, 30);
      });
      y += 18;
      ctx.fillStyle = '#5f6874';
      ctx.font = '18px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      wrapText(ctx, t('reportDisclaimer'), 104, y, 930, 26);
      return canvas;
    }

    function addCanvasToPdf(jsPDF, canvas) {
      const doc = new jsPDF({ orientation: 'p', unit: 'mm', format: 'a4', compress: true });
      const margin = 10;
      const pageWidth = 210;
      const pageHeight = 297;
      const contentWidth = pageWidth - margin * 2;
      const pxPerMm = canvas.width / contentWidth;
      const sliceHeight = Math.floor((pageHeight - margin * 2) * pxPerMm);
      let offset = 0;
      let page = 0;
      while (offset < canvas.height) {
        const partHeight = Math.min(sliceHeight, canvas.height - offset);
        const slice = document.createElement('canvas');
        slice.width = canvas.width;
        slice.height = partHeight;
        const sliceCtx = slice.getContext('2d');
        sliceCtx.drawImage(canvas, 0, offset, canvas.width, partHeight, 0, 0, canvas.width, partHeight);
        if (page > 0) doc.addPage();
        doc.addImage(slice.toDataURL('image/png'), 'PNG', margin, margin, contentWidth, partHeight / pxPerMm);
        offset += partHeight;
        page += 1;
      }
      return doc;
    }

    async function exportPdfReport() {
      calculate();
      if (!lastReport || !lastReport.rows.length) {
        exportStatus.textContent = t('exportEmpty');
        return;
      }
      exportButton.disabled = true;
      exportStatus.textContent = t('exportLoading');
      try {
        const jsPDF = await loadJsPdf();
        const canvas = createReportCanvas(lastReport);
        const doc = addCanvasToPdf(jsPDF, canvas);
        const stamp = new Date().toISOString().slice(0, 10);
        doc.save('chargeable-weight-report-' + stamp + '.pdf');
        exportStatus.textContent = t('exportReady');
      } catch (error) {
        exportStatus.textContent = t('exportFailed');
      } finally {
        exportButton.disabled = false;
      }
    }

    function addRow(data) {
      rowTemplate(data);
    }

    function restoreSavedState() {
      const saved = readSavedState();
      if (!saved) return false;
      rowsBody.innerHTML = '';
      rowId = 0;
      customDivisor.value = saved.customDivisor;
      if (saved.rows.length) {
        saved.rows.forEach((row) => addRow(row));
      } else {
        addRow();
      }
      setSaveStatus('saveRestored', 3000);
      return true;
    }

    root.querySelector('[data-add-row]').addEventListener('click', () => {
      addRow();
      calculate();
      scheduleSave();
    });
    root.querySelector('[data-load-sample]').addEventListener('click', () => {
      rowsBody.innerHTML = '';
      rowId = 0;
      addRow({ name: '自拍杆长条箱', qty: 4, l: 75, w: 35, h: 28, kg: 8 });
      addRow({ name: '配件重货箱', qty: 3, l: 42, w: 30, h: 24, kg: 14 });
      calculate();
      saveStateNow();
    });
    root.querySelector('[data-reset-rows]').addEventListener('click', () => {
      clearSavedState();
      rowsBody.innerHTML = '';
      rowId = 0;
      customDivisor.value = '6000';
      addRow();
      calculate();
      saveStateNow('saveCleared');
    });
    customDivisor.addEventListener('input', () => {
      calculate();
      scheduleSave();
    });
    exportButton.addEventListener('click', exportPdfReport);
    document.addEventListener('shipping:languagechange', () => {
      translateRows();
      calculate();
    });
    const restored = restoreSavedState();
    restoreReady = true;
    if (!restored) {
      addRow({ name: '示例轻泡箱', qty: 2, l: 60, w: 45, h: 40, kg: 8 });
      addRow({ name: '示例重货箱', qty: 1, l: 38, w: 28, h: 22, kg: 12 });
    }
    calculate();
  }

  initLanguage();
  initTheme();
  initAdSlots();
  initArticleFilter();
  initCopyButtons();
  initCalculator();
})();
