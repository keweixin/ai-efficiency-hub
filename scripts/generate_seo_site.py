from __future__ import annotations

import json
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
    {"slug": "ui-automation-flaky-answer", "group": "career", "category": "求职冲刺", "tag": "UI 自动化", "title": "UI 自动化不稳定怎么回答", "description": "面试中回答 UI 自动化不稳定问题时，可从定位器、显式等待、截图日志和用例边界展开。", "keyword": "UI 自动化稳定性优化", "problem": "UI 自动化不稳定是高频面试题。简单回答加等待不够，因为它没有体现你区分原因和控制误报的能力。", "method": "回答时先说现象，再说排查，再说改进。重点包括稳定定位器、显式等待、失败截图、页面源码、重试边界和不适合自动化的场景。", "steps": ["确认是元素加载、定位器变化还是环境问题。", "把脆弱 XPath 改成稳定属性或文本组合。", "使用显式等待等待关键状态。", "失败时保留截图、日志和页面源码。", "把频繁变化的一次性流程移出自动化范围。"], "prompt": "请帮我把 UI 自动化不稳定的经历改成 STAR 面试回答，要求包含背景、排查动作、改进方案和结果。", "mistakes": ["只说加 sleep。", "没有失败证据。", "把所有流程都自动化，忽视维护成本。"], "sources": source("selenium_waits", "selenium_locators", "google_helpful")},
    {"slug": "api-test-auth-token", "group": "career", "category": "求职冲刺", "tag": "接口测试", "title": "接口自动化 token 和鉴权怎么处理", "description": "接口自动化中 token 和鉴权处理思路：登录前置、会话上下文、角色账号和过期重试。", "keyword": "接口自动化 token 鉴权", "problem": "鉴权处理如果写死 token，用例很快失效，也难以切换环境和角色。面试时要说明如何让登录态可维护。", "method": "把登录接口封装成前置步骤，token 存在会话上下文或统一请求头。不同权限准备不同账号，关键接口验证未授权和权限不足。", "steps": ["封装登录方法，不在用例里写死 token。", "统一请求头和环境配置。", "token 过期时重新登录并记录日志。", "为普通用户、管理员和无权限用户准备账号。", "断言业务码和权限提示。"], "prompt": "请根据我的接口自动化项目，帮我组织 token 和鉴权处理的面试回答，包含为什么不能写死、如何封装、如何覆盖权限场景。", "mistakes": ["把 token 复制到每条用例。", "只测正常登录用户。", "没有覆盖未授权和权限不足。"], "sources": source("pytest_fixtures", "pytest_parametrize", "google_helpful")},
    {"slug": "api-assertion-design", "group": "career", "category": "求职冲刺", "tag": "接口测试", "title": "接口测试断言怎么设计", "description": "接口测试断言不应只看状态码，还应覆盖业务码、字段、错误信息和关键数据结果。", "keyword": "接口测试断言设计", "problem": "接口返回 200 不等于业务正确。断言设计太浅，会让问题漏掉，也会让面试回答显得没有测试思维。", "method": "把断言分成协议层、业务层和数据层。普通接口检查状态码和业务码，关键链路再检查字段、错误提示和数据库结果。", "steps": ["协议层检查状态码和响应时间。", "业务层检查 code、message 和关键字段。", "异常场景检查错误提示是否明确。", "关键链路检查数据是否真正变化。", "失败时输出请求、响应和断言差异。"], "prompt": "请根据这个接口文档，帮我设计正常、异常、边界和鉴权场景的断言点，并说明每个断言能发现什么问题。", "mistakes": ["只断言 200。", "没有异常场景。", "断言字段太多导致维护困难。"], "sources": source("pytest_parametrize", "google_helpful", "baidu_quality")},
    {"slug": "pytest-parametrize-fixture", "group": "career", "category": "求职冲刺", "tag": "pytest", "title": "pytest 参数化和 fixture 怎么讲", "description": "面试中讲 pytest 参数化和 fixture，可围绕减少重复、准备数据、共享前置和提高可维护性展开。", "keyword": "pytest 参数化 fixture", "problem": "很多初学者知道 pytest，但讲不清参数化和 fixture 的区别。面试时要说明它们分别解决什么问题。", "method": "参数化用于同一逻辑跑多组输入，fixture 用于准备前置条件和资源。两者结合可以让用例更短、更稳定。", "steps": ["用 parametrize 管理多组输入和预期结果。", "用 fixture 准备登录、测试数据或客户端。", "把环境配置从用例中抽离。", "失败输出应能看到是哪组参数。", "不要为了封装而隐藏业务意图。"], "prompt": "请帮我用通俗语言解释 pytest 参数化和 fixture 的区别，并给一个接口自动化场景中的面试回答。", "mistakes": ["把所有逻辑都塞进 fixture。", "参数名不清楚，失败时难定位。", "为了少写代码牺牲可读性。"], "sources": source("pytest_parametrize", "pytest_fixtures")},
    {"slug": "selenium-explicit-wait", "group": "career", "category": "求职冲刺", "tag": "Selenium", "title": "Selenium 显式等待怎么理解", "description": "Selenium 显式等待用于等待关键条件出现，比固定 sleep 更可控，适合解释 UI 自动化稳定性。", "keyword": "Selenium 显式等待", "problem": "UI 用例失败经常不是功能错，而是页面状态还没准备好。固定 sleep 会拖慢用例，也不一定稳定。", "method": "显式等待是等待某个条件满足，例如元素可见、可点击、文本出现。回答时要说明等待的是业务关键状态，不是盲目等待时间。", "steps": ["找出用例真正依赖的页面状态。", "等待元素可见或可点击。", "对异步加载结果等待文本或列表变化。", "设置合理超时时间。", "超时后保留截图和日志。"], "prompt": "请帮我把 Selenium 显式等待解释成面试回答，要求对比固定 sleep，并结合一个登录后等待首页元素的例子。", "mistakes": ["所有地方都 sleep 3 秒。", "等待了错误元素。", "没有超时证据。"], "sources": source("selenium_waits", "selenium_locators")},
    {"slug": "test-report-logs-screenshots", "group": "career", "category": "求职冲刺", "tag": "测试报告", "title": "测试报告、日志和截图怎么定位问题", "description": "自动化失败后应通过测试报告、请求响应、日志、截图和环境信息判断问题来源。", "keyword": "自动化测试问题排查", "problem": "测试报告如果只有通过和失败，价值很有限。好的报告应该帮助团队快速判断是脚本问题、数据问题、环境问题还是产品问题。", "method": "报告里保留用例名、步骤、环境、请求参数、响应摘要、错误堆栈和截图。失败后先分类，再决定是否重跑或提缺陷。", "steps": ["先看失败类型和错误信息。", "查看请求参数和响应内容。", "UI 用例查看截图和页面状态。", "检查测试数据是否满足前置条件。", "记录归因，避免同类问题重复出现。"], "prompt": "请根据这段失败日志和截图描述，帮我判断可能原因，并输出环境问题、数据问题、脚本问题、产品问题四类排查清单。", "mistakes": ["失败就重跑，没有归因。", "报告缺少请求和响应。", "截图没有和步骤对应。"], "sources": source("selenium_waits", "pytest_fixtures", "google_helpful")},
    {"slug": "ci-smoke-testing", "group": "career", "category": "求职冲刺", "tag": "CI", "title": "自动化测试接入 CI 先跑哪些用例", "description": "自动化测试接入 CI 应先选择稳定的冒烟用例，覆盖核心链路，避免一开始全量导致误报。", "keyword": "自动化测试 CI 冒烟用例", "problem": "把所有自动化用例一次性接入 CI，容易因为环境和数据不稳定导致大量失败，团队会失去信任。", "method": "先接核心冒烟用例：登录、关键查询、关键提交、权限校验。用例必须稳定、执行快、失败易定位。", "steps": ["筛选业务最关键的 5 到 20 条用例。", "确保测试数据可重复准备。", "失败时输出报告和通知。", "每日定时和提交触发分开。", "稳定后再逐步扩展覆盖范围。"], "prompt": "请根据我的系统模块，帮我筛选适合 CI 冒烟测试的用例，并说明每条用例为什么值得优先执行。", "mistakes": ["一开始全量接入。", "把不稳定 UI 用例放进主流程。", "失败没有通知和报告。"], "sources": source("pytest_fixtures", "google_helpful", "baidu_quality")},
    {"slug": "database-validation-testing", "group": "career", "category": "求职冲刺", "tag": "数据库校验", "title": "接口测试什么时候需要查数据库", "description": "数据库校验适合订单、库存、用户状态等关键链路，不是每条接口都必须查库。", "keyword": "接口测试 数据库校验", "problem": "接口返回成功只能说明响应看起来正常，不一定证明数据真正落库。但每条用例都查数据库也会增加维护成本。", "method": "关键链路查关键字段，普通查询接口以业务字段断言为主。查库前要准备独立数据，查库后要清理或隔离。", "steps": ["判断接口是否改变核心数据。", "明确要校验的字段。", "准备唯一测试数据。", "执行接口后查询数据状态。", "清理数据或使用隔离环境。"], "prompt": "请根据这个业务接口，判断是否需要数据库校验。如果需要，请列出校验字段、查询条件和可能发现的问题。", "mistakes": ["每条接口都查库，拖慢执行。", "查错环境或错数据。", "没有清理测试数据。"], "sources": source("pytest_fixtures", "google_helpful")},
    {"slug": "test-resume-project-description", "group": "career", "category": "求职冲刺", "tag": "简历", "title": "测试简历项目描述怎么写", "description": "测试简历项目描述要写清模块、测试点、方法、工具、结果和可追问细节。", "keyword": "测试简历项目描述", "problem": "简历里只写参与项目、负责测试，很难让招聘方判断你做了什么。测试岗需要体现测试点设计、问题定位和交付物。", "method": "项目经历按背景、任务、动作、结果写。动作要包括用例设计、接口验证、缺陷记录、报告输出和复测。", "steps": ["先写项目是什么和你负责的模块。", "写覆盖哪些核心流程。", "写使用什么方法或工具。", "写输出了哪些交付物。", "准备每条描述的追问答案。"], "prompt": "请把我的测试项目经历改写成 5 条简历 bullet，要求包含动作、对象、方法和结果，不要编造数据。", "mistakes": ["写精通但解释不了。", "只写工具名没有业务对象。", "项目结果无法被追问。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "ai-resume-polish-guide", "group": "career", "category": "求职冲刺", "tag": "AI 简历", "title": "AI 润色简历怎样避免编造经历", "description": "用 AI 润色简历时应提供真实经历和岗位 JD，让 AI 优化表达而不是新增事实。", "keyword": "AI 润色简历", "problem": "AI 改简历容易把经历写得很漂亮，但也可能新增你没有做过的工具、结果和数据。面试时这些内容会变成风险。", "method": "把 JD 和真实经历一起给 AI，要求标注缺失信息。所有新增数据必须用待补充标记，不允许直接生成具体数字。", "steps": ["先整理真实项目和职责。", "粘贴目标岗位 JD。", "让 AI 提取匹配关键词。", "改写时要求不新增事实。", "删除自己解释不了的技术词。"], "prompt": "你是招聘经理。请根据岗位 JD 和我的真实经历，指出匹配点、缺失能力和可优化表达。不要新增经历，缺少数据请标注【需补充】。", "mistakes": ["让 AI 直接生成完整简历。", "保留不懂的技术名词。", "把课程项目写成真实商业项目。"], "sources": source("google_ai", "google_helpful", "baidu_page")},
    {"slug": "fresh-graduate-project-star", "group": "career", "category": "求职冲刺", "tag": "STAR", "title": "应届生项目经历 STAR 表达", "description": "应届生项目经历可以用 STAR 结构讲清背景、任务、行动和结果，但不能夸大项目性质。", "keyword": "STAR 原则项目表达", "problem": "应届生项目不一定大，但只要能讲清你解决的问题和具体行动，就能成为面试材料。STAR 的价值是让经历有结构。", "method": "S 是项目背景，T 是你的任务，A 是你做了哪些具体动作，R 是交付物或改进结果。结果可以是报告、脚本、复盘，不一定是夸张数据。", "steps": ["说明项目来源和业务场景。", "明确你负责的模块。", "列出 3 个具体行动。", "说明遇到的难点。", "用交付物证明结果。"], "prompt": "请把我的课程项目整理成 STAR 面试回答，要求真实、不夸大，并列出面试官可能追问的 5 个问题。", "mistakes": ["把团队成果全写成个人成果。", "只讲技术，不讲任务背景。", "结果没有证据。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "no-internship-resume", "group": "career", "category": "求职冲刺", "tag": "简历", "title": "没有实习经历怎么写测试岗简历", "description": "没有实习经历时，可以用课程项目、自学练习、缺陷记录和测试报告证明测试岗能力。", "keyword": "无实习简历突破", "problem": "没有实习不是不能投测试岗，但简历必须提供能力证据。空写学习能力强，很难让招聘方相信。", "method": "把课程项目改成测试视角，把自学练习沉淀成脚本、用例、报告和复盘。重点写能被追问的内容。", "steps": ["列出课程项目和自学项目。", "为每个项目补测试点和用例。", "输出缺陷记录或测试报告。", "准备工具和流程的解释。", "删除和岗位无关的大段内容。"], "prompt": "我没有实习经历，但有这些课程项目和自学练习。请帮我筛选适合测试岗简历的内容，并改写成真实可追问的项目描述。", "mistakes": ["空写熟悉测试流程。", "把没做过的自动化写上去。", "项目描述和岗位无关。"], "sources": source("google_helpful", "baidu_quality")},
    {"slug": "test-interview-self-introduction", "group": "career", "category": "求职冲刺", "tag": "面试", "title": "测试岗面试自我介绍怎么准备", "description": "测试岗自我介绍应控制在 60 到 90 秒，讲清方向、项目、测试能力和求职动机。", "keyword": "测试岗自我介绍", "problem": "自我介绍不是复述简历，而是给面试官一个追问入口。太长会散，太短又看不出岗位匹配。", "method": "按个人背景、目标岗位、项目经历、测试能力、期待方向五句话组织。每句话都要能接上后续追问。", "steps": ["说明学历或转行背景。", "明确应聘测试或自动化测试。", "挑一个最相关项目。", "讲用例、接口、缺陷或报告能力。", "用一句话说明想继续提升的方向。"], "prompt": "请根据我的简历，生成 60 秒测试岗自我介绍。要求自然、真实、能引导面试官追问项目，不要夸大。", "mistakes": ["背诵过于官方。", "讲兴趣太多，岗位匹配太少。", "没有提可追问项目。"], "sources": source("google_helpful", "baidu_page")},
    {"slug": "bug-report-writing", "group": "career", "category": "求职冲刺", "tag": "缺陷报告", "title": "缺陷报告怎么写清复现步骤", "description": "缺陷报告要包含环境、前置条件、复现步骤、实际结果、预期结果、附件和影响范围。", "keyword": "缺陷报告编写规范", "problem": "缺陷报告写不清，开发就难复现，沟通成本会很高。好报告不是情绪表达，而是可验证事实。", "method": "报告按环境、版本、账号、前置数据、步骤、实际结果、预期结果、截图日志和影响范围来写。", "steps": ["先确认问题可复现。", "记录浏览器、环境和账号。", "步骤写成一条一条动作。", "实际结果和预期结果分开。", "附截图、日志或接口响应。"], "prompt": "请把我的问题描述改成规范缺陷报告，包含环境、前置条件、复现步骤、实际结果、预期结果和附件说明。", "mistakes": ["只写有 bug。", "步骤跳跃，别人无法复现。", "没有环境和版本信息。"], "sources": source("google_helpful", "baidu_quality")},
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


# Optimized renderer v2. The definitions below intentionally replace the
# first-pass renderer above while keeping the article data in one file.
SITE_NAME = "AI效率资源站"
SITE_DESCRIPTION = "面向大学生和职场新人的 AI 学习、求职与工具资源库"
DEFAULT_IMAGE = "assets/images/favicon.png"
FEATURED_SLUGS = [
    "cet-14-day-study-plan",
    "automation-test-interview-roadmap",
    "prompt-four-part-formula",
    "final-paper-outline-ai",
    "ai-resume-polish-guide",
    "ai-account-security-checklist",
]
GROUP_PAGE_COPY = {
    "campus": {
        "title": "校园效率区",
        "description": "校园效率区整理四六级备考、期末作业、活动策划和小组协作文章。",
        "lead": "把 AI 当成学习助教：拆计划、搭框架、查漏洞，但不替代自己的学习过程。",
        "buckets": [
            ("四六级备考", ["cet-14-day-study-plan", "cet-writing-template-safe-use", "cet-listening-review-method", "cet-reading-question-strategy", "cet-translation-common-patterns"]),
            ("期末作业", ["final-paper-topic-selection", "final-paper-outline-ai", "course-report-source-check", "ai-homework-integrity", "presentation-defense-prep"]),
            ("校园协作", ["club-event-plan-structure", "campus-singer-event-plan", "activity-budget-table", "club-promo-copywriting", "student-time-management-ai", "exam-wrong-question-review", "undergraduate-project-proposal", "group-assignment-collaboration"]),
        ],
    },
    "career": {
        "title": "求职冲刺区",
        "description": "求职冲刺区整理自动化测试面试、简历优化、项目表达和模拟面试文章。",
        "lead": "面向应届生和转行新人，把简历、面试和项目表达做成可练习、可复盘的流程。",
        "buckets": [
            ("自动化测试", ["automation-test-interview-roadmap", "ui-automation-flaky-answer", "api-test-auth-token", "api-assertion-design", "pytest-parametrize-fixture", "selenium-explicit-wait", "test-report-logs-screenshots", "ci-smoke-testing", "database-validation-testing"]),
            ("简历项目", ["test-resume-project-description", "ai-resume-polish-guide", "fresh-graduate-project-star", "no-internship-resume"]),
            ("面试表达", ["test-interview-self-introduction", "bug-report-writing", "qa-learning-roadmap", "mock-interview-prompt"]),
        ],
    },
    "tools": {
        "title": "AI 工具箱",
        "description": "AI 工具箱整理 GPT/Claude 入门、提示词模板、资料核验和账号安全文章。",
        "lead": "给 AI 工具新手准备的合规使用路径：先理解任务，再写提示词，最后核验结果。",
        "buckets": [
            ("Prompt 模板", ["gpt-claude-beginner-differences", "prompt-four-part-formula", "ai-summary-prompt", "ai-writing-polish-prompt", "ai-study-plan-prompt", "ai-meeting-notes-prompt", "ai-table-analysis-prompt"]),
            ("安全核验", ["ai-account-security-checklist", "prompt-injection-basics", "sensitive-info-redaction", "ai-result-verification"]),
            ("资料整理", ["ai-search-research-workflow", "personal-knowledge-base-ai", "ai-ppt-outline-prompt", "ai-weekly-review"]),
        ],
    },
}
STATIC_PAGES = {
    "about.html": {
        "title": "关于本站",
        "description": "了解 AI效率资源站的定位、内容边界和编辑原则。",
        "eyebrow": "About",
        "lead": "AI效率资源站面向大学生、应届生和职场新人，整理 AI 学习、求职和工具使用资料。",
        "sections": [
            ("内容定位", "本站关注可执行的效率方法，例如学习计划、资料整理、简历表达、面试准备、提示词模板和工具对比。内容可以由 AI 辅助起草，但发布前会围绕准确性、可执行性和合规边界进行人工整理。"),
            ("内容边界", "本站不提供替做作业、违反考试规则、学术不端、规避平台规则、账号买卖或任何可能伤害用户账号与设备安全的教程。"),
            ("后续计划", "第一版先验证内容方向和页面结构。后续会根据搜索数据补充专题页、下载型清单、工具清单和更细的学习路线。"),
        ],
    },
    "privacy.html": {
        "title": "隐私政策与 Cookie 声明",
        "description": "AI效率资源站隐私政策，向用户说明第三方广告 Cookie 收集、Google 个性化广告退订方式及隐私合规说明。",
        "eyebrow": "Privacy",
        "lead": "本隐私声明根据 Google AdSense 规范定制，向您透明化展示本网站及其合作伙伴关于 Cookie 与隐私保护的技术细节。",
        "sections": [
            ("Cookie 及同类技术的使用", "本站为免费提供学习与求职资源的静态网站。为了优化浏览体验并展示契合您个人偏好的广告内容，本站及第三方供应商（包括 Google 等广告发布商）可能会在您的浏览器中存储和读取 Cookie，或者使用网络信标（Web Beacons）收集与数据分析相关的日志信息。"),
            ("第三方广告供应商与 Google AdSense 说明", "1. Google 等第三方供应商会依据您此前访问本网站或其他网站的历史记录，使用 Cookie 向您投放广告；\n2. Google 对广告 Cookie 的合理使用，使其及其合作伙伴能够根据您对本站和/或互联网上其他网站的访问行为，向您精准投放更具相关性的广告；\n3. 如果您不希望接收个性化广告投放，可以随时通过访问 [Google 广告设置页面(https://www.google.com/settings/ads)] 停用该功能；\n4. 您也可以通过访问 [AboutAds 行业标准退订页面(https://www.aboutads.info)]，一键式选择停用或拒绝接受第三方广告供应商使用个性化广告 Cookie。"),
            ("GDPR 与 CCPA 数据选择权保障", "对于来自欧盟地区（GDPR）或加利福尼亚州（CCPA）等拥有严格隐私权法案国家与地区的用户，本站全面支持您的选择权利。若您在首页面或通过浏览器设置拒绝第三方跟踪，我们只会向您展示非个性化的泛用型赞助广告。您可随时在浏览器偏好设置中彻底清除已留存的 Cookie。"),
            ("信息保护与联系方式", "本站属于无需注册的静态演示项目，不收集诸如银行账户、密码或实名证件等任何个人敏感隐私信息。如果您因内容纠错、资源共建等目的主动向我们发送电子邮件，您邮件内包含的所有联系方式与信件内容均仅在必要合理范围内用于沟通，绝不向第三方透露或转售。"),
        ],
    },
    "contact.html": {
        "title": "联系合作",
        "description": "联系 AI效率资源站，进行内容建议、资源合作或广告合作咨询。",
        "eyebrow": "Contact",
        "lead": "欢迎提供选题建议、资料纠错、工具推荐和合规广告合作。",
        "sections": [
            ("合作类型", "可沟通内容共创、工具测评、合规联盟链接和广告位合作。暂不接受灰色工具、账号交易、规避规则或夸大收益类推广。"),
            ("联系方式", "邮箱：contact@example.com。如需内容合作或反馈文章选题，请通过邮箱说明需求和联系信息。"),
        ],
    },
}


def slug_to_article() -> dict[str, dict]:
    return {item["slug"]: item for item in ARTICLES}


def site_path(path: str) -> str:
    return f"{SITE_URL}/{path}" if path else f"{SITE_URL}/"


def path_prefix(path: str) -> str:
    return "../" if path.startswith("articles/") else ""


def image_file_from_src(src: str) -> Path:
    clean = src.replace("../", "")
    return ROOT / clean


def webp_path(src: str) -> str:
    return re.sub(r"\.(jpg|jpeg|png)$", ".webp", src, flags=re.I)


def image_dimensions(src: str) -> tuple[int, int]:
    try:
        from PIL import Image
        with Image.open(image_file_from_src(src)) as img:
            return img.size
    except Exception:
        return (1200, 675)


def ensure_webp_images() -> None:
    try:
        from PIL import Image
    except Exception:
        return
    for meta in IMAGES.values():
        src = image_file_from_src(meta["src"])
        target = src.with_suffix(".webp")
        if not src.exists():
            continue
        with Image.open(src) as img:
            img.convert("RGB").save(target, "WEBP", quality=78, method=6)


def json_script(data: dict | list) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def structured_webpage(name: str, description: str, path: str, page_type: str = "WebPage") -> dict:
    return {
        "@context": "https://schema.org",
        "@type": page_type,
        "name": name,
        "description": description,
        "url": site_path(path),
        "inLanguage": "zh-CN",
        "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": site_path("")},
    }


def meta_head(title: str, description: str, path: str, og_type: str = "website", image: str = DEFAULT_IMAGE, schema: dict | list | None = None, robots: str = "index, follow") -> str:
    prefix = path_prefix(path)
    canonical = site_path(path)
    image_url = site_path(image.replace("../", ""))
    schema_html = f'\n  <script type="application/ld+json">{json_script(schema)}</script>' if schema else ""
    return f"""  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="{esc(robots)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:locale" content="zh_CN">
  <meta property="og:type" content="{esc(og_type)}">
  <meta property="og:site_name" content="{SITE_NAME}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(image_url)}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{esc(image_url)}">
  <link rel="icon" href="{prefix}assets/images/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="{prefix}assets/images/apple-touch-icon.png">
  <link rel="stylesheet" href="{prefix}assets/styles.css">{schema_html}"""


def header_html(prefix: str = "") -> str:
    return f'<a class="skip-link" href="#main">跳到正文</a>\n  <header class="site-header"><div class="nav-wrap"><a class="brand" href="{prefix}index.html" aria-label="{SITE_NAME}首页"><span class="brand-mark">AI</span><span>{SITE_NAME}</span></a><nav class="site-nav" data-site-nav aria-label="主导航"></nav></div></header>'


def footer_html(prefix: str = "") -> str:
    return f'<footer class="site-footer"><div class="footer-inner" data-site-footer></div></footer><script src="{prefix}assets/site.js"></script>'


def article_card(article: dict, prefix: str = "") -> str:
    accent = GROUPS[article["group"]]["accent"]
    return f"""<article class="article-card {accent}" data-group="{esc(article['group'])}" data-tag="{esc(article['tag'])}">
  <div class="tag-list"><span class="tag free">免费文章</span><span class="tag">{esc(article['tag'])}</span></div>
  <h2>{esc(article['title'])}</h2>
  <p>{esc(article['description'])}</p>
  <a class="card-link" href="{prefix}{article_url(article['slug'])}">阅读文章</a>
</article>"""


def quick_answer(article: dict) -> str:
    group = article["group"]
    keyword = article["keyword"]
    tag = article["tag"]
    problem = article["problem"].rstrip("。")
    method = article["method"].rstrip("。")
    steps = article["steps"]

    if group == "campus":
        return (
            f"对于许多在“{tag}”中面临瓶颈或感到焦虑的在校大学生来说，面临的主要问题是：{problem}。"
            f"本指南提供的核心解决思路是：{method}。为了确保实践时绝无遗漏，"
            f"我们建议你将任务拆解为包含首步“{steps[0].rstrip('。')}”在内的 {len(steps)} 个关键执行动作，"
            f"并在每阶段完成后，对照我们提供的深度执行清单进行量化自评，彻底规避学术越界风险。"
        )
    elif group == "career":
        return (
            f"在求职准备或针对“{tag}”的技术技能提升中，很多求职者最大的痛点在于：{problem}。"
            f"对此，本篇指南向你推荐的系统级突破方案为：{method}。"
            f"我们已将整体流程拆解为包含“{steps[0].rstrip('。')}”在内的 {len(steps)} 项连贯动作，"
            f"并融合了高频面试追问与简历量化STAR原则，助你在面对面试官时展现出扎实的实际排错思维与工程素养。"
        )
    else:
        return (
            f"在大语言模型或 AI 交互工具的使用中，针对“{tag}”场景下高频出现的困境：{problem}，"
            f"本站梳理出的最佳执行策略是：{method}。在实操时，"
            f"建议以本指南给出的“{steps[0].rstrip('。')}”为出发点，规范你的输入约束（如四段式 Prompt）与边界核验，"
            f"把 AI 从简单的‘单次问答’改造成高确定性、高复用度的‘生产力共创底座’。"
        )


def execution_items(article: dict) -> list[str]:
    steps = article["steps"]
    group = article["group"]
    keyword = article["keyword"]

    items = []
    if group == "campus":
        items.append(f"仔细研读课程评分标准或考试说明，明确“{keyword}”的核心通过分值与答题/作业规范。")
        items.append(f"整理出个人真实的薄弱真题、待解决题目或课程数据，作为本次训练的唯一输入材料。")
        if len(steps) >= 3:
            items.append(f"执行第一步：{steps[0].rstrip('。')}，通过小样本验证方法的有效性。")
            items.append(f"执行中期步骤：{steps[1].rstrip('。')} 与 {steps[2].rstrip('。')}，完成核心内容编写。")
        else:
            items.append(f"核心实操步骤：依据文中指引，立即完成关于“{steps[0]}”的行动动作。")
        items.append("对照学校与任课老师的学术诚信守则，确保没有超出合理辅助边界，不留学术安全漏洞。")
    elif group == "career":
        items.append(f"对标目标求职岗位 JD 描述，找出面试官或架构师针对“{keyword}”最看重的核心考察能力点。")
        items.append(f"梳理出自己过往经历中真实的测试日志、错误堆栈、代码配置或数据环境，杜绝空泛描述。")
        if len(steps) >= 3:
            items.append(f"执行前期备战：{steps[0].rstrip('。')}，确保简历项目具有可追问的底层细节。")
            items.append(f"执行核心精进：{steps[1].rstrip('。')} 与 {steps[2].rstrip('。')}，夯实异常排查机制。")
        else:
            items.append(f"核心实操步骤：按照“{steps[0]}”的技术流程，在本地或测试环境完成脚本部署。")
        items.append("运用 STAR 结构重新提炼面试表述，对每项产出进行逻辑闭环自检，确保所有技术词都具备实战依据。")
    else:
        items.append(f"明确“{keyword}”的主体任务边界，并基于‘四段式公式’撰写包含角色、目标与格式的初始 Prompt。")
        items.append(f"准备高纯度的上下文参考材料，剔除无用冗余信息，并显式禁止 AI 捏造任何外部链接与陈旧事实。")
        if len(steps) >= 3:
            items.append(f"开始第一轮交互：重点实施‘{steps[0].rstrip('。')}’，获取高确定性的初步框架。")
            items.append(f"开启迭代校验：执行‘{steps[1].rstrip('。')}’及‘{steps[2].rstrip('。')}’，逼近终极期望交付物。")
        else:
            items.append(f"核心交互动作：通过‘{steps[0]}’来训练并约束模型的生成风格。")
        items.append("执行多平台或官方文档级别的盲测校验，重点筛查大模型因幻觉生成的虚假接口、函数名或配置属性。")
    return items


def deep_dive(article: dict) -> str:
    group = article["group"]
    keyword = article["keyword"]
    tag = article["tag"]
    problem = article["problem"].rstrip("。")
    method = article["method"].rstrip("。")

    if group == "campus":
        return (
            f"在深度优化“{keyword}”的进程中，我们必须高度重视学术诚信与课程大纲的配合度。"
            f"许多在校生容易陷入{problem}的焦灼状态，原因多在于追求‘走捷径’而丧失了独立思考能力。通过采取“{method}”的渐进式方法，"
            f"我们可以用 AI 整理繁冗数据、构建时间表或查找语法拼写错误，但要把关观点论证、个人真实体验与最终的定稿判断。"
            f"在应对‘{tag}’相关期末或等级性挑战时，将 AI 视作激发思维的智能教练，而不是代笔，才能获得真正的自我成长。"
        )
    elif group == "career":
        return (
            f"在求职准备和面试应对中，面对“{keyword}”这一典型考察点，"
            f"多数候选人常因{problem}而在回答时显得过于理论化。采用“{method}”的实践逻辑，"
            f"能帮你从底层打通‘理论与实战的壁垒’。面试官在评估你的‘{tag}’素养时，真正关心的是你在系统运行异常、"
            f"执行效率受限时的排错路线图和故障复原思路。因此，务必以真实的工程态度去沉淀脚本文档和日志堆栈，做到有据可查、经得起层层追问。"
        )
    else:
        return (
            f"在日常办公或软件研发中使用 AI，要时刻牢记‘精细化交互’的原则。攻克“{keyword}”这一效能卡点时，"
            f"若发生{problem}的现象，往往是因为对大语言模型的提问过于空泛。引入“{method}”的工程化工作流，"
            f"不仅能帮我们获取高质量的首轮反馈，还能帮助我们在处理‘{tag}’高频重复操作时快速提取公共逻辑。"
            f"时刻对大模型输出保持怀疑态度，坚持‘零信任、严核验’，才能让技术工具稳定地为你创造核心业务价值。"
        )


def faq_items(article: dict) -> list[tuple[str, str]]:
    group = article["group"]
    keyword = article["keyword"]
    tag = article["tag"]
    problem = article["problem"].rstrip("。")
    method = article["method"].rstrip("。")
    steps = article["steps"]

    faqs = []
    if group == "campus":
        faqs.append((
            f"用 AI 辅助“{keyword}”备考或完成作业，如何彻底避免学术不端与挂科风险？",
            f"核心在于分清“辅助”与“代替”。你可以让 AI 扮演辅导老师，协助你做学习计划（如我们的第一步：{steps[0]}）或用特定概念启发提纲。但绝对不能将 AI 直接生成的长篇文字直接粘贴为作业提交，且论文引用应一律以人工核验后的纸质教材、知网、谷歌学术等权威源文献为准。"
        ))
        faqs.append((
            f"针对“{tag}”模块复习时发现自己知识储备薄弱、做题正确率极低，该如何挽救？",
            f"这往往是由于{problem}引起的。不要一味盲目刷题或背诵范文。建议按照“{method}”的路径，先进行一次彻底的错题场景归因，找到是“词汇壁垒”、“语法定位”还是“逻辑跳跃”的问题。每天集中攻克一个卡点，做透一道真题的效益远超粗放地做十套卷子。"
        ))
        faqs.append((
            f"AI 给出的学习资料、真题详解、参考文献是否全都是真实可靠的？",
            "绝对不是。大语言模型经常会凭空捏造看似极为真实的文献名称、作者、年份或考试大纲数据（行业内称为“幻觉”）。在使用 AI 推送的任何公式、背景常识或文化典故之前，必须前往教育部官方网站、中国教育考试网等权威出处进行二次核验，不可未经考证即写入作业。"
        ))
    elif group == "career":
        faqs.append((
            f"在技术面试中，如果面试官针对我的“{keyword}”简历描述进行压力追问该怎么以STAR格式完美应对？",
            f"面试官旨在揭穿编造的简历。你可以基于我们提供的“{method}”，结合你在项目实战中的真实痛点（如：{problem}）来回答。例如：“在进行{steps[0].rstrip('。')}时，遇到了环境依赖冲突导致失败。我通过分析测试日志和源码定位，采用了显式等待/会话封装机制解决，最终实现了交付成果。”"
        ))
        faqs.append((
            f"如何把“{tag}”的项目经历修改得极具含金量，并且不容易在海投时被HR的AI初筛直接过滤掉？",
            f"避免写‘负责某系统的手工测试/编码’等划水句。要写出高含金量的动作与量化成果。建议采用：‘引入“{method}”优化{keyword}工作流，针对协议鉴权和高频异常场景设计自动化覆盖用例，编写高可用公共脚本，缩短提缺陷确认耗时，并使脚本长期误报率降至极低。’"
        ))
        faqs.append((
            f"本地自学或在校期间没有大厂正规实习经历，如何在简历中证明我在“{keyword}”上的工程实力？",
            "大厂注重的是正规的规范与工程习惯。你可以自己在本地或借助个人云搭建完整的 CI/CD 测试流：将编写的测试用例、配置文件、失败截图、测试报告及缺陷记录，完整、优雅地呈现在你的个人 GitHub 仓库上，并在简历上附上链接。这种公开的工程文档，说服力极大。"
        ))
    else:
        faqs.append((
            f"用 AI 跑“{keyword}”的相关工作，大模型总是答非所问、输出毫无深度甚至胡说八道，怎么破？",
            f"这多是因为你的 Prompt 缺乏对任务背景和模型角色的严格限定。请立刻尝试我们提供的‘四段式 Prompt 公式’：在首轮输入时明确给足真实约束材料，命令 AI 扮演资深专家角色，并分步引导其首先完成“{steps[0]}”这一具体分支任务。通过增设 Limit 限制，强制其标注不确定信息。"
        ))
        faqs.append((
            f"在处理公司的“{tag}”任务、周报或代码段时，如何妥善防范敏感机密信息泄露的数据合规风险？",
            "这是不可触碰的合规红线！严禁向任何云端 AI 接口发送包含公司未公开源码、客户个人真实隐私数据、真实鉴权 Token 或内部服务器 IP 连接串的信息。提问前，务必对输入内容进行彻底的本地脱敏，将一切真实变量改写为虚拟占位符（如 placeholder_var1 ），确保公司机密万无一失。"
        ))
        faqs.append((
            f"随着 AI 模型与提示词技巧的频繁更新迭代，如何建立自己关于“{keyword}”的长久核心效能护城河？",
            f"不要只做‘提示词收藏家’，而要学习底层的业务逻辑与模型微调边界。无论模型如何迭代，其需要的依旧是高质量的上下文输入和明确的输出验证机制。掌握我们推荐的“{method}”核心流，能让你在不同工具（GPT-4、Claude-3.5、各类 IDE 插件）间无缝切换，成为高效驾驭 AI 的超级个体。"
        ))
    return faqs


def article_schema(article: dict, path: str, image: str) -> list[dict]:
    group = GROUPS[article["group"]]
    faq = faq_items(article) if article["group"] in {"career", "tools"} else []
    schemas: list[dict] = [
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": article["title"],
            "description": article["description"],
            "image": site_path(image.replace("../", "")),
            "datePublished": TODAY,
            "dateModified": TODAY,
            "author": {"@type": "Organization", "name": SITE_NAME},
            "publisher": {"@type": "Organization", "name": SITE_NAME, "logo": {"@type": "ImageObject", "url": site_path(DEFAULT_IMAGE)}},
            "mainEntityOfPage": site_path(path),
            "inLanguage": "zh-CN",
            "articleSection": group["label"],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "首页", "item": site_path("")},
                {"@type": "ListItem", "position": 2, "name": group["label"], "item": site_path(group["page"])},
                {"@type": "ListItem", "position": 3, "name": article["title"], "item": site_path(path)},
            ],
        },
    ]
    if faq:
        schemas.append({
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in faq
            ],
        })
    return schemas


