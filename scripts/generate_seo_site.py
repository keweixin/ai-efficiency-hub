from __future__ import annotations

import datetime
from html import escape
from pathlib import Path
import json
import math
import re


ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "articles"
ASSETS_DIR = ROOT / "assets"
IMAGE_DIR = ASSETS_DIR / "images"
ARTICLE_IMAGE_DIR = IMAGE_DIR / "articles"

SITE_URL = "https://www.bevoorra.business"
SITE_NAME = "跨境运费避坑工具箱"
SITE_DESCRIPTION = "面向外贸员、跨境电商卖家、独立站卖家和 FBA 新手的体积重、CBM、计费重与渠道复核静态工具站。"
PUBLISHED_DATE = "2026-05-21"
TODAY = datetime.date.today().isoformat()
VERCEL_ANALYTICS_SCRIPT = "/_vercel/insights/script.js"


SOURCES = {
    "dhl_dct": (
        "DHL DCT Help：Volumetric weight",
        "https://dct.dhl.com/help",
    ),
    "ems_product": (
        "中国 EMS：国际及港澳台 EMS 产品概况",
        "https://my.ems.com.cn/intl/shipping/product/product_1.html",
    ),
    "ems_notice": (
        "中国 EMS：关于调整部分国际及港澳台邮件计泡规则的通知",
        "https://my.ems.com.cn/pcp-web/f/pcp/indexController/tonoticeindex?ntificationId=af3b06f2d6c6c51244472ad090c23ef9",
    ),
    "sf_rate": (
        "顺丰官网：Rates & Transit Time 支持说明",
        "https://www.sf-express.com/chn/en/price-query",
    ),
    "amazon_fba_pack": (
        "Amazon Seller Central Help：Packaging and prep requirements",
        "https://sellercentral.amazon.com/help/hub/reference/G201079430",
    ),
    "amazon_sp_api": (
        "Amazon SP-API：Create shipment without carton info",
        "https://developer-docs.amazon.com/sp-api/lang-en_EN/docs/create-shipment-without-carton-info",
    ),
    "google_helpful": (
        "Google Search Central：Creating helpful, reliable, people-first content",
        "https://developers.google.com/search/docs/fundamentals/creating-helpful-content",
    ),
    "google_spam": (
        "Google Search Central：Spam policies for Google web search",
        "https://developers.google.com/search/docs/essentials/spam-policies",
    ),
    "baidu_quality": (
        "百度搜索资源平台：百度搜索优质内容指南",
        "https://ziyuan.baidu.com/college/articleinfo?id=2947",
    ),
}


GROUPS = {
    "volume": {
        "label": "体积重与 CBM",
        "short": "体积重",
        "page": "volume.html",
        "eyebrow": "Volumetric Weight",
        "accent": "accent-green",
        "image": "volume",
        "lead": "先把长宽高、实重、体积重、CBM 和计费重算清楚，再看渠道报价是否需要复核。",
        "groups": ["体积重公式", "CBM", "混装核算", "进位复核"],
    },
    "channels": {
        "label": "渠道规则复核",
        "short": "渠道复核",
        "page": "channels.html",
        "eyebrow": "Channel Rules",
        "accent": "accent-blue",
        "image": "channels",
        "lead": "把 DHL、EMS、顺丰、标准空运和 FBA 头程分开看，避免用一个分母套所有渠道。",
        "groups": ["DHL", "EMS", "顺丰", "FBA 头程"],
    },
    "packing": {
        "label": "包装与拆单决策",
        "short": "包装拆单",
        "page": "packing.html",
        "eyebrow": "Packing Decisions",
        "accent": "accent-amber",
        "image": "packing",
        "lead": "围绕外箱尺寸、长边、空隙、混装和拆箱做复核，给发货前多一道可执行检查。",
        "groups": ["外箱测量", "拆箱判断", "装箱优化", "仓库复核"],
    },
}

GROUP_ORDER = ["volume", "channels", "packing"]

# Future pSEO expansion is intentionally disabled until Search Console data
# proves which route and product combinations deserve dedicated pages.
PSEO_EXPANSION_ENABLED = False
PSEO_PILOT_DIMENSIONS = {
    "routes": ["china-to-usa", "china-to-germany", "china-to-uk", "china-to-canada"],
    "channels": ["air-freight", "express", "fba-first-leg"],
    "products": ["electronics", "apparel", "small-appliances", "accessories"],
}


IMAGES = {
    "volume": {
        "src": "assets/images/articles/logistics-calculator.png",
        "webp": "assets/images/articles/logistics-calculator.webp",
        "alt": "计算器、纸箱和计量线条组成的跨境运费核算插图",
        "caption": "站内生成插图：用于表示体积重、CBM 和计费重核算。",
        "width": 1200,
        "height": 675,
    },
    "channels": {
        "src": "assets/images/articles/channel-routes.png",
        "webp": "assets/images/articles/channel-routes.webp",
        "alt": "不同物流渠道路线和纸箱节点组成的复核插图",
        "caption": "站内生成插图：用于表示不同承运渠道的规则差异。",
        "width": 1200,
        "height": 675,
    },
    "packing": {
        "src": "assets/images/articles/carton-checklist.png",
        "webp": "assets/images/articles/carton-checklist.webp",
        "alt": "纸箱、卷尺和检查清单组成的包装复核插图",
        "caption": "站内生成插图：用于表示外箱尺寸、包装和拆箱检查。",
        "width": 1200,
        "height": 675,
    },
}


def source(*keys: str) -> list[tuple[str, str]]:
    return [SOURCES[key] for key in keys]


