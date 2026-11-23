# Insurellm Expert Assistant

Knowledge assistant over a fictional insurance-tech document corpus. Documents are split into overlapping semantic chunks, embedded in Chroma, then retrieved with history-aware query rewriting, dual-query search, and LLM reranking before the answer is generated.

面向虚构保险科技公司 Insurellm 的知识库问答。文档经语义切块后写入 Chroma；提问时结合对话改写查询、双路召回并重排序，再生成带来源的回答。

## 能力

- 大模型语义切块：每块包含标题、摘要和原文，块之间约 25% 重叠
- 对话感知的查询改写，原问题与改写问句双路向量召回后去重合并
- 大模型按相关度重排序，保留 Top 10 作为生成上下文
- Gradio 对话界面，回答与检索片段、来源并排展示
- 150 题离线评测：检索看 MRR、nDCG、关键词覆盖率；回答用 LLM-as-judge 打准确性、完整性、相关性

## 知识库

`knowledge-base/` 约 76 篇 Markdown，分为四类：

| 目录 | 内容 |
| --- | --- |
| `company/` | 公司介绍、文化、招聘 |
| `employees/` | 员工档案 |
| `products/` | 8 条产品线 |
| `contracts/` | 客户合同 |

## 项目结构

```text
app.py              对话界面
evaluator.py        评测面板
ingest.py           切块、嵌入、写入向量库
answer.py           查询改写、召回、重排序、生成
evaluation/         评测集与指标
knowledge-base/     原始文档
preprocessed_db/    本地向量库（运行 ingest 后生成，不提交）
```

## 环境

需要 Python 3.11+，以及这些密钥：

| 变量 | 用途 |
| --- | --- |
| `OPENAI_API_KEY` | 切块模型 `openai/gpt-4.1-nano`，嵌入模型 `text-embedding-3-large` |
| `GROQ_API_KEY` | 查询改写、重排序和回答，模型 `groq/openai/gpt-oss-120b` |
| `OPENROUTER_API_KEY` | 评测裁判 `openrouter/deepseek/deepseek-v4.1-flash-1017`。只跑对话可以不填 |

```bash
uv sync
copy .env.example .env
```

把密钥填进 `.env`。

## 运行

在仓库根目录执行。入库会调用大模型切分全部文档，并重新生成 `preprocessed_db/`。速率受限时，把 `ingest.py` 里的 `WORKERS` 改成 `1`。

```bash
uv run python ingest.py
uv run python app.py
```

评测面板：

```bash
uv run python evaluator.py
```

只跑某一题（题号从 0 开始）。下面这条不依赖当前目录，在仓库里任意位置都能执行：

```bash
uv run python evaluation/eval.py 0
```

## 检索流程

1. 用当前问题和对话历史改写成一条更具体的检索问句。
2. 原问题、改写问句各取 20 条近邻，按正文去重合并。
3. 大模型输出相关度顺序，保留前 10 条。
4. 把带来源的片段放进系统提示，生成回答。