def render_picture(image: dict, eager: bool = False) -> str:
    width, height = image_dimensions(image["src"])
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (
        f'<picture><source srcset="{esc(webp_path(image["src"]))}" type="image/webp">'
        f'<img src="{esc(image["src"])}" alt="{esc(image["alt"])}" width="{width}" height="{height}" loading="{loading}" decoding="async"{priority}></picture>'
    )
def custom_alt_for(article: dict) -> str:
    group = article["group"]
    title = article["title"]
    kw = article["keyword"]
    if group == "campus":
        if "四六级" in title or "cet" in article["slug"]:
            return f"大学生正在精心整理{kw}的复习桌面，笔记本旁整齐摆放着四六级真题、单词卡片和14天日程备考表"
        elif "论文" in title or "作业" in title or "开题" in title:
            return f"学生在电脑前使用 AI 辅助拆解{kw}的研究大纲，屏幕上清晰展示着论点框架、参考文献与防学术越界边界"
        elif "活动" in title or "策划" in title or "预算" in title or "歌手" in title or "社团" in title:
            return f"校园社团干部在会议室讨论{kw}的执行方案，笔记本电脑上正投射出活动的流程细节、组员分工和预算明细表"
        else:
            return f"在校学生专注进行{kw}的学习管理，桌面笔记本显示着时间管理日程与本周学习效率卡"
    elif group == "career":
        if "自动化" in title or "测试" in title or "pytest" in title or "Selenium" in title or "api" in title or "接口" in title:
            return f"软件测试工程师在双屏显示器前调试{kw}，编辑器中正运行着 pytest 框架的代码断言和异常排查日志"
        elif "简历" in title or "STAR" in title or "实习" in title:
            return f"求职者根据岗位 JD 正在优化{kw}的简历，屏幕上突出展示了符合 STAR 原则的硬核项目贡献与结果数据"
        elif "自我介绍" in title or "面试" in title or "缺陷报告" in title:
            return f"应届生正在模拟演练{kw}的面试场景，电脑中正显示着经典问题的结构化回答思路与严厉的追问预案"
        else:
            return f"职场新人使用电脑专注整理{kw}，屏幕上展示着清晰的职业技能标签与项目交付物清单"
    else: # tools
        if "GPT" in title or "Claude" in title:
            return f"电脑屏幕上展示着 {kw} 场景下的智能对话界面，分屏对比了 GPT 与 Claude 的推理输出结果"
        elif "Prompt" in title or "公式" in title:
            return f"在 AI 提示词测试工具中输入{kw}的四段式公式，屏幕上正高效输出逻辑严密的高级回复模板"
        elif "安全" in title or "脱敏" in title or "隐私" in title:
            return f"安全审计人员正在核查{kw}的数据流程，屏幕中对涉及个人或企业隐私的敏感字段做了精确的模糊脱敏"
        else:
            return f"办公桌上的显示器呈现了{kw}的自动化工作流，屏幕右侧展示着个人效率知识库的目录结构"


