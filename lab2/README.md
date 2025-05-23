

# 家教服务系统 (Tutoring Service System)

本项目是一个家教服务系统示例，包含后端 Flask API 与前端 Vue.js 单页应用，提供用户注册/登录、家教信息发布、学生需求发布、信息查询、智能推荐、评价和问答功能。

## 🚀 快速开始

以下步骤假设你已经克隆了仓库并在项目根目录：

1. **进入项目目录**  
   ```bash
   cd /path/to/lab2
   ```

2. **创建并激活虚拟环境**  
   ```bash
   python3 -m venv lab2
   source lab2/bin/activate
   ```

3. **安装后端依赖**  
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **安装前端依赖**  
   ```bash
   cd ../frontend
   npm install
   ```

5. **初始化数据库**  
   - 默认使用 SQLite，脚本位于 `database/init.sql`。  
   - 执行：  
     ```bash
     cd ../database
     sqlite3 tutoring.db < init.sql
     ```
   - 如需使用 MySQL，请在 `backend/config.py` 中将 `DB_TYPE` 改为 `mysql`，并设置好 `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`，然后执行：
     ```bash
     mysql -u root -p < init.sql
     ```

## 💻 项目结构

```
lab2/
├── backend/                   # Flask 后端服务
│   ├── app.py                 # 应用入口
│   ├── db.py                  # 数据库连接工具
│   ├── config.py              # 配置管理
│   ├── requirements.txt       # 后端依赖
│   ├── routes/                # 各接口模块（Blueprint）
│   └── schemas.py             # 输入校验 Schemas
├── frontend/                  # Vue 前端项目
│   ├── package.json           # 前端依赖与脚本
│   └── src/                   # Vue 源代码（components, router, main.js）
└── database/                  # 数据库初始化脚本
    └── init.sql               # 创建表结构并插入示例数据
```

## ⚙️ 环境变量

可通过在 `backend/` 目录创建 `.env` 文件覆盖默认配置（使用 `python-decouple`）：

```bash
FLASK_DEBUG=True
DB_TYPE=sqlite
DB_NAME=../database/tutoring.db
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
CACHE_TIMEOUT=60
```

## 🔧 运行后端

1. 确认已激活虚拟环境  
2. 进入 `backend/` 目录  
   ```bash
   cd backend
   python app.py
   ```  
3. 默认监听 `http://localhost:5000`  

## 🔧 运行前端

1. 进入 `frontend/` 目录  
   ```bash
   cd frontend
   npm run serve
   ```  
2. 默认访问 `http://localhost:8080`  

> **注意**：请确保后端运行在 5000 端口，否则调整 `src/main.js` 中的 `axios.defaults.baseURL`。

## ✔️ 功能概览

- 用户注册 / 登录
- 家教信息发布 / 学生需求发布
- 家教与学生互相推荐
- 信息查询与筛选
- 评价系统（评分 + 评论）
- 简易问答接口

## 🛠️ 开发与部署

- **日志与监控**：集成 Prometheus Metrics、限流、缓存  
- **安全**：Flask-Talisman 添加安全头  
- **输入校验**：使用 Marshmallow  
- **容器化**：可自行 Docker 化部署  

## 📄 LICENSE

MIT License

## ✉️ 联系我们

如有问题，请联系项目负责人。