ARTICLES = [
    {
        "slug": "volumetric-weight-formula-dhl-ems-sf",
        "group": "volume",
        "tag": "体积重公式",
        "title": "体积重公式怎么计算：DHL、EMS、顺丰口径对照",
        "description": "用跨境发货场景解释体积重公式，区分 DHL 5000、EMS 6000 与顺丰不同产品口径，帮助发货前复核计费重。",
        "keyword": "体积重公式",
        "scenario": "新手卖家拿到报价单时，常只看每千克运费，却没有把外箱长宽高换算成体积重。对于自拍杆、收纳盒、灯具、毛绒类商品，外箱占用舱位可能比实际重量更关键。",
        "method": "先以单箱为单位记录长、宽、高和实重，再按渠道分母计算体积重，最后用实重与体积重较大值作为计费重的复核基准。DHL 官方帮助页给出的标准分母是 5000；中国 EMS 国际 EMS/e 特快页面显示超过计泡条件后按长宽高除以 6000；顺丰公开页则按产品列出不同分母，需要回到具体服务确认。",
        "example": "一箱货外箱为 75cm × 35cm × 28cm，实重 8kg。按 DHL 5000 计算，体积重为 14.7kg；按 6000 计算，体积重为 12.25kg。两个结果都高于实重，因此报价复核时不能只拿 8kg 去乘单价。",
        "table": ["箱号", "长宽高 cm", "实重 kg", "分母", "体积重 kg", "计费重 kg", "备注"],
        "steps": ["先确认尺寸是外箱尺寸，不是产品裸尺寸。", "按渠道分别套用 5000、6000 或承运商给出的分母。", "实重和体积重取较大值，再看是否需要进位。", "把长边超过阈值的箱子单独标记。", "拿计算结果与报价单逐行核对。"],
        "mistakes": ["把厘米和米混在一起计算。", "用产品尺寸替代外箱尺寸。", "把某个渠道的分母套到所有渠道。", "忽略多箱货每箱分别计费的可能性。"],
        "sources": source("dhl_dct", "ems_product", "sf_rate"),
    },
    {
        "slug": "cbm-calculation-cross-border",
        "group": "volume",
        "tag": "CBM",
        "title": "CBM 怎么算：外贸装箱前的体积核算",
        "description": "解释 CBM 的计算方式，以及它和体积重、装箱、空运海运复核之间的关系。",
        "keyword": "CBM 计算",
        "scenario": "外贸报价和头程发货里经常出现 CBM。很多卖家知道它代表立方米，却没有把每个 SKU 的外箱数量、箱规和总体积连起来核算，导致装箱和报价复核都缺少基准。",
        "method": "CBM 的基础公式是长 × 宽 × 高，再把立方厘米换算成立方米。以厘米为单位时，单箱 CBM 等于长 × 宽 × 高 ÷ 1,000,000，再乘以箱数得到总 CBM。它不等同于计费重，但能帮助判断货物是偏轻泡还是偏重货。",
        "example": "单箱 60cm × 40cm × 50cm，箱数 20 箱，单箱 CBM 是 0.12，总 CBM 是 2.4。如果总实重只有 180kg，平均密度约 75kg/CBM，通常应重点复核体积重和舱位占用。",
        "table": ["SKU", "箱数", "单箱尺寸", "单箱 CBM", "总 CBM", "总实重", "密度 kg/CBM"],
        "steps": ["每个 SKU 单独记录箱规和箱数。", "先算单箱 CBM，再汇总总 CBM。", "用总实重除以总 CBM 估算密度。", "密度偏低时重点复核体积重。", "把 CBM、实重、计费重同时交给货代复核。"],
        "mistakes": ["只统计产品数量，不统计箱数。", "把毫米、厘米、米单位混用。", "只看 CBM，不看实际重量。", "没有保留原始箱规来源。"],
        "sources": source("dhl_dct", "sf_rate", "google_helpful"),
    },
    {
        "slug": "chargeable-weight-actual-vs-volume",
        "group": "volume",
        "tag": "计费重",
        "title": "计费重为什么取实重和体积重较大值",
        "description": "面向跨境卖家解释计费重的底层逻辑，说明为什么实际重量很轻也可能按更高重量计费。",
        "keyword": "计费重",
        "scenario": "同样是 8kg 的货，一个小箱重货和一个大箱轻货占用的运输资源不同。跨境快递和空运通常会比较实重与体积重，用较大值作为计费重，这一点是报价复核的核心。",
        "method": "计费重的复核顺序是：先称实重，再量外箱尺寸，按渠道分母算体积重，然后取较大值。DHL 的说明明确会比较体积重和实际重量，并使用较高者计算运费；顺丰公开说明也列出实际重量与体积重量取较大值的逻辑。",
        "example": "某箱实重 6kg，外箱 50cm × 45cm × 40cm。按 6000 算体积重 15kg，按 5000 算体积重 18kg。即使实重只有 6kg，复核报价时也要按 15kg 或 18kg 这类计费重口径看。",
        "table": ["项目", "实重", "体积重", "较大值", "是否需复核", "复核说明"],
        "steps": ["先用同一单位整理实重和尺寸。", "按实际渠道使用对应分母。", "体积重大于实重时标记轻泡风险。", "多箱货按箱汇总计费重。", "复核报价是否说明了进位方式。"],
        "mistakes": ["只把总实重发给货代。", "认为轻货一定更便宜。", "没有区分单箱计费和整票汇总。", "漏看计费重的小数进位。"],
        "sources": source("dhl_dct", "sf_rate"),
    },
    {
        "slug": "divisor-5000-vs-6000",
        "group": "volume",
        "tag": "分母差异",
        "title": "分母 5000 和 6000 差在哪里",
        "description": "说明体积重分母越小计费重越高，并用跨境发货案例比较 5000 与 6000 的差异。",
        "keyword": "分母 5000 6000",
        "scenario": "报价单里常见长宽高除以 5000 或 6000。很多卖家只把它当成渠道差别，没有意识到同一箱货在两个分母下可能出现明显计费重差异。",
        "method": "在尺寸相同的情况下，分母越小，体积重越大。DHL 官方支持页面列出标准分母 5000；中国 EMS 页面和 2022 通知显示体积重量公式为长宽高除以 6000。计算时应把不同分母并排比较，而不是只算一个结果。",
        "example": "80cm × 35cm × 30cm 的外箱，体积为 84,000 立方厘米。除以 5000 是 16.8kg，除以 6000 是 14kg。若实重为 10kg，两种渠道都会按体积重方向复核，但 DHL 口径下更高。",
        "table": ["箱规", "分母 5000", "分母 6000", "实重", "计费重差异", "复核动作"],
        "steps": ["把外箱体积先算出来。", "并排计算 5000、6000 和自定义分母。", "看差异是否足以影响渠道选择。", "向承运商确认是否还有进位和附加规则。", "把结论写入报价复核表。"],
        "mistakes": ["以为 6000 一定适用于所有空运。", "只比较单价，不比较计费重。", "忽略长边规则对 EMS 的影响。", "没有记录报价使用的分母。"],
        "sources": source("dhl_dct", "ems_product", "ems_notice"),
    },
    {
        "slug": "multi-sku-mixed-cargo-weight",
        "group": "volume",
        "tag": "混装核算",
        "title": "多 SKU 混装货物怎么核算计费重",
        "description": "讲解多 SKU 混装时如何按箱或按 SKU 整理尺寸、重量和分母，避免总重口径掩盖轻泡货差异。",
        "keyword": "多 SKU 混装计费重",
        "scenario": "跨境卖家常把配件、轻泡品和重货混在一票发走。只看总实重会掩盖箱规差异，尤其是大件轻货和小件重货混装时，报价复核必须拆到箱或 SKU 级别。",
        "method": "先按箱号建立明细，每箱记录包含哪些 SKU、数量、外箱尺寸和实重。再按渠道分母计算每箱体积重，最后汇总计费重。若某些箱子的长边或体积重显著偏高，应单独做拆分比较。",
        "example": "一票货有 5 箱自拍杆、8 箱配件和 3 箱重型支架。自拍杆箱长边 75cm，配件箱体积小但实重大。把三类货混在一个总表里会看不出触发点，分箱表能直接暴露哪个 SKU 需要复核。",
        "table": ["箱号", "SKU 组成", "数量", "长宽高", "实重", "体积重", "计费重", "异常标签"],
        "steps": ["先按箱号整理，而不是只按产品整理。", "给每箱标注主 SKU 和混装 SKU。", "分别计算不同渠道计费重。", "筛出长边或体积重异常的箱子。", "对异常箱做拆箱或换渠道模拟。"],
        "mistakes": ["只给货代总件数和总重量。", "把混装箱当成标准箱处理。", "没有记录每箱实际装了什么。", "拆箱建议没有回到仓库可执行性。"],
        "sources": source("dhl_dct", "ems_product", "sf_rate"),
    },
    {
        "slug": "carton-vs-product-size",
        "group": "volume",
        "tag": "尺寸口径",
        "title": "产品尺寸和外箱尺寸为什么不能混用",
        "description": "解释跨境发货复核中产品裸尺寸、内盒尺寸、外箱尺寸的区别，避免体积重计算失真。",
        "keyword": "外箱尺寸",
        "scenario": "产品详情页上的尺寸通常是裸产品或零售包装尺寸，实际发货还会多出内盒、缓冲材料和外箱。用产品尺寸算体积重，常会低估计费重。",
        "method": "复核计费重时应使用承运环节可测量的外箱尺寸。产品尺寸用于选品和页面展示，内盒尺寸用于包装规划，外箱尺寸用于物流报价。三者必须分列，不要混在一个字段里。",
        "example": "一个灯具裸产品长 38cm，零售盒长 45cm，加缓冲后外箱长 58cm。如果只用 38cm 算，体积重会明显偏低；若发 EMS，还要关注外箱任一单边是否达到计泡条件。",
        "table": ["尺寸类型", "用途", "测量位置", "是否用于计费重复核", "备注"],
        "steps": ["给产品尺寸、内盒尺寸、外箱尺寸分列。", "拍照记录外箱测量方式。", "使用外箱最长边做阈值检查。", "更新装箱后再复核一次。", "把最终箱规写入发货交接单。"],
        "mistakes": ["直接拿商品页面尺寸报价。", "忽略缓冲材料带来的体积变化。", "只量最长边，不量宽和高。", "仓库换箱后没有同步表格。"],
        "sources": source("ems_product", "dhl_dct", "amazon_fba_pack"),
    },
    {
        "slug": "round-up-chargeable-weight",
        "group": "volume",
        "tag": "进位复核",
        "title": "计费重进位规则怎么影响报价复核",
        "description": "说明计费重小数进位、按箱进位和整票进位可能造成的差异，提醒跨境卖家复核报价单口径。",
        "keyword": "计费重进位",
        "scenario": "同样算出 12.25kg，有的报价会按 12.5kg，有的会按 13kg，有的多箱货每箱单独进位后再汇总。进位方式不清楚，报价复核就会差一截。",
        "method": "把进位规则作为单独字段询问承运商或货代。需要确认按 0.1kg、0.5kg 还是 1kg 进位，是单箱进位还是整票汇总后进位。顺丰公开页面就列出不同服务的进位说明，说明该规则不应被忽略。",
        "example": "10 箱货每箱计费重 2.26kg。若按单箱 0.5kg 进位，每箱可能按 2.5kg，合计 25kg；若整票汇总后进位，可能是 22.6kg 后再按规则处理。复核时要问清口径。",
        "table": ["箱数", "单箱计费重", "单箱进位", "整票进位", "差异", "待确认问题"],
        "steps": ["先保留未进位的原始计费重。", "询问进位单位和应用层级。", "多箱货同时计算单箱进位和整票进位。", "把差异写入报价复核备注。", "最终以承运商实际确认口径为准。"],
        "mistakes": ["只算公式，不算进位。", "把单箱进位误认为整票进位。", "报价单没有说明时直接默认。", "对小数差异不做记录。"],
        "sources": source("sf_rate", "dhl_dct"),
    },
    {
        "slug": "long-side-volume-trigger",
        "group": "volume",
        "tag": "长边提醒",
        "title": "长边超过阈值时为什么要单独复核",
        "description": "说明长边阈值对 EMS 等渠道体积重复核的重要性，并提醒规则可能随产品、地区和时间调整。",
        "keyword": "长边计泡",
        "scenario": "自拍杆、灯架、瑜伽垫、海报筒这类长条货，实际重量可能不高，但单边尺寸会触发计泡或特殊尺寸限制。旧经验容易过时，发货前应回到官方页面和报价工具确认。",
        "method": "对每箱计算最长边，并与渠道阈值对照。中国 EMS 产品页面显示国际 EMS/e 特快在任一单边长度超过 40cm 时开始计泡；2022 通知也说明部分国际及港澳台邮件从 60cm 调整到 40cm。实际发货仍需按产品和目的地复核。",
        "example": "一箱外箱 75cm × 18cm × 16cm、实重 3kg 的长条货，按 6000 算体积重 3.6kg。看起来差异不大，但长边已经值得单独标记，因为尺寸限制、计泡条件和渠道接受范围都要确认。",
        "table": ["箱号", "最长边", "渠道", "阈值口径", "是否标记", "复核结论"],
        "steps": ["每箱自动计算最长边。", "超过 40cm 的箱子先标记复核。", "查询对应渠道和目的地尺寸限制。", "必要时做拆箱或换箱模拟。", "保留承运商确认记录。"],
        "mistakes": ["仍按旧的 60cm 经验判断。", "只看体积重，不看尺寸限制。", "把一个产品的规则套到所有 EMS 产品。", "没有把长条货从混装中单独标出。"],
        "sources": source("ems_product", "ems_notice"),
    },
    {
        "slug": "density-ratio-light-bulky-goods",
        "group": "volume",
        "tag": "轻泡货",
        "title": "轻泡货和重货怎么用密度判断",
        "description": "用 kg/CBM 的密度思路帮助卖家判断货物偏轻泡还是偏重，从而决定复核重点。",
        "keyword": "轻泡货密度",
        "scenario": "选品阶段很难只凭感觉判断货物是否容易被体积重影响。用总实重除以总 CBM 得到密度，可以帮助卖家把风险提前放到包装和渠道复核环节。",
        "method": "密度不是承运商统一计费规则，但它是内部判断工具。密度低说明单位体积承载的重量少，通常要优先复核体积重；密度高则要关注限重、搬运和包装承压。",
        "example": "2.4CBM 的货总实重 180kg，密度约 75kg/CBM；0.5CBM 的金属配件总实重 220kg，密度 440kg/CBM。前者优先复核体积重，后者优先复核单箱重量、箱体强度和搬运要求。",
        "table": ["SKU", "总 CBM", "总实重", "密度 kg/CBM", "复核重点", "备注"],
        "steps": ["先算总 CBM 和总实重。", "用实重除以 CBM 得到密度。", "低密度货标记体积重复核。", "高密度货标记包装承重。", "根据密度决定是否拆分渠道比较。"],
        "mistakes": ["把密度当成最终运费。", "只看单个产品，不看整票混装。", "低密度货没有提前压缩包装。", "高密度货忽略单箱限重。"],
        "sources": source("dhl_dct", "sf_rate", "google_helpful"),
    },
    {
        "slug": "spreadsheet-cbm-template",
        "group": "volume",
        "tag": "表格模板",
        "title": "用表格做 CBM 与计费重复核模板",
        "description": "给跨境卖家一套可复制的表格字段，用于记录多 SKU 的 CBM、体积重、计费重和渠道分母。",
        "keyword": "CBM 计费重表格",
        "scenario": "一票货只有几箱时，手算还能勉强处理；一旦 SKU、箱数和渠道变多，就需要固定表格。表格的价值不是好看，而是让每次复核都能追溯字段来源。",
        "method": "表格应至少包含 SKU、箱号、箱数、长宽高、实重、CBM、渠道分母、体积重、计费重、长边提醒和报价备注。关键字段都用公式生成，人工只录入测量数据和承运商确认信息。",
        "example": "把 DHL、EMS、标准空运放成三列分母，并用同一组箱规自动计算三套计费重。这样报价单来之后，不需要重新手算，只要核对承运商采用的分母和进位规则。",
        "table": ["SKU", "箱号", "箱数", "长", "宽", "高", "实重", "CBM", "分母", "体积重", "计费重", "长边提醒"],
        "steps": ["录入字段只保留测量数据。", "计算字段统一用公式。", "渠道分母做成可切换列。", "异常提示单独高亮。", "每次报价保留一份快照。"],
        "mistakes": ["手动改公式结果。", "没有区分录入字段和计算字段。", "报价后覆盖原始箱规。", "多人协作时没有版本记录。"],
        "sources": source("dhl_dct", "ems_product", "sf_rate"),
    },
    {
        "slug": "dhl-volumetric-divisor-5000",
        "group": "channels",
        "tag": "DHL",
        "title": "DHL 体积重分母 5000 怎么用于报价复核",
        "description": "基于 DHL 官方帮助页说明，解释 DHL 体积重分母 5000 的计算和复核方式。",
        "keyword": "DHL 体积重 5000",
        "scenario": "DHL 报价常被新手拿来和空运、EMS 直接比每千克单价，但如果没有先按 5000 分母算计费重，单价对比就没有共同基础。",
        "method": "DHL 官方帮助页说明，体积重等于长 × 宽 × 高 ÷ 体积重分母，使用厘米和千克时标准分母为 5000，并与实际重量比较取较大值。复核时应按单箱外尺寸计算，再考虑多件货汇总。",
        "example": "一箱 60cm × 45cm × 40cm，实重 16kg。DHL 体积重为 21.6kg，因此报价复核应围绕 21.6kg 及其进位结果，而不是 16kg。",
        "table": ["箱号", "长宽高", "实重", "DHL 体积重", "复核计费重", "待确认进位"],
        "steps": ["确认箱规是厘米。", "用 5000 分母算每箱体积重。", "与实重取较大值。", "问清进位单位。", "把结果和 DHL 报价逐项核对。"],
        "mistakes": ["只比较 DHL 每千克单价。", "用 6000 分母估算 DHL。", "多箱货只算平均尺寸。", "不确认目的地和服务附加条件。"],
        "sources": source("dhl_dct", "google_helpful"),
    },
    {
        "slug": "ems-40cm-volume-weight-rule",
        "group": "channels",
        "tag": "EMS",
        "title": "EMS 40cm 计泡规则如何影响跨境发货复核",
        "description": "解释中国 EMS 国际 EMS/e 特快超过 40cm 进入计泡复核和 /6000 公式，并提醒旧 60cm 认知已经可能过时。",
        "keyword": "EMS 40cm 计泡",
        "scenario": "很多卖家仍记得较早的长边经验，但中国 EMS 公开页面和 2022 调整通知都显示，部分国际及港澳台邮件的计泡标准已经调整到任一单边超过 40cm 的口径。",
        "method": "复核 EMS 时，先检查任一单边是否超过计泡条件，再按长 × 宽 × 高 ÷ 6000 计算体积重。页面同时提醒查询结果仅供参考，以实际收寄计费为准，因此工具只能做发货前复核，不替代官方报价。",
        "example": "外箱 42cm × 32cm × 28cm，实重 4kg。最长边超过 40cm 口径，应进入 EMS 计泡复核。体积重约 6.27kg，高于实重，报价时要关注是否按体积重方向处理。",
        "table": ["箱号", "最长边", "是否超过 40cm", "实重", "体积重 /6000", "复核备注"],
        "steps": ["每箱计算最长边。", "超过 40cm 口径就标记复核。", "按 6000 分母算体积重。", "查目的地尺寸和限重。", "以官方报价工具或收寄确认为准。"],
        "mistakes": ["继续使用旧的 60cm 经验。", "只看重量不看长边。", "把 EMS 所有产品视为同一规则。", "没有保存官方确认口径。"],
        "sources": source("ems_product", "ems_notice"),
    },
    {
        "slug": "sf-express-volume-weight-rules",
        "group": "channels",
        "tag": "顺丰",
        "title": "顺丰体积重规则怎么保守理解",
        "description": "基于顺丰公开支持页，说明不同顺丰服务可能使用不同体积重分母，国际服务可见 /5000 口径。",
        "keyword": "顺丰体积重",
        "scenario": "顺丰服务类型多，国内、港澳台、国际、冷链和大件规则不完全一致。如果把某一个页面片段当成全部服务统一口径，很容易做出错误复核。",
        "method": "顺丰公开支持页列出实际重量与体积重量取较大值，并按不同服务列出 12000、6000、5000、3000 等体积系数。对于国际服务，页面可见长宽高除以 5000 的口径。实际发货时仍需以服务、流向和客服确认为准。",
        "example": "同一箱 55cm × 40cm × 35cm，按 6000 体积重约 12.83kg，按 5000 约 15.4kg。若选择顺丰不同服务，不能只拿一个结果判断，要把具体产品名称写进复核表。",
        "table": ["服务类型", "公开分母口径", "适用提醒", "需确认问题", "复核记录"],
        "steps": ["确认服务名称和寄递流向。", "查官方页面或询问客服。", "用可能分母并排试算。", "标注最终确认口径。", "保存报价截图或文本记录。"],
        "mistakes": ["把国内件规则套到国际件。", "只记住 6000 一个分母。", "忽略服务名称差异。", "没有复核进位方式。"],
        "sources": source("sf_rate", "google_helpful"),
    },
    {
        "slug": "standard-air-vs-express-divisor",
        "group": "channels",
        "tag": "标准空运",
        "title": "标准空运和国际快递为什么要分开算",
        "description": "解释标准空运、国际快递和 EMS 等渠道在分母、时效、限制和报价结构上的复核差异。",
        "keyword": "标准空运 分母",
        "scenario": "跨境卖家常把标准空运、国际快递和邮政渠道放在同一张表里比较。这样做可以，但前提是先把分母、时效、限制、附加项和计费重都拆清楚。",
        "method": "标准空运常见复核口径可先按 6000 做内部模拟，但不能写成所有线路固定规则。国际快递要按承运商官方口径，例如 DHL 5000。EMS 则要看计泡条件和 /6000。最终比较应落到总计费重和附加项，而不是单价。",
        "example": "一票轻泡货按 6000 算 80kg，按 DHL 5000 算 96kg。如果快递单价看似更低，但计费重更高，最终报价不一定更合适。工具应提示复核，而不是直接替用户下结论。",
        "table": ["渠道", "模拟分母", "计费重", "时效", "尺寸限制", "待确认附加项"],
        "steps": ["把渠道名称写完整。", "分别填入分母和进位口径。", "把时效和尺寸限制放在同一表里。", "计算总计费重后再比较报价。", "让承运商确认最终计费规则。"],
        "mistakes": ["只看每千克报价。", "把模拟分母当官方承诺。", "忽略尺寸限制和目的地差异。", "没有把附加项列入复核。"],
        "sources": source("dhl_dct", "ems_product", "sf_rate"),
    },
    {
        "slug": "fba-first-leg-quote-checklist",
        "group": "channels",
        "tag": "FBA 头程",
        "title": "FBA 头程报价复核清单",
        "description": "整理 FBA 头程发货前需要复核的箱规、箱数、重量、标签、包装和渠道规则。",
        "keyword": "FBA 头程报价复核",
        "scenario": "FBA 新手往往把注意力放在入仓流程，却忽略头程报价里的箱规、计费重、标签和包装要求。任何一个字段不一致，都可能影响运输复核或入仓处理。",
        "method": "先把物流计费复核和亚马逊入仓要求分开。物流侧关注箱规、重量、计费重和渠道；FBA 侧关注可扫描标签、箱内信息、包装安全和商品可接收状态。两边都要形成清单。",
        "example": "一票货准备走空运到 FBA 仓。报价复核表里要有每箱尺寸和实重；入仓交接里要有箱标、SKU、数量和包装要求。不要只把亚马逊创建货件截图发给货代。",
        "table": ["复核项", "物流侧字段", "FBA 侧字段", "负责人", "确认状态"],
        "steps": ["整理每箱箱规和重量。", "确认渠道分母和进位。", "核对 FBA 箱标和商品标签。", "检查包装是否满足入仓要求。", "发货前保存最终交接表。"],
        "mistakes": ["只核对亚马逊后台数量。", "不记录每箱尺寸。", "标签和箱内数量不一致。", "包装要求交给仓库口头处理。"],
        "sources": source("amazon_fba_pack", "amazon_sp_api", "dhl_dct"),
    },
    {
        "slug": "freight-forwarder-quote-reading",
        "group": "channels",
        "tag": "报价单",
        "title": "货代报价单怎么看才不漏复核项",
        "description": "用中性方式拆解货代报价单字段：渠道、分母、计费重、进位、附加项、时效和限制。",
        "keyword": "货代报价单复核",
        "scenario": "报价单通常不只是一行单价。渠道名称、计费重、分母、进位、附加项、截单时间和尺寸限制都可能影响最终决策。新手最容易漏掉口径说明。",
        "method": "把报价单拆成两层：第一层是计算字段，第二层是服务字段。计算字段包括箱规、实重、体积重、计费重、进位；服务字段包括渠道、时效、目的地、限制和需要额外确认的项目。",
        "example": "同一票货两个报价看起来每千克差 2 元，但一个按 5000 分母，一个按 6000 分母。只有把计费重算出来，再加上附加项和时效，才有比较意义。",
        "table": ["字段", "应填写内容", "复核问题", "是否已确认", "证据"],
        "steps": ["先确认渠道全称。", "找出分母和计费重口径。", "询问进位方式。", "列出可能附加项。", "把确认记录保存在报价表旁边。"],
        "mistakes": ["只看单价最低。", "不知道报价是否含附加项。", "没有问尺寸限制。", "没有保留书面确认。"],
        "sources": source("dhl_dct", "ems_product", "sf_rate"),
    },
    {
        "slug": "sea-air-express-cost-compare",
        "group": "channels",
        "tag": "渠道比较",
        "title": "海运、空运、国际快递比较时先看哪些字段",
        "description": "整理跨境发货比较不同渠道时的字段顺序，避免只按单价做判断。",
        "keyword": "海运 空运 快递 比较",
        "scenario": "海运、空运和国际快递的报价结构不同。海运更常关注 CBM、整柜散货和目的港费用；空运和快递更常关注计费重、分母和尺寸限制。直接按一行单价比较容易误判。",
        "method": "先确定货物是否急、是否轻泡、是否有长边或敏感属性，再分别整理 CBM、实重、计费重、时效、可达性和附加项。只有字段对齐后，渠道比较才有意义。",
        "example": "2CBM、160kg 的轻泡货，如果时效不急，海运可能进入比较；如果需要快速补货，则要在空运和快递之间复核计费重与时效。工具只能提示复核方向，最终还要看目的地和承运商确认。",
        "table": ["渠道", "主要计费基准", "适合场景", "限制项", "复核问题"],
        "steps": ["先判断时效要求。", "计算 CBM 和计费重。", "确认货物属性和目的地。", "把附加项单独列出。", "形成可解释的渠道比较结论。"],
        "mistakes": ["只按每千克或每立方比较。", "忽略目的地派送条件。", "没有考虑补货时间窗口。", "把一次报价当长期规则。"],
        "sources": source("dhl_dct", "sf_rate", "google_helpful"),
    },
    {
        "slug": "remote-area-surcharge-check",
        "group": "channels",
        "tag": "附加项",
        "title": "偏远地区和附加项为什么要提前问清",
        "description": "说明跨境报价中除计费重外，还应复核偏远地区、燃油、特殊处理等附加项。",
        "keyword": "跨境物流附加项",
        "scenario": "有些报价的计费重没问题，但最终金额仍有差异，原因可能来自目的地、特殊处理、燃油、住宅派送或其他附加项。附加项通常和渠道、国家、邮编、货物属性有关。",
        "method": "报价复核时不要只问分母，还要列出目的地邮编、派送类型、货物属性、尺寸和重量，让承运商或货代确认是否存在附加项。页面上没有明确说明的，不能自行假设为没有。",
        "example": "两票货计费重都是 20kg，但一个送到商业地址，一个送到偏远地址，最终金额可能不同。复核表应把邮编和派送条件列为必填字段。",
        "table": ["附加项", "触发信息", "需要提供的数据", "确认渠道", "备注"],
        "steps": ["整理目的地国家、城市和邮编。", "确认派送地址类型。", "提供完整箱规和重量。", "询问是否有特殊处理项。", "把确认结果写入报价单备注。"],
        "mistakes": ["只问基础运费。", "不提供邮编。", "特殊尺寸货不提前说明。", "附加项靠口头记忆。"],
        "sources": source("dhl_dct", "sf_rate"),
    },
    {
        "slug": "fuel-surcharge-and-accessorials",
        "group": "channels",
        "tag": "报价结构",
        "title": "燃油和其他费用项要怎样放进复核表",
        "description": "解释跨境发货报价复核表中基础运费、燃油、附加项和服务条件应分列记录。",
        "keyword": "跨境运费燃油附加",
        "scenario": "报价沟通中经常出现基础运费、燃油、附加项、报关服务和末端派送等不同费用项。把它们混成一个数字，会让后续复盘很困难。",
        "method": "复核表中应把基础计费重计算和费用项结构分开。先确认计费重，再确认每个费用项是否包含在报价中。若某项随时间浮动，应记录报价日期和有效期。",
        "example": "同样是 50kg 计费重，一个报价包含燃油，另一个报价燃油另计。表面单价不能直接比较，必须把包含项和不包含项拆出来。",
        "table": ["费用项", "是否包含", "计算基础", "有效期", "待确认问题"],
        "steps": ["先固定计费重。", "列出基础运费和附加项。", "确认燃油是否包含。", "记录报价有效期。", "复核最终总额口径。"],
        "mistakes": ["只保存总额。", "不记录报价日期。", "不知道哪些项目另计。", "不同报价包含项不一致仍直接比较。"],
        "sources": source("dhl_dct", "sf_rate", "google_helpful"),
    },
    {
        "slug": "customs-declared-value-basic-check",
        "group": "channels",
        "tag": "申报基础",
        "title": "申报价值和物流报价为什么要分开核对",
        "description": "以合规口径说明申报价值、货物信息和物流计费是不同问题，不能混在一起处理。",
        "keyword": "跨境申报价值核对",
        "scenario": "卖家在准备发货时，会同时处理申报价值、货物品名、箱规和物流报价。它们都影响发货，但性质不同：申报信息关系到合规和清关，计费重关系到运输费用复核。",
        "method": "复核时把申报资料和物流计费资料分表管理。申报侧保留真实品名、数量、材质、用途和价值依据；物流侧保留箱规、重量、分母和渠道。不要为了让表格简单而混用字段。",
        "example": "一箱配件的申报信息需要描述品名和数量，计费重复核需要长宽高和实重。两个表可以用同一个箱号关联，但不要用申报价值去解释运费差异。",
        "table": ["资料类型", "字段", "用途", "责任人", "复核方式"],
        "steps": ["给每箱设置唯一箱号。", "申报资料和物流资料分别整理。", "用箱号建立关联。", "申报信息以真实资料为准。", "物流报价以承运商确认口径为准。"],
        "mistakes": ["把申报金额当运费计算依据。", "品名描述过于模糊。", "申报表和箱规表无法对应。", "把合规问题交给计算工具判断。"],
        "sources": source("amazon_fba_pack", "google_spam", "baidu_quality"),
    },
    {
        "slug": "split-cartons-vs-mixed-cartons",
        "group": "packing",
        "tag": "拆箱判断",
        "title": "拆箱还是混装：发货前怎么做复核",
        "description": "说明拆箱和混装不是固定答案，应根据长边、体积重、实重、SKU 管理和仓库操作成本综合复核。",
        "keyword": "拆箱 混装",
        "scenario": "看到长边或体积重偏高时，很多人会立刻想到拆箱。但拆箱会增加箱数、标签、仓库操作和出错概率，不一定总是更好。正确做法是先模拟，再决定是否执行。",
        "method": "把原方案和拆箱方案并排计算：箱数、每箱尺寸、总 CBM、总实重、各渠道计费重、长边提醒和仓库可操作性。只有当差异明显且操作可控时，才进入实际拆箱。",
        "example": "一箱 80cm 长的轻货拆成两箱后，最长边下降，但总箱数增加，包装材料也增加。工具可以提示可能更优，但最终要由仓库和承运商确认。",
        "table": ["方案", "箱数", "总 CBM", "总计费重", "长边提醒", "操作风险"],
        "steps": ["先记录原装箱方案。", "模拟拆箱后的新箱规。", "分别计算渠道计费重。", "加入标签和操作风险。", "只把结论写成需要复核或可能更优。"],
        "mistakes": ["只为降低最长边而拆箱。", "忽略箱数增加后的进位。", "没有考虑仓库是否能执行。", "把工具建议当最终决定。"],
        "sources": source("ems_product", "dhl_dct", "amazon_fba_pack"),
    },
    {
        "slug": "carton-optimization-without-overpacking",
        "group": "packing",
        "tag": "装箱优化",
        "title": "装箱优化不要只追求更小体积",
        "description": "从包装安全和计费重两侧解释装箱优化，提醒不能为了降低体积而牺牲货损风险。",
        "keyword": "装箱优化",
        "scenario": "压缩外箱能降低体积重，但过度压缩会带来货损、变形、标签不可读和入仓异常。跨境发货的装箱优化必须同时看成本、保护和合规。",
        "method": "先确定货物可承受的堆叠和挤压范围，再寻找减少空隙的方式，例如调整内盒摆放、减少无效填充、选择更合适的标准箱。对于易碎品，保护优先级应高于单纯体积优化。",
        "example": "一箱玻璃制品如果为减少体积而取消缓冲材料，体积重可能下降，但破损风险明显上升。更稳的方案是减少无效空隙，同时保留必要保护。",
        "table": ["优化动作", "体积影响", "保护影响", "执行难度", "是否建议复核"],
        "steps": ["区分有效保护和无效空隙。", "先做样箱测试。", "记录优化前后尺寸。", "检查标签和条码位置。", "让仓库按固定标准执行。"],
        "mistakes": ["为了降低体积去掉必要缓冲。", "每批货箱规不一致。", "只做一次样箱不复测。", "忽略入仓和派送阶段的搬运风险。"],
        "sources": source("amazon_fba_pack", "dhl_dct", "google_helpful"),
    },
    {
        "slug": "long-item-shipping-selfie-stick-case",
        "group": "packing",
        "tag": "长条货",
        "title": "长条货发货复核：以自拍杆类产品为例",
        "description": "用长条货案例说明最长边、计泡、分母、拆箱和包装安全如何一起复核。",
        "keyword": "长条货发货",
        "scenario": "自拍杆、支架、灯杆、卷轴类产品常见问题是长边明显，但实重不一定高。它们既可能触发体积重复核，也可能遇到尺寸限制或特殊处理要求。",
        "method": "先把长条货从混装表里单独筛出来，记录最长边、包装后尺寸和实重。再按 EMS 超过 40cm 口径、DHL 5000 分母和其他渠道分母分别试算。对于可拆产品，可以模拟拆成更短箱规后的计费重差异。",
        "example": "75cm 长的自拍杆装箱后外箱长 82cm。即使总重量不高，也应先做长边提醒，再比较原箱、拆短包装和换渠道三种方案。任何方案都必须确保商品保护和仓库执行可行。",
        "table": ["方案", "最长边", "实重", "体积重 5000", "体积重 6000", "包装风险"],
        "steps": ["筛出最长边超过 40cm 的箱子。", "单独试算 5000 和 6000 分母。", "模拟拆短或换箱方案。", "检查产品是否允许拆分。", "让承运商确认尺寸接受范围。"],
        "mistakes": ["长条货混在总表里不标记。", "只看重量不看尺寸。", "为了拆短破坏产品包装。", "不确认目的地限制。"],
        "sources": source("ems_product", "ems_notice", "dhl_dct"),
    },
    {
        "slug": "protect-fragile-goods-and-void-fill",
        "group": "packing",
        "tag": "易碎品",
        "title": "易碎品包装如何兼顾保护和体积重",
        "description": "说明易碎品发货时如何区分必要缓冲和无效空隙，在保护优先前提下做体积复核。",
        "keyword": "易碎品包装体积重",
        "scenario": "易碎品往往需要缓冲，外箱会比产品大很多。卖家既担心体积重上升，也不能牺牲保护。复核的关键是找出无效空隙，而不是简单缩箱。",
        "method": "先确定商品破损风险和最低包装要求，再用样箱记录缓冲方案。必要缓冲保留，无效空隙优化。最终用优化后的外箱尺寸重新计算 CBM 和体积重。",
        "example": "陶瓷杯单个产品很小，但需要防撞材料。若外箱高度多出 8cm 空隙，可以通过调整内盒排列减少高度；但杯壁周围的保护不能随意取消。",
        "table": ["部位", "保护材料", "是否必要", "可优化空间", "复测尺寸"],
        "steps": ["先做跌落和挤压风险判断。", "标记必要缓冲区。", "寻找无效空隙。", "优化后重新量外箱。", "保留样箱照片和尺寸记录。"],
        "mistakes": ["只为降体积减少保护。", "优化后没有复测尺寸。", "易碎品和重货混装。", "没有把包装方案交给仓库固定执行。"],
        "sources": source("amazon_fba_pack", "dhl_dct"),
    },
    {
        "slug": "packaging-measurement-checklist",
        "group": "packing",
        "tag": "测量清单",
        "title": "包装测量清单：长宽高和重量怎么记录",
        "description": "给仓库和运营使用的包装测量清单，统一外箱长宽高、实重、箱号和照片记录。",
        "keyword": "包装测量清单",
        "scenario": "报价复核经常卡在仓库测量口径不统一：有人量产品，有人量外箱，有人四舍五入，有人没有拍照。清单能减少沟通成本。",
        "method": "测量清单应规定单位、测量对象、记录精度、照片要求和复测条件。所有物流复核字段都以最终封箱后的外箱为准，重量应包含包装材料。",
        "example": "仓库测量一箱货时，先贴箱号，再测最长边、宽、高和实重，拍一张带卷尺或标尺的照片。运营拿到表后才能计算体积重和 CBM。",
        "table": ["箱号", "测量人", "长", "宽", "高", "实重", "照片链接", "复测原因"],
        "steps": ["封箱后再测量。", "统一使用厘米和千克。", "每箱记录唯一箱号。", "异常箱拍照留存。", "报价前抽查复测。"],
        "mistakes": ["未封箱先测尺寸。", "重量不含包装材料。", "箱号和照片无法对应。", "异常数据没有复测。"],
        "sources": source("sf_rate", "dhl_dct", "amazon_fba_pack"),
    },
    {
        "slug": "warehouse-remeasure-process",
        "group": "packing",
        "tag": "仓库复测",
        "title": "仓库复测流程怎么设计",
        "description": "说明何时需要仓库复测外箱尺寸和重量，以及如何把复测结果同步给运营和货代。",
        "keyword": "仓库复测流程",
        "scenario": "包装调整、换箱、混装、拆箱和临时补货都会让原始箱规失效。如果仓库没有复测流程，报价表会继续使用旧数据。",
        "method": "把复测触发条件写清楚：换箱、拆箱、合箱、增加缓冲材料、箱体变形、抽检差异超过阈值。复测后更新箱规表，并保留旧版本，方便追溯报价差异。",
        "example": "运营要求把 10 箱改成 8 箱混装。仓库执行后必须重新测量每箱长宽高和实重，而不是继续沿用原来的 10 箱数据。",
        "table": ["触发条件", "复测动作", "同步对象", "截止时间", "记录位置"],
        "steps": ["定义复测触发条件。", "仓库复测后更新箱规表。", "运营重新计算计费重。", "货代按新数据复核报价。", "保留调整前后版本。"],
        "mistakes": ["换箱后不复测。", "只更新箱数不更新尺寸。", "复测数据只发聊天消息。", "旧报价和新箱规混用。"],
        "sources": source("dhl_dct", "amazon_fba_pack", "google_helpful"),
    },
    {
        "slug": "label-and-box-content-for-fba",
        "group": "packing",
        "tag": "FBA 标签",
        "title": "FBA 箱标和箱内信息如何配合物流复核",
        "description": "说明 FBA 发货中箱标、箱内信息、SKU 数量和物流箱规应如何关联，减少入仓和运输沟通问题。",
        "keyword": "FBA 箱标 箱内信息",
        "scenario": "FBA 头程不仅要算运费，还要让箱标、箱内 SKU、数量和实际外箱对应。物流表和 FBA 表脱节，容易让仓库、货代和运营各说各的。",
        "method": "用唯一箱号把物流箱规表和 FBA 箱内信息表关联起来。每箱既有长宽高、实重和计费重，也有 SKU、数量、箱标状态和条码可扫描检查。",
        "example": "箱号 A01 在物流表里是 60cm × 40cm × 38cm、18kg；在 FBA 表里应对应具体 SKU 和数量。若仓库换箱，两个表都要更新。",
        "table": ["箱号", "SKU", "数量", "箱标状态", "外箱尺寸", "实重", "复核人"],
        "steps": ["先建立箱号。", "每箱对应 SKU 和数量。", "贴标后检查可扫描。", "箱规表同步最终箱号。", "交接前抽查箱标和尺寸。"],
        "mistakes": ["物流箱号和 FBA 箱号不一致。", "换箱后不更新箱内信息。", "条码被胶带遮挡。", "只保存后台截图不保存箱规表。"],
        "sources": source("amazon_fba_pack", "amazon_sp_api"),
    },
    {
        "slug": "lightweight-bulky-items-packaging",
        "group": "packing",
        "tag": "轻泡包装",
        "title": "轻泡货包装怎么减少误判",
        "description": "针对轻泡货整理包装和复核思路：压缩无效体积、固定箱规、比较渠道分母和长边。",
        "keyword": "轻泡货包装",
        "scenario": "轻泡货看起来重量低，但运输中占用空间大，容易在报价复核时出现体积重高于实重的情况。包装优化能帮助减少误判，但不能代替渠道确认。",
        "method": "先用 CBM 和密度识别轻泡程度，再从包装结构入手减少无效空隙。优化后必须重新测量外箱，并分别计算 5000 与 6000 分母下的计费重。",
        "example": "毛绒类商品如果可以真空或压缩，需要确认是否影响产品恢复和平台入仓要求。压缩前后都要记录箱规，不能只凭经验判断。",
        "table": ["SKU", "优化前尺寸", "优化后尺寸", "恢复风险", "计费重变化", "是否执行"],
        "steps": ["先判断是否轻泡。", "找到无效空隙。", "评估压缩或换箱风险。", "优化后复测箱规。", "按多个渠道重新计算。"],
        "mistakes": ["压缩后产品无法恢复。", "优化只做一箱样品。", "没有同步仓库操作标准。", "忽略长边变化。"],
        "sources": source("dhl_dct", "ems_product", "amazon_fba_pack"),
    },
    {
        "slug": "heavy-small-items-mixed-loading",
        "group": "packing",
        "tag": "重货混装",
        "title": "小件重货混装时要注意什么",
        "description": "说明小件重货混装时不仅要看体积重，还要关注单箱实重、箱体承压、搬运和 SKU 对应关系。",
        "keyword": "小件重货混装",
        "scenario": "金属配件、工具、支架等小件重货体积不大，但单箱重量可能很高。它们和轻泡货混装时，不能只追求填满空间，还要看箱体承压和搬运安全。",
        "method": "把重货单箱重量作为单独复核项，设置合理上限并记录箱体承压。混装时避免重货压坏轻泡货，必要时分层、分箱或增加隔板。物流侧还要确认单箱限重和搬运要求。",
        "example": "一箱小配件体积重只有 8kg，但实重 28kg。它不属于体积重风险，却属于搬运和箱体强度复核对象。和轻泡货混装可能降低空隙，但会增加破损风险。",
        "table": ["SKU", "单箱实重", "箱体强度", "混装对象", "风险", "处理建议"],
        "steps": ["筛出高实重箱。", "确认单箱重量是否适合人工搬运。", "避免重货压轻货。", "记录箱体材质和承重。", "必要时单独分箱。"],
        "mistakes": ["只关注体积重，忽略实重。", "重货和易碎轻货直接混放。", "不确认单箱限重。", "箱体强度没有标准。"],
        "sources": source("sf_rate", "amazon_fba_pack", "dhl_dct"),
    },
    {
        "slug": "quote-audit-before-confirmation",
        "group": "packing",
        "tag": "下单前复核",
        "title": "确认发货前的报价复核清单",
        "description": "汇总确认发货前应检查的箱规、重量、分母、计费重、长边、附加项和规则来源。",
        "keyword": "发货前报价复核清单",
        "scenario": "发货前最后一次复核最容易被省略。运营觉得箱规已经发过，仓库觉得已经打包，货代觉得报价已经确认，但任何一个字段变化都可能让结果不同。",
        "method": "确认发货前，用一张清单把箱规、实重、分母、体积重、计费重、长边提醒、附加项、报价有效期和规则来源逐项打勾。没有确认的字段不要默认为通过。",
        "example": "如果仓库刚把 12 箱改成 10 箱，报价单仍按 12 箱计算，就需要重新复核。工具可以快速重算，但最终要把新箱规发给承运商确认。",
        "table": ["复核项", "当前值", "来源", "是否确认", "备注"],
        "steps": ["确认最终箱数。", "确认最终外箱尺寸和实重。", "确认渠道分母和进位。", "确认长边和尺寸限制。", "保存报价确认记录。"],
        "mistakes": ["改箱后沿用旧报价。", "只确认总额不确认口径。", "没有记录规则来源。", "仓库、运营、货代三方数据不一致。"],
        "sources": source("dhl_dct", "ems_product", "sf_rate", "amazon_fba_pack"),
    },
]


