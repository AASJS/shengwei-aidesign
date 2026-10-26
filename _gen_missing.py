import re

src = open('/workspace/website/index.html', encoding='utf-8').read()
head = re.search(r'<head>.*?</head>', src, re.S).group(0)
head = re.sub(r'<title>.*?</title>', '<title>我能带你做 ｜ 圣为Ai设计</title>', head)

foot = ('<footer class="site-foot"><a href="index.html">首页</a> · '
        '<a href="found-me.html">找到我</a> · <a href="what-i-do.html">我能带你做</a> · '
        '<a href="closed-loop.html">闭环</a> · <a href="pain-points.html">痛点</a> · '
        '<a href="course.html">课程</a> · <a href="signup.html">报名</a> ｜ '
        '© 2026 圣为Ai设计 · 由 AI 辅助搭建</footer>')

body1 = '''<body>
<a class="back-btn" href="index.html">← 首页</a>
<header class="site-head"><div class="logo">圣为Ai设计</div><div class="slogan">把「觉照」落进一人公司的每一天</div></header>
<main class="wrap">
  <p class="intro">不卖修行功效，只卖创作系统。<br>我能陪你从一张卡片，跑通一条属于你的<b>变现闭环</b>——工具包 · 入门课 · 私域成交，一步步来。</p>

  <div class="sec-title">四件事，逐步跑通</div>
  <div class="sec-sub">从表达，到产品，不跳步</div>
  <div class="grid">
    <div class="card"><div class="num">01</div><h3>知识卡片</h3><p>用 AI 把你的经验，变成好看、能发朋友圈 / 小红书 / 公众号的图文卡。</p></div>
    <div class="card"><div class="num">02</div><h3>工具包</h3><p>零基础自助做出有质感的卡片——复制指令、改字、截图即得图，不碰设计软件。</p></div>
    <div class="card"><div class="num">03</div><h3>入门课</h3><p>0 基础也能做出能变现的知识卡片，从一张卡跑通最小闭环。</p></div>
    <div class="card"><div class="num">04</div><h3>私域成交</h3><p>把卡片沉淀成可售卖的产品 / 服务，通过私域让创作被看见、被买单。</p></div>
  </div>

  <div class="sec-title">从一张到闭环的路径</div>
  <div class="sec-sub">先把第一张做出来，比想清楚更重要</div>
  <div class="steps">
    <div class="step"><div class="n">1</div><div><div class="sh">做出来</div><div class="sp">先跑通第一张卡片，不追求完美，只求完成。</div></div></div>
    <div class="step"><div class="n">2</div><div><div class="sh">成体系</div><div class="sp">把同一主题连成一组，建立你自己的视觉语言与表达节奏。</div></div></div>
    <div class="step"><div class="n">3</div><div><div class="sh">能交付</div><div class="sp">沉淀为可重复交付的产品 / 服务，让创作可被他人购买。</div></div></div>
    <div class="step"><div class="n">4</div><div><div class="sh">跑闭环</div><div class="sp">通过私域持续触达，让每一次表达都靠近成交一步。</div></div></div>
  </div>

  <a class="enroll-btn" href="signup.html">报名课程 →</a>
</main>
''' + foot + '</body>'

body2 = '''<body>
<a class="back-btn" href="index.html">← 首页</a>
<header class="site-head"><div class="logo">圣为Ai设计</div><div class="slogan">把「觉照」落进一人公司的每一天</div></header>
<main class="wrap">
  <p class="intro">填好信息，立刻生成你的<b>「已报名」海报</b>。<br>我们会在 24 小时内通过微信联系你。</p>

  <div id="formView">
    <form class="form-card" id="signupForm">
      <div class="field"><label>你的称呼<span class="req">*</span></label><input id="f-name" type="text" placeholder="怎么称呼你" required></div>
      <div class="field"><label>微信号<span class="req">*</span></label><input id="f-wx" type="text" placeholder="方便联系的微信" required></div>
      <div class="field"><label>你最想先突破哪一步？</label>
        <div class="checks">
          <label><input type="checkbox" name="step" value="卡片"> 做知识卡片</label>
          <label><input type="checkbox" name="step" value="工具包"> 用工具包</label>
          <label><input type="checkbox" name="step" value="入门课"> 上入门课</label>
          <label><input type="checkbox" name="step" value="私域"> 私域成交</label>
        </div>
      </div>
      <div class="field"><label>想对圣为说点什么</label><textarea id="f-msg" placeholder="你的目标、卡点，或任何想聊的"></textarea></div>
      <button class="submit" type="submit">提交报名 →</button>
    </form>
  </div>

  <div id="successView" class="success">
    <div class="ok">报名成功 ✦</div>
    <p>谢谢你的信任。保存下面的海报，<b>加微信时出示</b>，我拉你进进阶课内测群。</p>
    <div class="poster-share">
      <div class="ps-seal">圣为</div>
      <div class="ps-kicker">已报名</div>
      <div class="ps-title">知识卡片入门课</div>
      <div class="ps-name" id="ps-name">报名人：朋友</div>
      <div class="ps-rule"></div>
      <div class="ps-box">从一张卡片，跑通一条变现闭环。<br>把「觉照」落进一人公司的每一天。</div>
      <div class="ps-line" id="ps-wx">微信：—</div>
      <div class="ps-date">报名于 2026 · 圣为Ai设计</div>
      <div class="ps-sign">静心知识库 ｜ @圣为Ai设计</div>
      <button class="ps-save" type="button" onclick="window.print()">保存这张海报</button>
    </div>
  </div>
</main>
''' + foot + '''
<script>
document.getElementById('signupForm').addEventListener('submit', function(e){
  e.preventDefault();
  var name = (document.getElementById('f-name').value || '').trim() || '朋友';
  var wx = (document.getElementById('f-wx').value || '').trim() || '—';
  document.getElementById('ps-name').textContent = '报名人：' + name;
  document.getElementById('ps-wx').textContent = '微信：' + wx;
  document.getElementById('formView').style.display = 'none';
  document.getElementById('successView').classList.add('show');
  window.scrollTo(0, 0);
});
</script>
</body>'''

open('/workspace/website/what-i-do.html', 'w', encoding='utf-8').write(
    '<!doctype html>\n<html lang="zh-CN">\n' + head + '\n' + body1 + '\n')
open('/workspace/website/signup.html', 'w', encoding='utf-8').write(
    '<!doctype html>\n<html lang="zh-CN">\n' + head + '\n' + body2 + '\n')

print('生成完成：what-i-do.html, signup.html')
