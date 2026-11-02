# 手动部署到 GitHub Pages

本仓库保留整个项目，网站文件在 `dist/`，首页是 `dist/index.html`。使用 GitHub Actions 将 `dist` 发布到网站根路径。

## 首次配置

1. 将 `.github/workflows/pages.yml` 和本地修改同步到 GitHub 仓库的 `main` 分支，保留现有目录结构。
2. 打开仓库 Settings → Pages，Build and deployment → Source 改为 **GitHub Actions**。
3. Custom domain 保持 `multispeciesarctic.com`，保存。
4. 打开 Actions → **Deploy website to GitHub Pages** → **Run workflow**，选择 `main`，手动运行。
5. 等待检查和部署成功后，打开 https://multispeciesarctic.com/，检查首页、地图、图片和内页。
6. Settings → Pages 中勾选 **Enforce HTTPS**。

此工作流仅支持手动触发，推送文件不会自动触发此工作流。

## OVH DNS

根域名 `@` 的四条 A 记录分别指向：

- `185.199.108.153`
- `185.199.109.153`
- `185.199.110.153`
- `185.199.111.153`

本仓库属于 GitHub 组织 `UiT-Anthropology`，因此 `www` 的 CNAME 应指向 `uit-anthropology.github.io.`，不是操作账号的个人 GitHub Pages 域名。不添加协议和仓库路径。

保留邮箱和 NS 记录。移除指向旧网站的 A、AAAA 和 OVH 网站跳转记录。

## 后续更新

更新内容后，将本地改动同步到 `main`，然后再次手动运行 Actions 中的部署工作流。

`dist/CNAME` 已写入正式域名，`dist/.nojekyll` 用于直接发布静态文件。首页 canonical 指向正式域名。

不要继续使用 `Deploy from a branch → main → / (root)`：仓库根目录没有 `index.html`，该方式会发布错误的首页。不要只复制首页到根目录，否则它引用的资源和内页路径也需要一并移动。
