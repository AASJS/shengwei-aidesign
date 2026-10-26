# -*- coding: utf-8 -*-
"""
离线单文件版构建脚本（圣为Ai设计官网）
========================================
把 website/ 下的 9 个 HTML 页面合并为单个可离线打开的
「圣为Ai设计-全站离线版.html」，手机 file:// 直接打开即用。

用法：
    cd /workspace/website
    python3 scripts/build_offline.py

原理：读取 PAGES 列表 → 改写页内链接为 postMessage 导航 →
      注入高度上报脚本 → 9 页 JSON 注入外壳 → iframe.srcdoc 切换页面
      （用 srcdoc 而非 blob URL，规避手机 file:// 下 blob 被禁导致空白）
注意：改了任意一页 HTML 后必须重跑本脚本，否则离线版不会同步。
"""
import json, re, pathlib

SRC = pathlib.Path('/workspace/website')
PAGES = ['index.html','found-me.html','what-i-do.html','closed-loop.html',
         'pain-points.html','course.html','ai-start.html','juezhao.html','signup.html']
TITLES = {'index.html':'首页','found-me.html':'找到我','what-i-do.html':'我能带你做',
          'closed-loop.html':'闭环','pain-points.html':'痛点','course.html':'课程',
          'ai-start.html':'AI起跑线','juezhao.html':'觉照金句','signup.html':'报名'}
# 注：运营SOP 为公众号后台智能回复/话术配置，不对外展示，故不纳入离线版与公开导航

NAV_JS = """
(function(){
function send(m){try{parent.postMessage(m,'*');}catch(e){}}
document.addEventListener('click',function(e){
  var a=e.target&&e.target.closest?e.target.closest('[data-sgw]'):null;
  if(a){e.preventDefault();send({sgwNav:a.getAttribute('data-sgw')});}
},true);
var last=0;
/* 关键：高度只取 body.scrollHeight（真实内容高）。
   documentElement.scrollHeight 会被 iframe 当前视口高度托底，
   一旦被旧页面高度污染就永远缩不回去 → 出现大片空白仍可滑动。 */
function r(){var b=document.body;var h=b?b.scrollHeight:document.documentElement.scrollHeight;send({sgwH:h,sgwPage:'__SGW_PID__'});}
addEventListener('load',function(){r();setTimeout(r,400);setTimeout(r,1500);});
setTimeout(r,300);
addEventListener('resize',r);
new MutationObserver(function(){var now=Date.now();if(now-last>200){last=now;r();}}).observe(document.documentElement,{childList:true,subtree:true});
})();
"""

# 离线版兜底：iframe 高度=内容高，真实滚动发生在外层文档，
# 页内 IntersectionObserver 可能收不到滚动事件 → 部分内容块永不显示。
# 1.6s 后强制显示所有 data-reveal 块，宁可少个入场动画也不吞内容。
REVEAL_FALLBACK_JS = """
setTimeout(function(){try{
  var els=document.querySelectorAll('[data-reveal]');
  for(var i=0;i<els.length;i++){els[i].style.transitionDelay='0ms';els[i].classList.add('in');}
}catch(e){}},1600);
"""

# 首页自带独立导航（供线上单页使用），离线版外壳已有胶囊导航，隐藏避免重复
HIDE_INNER_NAV_CSS = "<style>#nav{display:none !important;}</style>"

def adapt(html, name):
    # 1) onclick="location.href='xxx.html'" → postMessage（带页面ID，供外壳丢弃过期消息）
    html = re.sub(r"location\.href='([a-z-]+\.html)'",
                  r"parent.postMessage({sgwNav:'\\1',sgwPage:'__SGW_PID__'},'*')", html)
    # 2) href="xxx.html" → data-sgw + void href
    html = re.sub(r'href="([a-z-]+\.html)"', r'href="javascript:void(0)" data-sgw="\1"', html)
    # 3) 注入导航/高度上报脚本 + 动画兜底 + 隐藏页内独立导航
    html = html.replace('</head>', HIDE_INNER_NAV_CSS + '\n</head>')
    html = html.replace('</body>', '<script>' + REVEAL_FALLBACK_JS + '</script>\n<script>' + NAV_JS + '</script>\n</body>')
    html = html.replace('__SGW_PID__', name)
    return html

pages_json = {}
for p in PAGES:
    raw = (SRC / p).read_text(encoding='utf-8')
    pages_json[p] = adapt(raw, p)

payload = json.dumps(pages_json, ensure_ascii=False, separators=(',',':'))
payload = payload.replace('<', '\\u003c')  # 防止 </script> 截断外壳脚本

nav_items = ''
for p in PAGES:
    cls = ' class="on"' if p == 'index.html' else ''
    nav_items += f'<button data-p="{p}"{cls}>{TITLES[p]}</button>'

shell = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>圣为Ai设计 · 全站离线版</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
html,body{background:#faf7f0;color:#2f2a26;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif;}
.nav{position:sticky;top:0;z-index:99;background:rgba(250,247,240,.96);border-bottom:1px solid #e8e1d3;
  display:flex;gap:6px;overflow-x:auto;padding:8px 10px;-webkit-overflow-scrolling:touch;scrollbar-width:none;}
.nav::-webkit-scrollbar{display:none;}
.nav button{flex:0 0 auto;border:1px solid #d8cfc0;background:#fff;color:#5a5248;font-size:13px;
  padding:6px 13px;border-radius:999px;cursor:pointer;white-space:nowrap;}
.nav button.on{background:#b5542d;border-color:#b5542d;color:#fff;font-weight:600;}
#frame-wrap{width:100%;}
iframe{width:100%;border:0;display:block;}
.loading{text-align:center;color:#9a8f80;font-size:13px;padding:40px 0;}
</style>
</head>
<body>
<nav class="nav" id="nav">__NAV_ITEMS__</nav>
<div id="frame-wrap"><iframe id="f" title="page"></iframe></div>
<script id="pages" type="application/json">__PAYLOAD__</script>
<script>
(function(){
var PAGES=JSON.parse(document.getElementById('pages').textContent);
var f=document.getElementById('f'), navbar=document.getElementById('nav');
var cur=null;
function go(k){
  if(!PAGES[k])return;
  cur=k;
  f.style.height='calc(100vh - 46px)';
  f.srcdoc=PAGES[k];
  window.scrollTo(0,0);
  var bs=navbar.querySelectorAll('button');
  for(var i=0;i<bs.length;i++){bs[i].classList.toggle('on',bs[i].getAttribute('data-p')===k);}
  var on=navbar.querySelector('button.on');
  if(on){navbar.scrollTo({left:on.offsetLeft-navbar.clientWidth/2+on.clientWidth/2,behavior:'smooth'});}
}
addEventListener('message',function(e){
  var d=e.data||{};
  /* 页面ID校验：切换页面瞬间，旧文档的 resize 仍会发来过期高度，
     不校验会把 iframe 撑高且再也回不去（空白可滑的根源之一） */
  if(d.sgwPage!==cur)return;
  if(d.sgwNav){go(d.sgwNav);}
  else if(d.sgwH&&typeof d.sgwH==='number'&&d.sgwH>50){f.style.height=d.sgwH+'px';}
});
navbar.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){go(b.getAttribute('data-p'));});});
go('index.html');
})();
</script>
</body>
</html>"""
shell = shell.replace('__NAV_ITEMS__', nav_items).replace('__PAYLOAD__', payload)

out = SRC / '圣为Ai设计-全站离线版.html'
out.write_text(shell, encoding='utf-8')
print('生成:', out, '大小:', round(out.stat().st_size/1024), 'KB')