FEATURED_SLUGS = [
    "volumetric-weight-formula-dhl-ems-sf",
    "divisor-5000-vs-6000",
    "ems-40cm-volume-weight-rule",
    "freight-forwarder-quote-reading",
    "split-cartons-vs-mixed-cartons",
    "quote-audit-before-confirmation",
]


STATIC_PAGES = {
    "about.html": {
        "title": f"关于 - {SITE_NAME}",
        "description": "了解跨境运费避坑工具箱的内容边界、适合人群和信息来源原则。",
        "h1": "关于本站",
        "body": [
            "跨境运费避坑工具箱面向外贸员、跨境电商卖家、独立站卖家和 FBA 新手，帮助用户在发货前整理箱规、实重、体积重、CBM、计费重和渠道规则。本站的目标不是替代承运商报价，而是给运营和仓库之间建立一套可复核的计算口径。",
            "本站内容采用保守表达：DHL、EMS、顺丰等渠道规则均以公开页面为基础，涉及具体产品、地区、目的地、进位方式和附加项时，均提醒用户以官方报价工具、客服或承运商最终确认为准。",
            "第一版不设置交易入口，不承诺固定节省金额，不提供灰色操作建议。所有工具都在浏览器本地运行，不需要注册登录，也不会上传用户录入的箱规和重量数据。",
        ],
    },
    "privacy.html": {
        "title": f"隐私政策 - {SITE_NAME}",
        "description": "说明跨境运费避坑工具箱如何处理本地计算数据、日志、广告和外部链接。",
        "h1": "隐私政策",
        "body": [
            "本站是纯静态页面。计费重计算器在用户浏览器本地运行，录入的 SKU、尺寸、重量和渠道分母不会被本站服务器接收或保存。",
            "站点可能使用 Vercel Web Analytics 和托管平台提供的基础访问日志，用于了解页面访问量、来源页面、设备类型和地区分布，并排查可用性问题。Vercel Web Analytics 不使用 cookie；计算器录入内容不会作为统计数据上传。我们不会要求用户提交账号密码、客户资料、订单明细或承运商合同信息。",
            "如果未来接入广告或统计服务，会在页面中补充对应说明。用户可以了解 Google 广告设置：<a href=\"https://adssettings.google.com/\" rel=\"noopener noreferrer\">Google Ads Settings</a>，也可以参考 <a href=\"https://optout.aboutads.info/\" rel=\"noopener noreferrer\">AboutAds 退订页面</a>。",
            "外部链接用于引用官方规则或资料来源。访问外部网站时，请以对方网站的隐私政策和服务条款为准。",
        ],
        "allow_html": True,
    },
    "contact.html": {
        "title": f"联系 - {SITE_NAME}",
        "description": "联系跨境运费避坑工具箱，反馈体积重、CBM、渠道规则和工具体验问题。",
        "h1": "联系与反馈",
        "body": [
            "如果你发现某个渠道规则引用已经更新，或工具计算口径需要补充，请通过页面底部邮箱反馈。反馈时建议附上公开来源链接、截图日期和适用产品名称。",
            "如果你希望参与烟雾测试，可以说明自己的角色、主要发货渠道、常见货物类型和希望工具优先解决的问题。第一版仅收集需求，不接入交易或账号系统。",
            "联系邮箱：hello@example.com。上线前可替换为你的真实业务邮箱。",
        ],
    },
}