def custom_caption_for(article: dict) -> str:
    kw = article["keyword"]
    return f"【实战配图】{kw}的科学流程与效率工作流示意（配图经过 AI 深度解析优化，遵循 SEO 与无障碍可读性规范）。"


def render_article(article: dict) -> str:
    group = GROUPS[article["group"]]
    image = IMAGES[group["image"]]
    custom_image = {
        "src": image["src"],
        "alt": custom_alt_for(article),
        "caption": custom_caption_for(article)
    }
    path = article_url(article["slug"])
    related = related_for(article)
    all_articles = [item for item in ARTICLES if item["group"] == article["group"]]
    idx = all_articles.index(article)
    prev_item = all_articles[idx - 1] if idx > 0 else None
    next_item = all_articles[idx + 1] if idx < len(all_articles) - 1 else None
    answer = quick_answer(article)
    checklist = sentence_list(execution_items(article))
    faq = faq_items(article) if article["group"] in {"career", "tools"} else []
    faq_html = ""
    faq_toc = ""
    if faq:
        faq_toc = '<a href="#faq">FAQ</a>'
        faq_html = f'<h2 id="faq">FAQ</h2>{"".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq)}'
    if article["group"] == "campus":
        template = (
            f"【课程/考试】我目前正在准备/撰写：{article['keyword']}。\n"
            f"【当前困惑】{article['problem'].rstrip('。')}，容易抓不住重点或偏离评分标准。\n"
            f"【我的背景】我是一名在校学生，计划每天投入不超过 90 分钟，我的课程知识点/弱项是【请在此填入你的弱项/课程名】。\n"
            f"【辅助目标】请根据“{article['method'].rstrip('。')}”的策略，帮我输出一份保姆级的学习提纲/复习拆解，"
            f"必须指出第一步‘{article['steps'][0].rstrip('。')}’的具体动作、我的防学术不端边界以及可自检的交付物。"
        )
        example = (
            f"以你今天要解决的“{article['keyword']}”为例，强烈建议你不要直接让 AI 全盘生成全文。"
            f"你可以先复制上面的模板，在【背景】中写清你当下的真实薄弱点和老师的字数要求。接着，重点完成第一步“{article['steps'][0]}”。"
            f"随后，把 AI 给出的建议 and 你的教材大纲对比，确保知识框架不偏离课程重点。写完后，"
            f"务必对照我们的‘执行清单’自检是否存在‘{article['mistakes'][0]}’的雷区，这样复习才能真正产生提分效果。"
        )
    elif article["group"] == "career":
        template = (
            f"【求职岗位/技能】我正在针对“{article['keyword']}”做面试或简历项目准备，对应的核心技能标签是【{article['tag']}】。\n"
            f"【实战卡点】在过往经历中，常见的难题是：{article['problem'].rstrip('。')}。\n"
            f"【优化策略】请基于“{article['method'].rstrip('。')}”的原则，帮我将这段背景提炼为符合 STAR 结构（背景、任务、行动、结果）的面试回答/简历 Bullet Points。\n"
            f"【追问预案】请模拟严厉的面试官，列出 3 个可能针对我‘{article['steps'][0].rstrip('。')}’等动作进行深挖的专业追问，并提供对应的排错/回答思路。"
        )
        example = (
            f"假设你在准备关于“{article['keyword']}”的面试。第一步绝对不是死记硬背面经，"
            f"而是应该把上方的模板发送给 AI，并把【实战卡点】替换成你本地运行脚本或排查问题的真实经历。"
            f"着重提炼你在“{article['steps'][0]}”阶段所做出的独特技术贡献。最后，对着‘常见错误’一栏核查，"
            f"确保在回答时避开‘{article['mistakes'][0]}’等低级失误，给面试官展现出极强的专业工程素养。"
        )
    else:
        template = (
            f"【AI工具任务】我需要利用 AI 工具攻克“{article['keyword']}”的场景，正在使用【请填入如 GPT-4o/Claude 3.5 Sonnet】。\n"
            f"【输入材料】我的原始材料/上下文是【请在此粘贴你的原始材料/配置】。\n"
            f"【核心约束】1. 绝不捏造任何未提及的事实、API 或配置；2. 根据“{article['method'].rstrip('。')}”的要求，"
            f"首先引导我执行‘{article['steps'][0].rstrip('。')}’这一步；3. 用 Markdown 表格输出执行清单，并明确标注出‘需人工二次核验’的参数或链接。"
        )
        example = (
            f"若你正要借助 AI 工具来应对“{article['keyword']}”的日常工作，可以立刻执行上方的定制 Prompt。"
            f"先把你要处理的背景材料粘贴进去，指示 AI 扮演你该领域的资深顾问。在生成结果中，"
            f"重点关注它是如何落实“{article['steps'][0]}”的。拿到代码、Prompt 模板或分析报告后，"
            f"使用我们的‘边界提醒’进行校验，剔除可能存在的过时配置或虚假信息，守护你的生产力红线。"
        )
    nav_links = []
    if prev_item:
        nav_links.append(f'<a class="card-link" href="{esc(prev_item["slug"])}.html">上一篇：{esc(prev_item["title"])}</a>')
    if next_item:
        nav_links.append(f'<a class="card-link" href="{esc(next_item["slug"])}.html">下一篇：{esc(next_item["title"])}</a>')
    nav_html = "".join(nav_links)
    title = f"{article['title']} - {SITE_NAME}"
    schema = article_schema(article, path, image["src"])
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
{meta_head(title, article["description"], path, "article", image["src"], schema)}
</head>
<body data-section="{esc(article['group'])}">
  {header_html("../")}
  <main id="main">
    <section class="article-hero"><div class="section-inner"><nav class="breadcrumb" aria-label="面包屑"><a href="../index.html">首页</a><span>/</span><a href="../{group['page']}">{esc(group['label'])}</a><span>/</span><span>{esc(article['title'])}</span></nav><span class="eyebrow">{esc(group['eyebrow'])}</span><h1>{esc(article['title'])}</h1><div class="article-meta"><span>{esc(article['category'])}</span><span>更新：{TODAY}</span><span>阅读约 7 分钟</span></div></div></section>
    <section class="section tight"><div class="section-inner"><article class="conversion-card seo-summary-card"><div class="conversion-copy"><div class="offer-meta"><span class="tag hot">快速答案</span><span class="tag free">{esc(article['tag'])}</span></div><h2>{esc(article['keyword'])}怎么先做对</h2><p>{esc(answer)}</p></div><div class="conversion-action"><a class="button hot full" href="#checklist">查看执行清单</a><a class="card-link" href="../{group['page']}">返回{esc(group['label'])}专题</a></div></article></div></section>
    <section class="section"><div class="section-inner article-layout">
      <article class="article-body">
        <figure class="article-image">{render_picture(custom_image)}<figcaption>{esc(custom_image['caption'])}</figcaption></figure>
        <h2 id="who">适合谁</h2>
        <p>{esc(article['problem'])}</p>
        <p>{esc(deep_dive(article))}</p>
        <p>{esc(f"为了让{article['keyword']}更容易落地，建议把本文当成一张操作卡，而不是一次性读完就结束。第一次阅读时只做标记，第二次阅读时复制模板并填入自己的真实材料，第三次再对照执行清单检查结果。这样的节奏能减少空泛感，也能让后续复盘有依据。")}</p>
        <h2 id="answer">快速答案</h2>
        <p>{esc(answer)}</p>
        <h2 id="method">核心方法</h2>
        <p>{esc(article['method'])}</p>
        <ol>{sentence_list(article['steps'])}</ol>
        <h2 id="checklist">执行清单</h2>
        <ul>{checklist}</ul>
        <h2 id="example">实操示例</h2>
        <p>{esc(example)}</p>
        <h2 id="template">可复制模板</h2>
        <p>下面这段模板适合直接复制到 AI 工具里，再把括号中的内容替换成自己的真实材料。输出后仍然要人工核验，尤其是涉及考试规则、工具版本、招聘要求和安全边界的信息。</p>
        <div class="code-block-wrapper">
          <pre><code>{esc(template)}</code></pre>
          <button class="copy-button" type="button" aria-label="复制模板">复制</button>
        </div>
        <p>{esc(article['prompt'])}</p>
        <h2 id="mistakes">常见错误</h2>
        <ul>{sentence_list(article['mistakes'])}</ul>
        <p>如果你发现自己反复遇到这些问题，不要急着增加更多资料。更有效的做法是回到任务目标，把输入材料、完成标准和检查动作补齐。搜索来的内容只能提供参考，最终是否适合你的课程、项目或岗位，还要结合自己的真实场景判断。</p>
        <h2 id="boundary">边界提醒</h2>
        <p>本站内容用于学习规划、效率提升和表达训练。涉及课程要求、考试安排、招聘信息、工具政策和安全风险时，应以官方说明、原始资料或任课老师要求为准。AI 可以帮助拆解任务、检查遗漏和优化表达，但不应替代个人判断，也不应生成无法核验的事实。</p>
        {faq_html}
        <h2 id="sources">参考来源</h2>
        <ul>{source_list(article['sources'])}</ul>
        <h2 id="related">相关文章</h2>
        <ul>{''.join(f'<li><a href="{esc(item["slug"])}.html">{esc(item["title"])}</a></li>' for item in related)}</ul>
        <nav class="article-pager" aria-label="文章翻页">{nav_html}</nav>
      </article>
      <aside class="sidebar"><nav class="toc"><strong>目录</strong><a href="#who">适合谁</a><a href="#answer">快速答案</a><a href="#method">核心方法</a><a href="#checklist">执行清单</a><a href="#example">实操示例</a><a href="#template">可复制模板</a><a href="#mistakes">常见错误</a><a href="#boundary">边界提醒</a>{faq_toc}<a href="#sources">参考来源</a></nav><div class="ad-slot" data-ad-slot></div></aside>
    </div></section>
  </main>
  {footer_html("../")}
