# GitHub Pages 传统分支部署

网站已放在仓库根目录：`index.html` 为首页，`assets/` 存放资源，其他 HTML、CSS、JS 文件也位于根目录。无需构建或自定义 Actions 工作流。

## 手动上线

1. 将本地全部改动同步到 GitHub 的 `main` 分支，包括文件移动和旧 `dist/`、`.github/workflows/pages.yml` 的删除。不要只同步 `index.html`。
2. 仓库 Settings → Pages → Build and deployment：
   - Source：**Deploy from a branch**
   - Branch：**main**
   - Folder：**/ (root)**
   - 点击 Save。
3. Custom domain 保持 `multispeciesarctic.com`。
4. 证书准备好后勾选 **Enforce HTTPS**。
5. 等待发布完成，访问 https://multispeciesarctic.com/ 并刷新缓存。

根目录的 `CNAME` 和 `.nojekyll` 必须保留。GitHub 的分支发布可能会显示平台自动生成的 Pages 构建任务，这是正常现象，不需要自己编写或手动运行 Actions。

## OVH DNS

`@` 的四条 A 记录：185.199.108.153、185.199.109.153、185.199.110.153、185.199.111.153。

`www` 的 CNAME：`uit-anthropology.github.io.`，因为仓库属于 UiT-Anthropology 组织。

## 本地维护

运行 `python build-species.py` 和 `python build-drive-library.py` 更新页面，运行 `python check-species.py` 检查。生成脚本现在直接写入根目录，不再生成 `dist`。本地预览仍使用 `node preview-server.mjs`。

后续推送到 `main` 会自动更新线上网站。