def esc(text: object) -> str:
    return escape(str(text), quote=True)


def site_path(path: str = "") -> str:
    path = path.lstrip("/")
    return f"{SITE_URL}/{path}" if path else SITE_URL


def article_href(article: dict, prefix: str = "") -> str:
    return f"{prefix}articles/{article['slug']}.html"


def sentence_list(items: list[str]) -> str:
    return "\n".join(f"<li>{esc(item)}</li>" for item in items)


def source_list(items: list[tuple[str, str]]) -> str:
    return "\n".join(
        f'<li><a href="{esc(url)}" rel="noopener noreferrer">{esc(title)}</a></li>'
        for title, url in items
    )


def slugify_anchor(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text).strip("-")
    return slug or "section"


def related_for(article: dict) -> list[dict]:
    same_group = [item for item in ARTICLES if item["group"] == article["group"] and item["slug"] != article["slug"]]
    if len(same_group) >= 3:
        return same_group[:3]
    others = [item for item in ARTICLES if item["slug"] != article["slug"] and item not in same_group]
    return (same_group + others)[:3]


def page_head(
    *,
    title: str,
    description: str,
    path: str,
    prefix: str = "",
    image: str | None = None,
    robots: str = "index, follow",
    json_ld: list[dict] | dict | None = None,
) -> str:
    canonical = site_path(path)
    image_url = site_path(image or "assets/images/favicon.png")
    if json_ld is None:
        json_ld = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "description": description,
            "url": canonical,
        }
    data = json.dumps(json_ld, ensure_ascii=False, separators=(",", ":"))
    return f"""<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="{esc(robots)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(image_url)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <link rel="icon" href="{prefix}assets/images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="{prefix}assets/images/apple-touch-icon.png">
  <link rel="stylesheet" href="{prefix}assets/styles.css">
  <script type="application/ld+json">{data}</script>
</head>"""


def layout_start(active: str = "", prefix: str = "") -> str:
    return f"""<body data-active="{esc(active)}">
  <a class="skip-link" href="#main" data-i18n="skip">跳到正文</a>
  <header class="site-header">
    <div class="nav-wrap">
      <a class="brand" href="{prefix}index.html" aria-label="{SITE_NAME}首页" data-i18n-aria="brandAria">
        <span class="brand-mark" aria-hidden="true">CBM</span>
        <span data-i18n="siteName">{SITE_NAME}</span>
      </a>
      <nav class="site-nav" data-site-nav aria-label="主导航" data-i18n-aria="mainNav"></nav>
      <div class="nav-tools">
        <button class="lang-toggle" type="button" data-lang-toggle aria-label="Switch language" aria-pressed="false">
          <span data-lang-current>EN</span>
        </button>
        <button class="theme-toggle" type="button" data-theme-toggle aria-label="切换深浅色" data-i18n-aria="themeToggle">◐</button>
      </div>
    </div>
  </header>
  <main id="main">"""


def layout_end(prefix: str = "") -> str:
    year = "2026"
    return f"""  </main>
  <footer class="site-footer">
    <div class="section-inner footer-grid">
      <div>
        <strong data-i18n="siteName">{SITE_NAME}</strong>
        <p data-i18n="footerDesc">用于发货前复核体积重、CBM、计费重和渠道口径。规则会变化，具体发货请以官方报价和承运商确认为准。</p>
      </div>
      <nav aria-label="页脚导航">
        <a href="{prefix}articles.html" data-i18n="footerArticles">文章索引</a>
        <a href="{prefix}tools.html" data-i18n="footerTools">计算工具</a>
        <a href="{prefix}smoke-test.html" data-i18n="footerSmoke">内测说明</a>
        <a href="{prefix}privacy.html" data-i18n="footerPrivacy">隐私政策</a>
        <a href="{prefix}contact.html" data-i18n="footerContact">联系</a>
      </nav>
      <p class="copyright" data-i18n="copyright">© {year} {SITE_NAME}. 本站不提供承运商报价承诺。</p>
    </div>
  </footer>
  <script>
    window.va = window.va || function () {{ (window.vaq = window.vaq || []).push(arguments); }};
  </script>
  <script defer src="{VERCEL_ANALYTICS_SCRIPT}" data-vercel-analytics></script>
  <script src="{prefix}assets/site.js"></script>
</body>"""


