# 离线单文件版构建脚本

把 `website/` 下的 9 个 HTML 页面合并为单个可离线打开的 `圣为Ai设计-全站离线版.html`。

## 用途
学员在手机上用 `file://` 直接打开离线版，无需联网、无需服务器，顶部导航条切换 9 个页面。适合无网环境演示、微信转发后本地留存。

## 用法
```bash
cd /workspace/website
python3 scripts/build_offline.py
```
输出：`/workspace/website/圣为Ai设计-全站离线版.html`（约 1MB）

## 原理
1. 读取脚本顶部 `PAGES` 列表中的 9 个页面（列表顺序即导航顺序）。
2. 把页内相对链接 `href="x.html"` 改写为 `data-sgw` + `postMessage` 导航，并注入高度上报脚本（子页把滚动高度上报给外壳，外壳同步 iframe 高度）。
3. 9 页 HTML 以 JSON 注入外壳 `<script type="application/json">`，并把 `</script>` 转义为 `\u003c` 防止截断外层脚本。
4. 外壳用 `iframe.srcdoc = PAGES[k]` 切换页面 —— **用 srcdoc 而非 blob URL**，规避手机 `file://` 下 blob 被浏览器禁用导致空白的问题。

## 注意事项
- **改了任意一页 HTML 后，必须重跑本脚本**，否则离线版不会同步更新。
- 新增 / 删除页面时，需同步修改本脚本顶部的 `PAGES` / `TITLES` 列表。
- 单页体积越大，离线版越大；大图建议控制体积（本项目单图多在 100–250KB 内）。
- 仅依赖 Python 标准库（`json` / `re` / `pathlib`），无需额外安装。