</body>
</html>
"""


def render_group_page(group_key: str, title: str | None = None, description: str | None = None, lead: str | None = None) -> str:
    meta = GROUP_PAGE_COPY[group_key]
    group = GROUPS[group_key]
    items = [item for item in ARTICLES if item["group"] == group_key]
    title = title or meta["title"]
    description = description or meta["description"]
    lead = lead or meta["lead"]
    cards = "\n".join(article_card(item) for item in items)
    buckets = []
    by_slug = slug_to_article()
    for bucket_title, slugs in meta["buckets"]:
        links = "".join(f'<li><a href="{article_url(by_slug[slug]["slug"])}">{esc(by_slug[slug]["title"])}</a></li>' for slug in slugs if slug in by_slug)
        buckets.append(f'<article class="resource-card"><h3>{esc(bucket_title)}</h3><ul class="compact-list">{links}</ul></article>')
    schema = structured_webpage(title, description, group["page"], "CollectionPage")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
{meta_head(f"{title} - {SITE_NAME}", description, group["page"], "website", DEFAULT_IMAGE, schema)}
</head>
<body data-section="{esc(group_key)}">
  {header_html()}
  <main id="main">
    <section class="article-hero"><div class="section-inner"><span class="eyebrow">{esc(group['eyebrow'])}</span><h1>{esc(title)}</h1><p class="hero-lede">{esc(lead)}</p></div></section>
    <section class="section"><div class="section-inner"><article class="offer-card seo-focus-card"><div class="offer-copy"><div class="offer-meta"><span class="tag hot">专题导航</span><span class="tag free">{len(items)} 篇文章</span></div><h2>先按主题找入口，再进入具体问题</h2><p>本专题按搜索问题拆分文章，每篇都给快速答案、执行清单、模板、常见错误和参考来源。</p></div><div class="offer-action"><a class="button hot" href="articles.html?group={group_key}">查看本专题全部文章</a><a class="card-link" href="{article_url(items[0]['slug'])}">先读：{esc(items[0]['tag'])}</a></div></article></div></section>
    <section class="section tight"><div class="section-inner"><div class="section-head"><div><h2>{esc(title)}分组导航</h2><p>优先从最接近你当前问题的分组进入，减少无效浏览。</p></div></div><div class="grid three">{"".join(buckets)}</div></div></section>
    <section class="section tight"><div class="section-inner"><div class="section-head"><div><h2>{esc(title)}文章列表</h2><p>所有文章均为免费阅读，优先解决一个具体问题，避免空泛堆词。</p></div></div><div class="grid three">{cards}</div></div></section>
  </main>
  {footer_html()}
</body>
</html>
"""


