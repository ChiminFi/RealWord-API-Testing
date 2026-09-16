# RealWorld API 自动化测试

[English](README.en.md) | **简体中文**

## 项目概述

本项目使用 Python、Pytest 和 Requests，对 RealWorld（Conduit）Django Ninja 后端进行 API 自动化测试。测试覆盖核心用户与文章流程、身份认证与权限控制、状态变化、错误响应以及部分 PostgreSQL 数据校验，并通过日志、HTML 报告和 GitHub Actions 呈现测试结果。

## 技术栈

Python 3.14 · Pytest · Requests · PostgreSQL · psycopg · python-dotenv · pytest-html · uv · GitHub Actions

## 测试范围

| 模块             | 代表性测试内容                                                                                       |
| ---------------- | ---------------------------------------------------------------------------------------------------- |
| 身份认证         | 用户注册、登录、使用 Bearer Token 获取当前用户；重复邮箱、缺失字段、错误密码，以及缺失或无效 Token。 |
| 文章             | 创建、查询、更新和删除；验证字段更新与 slug 变化；检查缺失必填数据和未授权修改。                     |
| 评论             | 创建、查询和删除；验证作者与正文；检查未登录创建评论及删除他人评论。                                 |
| 用户资料与关注流 | 关注、取消关注用户；验证用户资料中的关注状态，以及被关注用户的文章是否出现在关注流中。               |
| 收藏             | 收藏和取消收藏文章；验证 `favorited` 状态与 `favoritesCount`。                                       |
| 列表与分页       | 按作者筛选文章；验证 `limit`、`offset`、文章总数及最后一个不完整分页。                               |
| 数据库           | 检查数据库连接与预期表结构；对照文章创建后的存储字段，并确认删除后对应记录消失。                     |

## 测试设计

测试同时覆盖正常业务流程和异常场景，包括缺失身份凭证、无效请求数据、不存在的资源，以及尝试修改其他用户内容。除了 HTTP 状态码，测试还检查关键响应字段。

关注、收藏和关注流相关测试通过后续查询验证状态变化。文章测试进一步检查更新和删除后的数据一致性。分页测试使用一组动态生成的文章，覆盖最后一个不完整分页。

## 项目结构

```text
.
├── .github/workflows/api-testing.yml  # CI 执行与报告上传
├── conftest.py                        # Client、测试数据、用户、文章和数据库 fixtures
├── pyproject.toml                     # Python 项目与依赖配置
├── pytest.ini                         # markers 与控制台日志配置
├── src/
│   ├── clients/                       # 通用 HTTP Client 与各业务 Client
│   ├── config/settings.py             # 基于环境变量的配置
│   ├── db/db_client.py                # 数据库连接与 SQL 查询封装
│   └── utils/data_factory.py          # 动态测试数据生成
└── tests/
    ├── auth/
    ├── articles/
    ├── comments/
    ├── follow/
    ├── db/
    └── test_health.py
```

## 框架设计

`BaseClient` 统一管理 Requests Session、HTTP 方法、请求超时，以及请求方法、URL 和响应状态的日志。身份认证、文章、评论和用户资料 Client 在此基础上封装各自的 API 请求。

Pytest fixtures 提供可复用的 Client 和测试前置状态，包括已注册用户、用户拥有的文章、评论及数据库连接。数据工厂为用户、文章和评论生成唯一数据，减少测试用例之间的冲突。

## 数据库校验

部分测试在调用 API 后查询 PostgreSQL，验证文章创建和删除是否正确反映在数据库中。创建文章后，测试将 API 数据与 `articles_article` 表中的 slug、标题、描述和正文进行对照，并检查关联用户是否存在；删除文章后，确认对应记录已移除。

另有测试通过 `SELECT 1` 检查连接，并核对预期的表名。数据库连接参数来自环境变量，因此本地和 CI 可以连接不同的数据库。

## 已知问题

- **BUG-AUTH-001：** 无效 Bearer Token 用例期望 `GET /api/user` 返回 401，但后端当前返回 500。该测试使用 `pytest.mark.xfail(strict=True)`；如果测试意外通过，测试运行也会失败，以提示复核该问题。
- **重复收藏：** 同一篇文章第二次执行收藏请求时观察到失败，因此相应用例标记为 `xfail`。此处尚未将预期行为确定为业务契约；该标记只记录已观察到的问题，且未设置 `strict=True`。

## 日志与报告

`BaseClient` 记录请求方法、URL 和响应状态。Pytest 在控制台显示 INFO 级别日志。CI 使用 `pytest-html` 的 `--self-contained-html` 选项生成 `reports/report.html`，并将其作为 `pytest-report` 工作流产物上传。报告在测试运行时生成，不提交到仓库。

## CI

GitHub Actions 工作流在 push 和 pull request 时运行。它检出仓库、安装 uv 和 Python 3.14、执行 `uv sync`、请求 `$BASE_URL/api/articles` 预热部署在 Render 上的 API，然后运行测试。即使测试失败，工作流也会上传 HTML 报告。

工作流从 GitHub Secrets 读取 `BASE_URL`、`DB_HOST`、`DB_PORT`、`DB_NAME`、`DB_USER`、`DB_PASSWORD` 和 `DB_SSLMODE`。

## 本地运行

安装 [uv](https://docs.astral.sh/uv/)，并准备可访问的兼容 RealWorld API 和 PostgreSQL 数据库。在环境变量或本地 `.env` 文件中设置 `BASE_URL` 及上述 `DB_*` 变量。`BASE_URL` 默认值为 `http://localhost:8000`；数据库默认配置见 `src/config/settings.py`。仓库目前不包含 `.env.example` 文件。

```bash
uv sync
uv run pytest
uv run pytest -m smoke
uv run pytest -m db
```

已注册的 markers 为 `smoke`、`api` 和 `db`。当前测试使用 `smoke` 和 `db`，尚无测试标记为 `api`。数据库测试需要可连接且具有预期后端表结构的 PostgreSQL 实例。生成本地 HTML 报告可运行：

```bash
mkdir -p reports
uv run pytest --html=reports/report.html --self-contained-html
```

## 当前范围

当前项目聚焦 API 自动化测试与部分数据库校验。UI 自动化和性能测试不在本仓库当前范围内。