def render_picture(image: dict, prefix: str = "", eager: bool = False) -> str:
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return f"""<picture>
  <source srcset="{prefix}{esc(image['webp'])}" type="image/webp">
  <img src="{prefix}{esc(image['src'])}" alt="{esc(image['alt'])}" width="{image['width']}" height="{image['height']}" loading="{loading}" decoding="async"{priority}>
</picture>"""


def article_card(article: dict, prefix: str = "") -> str:
    group = GROUPS[article["group"]]
    return f"""<article class="article-card {group['accent']}" data-card-group="{article['group']}">
  <span class="eyebrow">{esc(group['short'])}</span>
  <h3>{esc(article['title'])}</h3>
  <p>{esc(article['description'])}</p>
  <div class="card-meta">
    <span>{esc(article['tag'])}</span>
    <span>{TODAY}</span>
  </div>
  <a class="card-link" href="{article_href(article, prefix)}">阅读文章</a>
</article>"""


def quick_answer(article: dict) -> str:
    return (
        f"{article['keyword']}的复核要先回到外箱尺寸和实重。"
        f"{article['method'].split('。')[0]}。"
        "工具计算只能帮助发现差异，最终发货仍应以官方报价工具、承运商或客服确认为准。"
    )


def render_table(headers: list[str], article: dict) -> str:
    cells = "".join(f"<th>{esc(item)}</th>" for item in headers)
    example = "".join("<td>待填写</td>" for _ in headers)
    return f"""<div class="table-scroll">
  <table>
    <thead><tr>{cells}</tr></thead>
    <tbody>
      <tr>{example}</tr>
      <tr><td colspan="{len(headers)}">示例：{esc(article['example'])}</td></tr>
    </tbody>
  </table>
</div>"""


def faq_items(article: dict) -> list[tuple[str, str]]:
    group = GROUPS[article["group"]]
    return [
        (
            f"{article['keyword']}可以直接决定选哪个渠道吗？",
            "不建议直接决定。计算结果只能说明体积重、实重和分母带来的差异，还要结合目的地、时效、货物属性、尺寸限制、进位方式和承运商确认口径。",
        ),
        (
            f"如果报价单和我算的{article['keyword']}不一致怎么办？",
            "先核对单位、外箱尺寸、箱数、分母、进位和是否逐箱计算，再把差异整理成问题发给承运商或货代确认。不要只问总额为什么不同。",
        ),
        (
            f"这篇内容适合{group['label']}场景吗？",
            f"适合做发货前复核清单。{article['scenario']}如果你的货物属性、目的地或服务类型不同，应把本文方法当作检查框架，而不是固定结论。",
        ),
    ]


def render_article(article: dict, prev_article: dict | None, next_article: dict | None) -> str:
    group = GROUPS[article["group"]]
    image = IMAGES[group["image"]]
    related = related_for(article)
    h1 = article["title"]
    title = f"{h1} - {SITE_NAME}"
    path = f"articles/{article['slug']}.html"
    article_schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "headline": h1,
                "description": article["description"],
                "datePublished": PUBLISHED_DATE,
                "dateModified": TODAY,
                "author": {"@type": "Organization", "name": SITE_NAME},
                "publisher": {"@type": "Organization", "name": SITE_NAME},
                "mainEntityOfPage": site_path(path),
                "image": site_path(image["src"]),
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "首页", "item": SITE_URL},
                    {"@type": "ListItem", "position": 2, "name": group["label"], "item": site_path(group["page"])},
                    {"@type": "ListItem", "position": 3, "name": h1, "item": site_path(path)},
                ],
            },
        ],
    }
    toc = [
        ("answer", "快速答案"),
        ("why", "为什么要复核"),
        ("method", "核心方法"),
        ("template", "可复制表格"),
        ("checklist", "执行清单"),
        ("mistakes", "常见误区"),
        ("boundary", "规则边界"),
        ("faq", "FAQ"),
        ("sources", "参考来源"),
    ]
    previous_next = []
    if prev_article:
        previous_next.append(f'<a class="button ghost" href="{prev_article["slug"]}.html">上一篇：{esc(prev_article["title"])}</a>')
    if next_article:
        previous_next.append(f'<a class="button ghost" href="{next_article["slug"]}.html">下一篇：{esc(next_article["title"])}</a>')
    faqs = "\n".join(
        f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"
        for q, a in faq_items(article)
    )
    related_html = "\n".join(f'<li><a href="{item["slug"]}.html">{esc(item["title"])}</a></li>' for item in related)
    html = f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=title, description=article['description'], path=path, prefix='../', image=image['src'], json_ld=article_schema)}
{layout_start(active=article['group'], prefix='../')}
    <section class="article-hero">
      <div class="section-inner">
        <nav class="breadcrumb" aria-label="面包屑">
          <a href="../index.html">首页</a><span>/</span><a href="../{group['page']}">{esc(group['label'])}</a><span>/</span><span>{esc(article['tag'])}</span>
        </nav>
        <span class="eyebrow">{esc(group['eyebrow'])}</span>
        <h1>{esc(h1)}</h1>
        <p>{esc(article['description'])}</p>
        <div class="article-meta"><span>{esc(group['label'])}</span><span>更新：{TODAY}</span><span>阅读约 7 分钟</span></div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner article-layout">
        <article class="article-body">
          <figure class="article-image">
            {render_picture(image, prefix='../', eager=True)}
            <figcaption>{esc(image['caption'])}</figcaption>
          </figure>
          <section class="answer-box" id="answer">
            <span class="tag">快速答案</span>
            <p>{esc(quick_answer(article))}</p>
          </section>
          <h2 id="why">为什么要复核</h2>
          <p>{esc(article['scenario'])}</p>
          <p>在跨境发货里，报价差异经常不是单价本身造成的，而是尺寸、重量、分母、进位、服务类型和附加项没有对齐。运营、仓库和货代如果使用不同口径，就会出现看似都正确、实际无法对账的情况。把这些字段先拆开，可以让沟通从“感觉不对”变成“哪一列需要确认”。</p>
          <p>本文采用公开来源和保守口径整理，不把任何渠道规则写成永久不变的结论。DHL、EMS、顺丰等承运商会按照服务、目的地、货物属性和时间调整规则。你可以用本文方法建立内部复核表，但最终发货前仍要回到官方报价工具、客服确认或承运商书面说明。</p>
          <h2 id="method">核心方法</h2>
          <p>{esc(article['method'])}</p>
          <p>{esc(article['example'])}</p>
          <p>实际操作时建议保留三类记录：第一是原始测量数据，包括外箱长宽高、实重、箱数和测量日期；第二是计算数据，包括 CBM、体积重、计费重和分母；第三是确认数据，包括渠道名称、服务类型、进位方式、附加项和确认来源。三类数据分开保存，后续出现差异时才能追溯。</p>
          <h2 id="template">可复制表格</h2>
          <p>下面的字段可以复制到表格工具中。录入字段由仓库或运营填写，计算字段用公式生成，确认字段由承运商或货代回复后补充。</p>
          {render_table(article['table'], article)}
          <pre><code>复核问题：{esc(article['keyword'])}
当前货物：请填写 SKU、箱数、外箱尺寸和实重
需要确认：分母、计泡阈值、进位方式、附加项、目的地限制
输出格式：请按箱号列出体积重、计费重、异常提醒和待确认问题</code></pre>
          <h2 id="checklist">执行清单</h2>
          <ol>{sentence_list(article['steps'])}</ol>
          <p>执行清单的重点是让每一步都有可检查的结果。比如“确认箱规”不够具体，应写成“封箱后测量每箱长宽高并拍照”；“问货代”也不够具体，应写成“确认该渠道使用的体积重分母、计费重进位和是否逐箱计算”。</p>
          <h2 id="mistakes">常见误区</h2>
          <ul>{sentence_list(article['mistakes'])}</ul>
          <p>这些误区的共同点，是把物流复核当成一次性心算。更稳的做法是让所有字段进入同一张表，并且标明来源。只要某个字段来自经验、聊天记录或旧报价，就应该标为待确认，而不是直接进入最终方案。</p>
          <h2 id="boundary">规则边界</h2>
          <p>本站不承诺固定节省金额，也不替代承运商报价。体积重、CBM 和计费重只是复核入口，真实发货还会受到目的地、货物属性、包装状态、通关资料、派送方式、旺季安排和承运商更新影响。任何涉及具体金额和服务承诺的决定，都应以官方页面、报价工具或承运商确认为准。</p>
          <h2 id="faq">FAQ</h2>
          <div class="faq-list">{faqs}</div>
          <h2 id="sources">参考来源</h2>
          <ul>{source_list(article['sources'])}</ul>
          <h2 id="related">相关文章</h2>
          <ul>{related_html}</ul>
          <nav class="post-nav" aria-label="上一篇下一篇">{''.join(previous_next)}</nav>
        </article>
        <aside class="sidebar">
          <nav class="toc" aria-label="文章目录">
            <strong>目录</strong>
            {''.join(f'<a href="#{anchor}">{esc(label)}</a>' for anchor, label in toc)}
          </nav>
          <div class="ad-slot" data-ad-slot></div>
        </aside>
      </div>
    </section>
{layout_end(prefix='../')}
</html>"""
    return html


def render_group_page(group_key: str) -> str:
    group = GROUPS[group_key]
    articles = [item for item in ARTICLES if item["group"] == group_key]
    cards = "\n".join(article_card(item) for item in articles)
    filters = "\n".join(f'<a class="chip" href="#{slugify_anchor(name)}">{esc(name)}</a>' for name in group["groups"])
    grouped = []
    for name in group["groups"]:
        subset = [item for item in articles if item["tag"] == name or name in item["title"] or name in item["description"]]
        if not subset:
            subset = articles[:3]
        grouped.append(
            f'<section class="topic-band" id="{slugify_anchor(name)}"><h2>{esc(name)}</h2><div class="article-grid compact">'
            + "\n".join(article_card(item) for item in subset[:4])
            + "</div></section>"
        )
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": group["label"],
        "description": group["lead"],
        "url": site_path(group["page"]),
    }
    return f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=f"{group['label']} - {SITE_NAME}", description=group['lead'], path=group['page'], image=IMAGES[group['image']]['src'], json_ld=schema)}
{layout_start(active=group_key)}
    <section class="page-hero">
      <div class="section-inner hero-grid">
        <div>
          <span class="eyebrow">{esc(group['eyebrow'])}</span>
          <h1>{esc(group['label'])}</h1>
          <p>{esc(group['lead'])}</p>
          <div class="hero-actions">
            <a class="button" href="tools.html">打开计算工具</a>
            <a class="button ghost" href="articles.html?group={group_key}">查看全部文章</a>
          </div>
        </div>
        <figure class="hero-visual">{render_picture(IMAGES[group['image']], eager=True)}<figcaption>{esc(IMAGES[group['image']]['caption'])}</figcaption></figure>
      </div>
    </section>
    <section class="section tight">
      <div class="section-inner">
        <div class="chip-row">{filters}</div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="section-head">
          <span class="eyebrow">Topic Map</span>
          <h2>专题文章</h2>
          <p>按实际发货复核顺序阅读：先算字段，再看渠道，再落到包装和交接。</p>
        </div>
        <div class="article-grid">{cards}</div>
        {''.join(grouped)}
      </div>
    </section>
{layout_end()}
</html>"""


def render_index() -> str:
    cards = "\n".join(
        f"""<article class="card {GROUPS[key]['accent']}">
  <span class="eyebrow">{esc(GROUPS[key]['eyebrow'])}</span>
  <h3>{esc(GROUPS[key]['label'])}</h3>
  <p>{esc(GROUPS[key]['lead'])}</p>
  <a class="card-link" href="{esc(GROUPS[key]['page'])}">进入专题</a>
</article>"""
        for key in GROUP_ORDER
    )
    featured = "\n".join(article_card(next(item for item in ARTICLES if item["slug"] == slug)) for slug in FEATURED_SLUGS)
    latest = "\n".join(article_card(item) for item in ARTICLES[-6:])
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "description": SITE_DESCRIPTION,
        "url": SITE_URL,
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{SITE_URL}/articles.html?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }
    return f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=f"{SITE_NAME} - 体积重 CBM 计费重复核", description=SITE_DESCRIPTION, path="", image="assets/images/articles/logistics-calculator.png", json_ld=schema)}
{layout_start(active='home')}
    <section class="hero">
      <div class="section-inner hero-grid">
        <div class="hero-copy">
          <span class="eyebrow">Cross-border Shipping Calculator</span>
          <h1>发货前先把体积重、CBM 和计费重算清楚</h1>
          <p>面向外贸员、跨境电商卖家、独立站卖家和 FBA 新手。用保守口径复核 DHL、EMS、顺丰和标准空运的分母差异，减少报价沟通中的口径误判。</p>
          <div class="hero-actions">
            <a class="button" href="tools.html">打开多 SKU 计算器</a>
            <a class="button ghost" href="smoke-test.html">查看内测说明</a>
          </div>
          <div class="trust-row" aria-label="站点特点">
            <span>本地计算</span><span>公开来源</span><span>不接交易</span><span>移动端可用</span>
          </div>
        </div>
        <figure class="hero-visual">{render_picture(IMAGES['volume'], eager=True)}<figcaption>{esc(IMAGES['volume']['caption'])}</figcaption></figure>
      </div>
    </section>
    <section class="section tight">
      <div class="section-inner">
        <div class="ad-slot wide" data-ad-slot></div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="section-head">
          <span class="eyebrow">Start Here</span>
          <h2>三条复核路径</h2>
          <p>先建立计算基准，再理解渠道差异，最后回到包装和拆单决策。</p>
        </div>
        <div class="card-grid">{cards}</div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="section-head split">
          <div>
            <span class="eyebrow">Pillar Articles</span>
            <h2>精选支柱文章</h2>
            <p>围绕体积重公式、分母差异、EMS 40cm 规则和报价单复核搭建第一批 SEO 入口。</p>
          </div>
          <a class="button ghost" href="articles.html">全站文章索引</a>
        </div>
        <div class="article-grid">{featured}</div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="section-head">
          <span class="eyebrow">Latest</span>
          <h2>最新更新</h2>
        </div>
        <div class="article-grid compact">{latest}</div>
      </div>
    </section>
{layout_end()}
</html>"""


def render_articles_index() -> str:
    groups = "".join(f'<button class="filter-chip" type="button" data-filter="{key}">{esc(GROUPS[key]["short"])}</button>' for key in GROUP_ORDER)
    cards = "\n".join(article_card(item) for item in ARTICLES)
    schema = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "全站文章索引",
        "description": "跨境物流体积重、CBM、渠道和包装复核文章索引。",
        "url": site_path("articles.html"),
    }
    return f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=f"文章索引 - {SITE_NAME}", description="按专题、标签和关键词筛选跨境运费复核文章。", path="articles.html", json_ld=schema)}
{layout_start(active='articles')}
    <section class="page-hero">
      <div class="section-inner narrow">
        <span class="eyebrow">Article Index</span>
        <h1>全站文章索引</h1>
        <p>从体积重公式、CBM、渠道分母到包装拆单，按长尾问题快速找到对应复核方法。</p>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="filter-panel" data-article-filter>
          <label for="article-search">关键词搜索</label>
          <input id="article-search" type="search" placeholder="输入 DHL、EMS、CBM、拆箱、FBA 等关键词" data-search-input>
          <div class="filter-row" aria-label="专题筛选">
            <button class="filter-chip is-active" type="button" data-filter="all">全部</button>
            {groups}
          </div>
        </div>
        <div class="article-grid" data-article-list>{cards}</div>
        <p class="empty-state" data-empty-state hidden>没有找到匹配文章，请换一个关键词。</p>
      </div>
    </section>
{layout_end()}
</html>"""