def render_index() -> str:
    cards = "\n".join(article_card(next(item for item in ARTICLES if item["slug"] == slug)) for slug in FEATURED_SLUGS)
    latest = "\n".join(article_card(item) for item in ARTICLES[-6:])
    schema = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "description": SITE_DESCRIPTION,
        "url": site_path(""),
        "inLanguage": "zh-CN",
        "potentialAction": {"@type": "SearchAction", "target": site_path("articles.html") + "?q={search_term_string}", "query-input": "required name=search_term_string"},
    }
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
{meta_head(f"{SITE_NAME} - 大学生与职场新人的 AI 学习求职导航", "AI效率资源站面向大学生和职场新人，提供 AI 学习方法、求职准备、提示词模板和工具安全内容。", "", "website", DEFAULT_IMAGE, schema)}
</head>
<body>
  {header_html()}
  <main id="main">
    <section class="hero"><div class="section-inner"><div class="hero-copy"><span class="eyebrow">AI efficiency hub</span><h1><span class="hero-line">把 AI 变成学习、</span><span class="hero-line">求职和日常工作</span><span class="hero-line">的效率工具。</span></h1><p class="hero-lede"><span class="mobile-line">这里专注大学生和职场新人的真实问题：</span><span class="mobile-line">备考、作业、简历、面试、提示词和账号安全。</span><span class="mobile-line">每篇文章都给快速答案、执行清单、模板和参考来源。</span></p><div class="hero-actions"><a class="button hot" href="articles.html">浏览全部文章</a><a class="button" href="career.html">查看求职专题</a><a class="button secondary" href="tools.html">学习 AI 工具</a></div></div><aside class="hero-panel" aria-label="站点内容概览"><div class="metric-grid"><div class="metric"><strong>50</strong><span>长文文章</span></div><div class="metric"><strong>3</strong><span>核心专题</span></div><div class="metric"><strong>0</strong><span>依赖构建</span></div></div></aside></div></section>
    <section id="sections" class="section"><div class="section-inner"><div class="section-head"><div><h2>三类人群，一套效率资源</h2><p>按校园、求职和 AI 工具三条路径组织内容，先解决真实问题，再整理成可复用方法。</p></div><a class="card-link" href="articles.html">进入全站索引</a></div><div class="grid three"><article class="card accent-green"><h3>校园效率区</h3><p>四六级、期末作业、活动策划和小组协作。</p><div class="tag-list"><span class="tag free">18 篇</span><span class="tag">大学生</span></div><a class="card-link" href="campus.html">进入专区</a></article><article class="card accent-blue"><h3>求职冲刺区</h3><p>自动化测试、简历、项目表达和模拟面试。</p><div class="tag-list"><span class="tag free">17 篇</span><span class="tag">应届生</span></div><a class="card-link" href="career.html">进入专区</a></article><article class="card accent-amber"><h3>AI 工具箱</h3><p>GPT/Claude 入门、Prompt、资料整理和账号安全。</p><div class="tag-list"><span class="tag free">15 篇</span><span class="tag">AI 工具</span></div><a class="card-link" href="tools.html">进入专区</a></article></div></div></section>
    <section class="section feature-band"><div class="section-inner"><div class="section-head"><div><h2>精选支柱文章</h2><p>先从搜索需求最明确的文章读起，再进入专题页继续延伸。</p></div></div><div class="grid three">{cards}</div></div></section>
    <section class="section tight"><div class="section-inner"><div class="section-head"><div><h2>最新整理</h2><p>持续补充围绕学习、求职和工具核验的长尾问题。</p></div></div><div class="grid three">{latest}</div></div></section>
  </main>
  {footer_html()}
