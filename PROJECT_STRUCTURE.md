# 项目结构

```text
fastapi-demo/
├── app/  # 应用包，包含 API、业务、基础设施与通用工具
│   ├── main.py  # FastAPI 应用入口
│   ├── api/  # API 层，负责路由定义
│   │   ├── __init__.py  # 将 api 标记为 Python 包
│   │   └── v1/  # 1 版 API
│   │       ├── __init__.py  # 将 v1 标记为 Python 包
│   │       └── endpoints/  # 按功能分组的路由处理器
│   │           ├── __init__.py  # 将 endpoints 标记为 Python 包
│   │           └── copywriting.py  # 文案相关路由
│   ├── core/  # 核心配置、日志与异常处理
│   │   ├── __init__.py  # 将 core 标记为 Python 包
│   │   ├── config.py  # 应用与模型配置
│   │   ├── logging.py  # 应用日志配置
│   │   └── exceptions.py  # 自定义应用异常
│   ├── schemas/  # 请求、响应与错误结构
│   │   ├── __init__.py  # 将 schemas 标记为 Python 包
│   │   ├── copywriting.py  # 文案请求/响应模型
│   │   └── common.py  # 通用错误响应模型
│   ├── services/  # 业务逻辑与流程编排
│   │   ├── __init__.py  # 将 services 标记为 Python 包
│   │   └── copywriting_service.py  # 文案生成流程
│   ├── domain/  # 领域规则与平台策略
│   │   ├── __init__.py  # 将 domain 标记为 Python 包
│   │   ├── enums.py  # 平台枚举
│   │   └── strategies/  # 各平台的生成策略
│   │       ├── __init__.py  # 将 strategies 标记为 Python 包
│   │       ├── xiaohongshu.py  # 小红书策略规则
│   │       └── douyin.py  # 抖音策略规则
│   ├── infrastructure/  # 外部系统集成与适配器
│   │   ├── __init__.py  # 将 infrastructure 标记为 Python 包
│   │   └── llm/  # 大模型适配层
│   │       ├── __init__.py  # 将 llm 标记为 Python 包
│   │       └── client.py  # 大模型客户端封装
│   └── utils/  # 工具函数
│       ├── __init__.py  # 将 utils 标记为 Python 包
│       └── text.py  # 文本辅助函数
├── tests/  # 自动化测试
│   ├── __init__.py  # 将 tests 标记为 Python 包
│   ├── test_copywriting_api.py  # API 接口测试
│   └── test_prompt_service.py  # Prompt / 策略测试
├── requirements.txt  # Python 依赖
├── .env.example  # 环境变量示例
└── README.md  # 项目概览与使用说明
```