def render_tools() -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "多 SKU 体积重与计费重计算器",
        "description": "浏览器本地运行的多 SKU 体积重、CBM、计费重和渠道分母复核工具。",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Any",
        "inLanguage": ["zh-CN", "en"],
        "isAccessibleForFree": True,
        "offers": {
            "@type": "Offer",
            "price": 0,
            "priceCurrency": "USD",
        },
        "featureList": [
            "多 SKU 外箱尺寸和实重录入",
            "DHL 5000、EMS 6000、标准空运 6000 和自定义分母对比",
            "CBM、体积重、计费重和长边复核提示",
            "浏览器本地自动保存和 PDF 报告导出",
            "中文与英文界面切换",
        ],
        "url": site_path("tools.html"),
    }
    return f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=f"多 SKU 体积重计算器 - {SITE_NAME}", description="纯静态多 SKU 体积重、CBM、计费重和渠道分母对比工具。", path="tools.html", image="assets/images/articles/logistics-calculator.png", json_ld=schema)}
{layout_start(active='tools')}
    <section class="page-hero">
      <div class="section-inner hero-grid">
        <div>
          <span class="eyebrow" data-i18n="toolsEyebrow">Calculator</span>
          <h1 data-i18n="toolsH1">多 SKU 体积重 / CBM / 计费重计算器</h1>
          <p data-i18n="toolsLead">录入每类货物的箱数、外箱尺寸和实重，本地计算 DHL 5000、EMS 6000、标准空运 6000 和自定义分母下的计费重，并提示长边复核项。</p>
          <div class="hero-actions">
            <a class="button" href="#calculator" data-i18n="startCalc">开始计算</a>
            <a class="button ghost" href="articles/volumetric-weight-formula-dhl-ems-sf.html" data-i18n="formulaLink">先看公式说明</a>
          </div>
        </div>
        <figure class="hero-visual">{render_picture(IMAGES['volume'], eager=True)}<figcaption data-i18n="visualCaption">{esc(IMAGES['volume']['caption'])}</figcaption></figure>
      </div>
    </section>
    <section class="section" id="calculator">
      <div class="section-inner">
        <div class="tool-shell" data-logistics-calculator>
          <div class="tool-header">
            <div>
              <span class="eyebrow" data-i18n="localTool">Local Tool</span>
              <h2 data-i18n="calcTitle">发货前复核表</h2>
              <p data-i18n="calcLead">数据只在浏览器内计算，并自动保存在当前浏览器本地，不会上传。默认 EMS 长边提醒按超过 40cm 标记，实际规则请以官方报价和收寄确认为准。</p>
            </div>
            <div class="tool-actions">
              <button class="button small" type="button" data-add-row data-i18n="addSku">添加 SKU</button>
              <button class="button ghost small" type="button" data-load-sample data-i18n="loadSample">载入示例</button>
              <button class="button ghost small" type="button" data-reset-rows data-i18n="resetRows">清空</button>
              <button class="button accent small" type="button" data-export-report data-i18n="exportPdf">导出 PDF 报告</button>
            </div>
          </div>
          <p class="tool-status" role="status" aria-live="polite" data-save-status></p>
          <p class="tool-status" role="status" aria-live="polite" data-export-status></p>
          <div class="calculator-grid">
            <div class="sku-panel">
              <div class="table-scroll">
                <table class="sku-table">
                  <thead>
                    <tr>
                      <th data-i18n="thSku">SKU / 箱型</th>
                      <th data-i18n="thQty">箱数</th>
                      <th data-i18n="thLength">长 cm</th>
                      <th data-i18n="thWidth">宽 cm</th>
                      <th data-i18n="thHeight">高 cm</th>
                      <th data-i18n="thWeight">单箱实重 kg</th>
                      <th data-i18n="thAction">操作</th>
                    </tr>
                  </thead>
                  <tbody data-sku-rows></tbody>
                </table>
              </div>
              <label class="custom-divisor" for="custom-divisor"><span data-i18n="customDivisor">自定义分母</span>
                <input id="custom-divisor" type="number" min="1000" step="100" value="6000" data-custom-divisor>
              </label>
            </div>
            <aside class="result-panel" aria-live="polite">
              <div class="metric-grid">
                <div><span data-i18n="metricActual">总实重</span><strong data-total-actual>0 kg</strong></div>
                <div><span data-i18n="metricCbm">总 CBM</span><strong data-total-cbm>0</strong></div>
                <div><span data-i18n="metricLongSide">最长边提醒</span><strong data-long-side>待录入</strong></div>
              </div>
              <div class="table-scroll">
                <table class="result-table">
                  <thead><tr><th data-i18n="channel">渠道</th><th data-i18n="divisor">分母</th><th data-i18n="volumeWeight">体积重</th><th data-i18n="chargeableWeight">计费重</th></tr></thead>
                  <tbody data-channel-results></tbody>
                </table>
              </div>
              <div class="notice-box" data-suggestion>录入箱规后显示复核提示。</div>
            </aside>
          </div>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="section-head">
          <span class="eyebrow" data-i18n="howToRead">How to Read</span>
          <h2 data-i18n="readTitle">工具输出怎么看</h2>
        </div>
        <div class="card-grid">
          <article class="card"><h3 data-i18n="readCard1Title">计费重不是最终报价</h3><p data-i18n="readCard1Text">它只是报价复核入口。还要确认进位、附加项、目的地限制和服务类型。</p></article>
          <article class="card"><h3 data-i18n="readCard2Title">长边提醒不是拦截规则</h3><p data-i18n="readCard2Text">默认按 EMS 超过 40cm 口径提醒，目的是提示你回到官方页面或客服确认。</p></article>
          <article class="card"><h3 data-i18n="readCard3Title">拆分建议只做复核</h3><p data-i18n="readCard3Text">工具只提示可能需要复核，不承诺某个方案一定更优。</p></article>
        </div>
      </div>
    </section>
{layout_end()}
</html>"""


def render_smoke_test() -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "跨境运费复核工具内测说明",
        "description": "用于承接外贸和跨境电商用户反馈的烟雾测试落地页。",
        "url": site_path("smoke-test.html"),
    }
    return f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=f"内测说明 - {SITE_NAME}", description="跨境运费复核工具烟雾测试页，说明适合人群、工具能力和反馈方式。", path="smoke-test.html", image="assets/images/articles/channel-routes.png", json_ld=schema)}
{layout_start(active='smoke')}
    <section class="hero smoke-hero">
      <div class="section-inner hero-grid">
        <div>
          <span class="eyebrow">Smoke Test</span>
          <h1>你是否也在发货前反复核对体积重和渠道分母？</h1>
          <p>这个页面用于验证跨境卖家是否真的需要一个轻量的 CBM 与计费重复核工具。当前版本免费内测，不接交易，只收集使用反馈。</p>
          <div class="hero-actions">
            <a class="button" href="tools.html">先试用计算器</a>
            <a class="button ghost" href="contact.html">提交内测反馈</a>
          </div>
        </div>
        <figure class="hero-visual">{render_picture(IMAGES['channels'], eager=True)}<figcaption>{esc(IMAGES['channels']['caption'])}</figcaption></figure>
      </div>
    </section>
    <section class="section">
      <div class="section-inner">
        <div class="card-grid">
          <article class="card"><span class="eyebrow">适合人群</span><h3>外贸员和跨境卖家</h3><p>需要在发货前把箱规、实重、CBM 和渠道分母整理清楚，避免报价沟通反复。</p></article>
          <article class="card"><span class="eyebrow">当前能力</span><h3>多 SKU 计费重复核</h3><p>支持 DHL 5000、EMS 6000、标准空运 6000 和自定义分母，自动汇总计费重和长边提醒。</p></article>
          <article class="card"><span class="eyebrow">反馈重点</span><h3>规则和流程是否贴近实际</h3><p>欢迎反馈你常用渠道、货物类型、报价单字段和最容易出错的复核点。</p></article>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="section-inner two-column">
        <div>
          <span class="eyebrow">Example</span>
          <h2>示例计算</h2>
          <p>假设一箱长条货外箱 75cm × 35cm × 28cm，实重 8kg。DHL 5000 口径下体积重为 14.7kg，EMS 6000 口径下体积重为 12.25kg。两个结果都高于实重，因此这票货应该进入体积重复核，而不是只按 8kg 看报价。</p>
          <p>如果你手里有混装货、长条货、轻泡货或 FBA 头程报价单，可以先用工具录入箱规，再把结果和承运商确认口径对照。</p>
        </div>
        <div class="answer-box">
          <span class="tag">内测登记占位</span>
          <h3>目前先用反馈页收集需求</h3>
          <p>正式表单上线前，可以通过联系页提交你的常见货物类型、渠道、箱数范围和最想自动化复核的字段。</p>
          <a class="button" href="contact.html">去反馈</a>
        </div>
      </div>
    </section>
{layout_end()}
</html>"""


def render_static_page(path: str, meta: dict) -> str:
    body_parts = []
    for paragraph in meta["body"]:
        if meta.get("allow_html"):
            body_parts.append(f"<p>{paragraph}</p>")
        else:
            body_parts.append(f"<p>{esc(paragraph)}</p>")
    return f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=meta['title'], description=meta['description'], path=path)}
{layout_start(active=path.removesuffix('.html'))}
    <section class="page-hero">
      <div class="section-inner narrow">
        <span class="eyebrow">Site Info</span>
        <h1>{esc(meta['h1'])}</h1>
      </div>
    </section>
    <section class="section">
      <div class="section-inner narrow prose-card">
        {''.join(body_parts)}
      </div>
    </section>
{layout_end()}
</html>"""


def render_404() -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
{page_head(title=f"页面未找到 - {SITE_NAME}", description="页面未找到，请返回首页或文章索引。", path="404.html", robots="noindex, follow")}
{layout_start(active='404')}
    <section class="page-hero">
      <div class="section-inner narrow">
        <span class="eyebrow">404</span>
        <h1>页面未找到</h1>
        <p>可能是旧链接已经被移除。你可以返回首页、文章索引或直接打开计算工具。</p>
        <div class="hero-actions">
          <a class="button" href="index.html">返回首页</a>
          <a class="button ghost" href="articles.html">文章索引</a>
        </div>
      </div>
    </section>
{layout_end()}
</html>"""


def render_search_index() -> str:
    items = [
        {
            "title": item["title"],
            "description": item["description"],
            "group": item["group"],
            "groupLabel": GROUPS[item["group"]]["label"],
            "tag": item["tag"],
            "href": f"articles/{item['slug']}.html",
        }
        for item in ARTICLES
    ]
    return json.dumps(items, ensure_ascii=False, indent=2)


