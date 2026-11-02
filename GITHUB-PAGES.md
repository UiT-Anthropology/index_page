# 手动部署到 GitHub Pages

发布目录：`dist/`。首页是 `dist/index.html`。

1. 创建或打开用于网站的 GitHub 仓库。免费方案使用公开仓库。
2. 将 `dist` **里面的全部内容**上传到仓库根目录，保留原有文件夹结构。不要把 `dist` 文件夹本身作为外层目录上传，也不要只上传 `index.html`。
3. 确认仓库根目录直接包含 `index.html`、`assets/`、`CNAME`、`.nojekyll` 及其他 HTML、CSS、JS 文件。若上传界面没有包含隐藏文件，请单独创建空的 `.nojekyll` 文件。
4. 仓库 Settings → Pages → Source 选择 Deploy from a branch；Branch 选择 main，目录选择 / (root)，保存。
5. Custom domain 填入 `multispeciesarctic.com` 并保存。
6. 等待部署和 DNS 检查完成、证书准备就绪后，勾选 Enforce HTTPS。
7. 打开 https://multispeciesarctic.com/，检查首页、图片、地图和内页链接。

`CNAME` 已写入正式域名，`.nojekyll` 用于直接发布静态文件。首页 canonical 已指向正式域名。

以后更新网站时，重新上传 `dist` 中变更的文件，并保留 `CNAME` 和 `.nojekyll`。不需要上传 Python 脚本、data、.openai 或本说明文件。

如果选择上传整个项目仓库，请不要将分支发布目录设置成 `dist`：GitHub 的分支发布仅支持根目录或 `/docs`。保留现有项目结构时应另行配置 GitHub Actions。