</body>
</html>
"""


def render_articles_index() -> str:
    cards = "\n".join(article_card(item) for item in ARTICLES)
    schema = structured_webpage("全部文章", "AI效率资源站全部文章索引，支持按专题、标签和关键词筛选。", "articles.html", "CollectionPage")
    tags = sorted({item["tag"] for item in ARTICLES})
    tag_buttons = "".join(f'<button class="filter-chip" type="button" data-filter-tag="{esc(tag)}">{esc(tag)}</button>' for tag in tags)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
{meta_head(f"全部文章 - {SITE_NAME}", "AI效率资源站全部文章索引，支持按校园、求职、AI 工具和关键词筛选。", "articles.html", "website", DEFAULT_IMAGE, schema)}
</head>
<body data-section="articles">
  {header_html()}
  <main id="main">
    <section class="article-hero"><div class="section-inner"><span class="eyebrow">Index</span><h1>全部文章</h1><p class="hero-lede">按专题、标签和关键词快速找到学习、求职和 AI 工具相关长文。</p></div></section>
    <section class="section tight"><div class="section-inner"><div class="search-panel" data-search-panel><label for="article-search">搜索文章</label><input id="article-search" type="search" placeholder="输入四六级、简历、Prompt、安全等关键词" autocomplete="off"><div class="filter-row" aria-label="专题筛选"><button class="filter-chip is-active" type="button" data-filter-group="all">全部</button><button class="filter-chip" type="button" data-filter-group="campus">校园</button><button class="filter-chip" type="button" data-filter-group="career">求职</button><button class="filter-chip" type="button" data-filter-group="tools">工具</button></div><div class="filter-row tag-filter" aria-label="标签筛选"><button class="filter-chip is-active" type="button" data-filter-tag="all">全部标签</button>{tag_buttons}</div><p class="search-count" data-search-count>共 50 篇文章</p></div></div></section>
    <section class="section tight"><div class="section-inner"><div class="grid three" data-article-index>{cards}</div></div></section>
  </main>
  {footer_html()}
</body>
</html>
"""


