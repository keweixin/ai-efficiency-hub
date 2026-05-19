from __future__ import annotations

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "articles"
SITE_URL = "https://ai-efficiency-hub.pages.dev"
TODAY = "2026-05-20"

SOURCES = {
    "google_helpful": ("Google Search Central：Creating helpful, reliable, people-first content", "https://developers.google.com/search/docs/fundamentals/creating-helpful-content"),
    "google_ai": ("Google Search Central：Guidance on generative AI content", "https://developers.google.com/search/docs/fundamentals/using-gen-ai-content"),
    "google_image": ("Google Search Central：Image SEO best practices", "https://developers.google.com/search/docs/advanced/guidelines/google-images"),
    "google_spam": ("Google Search Central：Spam policies for Google web search", "https://developers.google.com/search/docs/essentials/spam-policies"),
    "baidu_quality": ("百度搜索资源平台：百度搜索优质内容指南", "https://ziyuan.baidu.com/college/articleinfo?id=2947"),
    "baidu_page": ("百度搜索资源平台：百度搜索页面质量标准", "https://ziyuan.baidu.com/college/articleinfo?id=3436"),
    "cet": ("中国教育考试网：全国大学英语四、六级考试(CET)", "https://cet.neea.edu.cn/"),
    "selenium_waits": ("Selenium Documentation：Waiting Strategies", "https://www.selenium.dev/documentation/webdriver/waits/"),
    "selenium_locators": ("Selenium Documentation：Locating elements", "https://www.selenium.dev/documentation/webdriver/elements/locators/"),
    "pytest_parametrize": ("pytest documentation：Parametrizing tests", "https://docs.pytest.org/en/stable/how-to/parametrize.html"),
    "pytest_fixtures": ("pytest documentation：How to use fixtures", "https://docs.pytest.org/en/stable/how-to/fixtures.html"),
    "owasp_llm": ("OWASP：Top 10 for Large Language Model Applications", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"),
    "owasp_prompt": ("OWASP：Prompt Injection", "https://owasp.org/www-community/attacks/PromptInjection"),
}

IMAGES = {
    "campus": {
        "src": "../assets/images/articles/campus-study.jpg",
        "alt": "学生在笔记本电脑前整理学习资料",
        "caption": "学习类文章配图，图片来源：Unsplash。",
    },
    "career": {
        "src": "../assets/images/articles/career-team.jpg",
        "alt": "团队围绕笔记本电脑讨论项目和求职材料",
        "caption": "求职与项目表达类文章配图，图片来源：Unsplash。",
    },
    "tools": {
        "src": "../assets/images/articles/ai-tools-code.jpg",
        "alt": "笔记本电脑上的代码编辑器和工作台",
        "caption": "AI 工具和提示词类文章配图，图片来源：Unsplash。",
    },
}


def source(*keys: str) -> list[tuple[str, str]]:
    return [SOURCES[k] for k in keys]


ARTICLES = [
    # campus
    {"slug": "cet-14-day-study-plan", "group": "campus", "category": "校园效率", "tag": "四六级", "title": "四六级 14 天备考计划怎么安排", "description": "适合大学生的四六级 14 天备考计划，把词汇、阅读、听力、作文和翻译拆成每天可执行任务。", "keyword": "四六级 14 天备考计划", "problem": "距离考试不远，但复习材料很多，容易今天背单词、明天刷阅读，最后没有形成稳定节奏。", "method": "先做一次真题诊断，把低分模块排出来，再按词汇、阅读、听力、作文翻译四条线轮换训练。每天只设置一个主任务和一个可检查交付物。", "steps": ["第 1 天做完整诊断，记录四项得分和耗时。", "第 2 到 5 天补词汇和阅读定位，复盘同义替换。", "第 6 到 9 天练听力场景词、转折词和答案句。", "第 10 到 13 天集中写作文、翻译并让 AI 做结构检查。", "第 14 天只看错题和自己的句型库。"], "prompt": "你是四六级备考教练。根据我的四项得分和错题类型，为我安排未来 14 天复习表，每天不超过 90 分钟，并写清当天交付物。", "mistakes": ["只收藏资料但不复盘错题。", "把 AI 生成作文整篇背下来。", "每天目标太多，无法检查完成情况。"], "sources": source("cet", "google_helpful", "baidu_quality")},
    {"slug": "cet-writing-template-safe-use", "group": "campus", "category": "校园效率", "tag": "作文", "title": "四六级作文模板怎么用才不生硬", "description": "说明四六级作文模板的安全用法：保留结构、替换主题、准备理由库，不机械背诵整篇范文。", "keyword": "四六级作文模板", "problem": "很多同学找到了模板，却写出来像套话，题目稍微变化就不会改。模板真正有用的部分是结构，不是整篇照抄。", "method": "把模板拆成开头、观点、理由、例子和结尾五个部件。每个部件准备 2 到 3 个稳定句型，再用自己的校园例子填进去。", "steps": ["先判断题目是观点类、问题解决类还是利弊类。", "只保留段落结构，不固定整篇内容。", "每个主题准备两个可替换理由。", "用简单准确的词，少堆复杂从句。", "写完后检查是否回应题目关键词。"], "prompt": "请根据作文题目生成三段式提纲，要求包含两个普通大学生能写出来的理由和一个校园生活例子，不要直接写完整作文。", "mistakes": ["开头万能但后文和题目无关。", "理由过空，只写 important、good、bad。", "让 AI 写得太高级，考试现场无法复现。"], "sources": source("cet", "google_ai", "baidu_page")},
    {"slug": "cet-listening-review-method", "group": "campus", "category": "校园效率", "tag": "听力", "title": "四六级听力错题怎么复盘", "description": "把四六级听力错题复盘拆成场景词、转折词、答案句和下次动作，避免只对答案。", "keyword": "四六级听力错题复盘", "problem": "听力错题如果只看答案，下次依然会被同样的场景词和转折信息卡住。复盘要找到答案出现前后的信号。", "method": "每道错题记录题号、场景、错选原因、原文线索、信号词和下次训练动作。重点不在听懂每个词，而在听懂信息变化。", "steps": ["先标出题目问的是时间、地点、原因还是态度。", "回到原文找答案句前后各一句。", "记录 however、actually、instead 等转折词。", "把场景词放入自己的听力词表。", "第二天跟读答案句并复听同类题。"], "prompt": "请根据这段听力原文和我的错题，指出答案句、干扰信息、关键词和下次听题时应该注意的信号词。", "mistakes": ["听到原词就选，没有等完整句子。", "只写没听懂，不写具体卡点。", "复听时盲目循环，不做句子级跟读。"], "sources": source("cet", "google_helpful", "baidu_quality")},
    {"slug": "cet-reading-question-strategy", "group": "campus", "category": "校园效率", "tag": "阅读", "title": "四六级阅读题定位和排除法", "description": "讲解四六级阅读题如何先看题干、找定位句、识别同义替换，并排除范围扩大和偷换概念。", "keyword": "四六级阅读定位法", "problem": "阅读题不是比谁通读得快，而是比谁能把题干和原文对应起来。很多错题来自只找原词，不找同义表达。", "method": "先看题干圈关键词，再回原文找同义替换。定位后读前后各一句，最后用排除法处理过度绝对、偷换对象和范围扩大。", "steps": ["题干先圈数字、人名、专有名词和限定词。", "不要只找原词，重点找同义表达。", "定位后读前后各一句，确认上下文。", "排除 always、never 等过度绝对选项。", "复盘时写出原文依据，而不是只抄答案。"], "prompt": "请帮我分析这道阅读错题，输出题干关键词、原文定位句、同义替换、干扰项类型和下次解题步骤。", "mistakes": ["先通读全文导致时间不够。", "只看选项熟不熟悉，不回原文。", "推断题凭感觉选，没有写出依据。"], "sources": source("cet", "google_helpful", "baidu_page")},
    {"slug": "cet-translation-common-patterns", "group": "campus", "category": "校园效率", "tag": "翻译", "title": "四六级翻译常见句型和拆句方法", "description": "整理四六级翻译中常见的中文长句拆分方法、传统文化和社会发展类表达。", "keyword": "四六级翻译句型", "problem": "翻译长句最容易逐字硬译，结果主干不清、修饰语堆在一起。正确做法是先找主谓宾，再处理时间、地点、原因和定语。", "method": "把中文句子拆成主干和附加信息。遇到长定语可以拆成两个英文句子，先保证准确，再考虑表达丰富。", "steps": ["先找主语、谓语和宾语。", "把随着、由于、为了等状语单独处理。", "传统文化类词汇建立固定表达表。", "过长中文定语可以拆句。", "翻译后检查时态、单复数和搭配。"], "prompt": "请把这句中文翻译题拆成主干、修饰成分和英文表达建议。不要直接给唯一答案，请说明为什么这样拆。", "mistakes": ["中文顺序照搬到英文。", "为了高级词牺牲准确性。", "忽略名词单复数和动词时态。"], "sources": source("cet", "google_ai", "baidu_quality")},
    {"slug": "final-paper-topic-selection", "group": "campus", "category": "校园效率", "tag": "期末作业", "title": "期末论文选题怎么用 AI 辅助", "description": "说明如何用 AI 辅助期末论文选题：拆老师要求、评估资料可得性、控制题目范围。", "keyword": "期末论文选题 AI", "problem": "期末论文最常见的问题不是不会写，而是题目太大、资料难找、和课程知识点关系弱。AI 可以帮忙发散，但不能替你决定事实依据。", "method": "先把老师要求拆成评分项，再让 AI 给出候选题目。每个题目都要检查资料来源、可写范围、课程关联和风险。", "steps": ["复制老师要求并提取字数、引用和格式要求。", "列出自己熟悉的课程概念。", "让 AI 生成 5 个小题目并说明难度。", "筛掉资料难核验或范围过大的题目。", "把题目改成能回答的研究问题。"], "prompt": "课程名是【】，老师要求是【】，我熟悉的知识点是【】。请生成 5 个适合期末论文的小选题，并说明资料来源、难度和偏题风险。", "mistakes": ["题目大到像毕业论文。", "只看题目新不新，不看资料能不能核验。", "让 AI 直接写全文，忽略课程要求。"], "sources": source("google_ai", "google_helpful", "baidu_quality")},
    {"slug": "final-paper-outline-ai", "group": "campus", "category": "校园效率", "tag": "提纲", "title": "课程论文提纲怎么拆到三级标题", "description": "用 AI 辅助课程论文提纲，按研究问题、章节任务、证据材料拆成三级标题。", "keyword": "课程论文提纲", "problem": "很多课程论文提纲只有背景、现状、问题、对策，看似完整，实际每章不知道写什么。三级标题能把章节任务具体化。", "method": "一级标题回答大问题，二级标题说明分析角度，三级标题放证据、案例或步骤。AI 适合帮你检查标题之间是否重复。", "steps": ["先写一句研究问题。", "把问题拆成背景、分析、建议和结论。", "每个一级标题下写 2 到 3 个二级标题。", "三级标题只放证据、案例或操作步骤。", "检查每章是否回应题目。"], "prompt": "请根据我的论文题目和老师要求，生成三级标题提纲。每个标题后写一句本节要解决的问题，并指出哪些位置需要补资料。", "mistakes": ["一级标题太空，像模板套话。", "二级标题互相重复。", "没有证据位置，导致正文只能堆观点。"], "sources": source("google_helpful", "baidu_page")},
    {"slug": "course-report-source-check", "group": "campus", "category": "校园效率", "tag": "资料核验", "title": "课程作业资料来源怎么核验", "description": "讲解课程作业引用资料如何判断可靠性，区分教材、官网、论文、报告和普通经验文章。", "keyword": "课程作业资料核验", "problem": "AI 可以快速列资料，但也可能给出不存在或不适合引用的来源。课程作业真正需要的是可核验、可追溯、和题目相关的材料。", "method": "把资料分成核心依据和辅助材料。教材、官网、论文适合做核心依据，普通文章适合做现象观察，不能随便当权威结论。", "steps": ["检查来源主体是谁。", "确认发布时间和原文链接。", "判断资料和题目哪一章相关。", "把没有来源的数据标记为待核验。", "引用前回到原文确认上下文。"], "prompt": "请检查这 5 条资料是否适合放进课程作业，按可靠性、适用章节、需要核验的问题和引用风险做表格。", "mistakes": ["把 AI 编出来的参考文献当真。", "只看标题相关，不看正文依据。", "用自媒体观点替代课程概念。"], "sources": source("google_ai", "google_spam", "baidu_quality")},
    {"slug": "ai-homework-integrity", "group": "campus", "category": "校园效率", "tag": "学习边界", "title": "用 AI 做作业怎样避免越界", "description": "说明大学生使用 AI 辅助作业的边界：可以拆题、做提纲、查漏洞，但不能替代个人完成要求。", "keyword": "AI 作业边界", "problem": "AI 能提高效率，也容易让学生跳过思考过程。对课程作业来说，最重要的是让工具辅助学习，而不是替代个人完成要求。", "method": "把 AI 用在理解要求、拆提纲、检查逻辑和改表达。观点、数据、案例选择和最终判断应由自己完成，并保留资料核验过程。", "steps": ["先自己读懂题目和评分标准。", "让 AI 帮你拆任务，不让它直接输出终稿。", "所有事实、引用和案例回到来源核验。", "保留自己的观点和课程概念。", "提交前检查学校和课程规则。"], "prompt": "请帮我检查这份作业提纲是否偏题、是否缺少证据、是否有逻辑跳跃。不要代替我写正文。", "mistakes": ["把生成内容原样提交。", "引用没有核验的资料。", "观点和课程知识点脱节。"], "sources": source("google_ai", "google_helpful", "baidu_page")},
    {"slug": "presentation-defense-prep", "group": "campus", "category": "校园效率", "tag": "答辩", "title": "期末汇报和答辩怎么准备", "description": "整理期末汇报和答辩准备方法：PPT 结构、开场讲稿、老师追问和材料自查。", "keyword": "期末答辩准备", "problem": "很多同学 PPT 做完才发现不会讲。汇报不是把正文搬到幻灯片，而是用有限时间讲清问题、方法、结果和不足。", "method": "先写 60 秒开场，再准备每页 2 到 3 句讲稿。答辩问题按选题、资料、方法、局限和改进来准备。", "steps": ["第一页说明题目、课程和汇报人。", "第二页讲研究背景和问题。", "中间页只放关键证据和结论。", "最后页讲不足和改进方向。", "提前准备 5 个老师可能追问的问题。"], "prompt": "请根据我的课程作业提纲，生成 8 页 PPT 汇报结构和每页 2 句讲稿，并列出 6 个可能被问到的答辩问题。", "mistakes": ["PPT 字太多，像 Word 截图。", "只讲做了什么，不讲为什么。", "没有准备资料来源和局限说明。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "club-event-plan-structure", "group": "campus", "category": "校园效率", "tag": "活动策划", "title": "社团活动策划案基本结构", "description": "社团活动策划案应包含背景、目标、流程、分工、预算、风险和复盘指标。", "keyword": "社团活动策划案结构", "problem": "活动策划案如果只写意义和口号，很难真正执行。审批和落地更关心时间、场地、负责人、预算和风险。", "method": "把策划案写成执行文件：目标可衡量，流程有时间，分工有负责人，预算有说明，风险有预案。", "steps": ["用一句话说明为什么办活动。", "把目标写成报名人数、到场人数和传播结果。", "按时间顺序写活动流程。", "列出每个小组负责人。", "写清设备、人员、场地和安全预案。"], "prompt": "请根据活动主题、人数、预算和场地，生成一份活动策划案框架，必须包含流程表、分工表、预算表、风险预案和复盘指标。", "mistakes": ["目标不可衡量。", "预算只有总价没有明细。", "没有安全负责人和备用流程。"], "sources": source("google_helpful", "baidu_page")},
    {"slug": "campus-singer-event-plan", "group": "campus", "category": "校园效率", "tag": "校园活动", "title": "校园十佳歌手比赛策划思路", "description": "以校园十佳歌手比赛为例，说明活动目标、报名、彩排、决赛流程、宣传和复盘。", "keyword": "校园十佳歌手策划案", "problem": "校园歌手比赛看似简单，实际涉及报名、曲目、伴奏、彩排、评分、现场秩序和后续传播。缺一项就容易现场混乱。", "method": "按 T-14 到 T+3 做排期。前期解决报名和场地，中期解决彩排和物料，活动当天解决流程和秩序，结束后做复盘。", "steps": ["T-14 确认场地、预算和负责人。", "T-10 发布报名通知并收伴奏。", "T-5 做第一次彩排。", "T-1 检查音响、座位和签到表。", "T+1 发布结果和活动图文。"], "prompt": "请为校园十佳歌手比赛生成活动执行排期，包含报名、初选、彩排、决赛、宣传和复盘，每一项写负责人和交付物。", "mistakes": ["只写决赛当天流程。", "没有伴奏格式和备用设备要求。", "活动后不记录数据，下一次无法改进。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "activity-budget-table", "group": "campus", "category": "校园效率", "tag": "预算", "title": "活动预算表怎么做才清楚", "description": "说明校园活动预算表如何列费用项、单价、数量、负责人、用途和备用金。", "keyword": "活动预算表", "problem": "预算表不是写一个总金额就结束。审批人需要知道每笔钱买什么、为什么需要、谁负责、是否有备用方案。", "method": "预算表至少包含费用项、单价、数量、小计、用途、负责人和备注。对于不确定费用，单独列备用金并说明使用条件。", "steps": ["先按宣传、物料、奖品、设备和备用金分类。", "每项写清单价和数量。", "注明采购负责人。", "把可借用资源和必须采购资源分开。", "活动后记录实际支出和差异。"], "prompt": "请根据活动主题、预计人数和预算上限，生成一张活动预算表，包含费用项、单价、数量、小计、用途、负责人和是否可替代。", "mistakes": ["只有总预算，没有明细。", "奖品费用过高，忽略基础物料。", "没有预留突发费用。"], "sources": source("google_helpful", "baidu_page")},
    {"slug": "club-promo-copywriting", "group": "campus", "category": "校园效率", "tag": "宣传文案", "title": "社团活动宣传文案怎么写", "description": "校园活动宣传文案要说明对象、时间、地点、亮点和报名方式，避免只写情绪口号。", "keyword": "社团活动宣传文案", "problem": "很多活动文案很好看，但用户看完不知道谁能参加、什么时候开始、在哪里报名。宣传文案首先要降低行动成本。", "method": "文案分成标题、开头、亮点、信息块和行动提示。标题吸引注意，信息块负责说清时间地点和报名条件。", "steps": ["标题直接点出活动和人群。", "开头用一个真实场景引入。", "亮点控制在 3 条以内。", "时间、地点、报名方式单独成块。", "结尾提醒截止时间和联系人。"], "prompt": "请为这个校园活动写 3 个标题、1 段推文开头和 1 个报名信息块。要求清楚说明时间、地点、对象、亮点和报名方式。", "mistakes": ["只写热血口号，缺少基础信息。", "标题太长，手机端不易读。", "没有报名截止时间。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "student-time-management-ai", "group": "campus", "category": "校园效率", "tag": "时间管理", "title": "大学生怎么用 AI 做时间管理", "description": "讲解大学生如何用 AI 拆分课程、考试、社团和求职任务，形成周计划和复盘表。", "keyword": "大学生 AI 时间管理", "problem": "大学生的时间管理难点不是没有工具，而是课程、考试、社团和求职任务混在一起，优先级经常变化。", "method": "让 AI 帮你把任务拆成必须完成、可以简化、可以延期三类，再给每类设置完成标准。每天只追踪关键交付物。", "steps": ["列出本周所有任务和截止时间。", "标出必须完成的课程和考试任务。", "把大任务拆成 30 到 60 分钟动作。", "每天结束只复盘完成、卡点和明天动作。", "每周删除低价值任务。"], "prompt": "我本周有这些任务和截止时间，请帮我按重要程度和紧急程度排序，并拆成每天可执行计划，每天不超过 3 个核心任务。", "mistakes": ["把计划排满，没有缓冲。", "只记录待办，不写完成标准。", "每天换工具，反而增加负担。"], "sources": source("google_ai", "google_helpful", "baidu_quality")},
    {"slug": "exam-wrong-question-review", "group": "campus", "category": "校园效率", "tag": "错题复盘", "title": "考试错题复盘表怎么做", "description": "适合学生的错题复盘表：记录题型、错因、依据、下次动作，而不是只抄正确答案。", "keyword": "错题复盘表", "problem": "错题本如果只是题目和答案，很快会变成另一本看不完的资料。复盘的重点是找到重复错因。", "method": "每道错题写题型、知识点、错因、正确依据和下次动作。错因要具体到概念不清、审题遗漏、计算失误或时间分配。", "steps": ["当天只复盘最有代表性的错题。", "给错因做固定分类。", "写出正确答案的依据。", "设置下一次训练动作。", "每周统计重复错因。"], "prompt": "请根据我的错题记录，帮我整理错因分类、正确依据和下次训练动作，输出成表格。", "mistakes": ["所有错题都写没掌握。", "复盘耗时超过做题时间。", "没有回看重复错因。"], "sources": source("google_helpful", "baidu_page")},
    {"slug": "undergraduate-project-proposal", "group": "campus", "category": "校园效率", "tag": "项目开题", "title": "本科课程项目开题思路怎么写", "description": "课程项目开题应说明问题、目标、功能范围、技术路线、交付物和风险，不要一开始写大而全。", "keyword": "本科课程项目开题", "problem": "课程项目开题最怕目标过大。一个学期能完成的项目需要范围清楚、交付物明确、技术路线不过度复杂。", "method": "用问题、用户、功能、数据、技术、风险六个维度来写。每个维度都要落到能做出来的内容。", "steps": ["先写项目解决什么小问题。", "定义目标用户和使用场景。", "列出最小功能范围。", "说明数据从哪里来。", "写技术路线和工具。", "列出可能延期的风险。"], "prompt": "请根据我的课程项目想法，帮我写一份开题思路，包含问题背景、目标用户、核心功能、技术路线、交付物和风险控制。", "mistakes": ["功能堆太多，最后都做不深。", "技术路线写流行词，自己解释不了。", "没有风险和最小版本。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "group-assignment-collaboration", "group": "campus", "category": "校园效率", "tag": "小组作业", "title": "小组作业怎么分工和复盘", "description": "小组作业分工要明确交付物、截止时间和检查人，避免最后由一个人补全部内容。", "keyword": "小组作业分工", "problem": "小组作业翻车通常不是没人做，而是任务边界不清、交付格式不同、最后整合时发现内容不匹配。", "method": "把任务拆成资料、提纲、正文、PPT、讲稿和终审，每项指定负责人、截止时间和交付格式。AI 可以帮助统一风格和检查遗漏。", "steps": ["先确定共同题目和评分标准。", "把任务拆成具体交付物。", "约定文件命名和格式。", "设置整合人和终审人。", "结束后复盘延期和返工原因。"], "prompt": "请根据我们的小组作业题目和成员人数，生成分工表，包含任务、负责人、截止时间、交付格式、检查标准和风险。", "mistakes": ["只按章节分工，没有统一观点。", "没有中间检查环节。", "最后一天才整合格式。"], "sources": source("google_helpful", "baidu_page")},
]

ARTICLES += [
    # career
    {"slug": "automation-test-interview-roadmap", "group": "career", "category": "求职冲刺", "tag": "自动化测试", "title": "自动化测试面试准备路线", "description": "自动化测试面试准备路线，覆盖接口、UI、数据库、框架、CI 和项目复盘。", "keyword": "自动化测试面试准备", "problem": "自动化测试面试不能只背零散题目。面试官通常想知道你是否理解测试流程、能否定位失败原因、能否把项目讲清楚。", "method": "按接口、UI、数据、框架、报告和项目六个模块准备，每个模块准备一个真实例子和一个失败排查思路。", "steps": ["先梳理自己做过的项目链路。", "接口部分准备鉴权、参数化和断言。", "UI 部分准备等待、定位器和截图。", "框架部分准备分层和配置。", "项目部分准备背景、行动和结果。"], "prompt": "你是测试经理，请按接口、UI、数据库、框架和项目复盘面试我。一次只问一个问题，等我回答后指出不足并给更好的结构。", "mistakes": ["只背题，不会结合项目。", "把工具名堆满，但解释不了原理。", "结果只写完成了，没有说明价值。"], "sources": source("selenium_waits", "pytest_parametrize", "google_helpful")},
    {"slug": "ui-automation-flaky-answer", "group": "career", "category": "求职冲刺", "tag": "UI 自动化", "title": "UI 自动化不稳定怎么回答", "description": "面试中回答 UI 自动化不稳定问题时，可从定位器、显式等待、截图日志和用例边界展开。", "keyword": "UI 自动化不稳定面试回答", "problem": "UI 自动化不稳定是高频面试题。简单回答加等待不够，因为它没有体现你区分原因和控制误报的能力。", "method": "回答时先说现象，再说排查，再说改进。重点包括稳定定位器、显式等待、失败截图、页面源码、重试边界和不适合自动化的场景。", "steps": ["确认是元素加载、定位器变化还是环境问题。", "把脆弱 XPath 改成稳定属性或文本组合。", "使用显式等待等待关键状态。", "失败时保留截图、日志和页面源码。", "把频繁变化的一次性流程移出自动化范围。"], "prompt": "请帮我把 UI 自动化不稳定的经历改成 STAR 面试回答，要求包含背景、排查动作、改进方案和结果。", "mistakes": ["只说加 sleep。", "没有失败证据。", "把所有流程都自动化，忽视维护成本。"], "sources": source("selenium_waits", "selenium_locators", "google_helpful")},
    {"slug": "api-test-auth-token", "group": "career", "category": "求职冲刺", "tag": "接口测试", "title": "接口自动化 token 和鉴权怎么处理", "description": "接口自动化中 token 和鉴权处理思路：登录前置、会话上下文、角色账号和过期重试。", "keyword": "接口自动化 token 鉴权", "problem": "鉴权处理如果写死 token，用例很快失效，也难以切换环境和角色。面试时要说明如何让登录态可维护。", "method": "把登录接口封装成前置步骤，token 存在会话上下文或统一请求头。不同权限准备不同账号，关键接口验证未授权和权限不足。", "steps": ["封装登录方法，不在用例里写死 token。", "统一请求头和环境配置。", "token 过期时重新登录并记录日志。", "为普通用户、管理员和无权限用户准备账号。", "断言业务码和权限提示。"], "prompt": "请根据我的接口自动化项目，帮我组织 token 和鉴权处理的面试回答，包含为什么不能写死、如何封装、如何覆盖权限场景。", "mistakes": ["把 token 复制到每条用例。", "只测正常登录用户。", "没有覆盖未授权和权限不足。"], "sources": source("pytest_fixtures", "pytest_parametrize", "google_helpful")},
    {"slug": "api-assertion-design", "group": "career", "category": "求职冲刺", "tag": "接口测试", "title": "接口测试断言怎么设计", "description": "接口测试断言不应只看状态码，还应覆盖业务码、字段、错误信息和关键数据结果。", "keyword": "接口测试断言设计", "problem": "接口返回 200 不等于业务正确。断言设计太浅，会让问题漏掉，也会让面试回答显得没有测试思维。", "method": "把断言分成协议层、业务层和数据层。普通接口检查状态码和业务码，关键链路再检查字段、错误提示和数据库结果。", "steps": ["协议层检查状态码和响应时间。", "业务层检查 code、message 和关键字段。", "异常场景检查错误提示是否明确。", "关键链路检查数据是否真正变化。", "失败时输出请求、响应和断言差异。"], "prompt": "请根据这个接口文档，帮我设计正常、异常、边界和鉴权场景的断言点，并说明每个断言能发现什么问题。", "mistakes": ["只断言 200。", "没有异常场景。", "断言字段太多导致维护困难。"], "sources": source("pytest_parametrize", "google_helpful", "baidu_quality")},
    {"slug": "pytest-parametrize-fixture", "group": "career", "category": "求职冲刺", "tag": "pytest", "title": "pytest 参数化和 fixture 怎么讲", "description": "面试中讲 pytest 参数化和 fixture，可围绕减少重复、准备数据、共享前置和提高可维护性展开。", "keyword": "pytest 参数化 fixture", "problem": "很多初学者知道 pytest，但讲不清参数化和 fixture 的区别。面试时要说明它们分别解决什么问题。", "method": "参数化用于同一逻辑跑多组输入，fixture 用于准备前置条件和资源。两者结合可以让用例更短、更稳定。", "steps": ["用 parametrize 管理多组输入和预期结果。", "用 fixture 准备登录、测试数据或客户端。", "把环境配置从用例中抽离。", "失败输出应能看到是哪组参数。", "不要为了封装而隐藏业务意图。"], "prompt": "请帮我用通俗语言解释 pytest 参数化和 fixture 的区别，并给一个接口自动化场景中的面试回答。", "mistakes": ["把所有逻辑都塞进 fixture。", "参数名不清楚，失败时难定位。", "为了少写代码牺牲可读性。"], "sources": source("pytest_parametrize", "pytest_fixtures")},
    {"slug": "selenium-explicit-wait", "group": "career", "category": "求职冲刺", "tag": "Selenium", "title": "Selenium 显式等待怎么理解", "description": "Selenium 显式等待用于等待关键条件出现，比固定 sleep 更可控，适合解释 UI 自动化稳定性。", "keyword": "Selenium 显式等待", "problem": "UI 用例失败经常不是功能错，而是页面状态还没准备好。固定 sleep 会拖慢用例，也不一定稳定。", "method": "显式等待是等待某个条件满足，例如元素可见、可点击、文本出现。回答时要说明等待的是业务关键状态，不是盲目等待时间。", "steps": ["找出用例真正依赖的页面状态。", "等待元素可见或可点击。", "对异步加载结果等待文本或列表变化。", "设置合理超时时间。", "超时后保留截图和日志。"], "prompt": "请帮我把 Selenium 显式等待解释成面试回答，要求对比固定 sleep，并结合一个登录后等待首页元素的例子。", "mistakes": ["所有地方都 sleep 3 秒。", "等待了错误元素。", "没有超时证据。"], "sources": source("selenium_waits", "selenium_locators")},
    {"slug": "test-report-logs-screenshots", "group": "career", "category": "求职冲刺", "tag": "测试报告", "title": "测试报告、日志和截图怎么定位问题", "description": "自动化失败后应通过测试报告、请求响应、日志、截图和环境信息判断问题来源。", "keyword": "测试报告 日志 截图 定位问题", "problem": "测试报告如果只有通过和失败，价值很有限。好的报告应该帮助团队快速判断是脚本问题、数据问题、环境问题还是产品问题。", "method": "报告里保留用例名、步骤、环境、请求参数、响应摘要、错误堆栈和截图。失败后先分类，再决定是否重跑或提缺陷。", "steps": ["先看失败类型和错误信息。", "查看请求参数和响应内容。", "UI 用例查看截图和页面状态。", "检查测试数据是否满足前置条件。", "记录归因，避免同类问题重复出现。"], "prompt": "请根据这段失败日志和截图描述，帮我判断可能原因，并输出环境问题、数据问题、脚本问题、产品问题四类排查清单。", "mistakes": ["失败就重跑，没有归因。", "报告缺少请求和响应。", "截图没有和步骤对应。"], "sources": source("selenium_waits", "pytest_fixtures", "google_helpful")},
    {"slug": "ci-smoke-testing", "group": "career", "category": "求职冲刺", "tag": "CI", "title": "自动化测试接入 CI 先跑哪些用例", "description": "自动化测试接入 CI 应先选择稳定的冒烟用例，覆盖核心链路，避免一开始全量导致误报。", "keyword": "自动化测试 CI 冒烟用例", "problem": "把所有自动化用例一次性接入 CI，容易因为环境和数据不稳定导致大量失败，团队会失去信任。", "method": "先接核心冒烟用例：登录、关键查询、关键提交、权限校验。用例必须稳定、执行快、失败易定位。", "steps": ["筛选业务最关键的 5 到 20 条用例。", "确保测试数据可重复准备。", "失败时输出报告和通知。", "每日定时和提交触发分开。", "稳定后再逐步扩展覆盖范围。"], "prompt": "请根据我的系统模块，帮我筛选适合 CI 冒烟测试的用例，并说明每条用例为什么值得优先执行。", "mistakes": ["一开始全量接入。", "把不稳定 UI 用例放进主流程。", "失败没有通知和报告。"], "sources": source("pytest_fixtures", "google_helpful", "baidu_quality")},
    {"slug": "database-validation-testing", "group": "career", "category": "求职冲刺", "tag": "数据库校验", "title": "接口测试什么时候需要查数据库", "description": "数据库校验适合订单、库存、用户状态等关键链路，不是每条接口都必须查库。", "keyword": "接口测试 数据库校验", "problem": "接口返回成功只能说明响应看起来正常，不一定证明数据真正落库。但每条用例都查数据库也会增加维护成本。", "method": "关键链路查关键字段，普通查询接口以业务字段断言为主。查库前要准备独立数据，查库后要清理或隔离。", "steps": ["判断接口是否改变核心数据。", "明确要校验的字段。", "准备唯一测试数据。", "执行接口后查询数据状态。", "清理数据或使用隔离环境。"], "prompt": "请根据这个业务接口，判断是否需要数据库校验。如果需要，请列出校验字段、查询条件和可能发现的问题。", "mistakes": ["每条接口都查库，拖慢执行。", "查错环境或错数据。", "没有清理测试数据。"], "sources": source("pytest_fixtures", "google_helpful")},
    {"slug": "test-resume-project-description", "group": "career", "category": "求职冲刺", "tag": "简历", "title": "测试岗简历项目经历怎么写", "description": "测试岗简历项目经历要写清模块、测试点、方法、工具、结果和可追问细节。", "keyword": "测试岗简历项目经历", "problem": "简历里只写参与项目、负责测试，很难让招聘方判断你做了什么。测试岗需要体现测试点设计、问题定位和交付物。", "method": "项目经历按背景、任务、动作、结果写。动作要包括用例设计、接口验证、缺陷记录、报告输出和复测。", "steps": ["先写项目是什么和你负责的模块。", "写覆盖哪些核心流程。", "写使用什么方法或工具。", "写输出了哪些交付物。", "准备每条描述的追问答案。"], "prompt": "请把我的测试项目经历改写成 5 条简历 bullet，要求包含动作、对象、方法和结果，不要编造数据。", "mistakes": ["写精通但解释不了。", "只写工具名没有业务对象。", "项目结果无法被追问。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "ai-resume-polish-guide", "group": "career", "category": "求职冲刺", "tag": "AI 简历", "title": "AI 润色简历怎样避免编造经历", "description": "用 AI 润色简历时应提供真实经历和岗位 JD，让 AI 优化表达而不是新增事实。", "keyword": "AI 润色简历", "problem": "AI 改简历容易把经历写得很漂亮，但也可能新增你没有做过的工具、结果和数据。面试时这些内容会变成风险。", "method": "把 JD 和真实经历一起给 AI，要求标注缺失信息。所有新增数据必须用待补充标记，不允许直接生成具体数字。", "steps": ["先整理真实项目和职责。", "粘贴目标岗位 JD。", "让 AI 提取匹配关键词。", "改写时要求不新增事实。", "删除自己解释不了的技术词。"], "prompt": "你是招聘经理。请根据岗位 JD 和我的真实经历，指出匹配点、缺失能力和可优化表达。不要新增经历，缺少数据请标注【需补充】。", "mistakes": ["让 AI 直接生成完整简历。", "保留不懂的技术名词。", "把课程项目写成真实商业项目。"], "sources": source("google_ai", "google_helpful", "baidu_page")},
    {"slug": "fresh-graduate-project-star", "group": "career", "category": "求职冲刺", "tag": "STAR", "title": "应届生项目经历 STAR 表达", "description": "应届生项目经历可以用 STAR 结构讲清背景、任务、行动和结果，但不能夸大项目性质。", "keyword": "应届生项目 STAR", "problem": "应届生项目不一定大，但只要能讲清你解决的问题和具体行动，就能成为面试材料。STAR 的价值是让经历有结构。", "method": "S 是项目背景，T 是你的任务，A 是你做了哪些具体动作，R 是交付物或改进结果。结果可以是报告、脚本、复盘，不一定是夸张数据。", "steps": ["说明项目来源和业务场景。", "明确你负责的模块。", "列出 3 个具体行动。", "说明遇到的难点。", "用交付物证明结果。"], "prompt": "请把我的课程项目整理成 STAR 面试回答，要求真实、不夸大，并列出面试官可能追问的 5 个问题。", "mistakes": ["把团队成果全写成个人成果。", "只讲技术，不讲任务背景。", "结果没有证据。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "no-internship-resume", "group": "career", "category": "求职冲刺", "tag": "简历", "title": "没有实习经历怎么写测试岗简历", "description": "没有实习经历时，可以用课程项目、自学练习、缺陷记录和测试报告证明测试岗能力。", "keyword": "没有实习测试岗简历", "problem": "没有实习不是不能投测试岗，但简历必须提供能力证据。空写学习能力强，很难让招聘方相信。", "method": "把课程项目改成测试视角，把自学练习沉淀成脚本、用例、报告和复盘。重点写能被追问的内容。", "steps": ["列出课程项目和自学项目。", "为每个项目补测试点和用例。", "输出缺陷记录或测试报告。", "准备工具和流程的解释。", "删除和岗位无关的大段内容。"], "prompt": "我没有实习经历，但有这些课程项目和自学练习。请帮我筛选适合测试岗简历的内容，并改写成真实可追问的项目描述。", "mistakes": ["空写熟悉测试流程。", "把没做过的自动化写上去。", "项目描述和岗位无关。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "test-interview-self-introduction", "group": "career", "category": "求职冲刺", "tag": "面试", "title": "测试岗面试自我介绍怎么准备", "description": "测试岗自我介绍应控制在 60 到 90 秒，讲清方向、项目、测试能力和求职动机。", "keyword": "测试岗自我介绍", "problem": "自我介绍不是复述简历，而是给面试官一个追问入口。太长会散，太短又看不出岗位匹配。", "method": "按个人背景、目标岗位、项目经历、测试能力、期待方向五句话组织。每句话都要能接上后续追问。", "steps": ["说明学历或转行背景。", "明确应聘测试或自动化测试。", "挑一个最相关项目。", "讲用例、接口、缺陷或报告能力。", "用一句话说明想继续提升的方向。"], "prompt": "请根据我的简历，生成 60 秒测试岗自我介绍。要求自然、真实、能引导面试官追问项目，不要夸大。", "mistakes": ["背诵过于官方。", "讲兴趣太多，岗位匹配太少。", "没有提可追问项目。"], "sources": source("google_helpful", "baidu_page")},
    {"slug": "bug-report-writing", "group": "career", "category": "求职冲刺", "tag": "缺陷报告", "title": "缺陷报告怎么写清复现步骤", "description": "缺陷报告要包含环境、前置条件、复现步骤、实际结果、预期结果、附件和影响范围。", "keyword": "缺陷报告复现步骤", "problem": "缺陷报告写不清，开发就难复现，沟通成本会很高。好报告不是情绪表达，而是可验证事实。", "method": "报告按环境、版本、账号、前置数据、步骤、实际结果、预期结果、截图日志和影响范围来写。", "steps": ["先确认问题可复现。", "记录浏览器、环境和账号。", "步骤写成一条一条动作。", "实际结果和预期结果分开。", "附截图、日志或接口响应。"], "prompt": "请把我的问题描述改成规范缺陷报告，包含环境、前置条件、复现步骤、实际结果、预期结果和附件说明。", "mistakes": ["只写有 bug。", "步骤跳跃，别人无法复现。", "没有环境和版本信息。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "qa-learning-roadmap", "group": "career", "category": "求职冲刺", "tag": "学习路线", "title": "零基础测试工程师学习路线", "description": "零基础测试工程师可按软件基础、测试方法、接口测试、自动化、数据库和项目表达逐步学习。", "keyword": "测试工程师学习路线", "problem": "零基础学测试容易一上来追工具，结果用例设计和缺陷分析都不稳。学习路线应该先方法，再工具。", "method": "第一阶段学测试基础和用例设计，第二阶段学接口和数据库，第三阶段学自动化和报告，最后整理项目表达。", "steps": ["学习软件测试基本概念。", "练等价类、边界值和场景法。", "学习 HTTP、接口文档和断言。", "掌握 SQL 基础查询。", "用 pytest 或 Selenium 做小项目。"], "prompt": "请为零基础测试求职者制定 8 周学习路线，每周包含学习目标、练习任务、交付物和自测问题。", "mistakes": ["只看视频不做项目。", "跳过用例设计直接写脚本。", "学很多工具但没有面试材料。"], "sources": source("pytest_fixtures", "selenium_waits", "google_helpful")},
    {"slug": "mock-interview-prompt", "group": "career", "category": "求职冲刺", "tag": "模拟面试", "title": "用 AI 做模拟面试怎么提问", "description": "AI 模拟面试应采用一问一答模式，围绕简历项目追问，并在回答后给结构化反馈。", "keyword": "AI 模拟面试 Prompt", "problem": "一次性让 AI 生成面试答案，练不出临场能力。真正有效的是让 AI 像面试官一样追问。", "method": "把简历和目标岗位给 AI，要求一次只问一个问题，回答后指出问题，再给更好的结构。最后输出复盘表。", "steps": ["提供目标岗位和简历项目。", "限定问题范围和难度。", "要求一次只问一个。", "回答后让 AI 追问细节。", "结束后整理高频漏洞。"], "prompt": "你是测试岗位面试官，请根据我的简历进行模拟面试。一次只问一个问题，等我回答后点评，再继续追问。结束后给我复盘表。", "mistakes": ["只看标准答案不练表达。", "没有把自己的项目材料放进去。", "不让 AI 追问细节。"], "sources": source("google_ai", "google_helpful", "baidu_quality")},
]

ARTICLES += [
    # tools
    {"slug": "gpt-claude-beginner-differences", "group": "tools", "category": "AI 工具箱", "tag": "入门", "title": "GPT 和 Claude 新手怎么选", "description": "GPT 和 Claude 新手选择指南，从任务类型、上下文、文件处理、结果核验和使用习惯比较。", "keyword": "GPT Claude 新手怎么选", "problem": "新手常把模型当成万能工具，纠结哪个更强。真正影响结果的是任务类型、上下文质量和核验方法。", "method": "先按任务选择工具：写作、总结、代码、资料分析、头脑风暴和表格处理。再用同一任务测试输出是否稳定。", "steps": ["明确任务是写作、总结还是分析。", "准备完整背景和材料。", "规定输出格式。", "让模型标出不确定信息。", "重要结论回到来源核验。"], "prompt": "我想完成任务【】，材料是【】，请先判断适合用哪类 AI 助手，并给出提问模板、输出格式和核验清单。", "mistakes": ["只问哪个模型最强。", "不给上下文就要求高质量。", "把输出直接当事实。"], "sources": source("google_ai", "google_helpful", "baidu_quality")},
    {"slug": "prompt-four-part-formula", "group": "tools", "category": "AI 工具箱", "tag": "Prompt", "title": "稳定 Prompt 的四段式公式", "description": "稳定 Prompt 通常包含角色、目标、材料和输出格式，适合学习、求职和办公任务。", "keyword": "Prompt 四段式公式", "problem": "很多人只会说帮我优化，结果 AI 不知道优化什么、为谁优化、输出成什么样。Prompt 的稳定性来自明确约束。", "method": "四段式公式是角色、目标、材料、输出格式。复杂任务再补充限制条件和验收标准。", "steps": ["指定 AI 扮演的角色。", "说明任务目标和使用场景。", "粘贴真实材料。", "规定输出格式。", "要求标注不确定信息。"], "prompt": "你是【角色】。我需要【目标】。材料是【粘贴】。限制是【限制】。请按【表格/清单/段落】输出，并标注需要核验的信息。", "mistakes": ["没有提供材料。", "输出格式不明确。", "让 AI 自行假设关键事实。"], "sources": source("google_ai", "google_helpful", "owasp_llm")},
    {"slug": "ai-summary-prompt", "group": "tools", "category": "AI 工具箱", "tag": "总结", "title": "AI 总结资料怎么避免漏重点", "description": "AI 总结资料时应要求列出核心观点、原文依据、不确定信息和可执行动作，避免只给概括。", "keyword": "AI 总结资料 Prompt", "problem": "只说总结一下，AI 往往会给一段漂亮但不够可用的概括。学习和工作需要的是重点、依据和下一步。", "method": "要求 AI 输出一句话概括、核心观点、原文依据、术语解释、行动清单和待核验信息。", "steps": ["先说明资料用途。", "要求逐条列核心观点。", "每个观点附原文依据。", "把不确定信息单独列出。", "最后输出行动清单。"], "prompt": "请总结以下资料，输出：一句话概括、5 个核心观点、每个观点的原文依据、术语解释、可执行动作和需要核验的信息。", "mistakes": ["只要摘要，不要依据。", "资料太长但不分段。", "不区分事实和建议。"], "sources": source("google_ai", "google_helpful", "baidu_page")},
    {"slug": "ai-writing-polish-prompt", "group": "tools", "category": "AI 工具箱", "tag": "写作", "title": "AI 写作润色 Prompt 怎么写", "description": "AI 写作润色应保留原意、不新增事实、减少空话，并输出修改说明和证据缺口。", "keyword": "AI 写作润色 Prompt", "problem": "润色最危险的是越改越像宣传稿，甚至加入原文没有的信息。好润色应该让表达更清楚，而不是替换作者思考。", "method": "要求保留原意、不新增事实、减少重复、拆长句、标出缺少证据的位置，并说明改动原因。", "steps": ["说明读者是谁。", "说明希望语气正式还是自然。", "要求不新增事实。", "输出修改后版本和修改说明。", "标记需要补证据的句子。"], "prompt": "请润色下面文字。要求保留原意，不新增事实，减少空话，拆短长句，标注缺少证据的位置，并输出修改说明。", "mistakes": ["让 AI 自由发挥。", "保留新增的虚假事实。", "只看文字漂亮，不看逻辑是否成立。"], "sources": source("google_ai", "google_spam", "baidu_quality")},
    {"slug": "ai-study-plan-prompt", "group": "tools", "category": "AI 工具箱", "tag": "学习计划", "title": "用 AI 制定学习计划怎么提问", "description": "用 AI 制定学习计划时，应提供目标、基础、时间、截止日期和薄弱点，并要求输出完成标准。", "keyword": "AI 学习计划 Prompt", "problem": "学习计划失败通常不是计划不够漂亮，而是没有考虑真实时间、基础和反馈。AI 需要这些信息才能拆出可执行任务。", "method": "提供目标、当前基础、每天可用时间、截止日期和薄弱点。输出必须包含每日任务、耗时、完成标准和补救方案。", "steps": ["写清目标和截止日期。", "说明当前水平。", "给出每天可投入时间。", "列出薄弱点和已有资料。", "要求计划包含复盘问题。"], "prompt": "你是学习计划教练。我的目标是【】，基础是【】，每天可投入【】，截止日期【】。请制定计划，包含每日任务、耗时、完成标准和补救方案。", "mistakes": ["计划排太满。", "没有完成标准。", "不根据执行情况调整。"], "sources": source("google_ai", "google_helpful", "baidu_quality")},
    {"slug": "ai-meeting-notes-prompt", "group": "tools", "category": "AI 工具箱", "tag": "会议纪要", "title": "会议纪要 Prompt 怎么整理待办", "description": "AI 整理会议纪要时应输出结论、待办、负责人、截止时间、风险和待确认事项。", "keyword": "AI 会议纪要 Prompt", "problem": "会议纪要如果只记录讨论内容，后续仍然没人知道该做什么。真正有用的是结论和行动项。", "method": "把会议记录交给 AI 后，要求按结论、待办、负责人、截止时间、风险和待确认事项输出。缺失信息用待确认标记。", "steps": ["先提供完整会议记录。", "要求区分结论和讨论。", "待办必须有负责人。", "没有截止时间就标待确认。", "列出风险和下一次会议议题。"], "prompt": "请把以下会议记录整理成纪要，输出结论、待办、负责人、截止时间、风险和待确认事项。缺失负责人或时间请标注【待确认】。", "mistakes": ["把所有发言都写进去。", "待办没有负责人。", "遗漏争议点和风险。"], "sources": source("google_ai", "google_helpful")},
    {"slug": "ai-table-analysis-prompt", "group": "tools", "category": "AI 工具箱", "tag": "表格", "title": "让 AI 整理表格和清单怎么提问", "description": "让 AI 整理表格时，应指定列名、排序规则、缺失值处理和输出格式，避免生成不可用表格。", "keyword": "AI 整理表格 Prompt", "problem": "表格任务最怕列名不清和规则不明。AI 可能把数据改写得好看，却破坏原始含义。", "method": "先规定列名、数据来源、排序规则、缺失值标记和禁止新增信息。必要时让 AI 先检查数据问题。", "steps": ["说明表格用途。", "固定列名和顺序。", "规定缺失值写待确认。", "说明排序或分组规则。", "要求保留原始数据含义。"], "prompt": "请把以下信息整理成表格，列名固定为【】。缺失信息写【待确认】，不要新增事实。最后列出数据中不一致或需要核验的位置。", "mistakes": ["没有列名。", "让 AI 自动补数据。", "输出表格太宽，手机端难读。"], "sources": source("google_ai", "google_helpful", "baidu_page")},
    {"slug": "ai-account-security-checklist", "group": "tools", "category": "AI 工具箱", "tag": "账号安全", "title": "AI 账号安全检查清单", "description": "AI 账号安全检查清单，包括密码、二次验证、敏感信息、授权应用和设备管理。", "keyword": "AI 账号安全清单", "problem": "AI 工具经常绑定邮箱、文件和第三方授权。新手只关注怎么用，容易忽略账号和资料边界。", "method": "建立固定检查清单：不同平台不同密码、开启二次验证、不上传敏感信息、定期检查授权、重要资料先脱敏。", "steps": ["检查密码是否复用。", "开启二次验证。", "删除不再使用的第三方授权。", "上传文件前删除敏感信息。", "重要结论人工复核。"], "prompt": "请根据我的 AI 工具使用场景，生成账号安全检查清单，包含密码、授权、文件上传、敏感信息和结果核验。", "mistakes": ["把验证码或密钥发给 AI。", "长期不检查第三方授权。", "公司或个人敏感资料未脱敏。"], "sources": source("owasp_llm", "google_ai", "baidu_quality")},
    {"slug": "prompt-injection-basics", "group": "tools", "category": "AI 工具箱", "tag": "安全", "title": "Prompt Injection 是什么", "description": "Prompt Injection 是针对大语言模型的提示词攻击，可能让模型忽略原指令或泄露敏感信息。", "keyword": "Prompt Injection 是什么", "problem": "很多人把 Prompt Injection 理解成普通提示词技巧，实际上它是 AI 应用安全中的重要风险。", "method": "理解它的关键是区分指令和不可信内容。外部网页、用户输入、文档内容都可能包含让模型改变行为的文字。", "steps": ["不要把外部内容当成可信指令。", "敏感操作前增加人工确认。", "限制模型能访问的数据和工具。", "对输出做验证和过滤。", "记录异常指令和风险来源。"], "prompt": "请用初学者能懂的方式解释 Prompt Injection，并给出在个人学习和企业应用中分别应该注意的防护动作。", "mistakes": ["以为只要提示词写得强就安全。", "让模型直接执行高风险动作。", "把外部文档中的指令当真。"], "sources": source("owasp_prompt", "owasp_llm", "google_ai")},
    {"slug": "sensitive-info-redaction", "group": "tools", "category": "AI 工具箱", "tag": "脱敏", "title": "上传资料给 AI 前怎么脱敏", "description": "上传资料给 AI 前应删除姓名、电话、身份证、账号、密钥、客户信息和公司内部细节。", "keyword": "AI 资料脱敏", "problem": "AI 处理文档很方便，但上传前不脱敏可能暴露个人、客户或公司信息。安全使用的第一步是减少输入风险。", "method": "把敏感信息替换成占位符，例如【姓名】、【手机号】、【客户 A】、【密钥已删除】。保留任务所需结构，删除无关细节。", "steps": ["识别个人身份信息。", "删除账号、密码、token 和密钥。", "替换客户和公司内部名称。", "保留必要字段结构。", "上传前再扫一遍敏感词。"], "prompt": "请帮我检查以下文本中可能需要脱敏的信息，并输出脱敏后的版本。不要保留身份证、手机号、账号、密钥或客户真实名称。", "mistakes": ["只删除姓名，保留手机号。", "保留 token 或 API key。", "把公司内部数据原样上传。"], "sources": source("owasp_llm", "google_ai", "google_spam")},
    {"slug": "ai-result-verification", "group": "tools", "category": "AI 工具箱", "tag": "核验", "title": "AI 输出结果怎么核验", "description": "AI 输出结果要区分事实、建议和推测，涉及时间、政策、工具版本和考试规则时回到官方来源。", "keyword": "AI 输出核验", "problem": "AI 输出流畅不代表正确。越是看起来完整的回答，越需要检查事实来源和适用条件。", "method": "把输出拆成事实、建议和推测三类。事实查来源，建议看适用场景，推测要求模型标注不确定性。", "steps": ["圈出具体数字、时间和政策。", "检查是否有来源。", "回到官方文档或原始材料核对。", "让 AI 标出不确定信息。", "保留自己的判断记录。"], "prompt": "请审查你刚才的回答，区分确定事实、推测、建议和需要外部核验的信息，并给出更谨慎的版本。", "mistakes": ["只看回答是否顺。", "不查工具版本和政策变化。", "把建议当事实。"], "sources": source("google_ai", "google_helpful", "baidu_quality")},
    {"slug": "ai-search-research-workflow", "group": "tools", "category": "AI 工具箱", "tag": "资料检索", "title": "用 AI 做资料检索的正确流程", "description": "用 AI 做资料检索应先定义问题、找来源、提取观点、核验事实，再整理成自己的笔记。", "keyword": "AI 资料检索流程", "problem": "让 AI 直接给资料，很容易得到没有出处的概括。更稳的流程是先找来源，再让 AI 辅助阅读和整理。", "method": "先列问题和关键词，找到官方或权威来源，再把来源内容交给 AI 总结。最后保留链接和抓取时间。", "steps": ["写清研究问题。", "列出中英文关键词。", "优先找官方文档和原始资料。", "让 AI 提取观点和证据。", "整理来源清单和待核验项。"], "prompt": "请根据我的研究问题，生成检索关键词、优先来源类型、资料筛选标准和笔记模板，不要编造具体来源。", "mistakes": ["直接让 AI 编参考资料。", "只看二手文章。", "笔记没有来源链接。"], "sources": source("google_ai", "google_helpful", "baidu_page")},
    {"slug": "personal-knowledge-base-ai", "group": "tools", "category": "AI 工具箱", "tag": "知识库", "title": "用 AI 整理个人知识库", "description": "用 AI 整理个人知识库，应把资料转成主题、适用场景、操作步骤、常见错误和下次行动。", "keyword": "AI 个人知识库", "problem": "收藏文章不等于建立知识库。真正可复用的笔记要能回答什么时候用、怎么用、容易错在哪里。", "method": "让 AI 把资料整理成标题、场景、核心结论、步骤、模板、相关概念和下次行动。每条笔记保留来源。", "steps": ["先按主题归档。", "每篇笔记写适用场景。", "提取可执行步骤。", "记录常见错误。", "用内链关联相关主题。"], "prompt": "请把以下材料整理成个人知识库笔记，包含标题、适用场景、核心结论、操作步骤、常见错误、可复用模板和相关概念。", "mistakes": ["只复制原文。", "没有适用场景。", "笔记之间没有关联。"], "sources": source("google_ai", "google_helpful")},
    {"slug": "ai-ppt-outline-prompt", "group": "tools", "category": "AI 工具箱", "tag": "PPT", "title": "用 AI 做 PPT 大纲怎么提问", "description": "AI 做 PPT 大纲时要说明听众、目标、页数、场景和每页要回答的问题。", "keyword": "AI PPT 大纲 Prompt", "problem": "让 AI 直接做 PPT，常出现页面好看但逻辑松散。先做好大纲，才能保证每页服务于汇报目标。", "method": "输入听众、汇报目的、时长、页数和已有材料。要求每页有标题、核心信息、讲述要点和需要的图表。", "steps": ["说明听众是谁。", "说明汇报目标。", "限制页数和时间。", "提供已有材料。", "让 AI 输出每页要回答的问题。"], "prompt": "请根据我的汇报主题、听众和材料，生成 PPT 大纲。每页包含标题、核心观点、讲述要点、需要的图表和预计讲述时间。", "mistakes": ["页数太多。", "每页只有标题没有观点。", "没有考虑听众关心什么。"], "sources": source("google_ai", "google_helpful", "baidu_quality")},
    {"slug": "ai-weekly-review", "group": "tools", "category": "AI 工具箱", "tag": "复盘", "title": "用 AI 做每周复盘怎么写", "description": "每周复盘可以让 AI 帮你整理目标、完成情况、卡点、原因和下周行动，但事实要自己提供。", "keyword": "AI 每周复盘", "problem": "复盘如果只写本周很忙，就不会带来改进。AI 可以帮你从记录中提取模式，但不能替你提供真实事实。", "method": "把本周计划、完成记录、未完成原因和情绪状态输入 AI，让它整理成目标、结果、问题、根因和下周动作。", "steps": ["列出本周目标。", "写完成和未完成事项。", "说明卡点和原因。", "让 AI 归纳重复问题。", "下周只保留 3 个重点动作。"], "prompt": "请根据我的本周记录做复盘，输出目标、实际结果、关键问题、根因分析、下周 3 个重点行动和需要放弃的低价值任务。", "mistakes": ["只总结成果，不分析未完成。", "下周动作太多。", "复盘没有数据或记录。"], "sources": source("google_ai", "google_helpful", "baidu_page")},
]


GROUPS = {
    "campus": {"label": "校园效率", "page": "campus.html", "eyebrow": "Campus", "accent": "accent-green", "image": "campus"},
    "career": {"label": "求职冲刺", "page": "career.html", "eyebrow": "Career", "accent": "accent-blue", "image": "career"},
    "tools": {"label": "AI 工具", "page": "tools.html", "eyebrow": "Tools", "accent": "accent-amber", "image": "tools"},
}


def esc(text: str) -> str:
    return escape(text, quote=True)


def article_url(slug: str) -> str:
    return f"articles/{slug}.html"


def sentence_list(items: list[str]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def source_list(items: list[tuple[str, str]]) -> str:
    return "".join(f'<li><a href="{esc(url)}">{esc(title)}</a></li>' for title, url in items)


def related_for(article: dict) -> list[dict]:
    same = [item for item in ARTICLES if item["group"] == article["group"] and item["slug"] != article["slug"]]
    return same[:3]


def article_body_text(article: dict) -> str:
    parts = [
        article["problem"], article["method"], article["prompt"],
        *article["steps"], *article["mistakes"],
    ]
    return "".join(parts)


def render_article(article: dict) -> str:
    group = GROUPS[article["group"]]
    image = IMAGES[group["image"]]
    related = related_for(article)
    h1 = article["title"]
    title = f"{h1} - AI效率资源站"
    summary = (
        f"{article['keyword']}这类问题，适合先拆清场景，再按步骤执行。"
        f"本文围绕{article['tag']}给出可操作方法、Prompt 模板、常见错误和安全边界。"
    )
    extra = (
        f"从搜索用户的角度看，{article['keyword']}不是一个只需要概念解释的问题。"
        f"真正有帮助的页面应该告诉读者先做什么、怎样检查结果、哪些地方需要回到官方资料或原始材料核验。"
        f"所以本文不追求堆关键词，而是把流程拆成能照着做的动作。"
    )
    example = (
        f"举个简单场景：如果你今天就要处理{article['keyword']}，不要先打开一堆网页来回收藏。"
        f"更稳的做法是先写下当前任务、可用时间、已有材料和最终要交付的东西，再按本文步骤逐项推进。"
        f"完成后用一个小清单检查：目标是否明确，材料是否真实，步骤是否能执行，结果是否能被别人复查。"
        f"这种写法对搜索用户也更友好，因为读者进入页面后能马上判断自己是否适用，而不是读完仍然不知道下一步该做什么。"
    )
    template = (
        f"【任务】我正在处理：{article['keyword']}。\n"
        f"【背景】{article['problem']}\n"
        "【输出】请按步骤、检查表、常见错误、下一步行动输出。"
    )
    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(article['description'])}">
  <link rel="icon" href="../assets/images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="../assets/images/apple-touch-icon.png">
  <link rel="stylesheet" href="../assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="site-header"><div class="nav-wrap"><a class="brand" href="../index.html"><span class="brand-mark">AI</span><span>AI效率资源站</span></a><nav class="site-nav" data-site-nav aria-label="主导航"></nav></div></header>
  <main id="main">
    <section class="article-hero"><div class="section-inner"><span class="eyebrow">{esc(group['eyebrow'])}</span><h1>{esc(h1)}</h1><div class="article-meta"><span>{esc(article['category'])}</span><span>更新：{TODAY}</span><span>阅读约 6 分钟</span></div></div></section>
    <section class="section tight"><div class="section-inner"><article class="conversion-card seo-summary-card"><div class="conversion-copy"><div class="offer-meta"><span class="tag hot">本文重点</span><span class="tag free">{esc(article['tag'])}</span></div><h2>{esc(article['keyword'])}，先解决真实使用场景</h2><p>{esc(summary)}</p></div><div class="conversion-action"><a class="button hot full" href="#method">查看核心方法</a><a class="card-link" href="../{group['page']}">返回{group['label']}专题</a></div></article></div></section>
    <section class="section"><div class="section-inner article-layout">
      <article class="article-body">
        <figure class="article-image"><img src="{esc(image['src'])}" alt="{esc(image['alt'])}" loading="lazy"><figcaption>{esc(image['caption'])}</figcaption></figure>
        <h2 id="who">适合谁</h2>
        <p>{esc(article['problem'])}</p>
        <p>{esc(extra)}</p>
        <h2 id="method">核心方法</h2>
        <p>{esc(article['method'])}</p>
        <ol>{sentence_list(article['steps'])}</ol>
        <h2 id="example">实操示例</h2>
        <p>{esc(example)}</p>
        <h2 id="template">可复制模板</h2>
        <p>下面这段模板适合直接复制到 AI 工具里，再把括号中的内容替换成自己的真实材料。输出后仍然要人工核验，尤其是涉及考试规则、工具版本、招聘要求和安全边界的信息。</p>
        <pre><code>{esc(template)}</code></pre>
        <p>{esc(article['prompt'])}</p>
        <h2 id="mistakes">常见错误</h2>
        <ul>{sentence_list(article['mistakes'])}</ul>
        <p>如果你发现自己反复遇到这些问题，不要急着增加更多资料。更有效的做法是回到任务目标，把输入材料、完成标准和检查动作补齐。搜索来的内容只能提供参考，最终是否适合你的课程、项目或岗位，还要结合自己的真实场景判断。</p>
        <h2 id="boundary">边界提醒</h2>
        <p>本站内容用于学习规划、效率提升和表达训练。涉及课程要求、考试安排、招聘信息、工具政策和安全风险时，应以官方说明、原始资料或任课老师要求为准。AI 可以帮助拆解任务、检查遗漏和优化表达，但不应替代个人判断，也不应生成无法核验的事实。</p>
        <h2 id="sources">参考来源</h2>
        <ul>{source_list(article['sources'])}</ul>
        <h2 id="related">相关文章</h2>
        <ul>{''.join(f'<li><a href="{esc(item["slug"])}.html">{esc(item["title"])}</a></li>' for item in related)}</ul>
      </article>
      <aside class="sidebar"><nav class="toc"><strong>目录</strong><a href="#who">适合谁</a><a href="#method">核心方法</a><a href="#example">实操示例</a><a href="#template">可复制模板</a><a href="#mistakes">常见错误</a><a href="#boundary">边界提醒</a><a href="#sources">参考来源</a></nav><div class="ad-slot" data-ad-slot></div></aside>
    </div></section>
  </main>
  <footer class="site-footer"><div class="footer-inner" data-site-footer></div></footer><script src="../assets/site.js"></script>
</body>
</html>
"""
    return html


def card(article: dict) -> str:
    accent = GROUPS[article["group"]]["accent"]
    return f"""<article class="article-card {accent}">
  <div class="tag-list"><span class="tag free">免费文章</span><span class="tag">{esc(article['tag'])}</span></div>
  <h2>{esc(article['title'])}</h2>
  <p>{esc(article['description'])}</p>
  <a class="card-link" href="{article_url(article['slug'])}">阅读文章</a>
</article>"""


def render_group_page(group_key: str, title: str, description: str, lead: str) -> str:
    items = [item for item in ARTICLES if item["group"] == group_key]
    group = GROUPS[group_key]
    cards = "\n".join(card(item) for item in items)
    first = items[0]
    second = items[1]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)} - AI效率资源站</title>
  <meta name="description" content="{esc(description)}">
  <link rel="icon" href="assets/images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="site-header"><div class="nav-wrap"><a class="brand" href="index.html"><span class="brand-mark">AI</span><span>AI效率资源站</span></a><nav class="site-nav" data-site-nav aria-label="主导航"></nav></div></header>
  <main id="main">
    <section class="article-hero"><div class="section-inner"><span class="eyebrow">{esc(group['eyebrow'])}</span><h1>{esc(title)}</h1><p class="hero-lede">{esc(lead)}</p></div></section>
    <section class="section"><div class="section-inner"><article class="offer-card seo-focus-card"><div class="offer-copy"><div class="offer-meta"><span class="tag hot">专题导航</span><span class="tag free">{len(items)} 篇文章</span></div><h2>先读支柱文章，再按具体问题深入</h2><p>本专题按搜索问题拆分文章，每篇都给步骤、模板、常见错误和参考来源。</p></div><div class="offer-action"><a class="button hot" href="{article_url(first['slug'])}">阅读：{esc(first['tag'])}</a><a class="card-link" href="{article_url(second['slug'])}">继续看：{esc(second['tag'])}</a></div></article></div></section>
    <section class="section tight"><div class="section-inner"><div class="section-head"><div><h2>{esc(title)}文章列表</h2><p>所有文章均为免费阅读，优先解决一个具体问题，避免空泛堆词。</p></div></div><div class="grid three">{cards}</div></div></section>
  </main>
  <footer class="site-footer"><div class="footer-inner" data-site-footer></div></footer><script src="assets/site.js"></script>
</body>
</html>
"""


def render_index() -> str:
    featured = [
        "cet-14-day-study-plan",
        "automation-test-interview-roadmap",
        "prompt-four-part-formula",
        "final-paper-outline-ai",
        "ai-resume-polish-guide",
        "ai-account-security-checklist",
    ]
    cards = "\n".join(card(next(item for item in ARTICLES if item["slug"] == slug)) for slug in featured)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI效率资源站 - 大学生与职场新人的 AI 学习求职导航</title>
  <meta name="description" content="AI效率资源站面向大学生和职场新人，提供 AI 学习方法、求职准备、提示词模板和工具安全内容。">
  <link rel="icon" href="assets/images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="assets/images/apple-touch-icon.png">
  <link rel="stylesheet" href="assets/styles.css">
</head>
<body>
  <a class="skip-link" href="#main">跳到正文</a>
  <header class="site-header"><div class="nav-wrap"><a class="brand" href="index.html" aria-label="AI效率资源站首页"><span class="brand-mark">AI</span><span>AI效率资源站</span></a><nav class="site-nav" data-site-nav aria-label="主导航"></nav></div></header>
  <main id="main">
    <section class="hero"><div class="section-inner"><div class="hero-copy"><span class="eyebrow">AI efficiency hub</span><h1><span class="hero-line">把 AI 变成学习、</span><span class="hero-line">求职和日常工作</span><span class="hero-line">的效率工具。</span></h1><p class="hero-lede"><span class="mobile-line">这里专注大学生和职场新人的真实问题：</span><span class="mobile-line">备考、作业、简历、面试、提示词和账号安全。</span><span class="mobile-line">每篇文章都给步骤、模板、常见错误和参考来源。</span></p><div class="hero-actions"><a class="button hot" href="career.html">查看求职专题</a><a class="button" href="campus.html">浏览校园专题</a><a class="button secondary" href="tools.html">学习 AI 工具</a></div></div><aside class="hero-panel" aria-label="站点内容概览"><div class="metric-grid"><div class="metric"><strong>50</strong><span>长文文章</span></div><div class="metric"><strong>3</strong><span>核心专题</span></div><div class="metric"><strong>0</strong><span>依赖构建</span></div></div></aside></div></section>
    <section id="sections" class="section"><div class="section-inner"><div class="section-head"><div><h2>三类人群，一套效率资源</h2><p>第一阶段先做好可收录内容，不放强商业按钮，重点提升页面质量和站内结构。</p></div></div><div class="grid three"><article class="card accent-green"><h3>校园效率区</h3><p>四六级、期末作业、活动策划和小组协作。</p><div class="tag-list"><span class="tag free">18 篇</span><span class="tag">大学生</span></div><a class="card-link" href="campus.html">进入专区</a></article><article class="card accent-blue"><h3>求职冲刺区</h3><p>自动化测试、简历、项目表达和模拟面试。</p><div class="tag-list"><span class="tag free">17 篇</span><span class="tag">应届生</span></div><a class="card-link" href="career.html">进入专区</a></article><article class="card accent-amber"><h3>AI 工具箱</h3><p>GPT/Claude 入门、Prompt、资料整理和账号安全。</p><div class="tag-list"><span class="tag free">15 篇</span><span class="tag">AI 工具</span></div><a class="card-link" href="tools.html">进入专区</a></article></div></div></section>
    <section class="section feature-band"><div class="section-inner"><div class="section-head"><div><h2>精选支柱文章</h2><p>先从搜索需求最明确的文章读起，再进入专题页继续延伸。</p></div></div><div class="grid three">{cards}</div></div></section>
  </main>
  <footer class="site-footer"><div class="footer-inner" data-site-footer></div></footer><script src="assets/site.js"></script>
</body>
</html>
"""


def render_site_js() -> str:
    featured = [
        ("四六级 14 天备考计划", "articles/cet-14-day-study-plan.html", "校园效率", "把词汇、阅读、听力、作文拆成每天可执行任务。"),
        ("自动化测试面试准备路线", "articles/automation-test-interview-roadmap.html", "求职冲刺", "按接口、UI、数据库、框架和项目复盘准备。"),
        ("稳定 Prompt 的四段式公式", "articles/prompt-four-part-formula.html", "AI 工具", "用角色、目标、材料、输出格式提升回答稳定性。"),
    ]
    resources = ",\n".join(
        f'    {{ title: "{title}", href: "{href}", category: "{cat}", summary: "{summary}" }}'
        for title, href, cat, summary in featured
    )
    return f"""const siteConfig = {{
  name: "AI效率资源站",
  tagline: "面向大学生和职场新人的 AI 学习、求职与工具资源库",
  adPlaceholder: "赞助内容区域：后续展示与学习、求职和效率工具相关的合规推荐",
  featuredResources: [
{resources}
  ]
}};

function resolvePath(path) {{
  const inArticle = location.pathname.includes("/articles/");
  if (/^https?:/.test(path) || path.startsWith("#")) return path;
  return inArticle ? `../${{path}}` : path;
}}

function buildNav() {{
  const nav = document.querySelector("[data-site-nav]");
  if (!nav) return;
  const links = [["首页", "index.html"], ["校园", "campus.html"], ["求职", "career.html"], ["工具", "tools.html"], ["关于", "about.html"]];
  const current = location.pathname.split("/").pop() || "index.html";
  nav.innerHTML = links.map(([label, href]) => {{
    const active = current === href ? ' aria-current="page"' : "";
    return `<a href="${{resolvePath(href)}}"${{active}}>${{label}}</a>`;
  }}).join("");
}}

function buildFooter() {{
  const footer = document.querySelector("[data-site-footer]");
  if (!footer) return;
  const year = new Date().getFullYear();
  footer.innerHTML = `
    <div>
      <strong>${{siteConfig.name}}</strong>
      <p>${{siteConfig.tagline}}。本站内容用于学习和效率参考，不替代课程要求、考试规则、官方文档或个人判断。</p>
      <p>© ${{year}} ${{siteConfig.name}}. All rights reserved.</p>
    </div>
    <nav class="footer-links" aria-label="Footer">
      <a href="${{resolvePath("about.html")}}">关于本站</a>
      <a href="${{resolvePath("privacy.html")}}">隐私政策</a>
      <a href="${{resolvePath("contact.html")}}">联系合作</a>
      <a href="${{resolvePath("sitemap.xml")}}">站点地图</a>
    </nav>`;
}}

function buildAdSlots() {{
  document.querySelectorAll("[data-ad-slot]").forEach((slot) => {{
    slot.innerHTML = `<div><strong>赞助内容区域</strong><span>${{siteConfig.adPlaceholder}}</span></div>`;
  }});
}}

function buildFeaturedResources() {{
  const target = document.querySelector("[data-featured-resources]");
  if (!target) return;
  target.innerHTML = siteConfig.featuredResources.map((item) => `
    <article class="resource-card">
      <span class="tag">${{item.category}}</span>
      <h3>${{item.title}}</h3>
      <p>${{item.summary}}</p>
      <a class="card-link" href="${{resolvePath(item.href)}}">查看资源</a>
    </article>
  `).join("");
}}

document.addEventListener("DOMContentLoaded", () => {{
  buildNav();
  buildFooter();
  buildAdSlots();
  buildFeaturedResources();
}});
"""


def render_sitemap() -> str:
    urls = ["", "campus.html", "career.html", "tools.html", "about.html", "privacy.html", "contact.html"]
    urls += [article_url(item["slug"]) for item in ARTICLES]
    locs = "\n".join(f"  <url><loc>{SITE_URL}/{url}</loc></url>" if url else f"  <url><loc>{SITE_URL}/</loc></url>" for url in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{locs}\n</urlset>\n'


def render_attributions() -> str:
    return """# Image Attributions

Images are stored locally under `assets/images/articles/` to avoid hotlinking.

- `campus-study.jpg`: Unsplash source image, used under the Unsplash License. Source URL: https://images.unsplash.com/photo-1516321318423-f06f85e504b3
- `career-team.jpg`: Unsplash source image, used under the Unsplash License. Source URL: https://images.unsplash.com/photo-1519389950473-47ba0277781c
- `ai-tools-code.jpg`: Unsplash source image, used under the Unsplash License. Source URL: https://images.unsplash.com/photo-1498050108023-c5249f4df085
- Unsplash License: https://unsplash.com/license
"""


def main() -> None:
    ARTICLES_DIR.mkdir(exist_ok=True)
    for old in ARTICLES_DIR.glob("*.html"):
        old.unlink()
    for article in ARTICLES:
        (ARTICLES_DIR / f"{article['slug']}.html").write_text(render_article(article), encoding="utf-8", newline="\n")
    (ROOT / "index.html").write_text(render_index(), encoding="utf-8", newline="\n")
    (ROOT / "campus.html").write_text(render_group_page("campus", "校园效率区", "校园效率区整理四六级备考、期末作业、活动策划和小组协作文章。", "把 AI 当成学习助教：拆计划、搭框架、查漏洞，但不替代自己的学习过程。"), encoding="utf-8", newline="\n")
    (ROOT / "career.html").write_text(render_group_page("career", "求职冲刺区", "求职冲刺区整理自动化测试面试、简历优化、项目表达和模拟面试文章。", "面向应届生和转行新人，把简历、面试和项目表达做成可练习、可复盘的流程。"), encoding="utf-8", newline="\n")
    (ROOT / "tools.html").write_text(render_group_page("tools", "AI 工具箱", "AI 工具箱整理 GPT/Claude 入门、提示词模板、资料核验和账号安全文章。", "给 AI 工具新手准备的合规使用路径：先理解任务，再写提示词，最后核验结果。"), encoding="utf-8", newline="\n")
    (ROOT / "assets" / "site.js").write_text(render_site_js(), encoding="utf-8", newline="\n")
    (ROOT / "sitemap.xml").write_text(render_sitemap(), encoding="utf-8", newline="\n")
    (ROOT / "assets" / "images" / "ATTRIBUTIONS.md").write_text(render_attributions(), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