def render_site_js() -> str:
    nav_items = [
        {"href": "index.html", "label": "首页", "labelEn": "Home", "key": "home"},
        {"href": "articles.html", "label": "文章", "labelEn": "Articles", "key": "articles"},
        {"href": GROUPS["volume"]["page"], "label": "体积重", "labelEn": "Volumetric", "key": "volume"},
        {"href": GROUPS["channels"]["page"], "label": "渠道", "labelEn": "Channels", "key": "channels"},
        {"href": GROUPS["packing"]["page"], "label": "包装", "labelEn": "Packing", "key": "packing"},
        {"href": "tools.html", "label": "工具", "labelEn": "Tools", "key": "tools"},
        {"href": "smoke-test.html", "label": "内测", "labelEn": "Beta", "key": "smoke"},
    ]
    return f"""(() => {{
  const site = {{
    name: {json.dumps(SITE_NAME, ensure_ascii=False)},
    description: {json.dumps(SITE_DESCRIPTION, ensure_ascii=False)},
    nav: {json.dumps(nav_items, ensure_ascii=False)}
  }};

  const JSPDF_SRC = 'https://cdn.jsdelivr.net/npm/jspdf@4.2.1/dist/jspdf.umd.min.js';

  const i18n = {{
    zh: {{
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
      divisorWarning: 'DHL 5000 与标准空运 6000 的整票计费重差异约 {{diff}} kg，建议不要只比较每千克单价。',
      emsPieceWarning: 'EMS 逐箱长边复核与标准空运整票 6000 模拟差异约 {{diff}} kg，建议把长边箱单独发给承运商确认。',
      emsNoDimWarning: 'EMS 未触发长边计泡时可能按实重模拟，与标准空运整票 6000 差异约 {{diff}} kg，建议确认对应产品和目的地口径。',
      densityWarning: '当前密度约 {{density}} kg/CBM，偏轻泡，建议重点复核体积重。',
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
    }},
    en: {{
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
      divisorWarning: 'The shipment-level DHL 5000 vs standard air 6000 chargeable-weight difference is about {{diff}} kg. Do not compare only the per-kg rate.',
      emsPieceWarning: 'The EMS piece-level long-side review vs standard air shipment-level 6000 simulation differs by about {{diff}} kg. Send long-side cartons to the carrier for confirmation.',
      emsNoDimWarning: 'When EMS long-side volumetric review is not triggered, EMS may simulate on actual weight. The difference from standard air shipment-level 6000 is about {{diff}} kg; confirm product and destination rules.',
      densityWarning: 'Current density is about {{density}} kg/CBM, which looks light and bulky. Prioritize volumetric-weight review.',
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
    }}
  }};

  function resolvePrefix() {{
    return location.pathname.includes('/articles/') ? '../' : '';
  }}

  function storageGet(key) {{
    try {{
      return window.localStorage.getItem(key);
    }} catch (error) {{
      return null;
    }}
  }}

  function storageSet(key, value) {{
    try {{
      window.localStorage.setItem(key, value);
      return true;
    }} catch (error) {{
      return false;
    }}
  }}

  function storageRemove(key) {{
    try {{
      window.localStorage.removeItem(key);
      return true;
    }} catch (error) {{
      return false;
    }}
  }}

  function currentLang() {{
    return storageGet('shipping-lang') === 'en' ? 'en' : 'zh';
  }}

  function t(key) {{
    const lang = currentLang();
    return (i18n[lang] && i18n[lang][key]) || i18n.zh[key] || key;
  }}

  function initNav() {{
    const prefix = resolvePrefix();
    const active = document.body.dataset.active || '';
    const lang = currentLang();
    document.querySelectorAll('[data-site-nav]').forEach((nav) => {{
      nav.innerHTML = site.nav.map((item) => {{
        const cls = active === item.key ? ' class="is-active"' : '';
        const label = lang === 'en' ? item.labelEn : item.label;
        return `<a${{cls}} href="${{prefix}}${{item.href}}">${{label}}</a>`;
      }}).join('');
    }});
  }}

  function applyLanguage() {{
    const lang = currentLang();
    document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
    document.querySelectorAll('[data-i18n]').forEach((node) => {{
      node.textContent = t(node.dataset.i18n);
    }});
    document.querySelectorAll('[data-i18n-aria]').forEach((node) => {{
      node.setAttribute('aria-label', t(node.dataset.i18nAria));
    }});
    document.querySelectorAll('[data-i18n-placeholder]').forEach((node) => {{
      node.setAttribute('placeholder', t(node.dataset.i18nPlaceholder));
    }});
    document.querySelectorAll('[data-lang-toggle]').forEach((button) => {{
      button.setAttribute('aria-pressed', String(lang === 'en'));
    }});
    document.querySelectorAll('[data-lang-current]').forEach((node) => {{
      node.textContent = t('langButton');
    }});
    initNav();
    document.dispatchEvent(new CustomEvent('shipping:languagechange', {{ detail: {{ lang }} }}));
  }}

  function initLanguage() {{
    document.querySelectorAll('[data-lang-toggle]').forEach((button) => {{
      button.addEventListener('click', () => {{
        storageSet('shipping-lang', currentLang() === 'en' ? 'zh' : 'en');
        applyLanguage();
      }});
    }});
    applyLanguage();
  }}

  function initTheme() {{
    const root = document.documentElement;
    const saved = storageGet('shipping-theme');
    if (saved === 'dark') root.classList.add('dark-theme');
    if (saved === 'light') root.classList.add('light-theme');
    document.querySelectorAll('[data-theme-toggle]').forEach((button) => {{
      button.addEventListener('click', () => {{
        const isDark = root.classList.toggle('dark-theme');
        root.classList.remove('light-theme');
        storageSet('shipping-theme', isDark ? 'dark' : 'light');
      }});
    }});
  }}

  function initAdSlots() {{
    document.querySelectorAll('[data-ad-slot]').forEach((slot) => {{
      slot.innerHTML = '<strong>赞助内容区域</strong><span>预留给合规广告或渠道服务说明。当前不加载第三方广告脚本。</span>';
    }});
  }}

  function initArticleFilter() {{
    const root = document.querySelector('[data-article-filter]');
    const list = document.querySelector('[data-article-list]');
    if (!root || !list) return;
    const input = root.querySelector('[data-search-input]');
    const chips = Array.from(root.querySelectorAll('[data-filter]'));
    const cards = Array.from(list.querySelectorAll('[data-card-group]'));
    const empty = document.querySelector('[data-empty-state]');
    const params = new URLSearchParams(location.search);
    let activeGroup = params.get('group') || 'all';
    const initialQuery = params.get('q') || '';
    if (initialQuery) input.value = initialQuery;

    function apply() {{
      const q = (input.value || '').trim().toLowerCase();
      let visible = 0;
      chips.forEach((chip) => chip.classList.toggle('is-active', chip.dataset.filter === activeGroup));
      cards.forEach((card) => {{
        const groupOk = activeGroup === 'all' || card.dataset.cardGroup === activeGroup;
        const textOk = !q || card.textContent.toLowerCase().includes(q);
        const show = groupOk && textOk;
        card.hidden = !show;
        if (show) visible += 1;
      }});
      if (empty) empty.hidden = visible !== 0;
    }}

    chips.forEach((chip) => chip.addEventListener('click', () => {{
      activeGroup = chip.dataset.filter || 'all';
      apply();
    }}));
    input.addEventListener('input', apply);
    apply();
  }}

  function initCopyButtons() {{
    document.querySelectorAll('pre').forEach((pre) => {{
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
      button.addEventListener('click', async () => {{
        const text = pre.textContent || '';
        try {{
          await navigator.clipboard.writeText(text);
          button.textContent = '已复制';
          button.classList.add('copied');
          setTimeout(() => {{
            button.textContent = '复制';
            button.classList.remove('copied');
          }}, 1600);
        }} catch (error) {{
          button.textContent = '复制失败';
          setTimeout(() => button.textContent = '复制', 1600);
        }}
      }});
    }});
  }}

  function round(value, digits = 2) {{
    if (!Number.isFinite(value)) return 0;
    const factor = Math.pow(10, digits);
    return Math.round(value * factor) / factor;
  }}

  function initCalculator() {{
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
      {{ key: 'dhlChannel', divisor: 5000, mode: 'shipment' }},
      {{ key: 'emsChannel', divisor: 6000, mode: 'ems-piece' }},
      {{ key: 'airChannel', divisor: 6000, mode: 'shipment' }},
      {{ key: 'customChannel', divisor: 'custom', mode: 'shipment' }}
    ];

    function setSaveStatus(key, delay = 2200) {{
      if (!saveStatus) return;
      saveStatus.textContent = key ? t(key) : '';
      if (key && delay) {{
        window.clearTimeout(saveStatus.dataset.timer || 0);
        const timer = window.setTimeout(() => {{
          if (saveStatus.textContent === t(key)) saveStatus.textContent = '';
        }}, delay);
        saveStatus.dataset.timer = String(timer);
      }}
    }}

    function getRawRows() {{
      return Array.from(rowsBody.querySelectorAll('tr')).map((tr) => {{
        const value = (field) => {{
          const node = tr.querySelector(`[data-field="${{field}}"]`);
          return node ? String(node.value || '').trim() : '';
        }};
        return {{
          name: value('name').slice(0, 120),
          qty: value('qty'),
          l: value('l'),
          w: value('w'),
          h: value('h'),
          kg: value('kg')
        }};
      }}).filter((row) => Object.values(row).some(Boolean));
    }}

    function sanitizeStoredRows(rows) {{
      if (!Array.isArray(rows)) return [];
      return rows.slice(0, 300).map((row) => {{
        const safe = row && typeof row === 'object' ? row : {{}};
        return {{
          name: String(safe.name || '').slice(0, 120),
          qty: String(safe.qty || ''),
          l: String(safe.l || ''),
          w: String(safe.w || ''),
          h: String(safe.h || ''),
          kg: String(safe.kg || '')
        }};
      }}).filter((row) => Object.values(row).some(Boolean));
    }}

    function readSavedState() {{
      const raw = storageGet(storageKey);
      if (!raw) return null;
      try {{
        const parsed = JSON.parse(raw);
        if (!parsed || parsed.version !== 1) throw new Error('Unsupported calculator state');
        const rows = sanitizeStoredRows(parsed.rows);
        const custom = Math.max(1000, Number(parsed.customDivisor) || 6000);
        return {{ rows, customDivisor: String(custom) }};
      }} catch (error) {{
        storageRemove(storageKey);
        return null;
      }}
    }}

    function saveStateNow(statusKey = 'saveReady') {{
      if (!restoreReady) return;
      const payload = {{
        version: 1,
        savedAt: new Date().toISOString(),
        customDivisor: String(customDivisor.value || '6000'),
        rows: getRawRows()
      }};
      if (storageSet(storageKey, JSON.stringify(payload))) {{
        setSaveStatus(statusKey);
      }} else {{
        setSaveStatus('saveUnavailable', 3600);
      }}
    }}

    function scheduleSave() {{
      if (!restoreReady) return;
      window.clearTimeout(saveTimer);
      saveTimer = window.setTimeout(() => saveStateNow(), 350);
    }}

    function clearSavedState() {{
      window.clearTimeout(saveTimer);
      storageRemove(storageKey);
      setSaveStatus('saveCleared');
    }}

    function rowTemplate(data = {{}}) {{
      rowId += 1;
      const id = rowId;
      const defaults = Object.assign({{ name: '', qty: 1, l: '', w: '', h: '', kg: '' }}, data);
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td><label class="sr-only" for="sku-name-${{id}}" data-row-label="thSku">${{t('thSku')}}</label><input id="sku-name-${{id}}" type="text" placeholder="${{t('skuPlaceholder')}}" data-field="name"></td>
        <td><label class="sr-only" for="sku-qty-${{id}}" data-row-label="thQty">${{t('thQty')}}</label><input id="sku-qty-${{id}}" type="number" min="1" step="1" data-field="qty"></td>
        <td><label class="sr-only" for="sku-l-${{id}}" data-row-label="thLength">${{t('thLength')}}</label><input id="sku-l-${{id}}" type="number" min="0" step="0.1" data-field="l"></td>
        <td><label class="sr-only" for="sku-w-${{id}}" data-row-label="thWidth">${{t('thWidth')}}</label><input id="sku-w-${{id}}" type="number" min="0" step="0.1" data-field="w"></td>
        <td><label class="sr-only" for="sku-h-${{id}}" data-row-label="thHeight">${{t('thHeight')}}</label><input id="sku-h-${{id}}" type="number" min="0" step="0.1" data-field="h"></td>
        <td><label class="sr-only" for="sku-kg-${{id}}" data-row-label="thWeight">${{t('thWeight')}}</label><input id="sku-kg-${{id}}" type="number" min="0" step="0.01" data-field="kg"></td>
        <td><button class="icon-button" type="button" aria-label="${{t('deleteRow')}}" data-remove-row>${{t('deleteShort')}}</button></td>
      `;
      rowsBody.appendChild(tr);
      ['name', 'qty', 'l', 'w', 'h', 'kg'].forEach((field) => {{
        const input = tr.querySelector(`[data-field="${{field}}"]`);
        if (input) input.value = defaults[field] ?? '';
      }});
      tr.querySelectorAll('input').forEach((input) => input.addEventListener('input', () => {{
        calculate();
        scheduleSave();
      }}));
      tr.querySelector('[data-remove-row]').addEventListener('click', () => {{
        tr.remove();
        if (!rowsBody.children.length) addRow();
        calculate();
        scheduleSave();
      }});
      calculate();
    }}

    function getRows() {{
      return Array.from(rowsBody.querySelectorAll('tr')).map((tr) => {{
        const value = (field) => {{
          const node = tr.querySelector(`[data-field="${{field}}"]`);
          return node ? node.value : '';
        }};
        return {{
          name: value('name'),
          qty: Math.max(0, Number(value('qty')) || 0),
          l: Math.max(0, Number(value('l')) || 0),
          w: Math.max(0, Number(value('w')) || 0),
          h: Math.max(0, Number(value('h')) || 0),
          kg: Math.max(0, Number(value('kg')) || 0)
        }};
      }}).filter((row) => row.qty && row.l && row.w && row.h);
    }}

    function shipmentCalc(rows, actual, divisor) {{
      const volume = rows.reduce((sum, row) => {{
        return sum + (row.l * row.w * row.h / divisor) * row.qty;
      }}, 0);
      return {{ volume: round(volume), chargeable: round(Math.max(actual, volume)) }};
    }}

    function emsPieceCalc(rows) {{
      let volume = 0;
      let chargeable = 0;
      rows.forEach((row) => {{
        const volumePer = row.l * row.w * row.h / 6000;
        const actualPer = row.kg || 0;
        const hasLongSide = row.l > 40 || row.w > 40 || row.h > 40;
        volume += volumePer * row.qty;
        chargeable += (hasLongSide ? Math.max(volumePer, actualPer) : actualPer) * row.qty;
      }});
      return {{ volume: round(volume), chargeable: round(chargeable) }};
    }}

    function calcChannel(rows, actual, channel, customDivisorValue) {{
      const divisor = channel.divisor === 'custom' ? customDivisorValue : channel.divisor;
      const result = channel.mode === 'ems-piece'
        ? emsPieceCalc(rows)
        : shipmentCalc(rows, actual, divisor);
      return {{
        key: channel.key,
        name: t(channel.key),
        divisor,
        volume: result.volume,
        chargeable: result.chargeable
      }};
    }}

    function translateRows() {{
      rowsBody.querySelectorAll('[data-row-label]').forEach((label) => {{
        label.textContent = t(label.dataset.rowLabel);
      }});
      rowsBody.querySelectorAll('[data-field="name"]').forEach((input) => {{
        input.setAttribute('placeholder', t('skuPlaceholder'));
      }});
      rowsBody.querySelectorAll('[data-remove-row]').forEach((button) => {{
        button.textContent = t('deleteShort');
        button.setAttribute('aria-label', t('deleteRow'));
      }});
    }}

    function calculate() {{
      const rows = getRows();
      const actual = rows.reduce((sum, row) => sum + row.kg * row.qty, 0);
      const cbm = rows.reduce((sum, row) => sum + (row.l * row.w * row.h / 1000000) * row.qty, 0);
      const longest = rows.reduce((max, row) => Math.max(max, row.l, row.w, row.h), 0);
      totalActual.textContent = `${{round(actual)}} kg`;
      totalCbm.textContent = `${{round(cbm, 4)}} CBM`;
      longSide.textContent = longest ? `${{round(longest, 1)}} cm${{longest > 40 ? t('needReview') : ''}}` : t('pending');

      const custom = Math.max(1000, Number(customDivisor.value) || 6000);
      const channelData = channels.map((channel) => calcChannel(rows, actual, channel, custom));
      channelResults.innerHTML = channelData.map((item) => {{
        return `<tr><td>${{item.name}}</td><td>${{item.divisor}}</td><td>${{item.volume}} kg</td><td><strong>${{item.chargeable}} kg</strong></td></tr>`;
      }}).join('');

      if (!rows.length) {{
        suggestion.textContent = t('emptySuggestion');
        lastReport = {{ rows, actual, cbm, longest, channelData, warnings: [] }};
        return;
      }}
      const dhl = channelData.find((item) => item.key === 'dhlChannel')?.chargeable || 0;
      const ems = channelData.find((item) => item.key === 'emsChannel')?.chargeable || 0;
      const air = channelData.find((item) => item.key === 'airChannel')?.chargeable || 0;
      const divisorDiff = round(Math.abs(dhl - air));
      const emsDiff = round(Math.abs(ems - air));
      const warnings = [];
      if (longest > 40) warnings.push(t('longSideWarning'));
      if (divisorDiff > 0) warnings.push(t('divisorWarning').replace('{{diff}}', divisorDiff));
      if (emsDiff > 0) warnings.push(t(longest > 40 ? 'emsPieceWarning' : 'emsNoDimWarning').replace('{{diff}}', emsDiff));
      const density = cbm ? actual / cbm : 0;
      if (density && density < 120) warnings.push(t('densityWarning').replace('{{density}}', round(density)));
      if (!warnings.length) warnings.push(t('normalWarning'));
      suggestion.textContent = warnings.join(' ');
      lastReport = {{ rows, actual: round(actual), cbm: round(cbm, 4), longest: round(longest, 1), channelData, warnings }};
    }}

    function loadJsPdf() {{
      if (window.jspdf && window.jspdf.jsPDF) return Promise.resolve(window.jspdf.jsPDF);
      return new Promise((resolve, reject) => {{
        const existing = document.querySelector('script[data-jspdf]');
        if (existing) {{
          existing.addEventListener('load', () => resolve(window.jspdf.jsPDF), {{ once: true }});
          existing.addEventListener('error', reject, {{ once: true }});
          return;
        }}
        const script = document.createElement('script');
        script.src = JSPDF_SRC;
        script.async = true;
        script.defer = true;
        script.dataset.jspdf = 'true';
        script.onload = () => resolve(window.jspdf.jsPDF);
        script.onerror = reject;
        document.head.appendChild(script);
      }});
    }}

    function wrapText(ctx, text, x, y, maxWidth, lineHeight) {{
      const chars = Array.from(String(text || ''));
      let line = '';
      let cursorY = y;
      chars.forEach((char) => {{
        const test = line + char;
        if (ctx.measureText(test).width > maxWidth && line) {{
          ctx.fillText(line, x, cursorY);
          line = char.trimStart();
          cursorY += lineHeight;
        }} else {{
          line = test;
        }}
      }});
      if (line) ctx.fillText(line, x, cursorY);
      return cursorY + lineHeight;
    }}

    function drawTable(ctx, title, headers, rows, x, y, widths) {{
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
      headers.forEach((header, index) => {{
        ctx.strokeRect(cursorX, y, widths[index], rowHeight);
        ctx.fillText(header, cursorX + 12, y + 27);
        cursorX += widths[index];
      }});
      y += rowHeight;
      ctx.font = '18px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      rows.forEach((row, rowIndex) => {{
        cursorX = x;
        ctx.fillStyle = rowIndex % 2 ? '#fbfcfd' : '#ffffff';
        ctx.fillRect(x, y, widths.reduce((sum, width) => sum + width, 0), rowHeight);
        ctx.fillStyle = '#20252b';
        row.forEach((cell, index) => {{
          ctx.strokeRect(cursorX, y, widths[index], rowHeight);
          ctx.fillText(String(cell), cursorX + 12, y + 27);
          cursorX += widths[index];
        }});
        y += rowHeight;
      }});
      return y + 34;
    }}

    function createReportCanvas(report) {{
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
      (report.warnings.length ? report.warnings : [t('normalWarning')]).forEach((note) => {{
        y = wrapText(ctx, '• ' + note, 124, y, 920, 30);
      }});
      y += 18;
      ctx.fillStyle = '#5f6874';
      ctx.font = '18px Microsoft YaHei, Noto Sans SC, Arial, sans-serif';
      wrapText(ctx, t('reportDisclaimer'), 104, y, 930, 26);
      return canvas;
    }}

    function addCanvasToPdf(jsPDF, canvas) {{
      const doc = new jsPDF({{ orientation: 'p', unit: 'mm', format: 'a4', compress: true }});
      const margin = 10;
      const pageWidth = 210;
      const pageHeight = 297;
      const contentWidth = pageWidth - margin * 2;
      const pxPerMm = canvas.width / contentWidth;
      const sliceHeight = Math.floor((pageHeight - margin * 2) * pxPerMm);
      let offset = 0;
      let page = 0;
      while (offset < canvas.height) {{
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
      }}
      return doc;
    }}

    async function exportPdfReport() {{
      calculate();
      if (!lastReport || !lastReport.rows.length) {{
        exportStatus.textContent = t('exportEmpty');
        return;
      }}
      exportButton.disabled = true;
      exportStatus.textContent = t('exportLoading');
      try {{
        const jsPDF = await loadJsPdf();
        const canvas = createReportCanvas(lastReport);
        const doc = addCanvasToPdf(jsPDF, canvas);
        const stamp = new Date().toISOString().slice(0, 10);
        doc.save('chargeable-weight-report-' + stamp + '.pdf');
        exportStatus.textContent = t('exportReady');
      }} catch (error) {{
        exportStatus.textContent = t('exportFailed');
      }} finally {{
        exportButton.disabled = false;
      }}
    }}

    function addRow(data) {{
      rowTemplate(data);
    }}

    function restoreSavedState() {{
      const saved = readSavedState();
      if (!saved) return false;
      rowsBody.innerHTML = '';
      rowId = 0;
      customDivisor.value = saved.customDivisor;
      if (saved.rows.length) {{
        saved.rows.forEach((row) => addRow(row));
      }} else {{
        addRow();
      }}
      setSaveStatus('saveRestored', 3000);
      return true;
    }}

    root.querySelector('[data-add-row]').addEventListener('click', () => {{
      addRow();
      calculate();
      scheduleSave();
    }});
    root.querySelector('[data-load-sample]').addEventListener('click', () => {{
      rowsBody.innerHTML = '';
      rowId = 0;
      addRow({{ name: '自拍杆长条箱', qty: 4, l: 75, w: 35, h: 28, kg: 8 }});
      addRow({{ name: '配件重货箱', qty: 3, l: 42, w: 30, h: 24, kg: 14 }});
      calculate();
      saveStateNow();
    }});
    root.querySelector('[data-reset-rows]').addEventListener('click', () => {{
      clearSavedState();
      rowsBody.innerHTML = '';
      rowId = 0;
      customDivisor.value = '6000';
      addRow();
      calculate();
      saveStateNow('saveCleared');
    }});
    customDivisor.addEventListener('input', () => {{
      calculate();
      scheduleSave();
    }});
    exportButton.addEventListener('click', exportPdfReport);
    document.addEventListener('shipping:languagechange', () => {{
      translateRows();
      calculate();
    }});
    const restored = restoreSavedState();
    restoreReady = true;
    if (!restored) {{
      addRow({{ name: '示例轻泡箱', qty: 2, l: 60, w: 45, h: 40, kg: 8 }});
      addRow({{ name: '示例重货箱', qty: 1, l: 38, w: 28, h: 22, kg: 12 }});
    }}
    calculate();
  }}

  initLanguage();
  initTheme();
  initAdSlots();
  initArticleFilter();
  initCopyButtons();
  initCalculator();
}})();
"""