def render_static_page(path: str, meta: dict) -> str:
    sections = "".join(f"<h2>{esc(title)}</h2><p>{esc(body)}</p>" for title, body in meta["sections"])
    schema = structured_webpage(meta["title"], meta["description"], path, "AboutPage" if path == "about.html" else "WebPage")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
{meta_head(f"{meta['title']} - {SITE_NAME}", meta["description"], path, "website", DEFAULT_IMAGE, schema)}
</head>
<body>
  {header_html()}
  <main id="main">
    <section class="article-hero"><div class="section-inner"><span class="eyebrow">{esc(meta['eyebrow'])}</span><h1>{esc(meta['title'])}</h1><p class="hero-lede">{esc(meta['lead'])}</p></div></section>
    <section class="section"><div class="section-inner article-body">{sections}</div></section>
  </main>
  {footer_html()}
</body>
</html>
"""


def render_404() -> str:
    schema = structured_webpage("页面未找到", "AI效率资源站 404 页面，帮助用户返回文章索引或首页。", "404.html", "WebPage")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
{meta_head(f"页面未找到 - {SITE_NAME}", "页面未找到，可以返回 AI效率资源站首页或全部文章索引继续浏览。", "404.html", "website", DEFAULT_IMAGE, schema, "noindex, follow")}
</head>
<body>
  {header_html()}
  <main id="main">
    <section class="article-hero"><div class="section-inner"><span class="eyebrow">404</span><h1>页面未找到</h1><p class="hero-lede">这个链接可能已经移动。你可以返回首页，或者进入全部文章索引继续查找。</p><div class="hero-actions"><a class="button hot" href="articles.html">浏览全部文章</a><a class="button secondary" href="index.html">返回首页</a></div></div></section>
  </main>
  {footer_html()}
</body>
</html>
"""


