# ============ 基础镜像 ============
# 使用轻量级 nginx alpine 镜像（约 8MB）
FROM nginx:1.27-alpine

# 元信息
LABEL maintainer="blackanubis"
LABEL version="1.0"
LABEL description="英语分级词汇练习网页 · 江苏版"
LABEL org.opencontainers.image.source="https://github.com/blackanubis/englishbook"

# 设置时区
ENV TZ=Asia/Shanghai

# 删除默认页面
RUN rm -rf /usr/share/nginx/html/*

# 拷贝静态资源
COPY index.html /usr/share/nginx/html/index.html
COPY vocab-data/ /usr/share/nginx/html/vocab-data/
COPY sentence-data/ /usr/share/nginx/html/sentence-data/
COPY vocab-data-js/ /usr/share/nginx/html/vocab-data-js/
COPY sentence-data-js/ /usr/share/nginx/html/sentence-data-js/

# 拷贝 Nginx 配置（启用 gzip、长缓存、正确 MIME）
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -q --spider http://localhost/ || exit 1

# 暴露端口
EXPOSE 13001

# 启动 nginx
CMD ["nginx", "-g", "daemon off;"]