def render_sitemap() -> str:
    pages = ["index.html", "articles.html", "tools.html", "smoke-test.html", *[GROUPS[key]["page"] for key in GROUP_ORDER], *STATIC_PAGES.keys()]
    urls = [site_path(page if page != "index.html" else "") for page in pages]
    urls += [site_path(f"articles/{item['slug']}.html") for item in ARTICLES]
    body = "\n".join(
        f"  <url><loc>{esc(url)}</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>"
        for url in urls
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'


def render_robots() -> str:
    return f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n"


def render_attributions() -> str:
    return """# Image Attributions

Images in this site are generated locally for the static website and stored under `assets/images/articles/`.

- `logistics-calculator.png` / `.webp`: locally generated illustration for volumetric weight and CBM calculation.
- `channel-routes.png` / `.webp`: locally generated illustration for logistics channel comparison.
- `carton-checklist.png` / `.webp`: locally generated illustration for carton measurement and packing checks.

No article image is hotlinked from an external website.
"""


def write_site_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def ensure_visual_assets() -> None:
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return

    ARTICLE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)

    def rounded(draw, box, fill, outline=None, width=1, radius=26):
        draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)

    def save_article_image(name: str, theme: str) -> None:
        img = Image.new("RGB", (1200, 675), "#f6f8fb")
        draw = ImageDraw.Draw(img)
        colors = {
            "volume": ("#19705a", "#285a9b", "#f1c27d"),
            "channels": ("#285a9b", "#19705a", "#d9e6ff"),
            "packing": ("#9a5c09", "#19705a", "#f5dfb8"),
        }[theme]
        for y in range(80, 640, 90):
            draw.line((60, y, 1140, y), fill="#e2e7ef", width=2)
        for x in range(120, 1120, 140):
            draw.line((x, 60, x, 615), fill="#edf1f6", width=2)
        rounded(draw, (110, 130, 420, 500), "#ffffff", "#d6dde8", 3, 36)
        rounded(draw, (150, 180, 380, 250), colors[2], "#d09b4b", 3, 18)
        rounded(draw, (155, 270, 250, 365), "#ffffff", colors[0], 5, 16)
        rounded(draw, (275, 270, 370, 365), "#ffffff", colors[1], 5, 16)
        for i in range(4):
            for j in range(3):
                rounded(draw, (160 + j * 70, 390 + i * 26, 205 + j * 70, 408 + i * 26), "#eaf0f7", None, 1, 8)

        if theme == "channels":
            points = [(560, 190), (760, 290), (1010, 190), (930, 470), (650, 480)]
            for a, b in zip(points, points[1:] + points[:1]):
                draw.line((*a, *b), fill=colors[0], width=8)
            for idx, (x, y) in enumerate(points):
                rounded(draw, (x - 46, y - 34, x + 46, y + 34), "#ffffff", colors[idx % 2], 4, 20)
            draw.polygon([(690, 235), (735, 250), (690, 265)], fill=colors[0])
        elif theme == "packing":
            for x, y, w, h in [(560, 250, 180, 150), (760, 190, 210, 180), (690, 405, 250, 120)]:
                rounded(draw, (x, y, x + w, y + h), "#f8d9a7", "#b98230", 4, 18)
                draw.line((x, y + 42, x + w, y + 42), fill="#b98230", width=4)
            draw.line((555, 565, 1030, 565), fill=colors[0], width=10)
            for x in range(580, 1010, 55):
                draw.line((x, 550, x, 580), fill=colors[0], width=5)
        else:
            rounded(draw, (560, 160, 1030, 485), "#ffffff", "#d6dde8", 4, 32)
            for y in [235, 310, 385]:
                draw.line((610, y, 980, y), fill="#dce3ed", width=5)
            for x in [700, 820, 940]:
                draw.line((x, 190, x, 440), fill="#edf1f6", width=4)
            draw.arc((710, 250, 1010, 550), 200, 338, fill=colors[0], width=16)
            draw.polygon([(1010, 382), (1040, 415), (996, 430)], fill=colors[0])

        draw.text((118, 540), SITE_NAME, fill="#20252b")
        draw.text((118, 570), "CBM / Volumetric Weight / Chargeable Weight", fill="#5f6874")
        png = ARTICLE_IMAGE_DIR / f"{name}.png"
        webp = ARTICLE_IMAGE_DIR / f"{name}.webp"
        img.save(png, "PNG")
        img.save(webp, "WEBP", quality=88)

    save_article_image("logistics-calculator", "volume")
    save_article_image("channel-routes", "channels")
    save_article_image("carton-checklist", "packing")

    icon = Image.new("RGB", (512, 512), "#19705a")
    draw = ImageDraw.Draw(icon)
    rounded(draw, (96, 160, 416, 360), "#ffffff", "#ffffff", 1, 48)
    draw.line((96, 225, 416, 225), fill="#19705a", width=16)
    draw.line((256, 160, 256, 360), fill="#19705a", width=16)
    draw.arc((150, 90, 362, 302), 200, 340, fill="#f1c27d", width=20)
    draw.polygon([(360, 190), (405, 218), (354, 242)], fill="#f1c27d")
    icon.save(IMAGE_DIR / "favicon.png", "PNG")
    icon.resize((180, 180)).save(IMAGE_DIR / "apple-touch-icon.png", "PNG")
    icon.save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (128, 128), (256, 256)])


def clean_old_outputs() -> None:
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    for path in ARTICLES_DIR.glob("*.html"):
        path.unlink()
    for old_page in ["campus.html", "career.html"]:
        target = ROOT / old_page
        if target.exists():
            target.unlink()


def main() -> None:
    ensure_visual_assets()
    clean_old_outputs()
    ordered = ARTICLES
    for index, article in enumerate(ordered):
        prev_article = ordered[index - 1] if index > 0 else None
        next_article = ordered[index + 1] if index < len(ordered) - 1 else None
        write_site_file(ARTICLES_DIR / f"{article['slug']}.html", render_article(article, prev_article, next_article))

    write_site_file(ROOT / "index.html", render_index())
    write_site_file(ROOT / "articles.html", render_articles_index())
    write_site_file(ROOT / "tools.html", render_tools())
    write_site_file(ROOT / "smoke-test.html", render_smoke_test())
    for key in GROUP_ORDER:
        write_site_file(ROOT / GROUPS[key]["page"], render_group_page(key))
    for path, meta in STATIC_PAGES.items():
        write_site_file(ROOT / path, render_static_page(path, meta))
    write_site_file(ROOT / "404.html", render_404())
    write_site_file(ASSETS_DIR / "site.js", render_site_js())
    write_site_file(ASSETS_DIR / "search-index.json", render_search_index())
    write_site_file(ROOT / "sitemap.xml", render_sitemap())
    write_site_file(ROOT / "robots.txt", render_robots())
    write_site_file(IMAGE_DIR / "ATTRIBUTIONS.md", render_attributions())
    print(f"Generated {len(ARTICLES)} logistics articles for {SITE_NAME}.")


if __name__ == "__main__":
    main()
