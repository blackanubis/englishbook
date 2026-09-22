# 英语分级词汇练习网页 · 江苏版

> 一个零依赖、纯静态、可 Docker 一键部署的英语学习网页

## ✨ 特性

- 📚 **覆盖完整学段**：启蒙 → 小学 → 初中 → 高中 + 江苏特色词汇
- 📊 **内置 + 扩展词库**：5300+ 词条，含音标、释义、例句
- 📖 **配套句子库**：800+ 句型，覆盖高考作文模板、阅读理解、商务口语
- 🎯 **5 大功能模块**：单词卡片、句子练习、练习中心、错题本、学习统计
- 💾 **本地存储**：所有学习数据保存在浏览器 localStorage
- 🚀 **零依赖**：单文件 HTML，无后端，纯静态部署
- 🐳 **Docker 一键部署**：内含完整 Docker 化方案

## 📁 项目结构

```
english-vocab-practice/
├── index.html               # 主程序（所有逻辑都在内）
├── vocab-data/              # 词汇库原始 JSON
│   ├── vocab-enlighten-1.json ~ vocab-enlighten-5.json
│   ├── vocab-primary.json + vocab-primary-1~6.json
│   ├── vocab-junior.json + vocab-junior-1~5.json
│   ├── vocab-senior.json + vocab-senior-1~9.json
│   └── README.md            # 词汇说明
├── sentence-data/           # 句子库原始 JSON
│   └── sentences-batch-1/2/3.json
├── vocab-data-js/           # 词汇库自动加载模块（构建时生成）
├── sentence-data-js/        # 句子库自动加载模块（构建时生成）
├── Dockerfile               # Docker 镜像构建文件
├── docker-compose.yml       # 一键部署配置
├── nginx.conf               # Nginx 配置（端口 13001、gzip、缓存）
└── .gitignore
```

## 🐳 Docker 部署（推荐）

### 前置要求

- Docker Engine >= 20.10
- Docker Compose v2

### 方式 A：拉取预构建镜像（最快，推荐）

每次 push 到 `main` 分支，GitHub Actions 自动构建并推送镜像到 **GHCR**，任何人无需本地构建即可部署：

```bash
# 创建 docker-compose.yml（复制下方代码）
mkdir englishbook && cd englishbook
curl -O https://raw.githubusercontent.com/blackanubis/englishbook/main/docker-compose.yml
# 编辑 docker-compose.yml 取消 image 行注释（推荐）：
#   image: ghcr.io/blackanubis/englishbook:latest

# 一键启动
docker-compose up -d
```

或者直接用命令行拉取镜像运行：

```bash
docker run -d \
  --name englishbook \
  -p 13001:13001 \
  --restart unless-stopped \
  ghcr.io/blackanubis/englishbook:latest
```

**镜像地址**：
- GitHub Container Registry：`ghcr.io/blackanubis/englishbook:latest`

### 方式 B：从源码构建（适合二次开发）

```bash
# 克隆仓库
git clone https://github.com/blackanubis/englishbook.git
cd englishbook

# 一键启动（后台模式，构建镜像 + 启动）
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

部署后访问：**http://localhost:13001**

如需修改端口，编辑 `docker-compose.yml` 中的 `"13001:13001"`。

### 手动 Docker 命令

```bash
# 构建镜像
docker build -t englishbook:latest .

# 运行
docker run -d --name englishbook -p 13001:13001 --restart unless-stopped englishbook:latest

# 停止
docker stop englishbook

# 查看日志
docker logs englishbook
```

### 镜像信息

- **基础镜像**：`nginx:1.27-alpine`（约 8MB）
- **大小**：约 30MB（含词库 + 句子库）
- **架构**：linux/amd64 + linux/arm64（自动构建）
- **健康检查**：每 30 秒访问首页

### 🔄 自动构建镜像（GitHub Actions）

仓库自带 `.github/workflows/docker.yml`，**每次 push 到 main 分支会自动触发构建**：

1. ✅ 自动构建多架构镜像（amd64 + arm64）
2. ✅ 自动推送到 GHCR
3. ✅ 自动生成 tags：`latest` / `<branch>` / `<sha>` / `<semver>`
4. ✅ 启用 GHA 缓存加速构建

查看构建进度：https://github.com/blackanubis/englishbook/actions

## 🔧 不使用 Docker 的部署

### 方式 1：Nginx 手动部署

```nginx
server {
    listen 8080;
    server_name _;
    root /path/to/english-vocab-practice;
    index index.html;
}
```

### 方式 2：Python 简易 HTTP 服务器

```bash
cd english-vocab-practice
python -m http.server 8080
```

### 方式 3：直接打开

```bash
# 直接双击 index.html（注意：部分浏览器对 file:// 的同源策略可能限制）
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

## 🔄 更新词库

如需添加新词或新句子：

1. 修改 `vocab-data/*.json` 或 `sentence-data/*.json`
2. 重新构建镜像：`docker-compose up -d --build`
3. 浏览器强制刷新：Ctrl + F5

## ⚙️ Nginx 配置特性

- ✅ 端口 13001
- ✅ Gzip 压缩（节省 60-70% 带宽）
- ✅ 静态资源长缓存（JS/CSS 7 天，图片 30 天）
- ✅ HTML 不缓存（更新立即可见）
- ✅ MIME 类型兜底
- ✅ 健康检查（自动监控容器状态）

## 📊 词汇库统计（内置 + 扩展）

| 学段 | 内置 | 扩展 | **合计** |
|------|------|------|----------|
| 启蒙 | 52 | 245 | **297** |
| 小学 | 177 | 594 | **771** |
| 初中 | 233 | 1387 | **1620** |
| 高中 | 288 | 2644 | **2932** |
| 江苏特色 | 61 | 0 | **61** |
| **总计** | **811** | **4870** | **5681** |

> 扩展词库运行时从 `vocab-data/*.json` 动态加载，无需重新构建镜像即可更新词库。

## 📖 句子库

3 批共 **677 句**，覆盖高考作文模板、阅读理解、日常口语、商务职场、江苏特色场景。

## 📝 许可证

MIT