def render_search_index() -> str:
    data = [
        {
            "title": item["title"],
            "description": item["description"],
            "href": article_url(item["slug"]),
            "group": item["group"],
            "groupLabel": GROUPS[item["group"]]["label"],
            "tag": item["tag"],
            "keyword": item["keyword"],
        }
        for item in ARTICLES
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)


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
  name: "{SITE_NAME}",
  tagline: "{SITE_DESCRIPTION}",
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
  const links = [["首页", "index.html"], ["文章", "articles.html"], ["校园", "campus.html"], ["求职", "career.html"], ["工具", "tools.html"], ["关于", "about.html"]];
  const current = location.pathname.split("/").pop() || "index.html";
  const section = document.body.dataset.section || "";
  const activeBySection = {{ campus: "campus.html", career: "career.html", tools: "tools.html", articles: "articles.html" }};
  nav.innerHTML = links.map(([label, href]) => {{
    const active = current === href || activeBySection[section] === href ? ' aria-current="page"' : "";
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
      <p>${{siteConfig.tagline}}。本站坚决抵制任何形式的学术越界或违反学术诚信的行为。所有 AI 工具使用方法均旨在辅助思路拆解与学习效率提升，最终成果的真实性与合规性完全由使用者个人负责，请严格遵守所在学校、考试中心和工作单位的守则。</p>
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
  // 1. Asynchronously load Google AdSense script once using ca-pub-7663008606677915
  if (!document.querySelector('script[src*="pagead2.googlesyndication.com"]')) {{
    const adScript = document.createElement("script");
    adScript.async = true;
    adScript.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7663008606677915";
    adScript.crossOrigin = "anonymous";
    document.head.appendChild(adScript);
  }}

  // 2. Loop through and initialize all ad containers with CLS mitigation (min-height: 250px)
  document.querySelectorAll("[data-ad-slot]").forEach((slot) => {{
    slot.innerHTML = `
      <ins class="adsbygoogle"
           style="display:block; min-height: 250px;"
           data-ad-client="ca-pub-7663008606677915"
           data-ad-slot="1234567890"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
    `;
    try {{
      (window.adsbygoogle = window.adsbygoogle || []).push({{}});
    }} catch (e) {{
      console.warn("AdSense push error:", e);
    }}
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

async function buildArticleSearch() {{
  const target = document.querySelector("[data-article-index]");
  const panel = document.querySelector("[data-search-panel]");
  if (!target || !panel) return;
  let items = [];
  try {{
    const response = await fetch(resolvePath("assets/search-index.json"));
    items = await response.json();
  }} catch (error) {{
    items = Array.from(target.querySelectorAll(".article-card")).map((card) => ({{
      title: card.querySelector("h2")?.textContent || "",
      description: card.querySelector("p")?.textContent || "",
      href: card.querySelector("a")?.getAttribute("href") || "#",
      group: card.dataset.group || "",
      tag: card.dataset.tag || "",
      keyword: card.textContent || ""
    }}));
  }}
  const input = panel.querySelector("#article-search");
  const count = panel.querySelector("[data-search-count]");
  let group = new URLSearchParams(location.search).get("group") || "all";
  let tag = "all";
  const render = () => {{
    const q = (input.value || "").trim().toLowerCase();
    const filtered = items.filter((item) => {{
      const text = `${{item.title}} ${{item.description}} ${{item.tag}} ${{item.keyword}}`.toLowerCase();
      return (group === "all" || item.group === group) && (tag === "all" || item.tag === tag) && (!q || text.includes(q));
    }});
    target.innerHTML = filtered.map((item) => `<article class="article-card" data-group="${{item.group}}" data-tag="${{item.tag}}"><div class="tag-list"><span class="tag free">免费文章</span><span class="tag">${{item.tag}}</span></div><h2>${{item.title}}</h2><p>${{item.description}}</p><a class="card-link" href="${{item.href}}">阅读文章</a></article>`).join("") || `<p class="empty-state">没有找到匹配文章，可以换一个关键词。</p>`;
    if (count) count.textContent = `共 ${{filtered.length}} 篇文章`;
  }};
  panel.querySelectorAll("[data-filter-group]").forEach((button) => {{
    if (button.dataset.filterGroup === group) button.classList.add("is-active");
    button.addEventListener("click", () => {{
      group = button.dataset.filterGroup || "all";
      panel.querySelectorAll("[data-filter-group]").forEach((el) => el.classList.toggle("is-active", el === button));
      render();
    }});
  }});
  panel.querySelectorAll("[data-filter-tag]").forEach((button) => {{
    button.addEventListener("click", () => {{
      tag = button.dataset.filterTag || "all";
      panel.querySelectorAll("[data-filter-tag]").forEach((el) => el.classList.toggle("is-active", el === button));
      render();
    }});
  }});
  input?.addEventListener("input", render);
  render();
}}

function initCopyButtons() {{
  document.querySelectorAll(".copy-button").forEach((btn) => {{
    btn.addEventListener("click", async () => {{
      const pre = btn.previousElementSibling;
      const code = pre ? (pre.querySelector("code")?.textContent || "") : "";
      try {{
        await navigator.clipboard.writeText(code);
        const originalText = btn.textContent || "复制";
        btn.textContent = "已复制！";
        btn.classList.add("copied");
        setTimeout(() => {{
          btn.textContent = originalText;
          btn.classList.remove("copied");
        }}, 2000);
      }} catch (err) {{
        console.error("Failed to copy:", err);
      }}
    }});
  }});
}}

document.addEventListener("DOMContentLoaded", () => {{
  buildNav();
  buildFooter();
  buildAdSlots();
  buildFeaturedResources();
  buildArticleSearch();
  initCopyButtons();
}});
"""


def render_sitemap() -> str:
    urls = ["", "index.html", "articles.html", "campus.html", "career.html", "tools.html", "about.html", "privacy.html", "contact.html"]
    urls += [article_url(item["slug"]) for item in ARTICLES]
    locs = "\n".join(f"  <url><loc>{site_path(url)}</loc><lastmod>{TODAY}</lastmod></url>" if url else f"  <url><loc>{site_path('')}</loc><lastmod>{TODAY}</lastmod></url>" for url in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{locs}\n</urlset>\n'


def write_site_file(path: Path, content: str) -> None:
    normalized = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")


def main() -> None:
    ensure_webp_images()
    ARTICLES_DIR.mkdir(exist_ok=True)
    for old in ARTICLES_DIR.glob("*.html"):
        old.unlink()
    for article in ARTICLES:
        write_site_file(ARTICLES_DIR / f"{article['slug']}.html", render_article(article))
    write_site_file(ROOT / "index.html", render_index())
    write_site_file(ROOT / "articles.html", render_articles_index())
    for group_key in GROUPS:
        write_site_file(ROOT / GROUPS[group_key]["page"], render_group_page(group_key))
    for path, meta in STATIC_PAGES.items():
        write_site_file(ROOT / path, render_static_page(path, meta))
    write_site_file(ROOT / "404.html", render_404())
    write_site_file(ROOT / "assets" / "site.js", render_site_js())
    write_site_file(ROOT / "assets" / "search-index.json", render_search_index())
    write_site_file(ROOT / "sitemap.xml", render_sitemap())
    write_site_file(ROOT / "assets" / "images" / "ATTRIBUTIONS.md", render_attributions())


if __name__ == "__main__":
    main()
