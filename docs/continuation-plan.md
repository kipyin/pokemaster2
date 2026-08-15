# Pokemaster2 续作盘点与路线图

> 对「封尘多年」仓库的现状勘察结论，以及如何接着做的建议。  
> 代码、标识符、路径保持原文；说明用简体中文。  
>
> **产品初衷（已与作者确认）**：做成 **command line 上能玩的 text 版 Pokémon**；  
> 领域规则做成可复用的底层时，同一套核心应能挂上 **桌面养成/对战** 等其它壳，而不是绑死在终端 UI。

## 1. 项目是什么

**一句话（产品）**：在电脑上玩的、文本优先的宝可梦游戏——探索/遭遇、对战、捕捉、养成；第一载体是 CLI。  
**一句话（技术）**：把「和正作同类的个体与规则」放进可测试的 **game core**；CLI / 桌面都只是 core 外的 presentation。

| 项目 | 说明 |
|------|------|
| 包名 | `pokemaster2` |
| 口号（历史） | Get Real, Living™ Pokémon in Python |
| 版本 | `21.12.3`（CalVer：`year.month.minor`） |
| 状态 | PyPI 上 **Pre-Alpha**；有库脚手架，**尚无可玩循环** |
| 仓库 | https://github.com/kipyin/pokemaster2 |
| 前身 | https://github.com/kipyin/pokemaster（README 已指向本仓库） |
| 最后有效功能提交 | 约 2021-12 |
| 最后合并活动 | 2022-01 Dependabot；之后仅有未合并依赖 PR（至 2023-02） |

**与前身 / 当前代码的错位**

- v1 公开形态偏 **库**（`Pokemon(national_id=1, level=5)`），依赖外部 veekun/pokedex。
- v2 继续偏 **库 + 灌库 CLI**（`pokemaster2 load`），cookiecutter 现代 Python 包模板。
- **作者初衷是游戏**。现有 PRNG / Stats / 图鉴灌库是游戏 core 的零件，不是终点；  
  缺的是 **会话状态、地图/遭遇、对战回合、存档、以及 `play` 入口**。

历史库 API 仍有价值：它应下沉为 core，而不是唯一产品面。

```text
理想（确认后）:

  pokemaster2 play          ← 文本游戏（第一产品）
       │
       ▼
  ┌─────────────────────────────────────┐
  │  game core（无 UI）                  │
  │  个体 / 公式 / 图鉴 / 对战 / 存档     │
  └─────────────────────────────────────┘
       │                    │
       ▼                    ▼
   CLI / TUI            日后桌面 GUI 等
```

---

## 2. 仓库结构（现状）

```
src/pokemaster2/
  __init__.py          # 仅版本元数据，无公开 API
  cli.py               # click：仅有 load（维护向），无 play
  prng.py              # 第 3 世代 LCG，可生成 PID / IV 基因
  pokemon.py           # Stats + 未完成的 BasePokemon
  db/
    tables.py          # Pokemon, PokemonSpecies（peewee）
    io.py              # load / get_database / get_csv_dir
    default.py         # 默认 DB URI、CSV 路径
src/data/csv/
  pokemon.csv          # ~964 行（veekun 风格）
  pokemon_species.csv  # ~807 行
tests/                 # PRNG / Stats / CLI / db 基础测试
docs/                  # Sphinx + furo，usage 几乎为空
```

工具链：Poetry、nox、invoke、pre-commit、towncrier、bump2version、GitHub Actions。

**相对「可玩游戏」的缺口**：无 player/party、无 battle loop、无 world/encounter、无 save、无 `play` 命令；数据表也远不够支撑对战与招式。

---

## 3. 已完成 vs 未完成

### 3.1 已经可用（有代码 + 测试）— 可作为 core 零件

| 模块 | 能力 | 成熟度 |
|------|------|--------|
| `prng.PRNG` | Gen3 LCG；`generate_pid_and_iv(method=1\|2\|4)` | 高 |
| `pokemon.Stats` | 逐点运算、从 gene 拆 IV | 中高；IV 应 0–31 |
| `db.tables` / `io.load` | 两表 + CSV 灌库 | 中；列对齐与 URI 有债 |
| CLI `load` | 维护向 | 能跑；**不是游戏** |

### 3.2 骨架 / 缺失（游戏路径）

| 能力 | 状态 |
|------|------|
| 活体 `Pokemon` 工厂、升级/进化 | 大部注释或未写 |
| 招式、PP、类型克制、伤害 | 无 |
| 对战状态机（选招→结算→胜负） | 无 |
| 队伍、背包、金钱、徽章 | 无 |
| 地点 / 遭遇表 / 野生生成 | 无 |
| 存档 / 读档 | 无 |
| `pokemaster2 play` | 无 |
| 桌面 UI | 无（也不应现阶段做） |

### 3.3 数据层（按「先能打一小场」裁剪）

不必一次对齐全 veekun。文本 MVP 最小集约：

| 数据 | 用途 |
|------|------|
| 种族 + 种族值 + 类型 | 个体与克制 |
| 性格 + 经验曲线 | 能力值与升级 |
| 招式 + 学习面（可先手写一小张表） | 对战 |
| 类型效果表 | 伤害 |
| （稍后）特性、道具、遭遇 | 厚度 |

全量图鉴同步是 **内容管线**，服务游戏，不是第一目标。

---

## 4. 工程健康度（摘要）

Python 锁在 `<3.11`、flakehell 已死、Actions/依赖停在 2021–22——**Milestone 0 仍建议先做**，否则游戏代码难在现代环境跑。细节见文末技术债列表。

---

## 5. 架构原则：一份 core，多种壳

### 5.1 为什么这样拆

| 做法 | 结果 |
|------|------|
| 逻辑写在 `print` / Click 回调里 | CLI 能玩，桌面只能重写 → 失败 |
| 先做「完美引擎」再做游戏 | 长期无可玩、易再次封尘 |
| **core 无 UI + 先做一个极窄可玩环** | CLI 验证规则；桌面后换壳 |

桌面养成/对战 **可以** 建立在同一底层上，条件是：

1. core **不** `print`、不读 stdin、不绑定 click/Qt；
2. 对战与养成是 **纯状态 + 命令**（输入意图 → 新状态 + 事件列表）；
3. UI 只负责：展示事件、收集「选第几招/哪个菜单」、调 core、画结果。

### 5.2 推荐分层

```text
presentation/          # 可多套，互不依赖
  cli/                 # play、菜单、文本渲染（第一套）
  desktop/             # 日后：Godot / Qt / Tauri… 仅适配器

game/                  # 应用层：用例（开战、结算回合、捕捉、存档）
  session.py           # 当前游戏会话
  commands.py          # PlayerIntent → 结果

core/                  # 领域，无 I/O
  rng.py
  formula.py           # 能力值、伤害、命中…
  pokemon.py           # 个体
  battle.py            # 回合状态机
  party.py
  dex/                 # 只读图鉴

infra/                 # 适配真实世界
  dex_sqlite.py / json
  save_json.py
```

**对战 API 形态（示意）——利于 CLI 与 GUI 共用：**

```python
# 伪代码：UI 无关
battle = Battle.start(player_party, foe)
while not battle.is_over:
    view = battle.public_view()          # 给 UI 的只读快照
    intent = ui.pick_move(view)          # CLI 问数字 / GUI 点按钮
    events = battle.apply(intent)        # ["used Tackle", "dealt 12", ...]
    ui.render(events)
```

养成同理：`party`、`inventory`、`pokedex_progress` 在 core；「训练家之家」屏幕只是编辑这些状态的壳。

### 5.3 Tech stack 建议（服务游戏，而非库炫技）

| 层级 | 建议 | 说明 |
|------|------|------|
| 语言 | Python 3.10+ | 与现仓库一致，先复活再谈 |
| 运行时依赖 | 尽量瘦 | core 最好接近 stdlib；click 仅 presentation |
| 图鉴 | 预置 SQLite 或 Gen 子集 JSON | 装完能玩；`load` 留给贡献者 |
| ORM | peewee 可留在 infra，**勿泄漏进 core** | 桌面/CLI 都不该 import tables |
| 存档 | JSON/SQLite 文件 | 路径可配；方便桌面「打开存档」 |
| CLI | click 或少量 prompt_toolkit | MVP 用 click 足够；TUI 以后再加 |
| 桌面（远期） | **不要现在选死** | 候选：Godot（玩法向）、Qt/PySide、或 core 出 IPC 给别的 UI；原则是 **先有稳定 battle/party API** |
| 网络 | MVP 不做 | 单机本地 |

**明确不做（到第一个可玩版本之前）：** 联机、完整主线剧情、全图鉴收集强迫症、像素大地图引擎、与 Showdown 同步的全世代招式效果。

---

## 6. 建议产品切片（游戏优先）

原则：**垂直可玩环 > 横向内容宽度**。  
每一里程碑结束时，应能回答：「玩家现在能干什么？」

### Milestone 0 — 复活工程

- 现代 Python、ruff、CI、修好 DB 路径与 CSV 安全 load  
- **验收**：`poetry install` && `pytest` 全绿  

### Milestone 1 — 可玩的最小对战（文本）

玩家能：

```bash
pokemaster2 play
# 选一只御三家（或固定妙蛙种子）→ 遇一只野生 → 菜单：Fight / Run
# Fight → 选招 → 看到伤害与 HP 变化 → 打赢或逃跑 → 结束
```

背后 core：

- 固定 seed 可复现的个体生成（PRNG + 能力值公式）  
- 极简招式表（可硬编码 5～10 个招式 + 2～3 只怪）  
- `Battle` 状态机 + 类型克制 + 伤害公式（Gen3 简化版即可）  
- CLI 只做菜单与叙述  

**验收**：不靠改代码，命令行里打完一场；pytest 锁死若干战斗向量。  
**非目标**：进化、道具、AI 精巧、地图。

### Milestone 2 — 一场「短征程」

- 3～5 个地点文案 + 遭遇表  
- 队伍最多 6 只、捕捉（简化概率）、中心恢复  
- 经验与升级、学招（可简化）  
- 存档 / 读档  

**验收**：一局 15～30 分钟的「出发 → 打几场 → 抓一只 → 存盘 → 读盘继续」。

### Milestone 3 — 养成厚度 + 稳定 core API

- 进化、更完整招式/道具、更像样的训练家战  
- 冻结 `core` 的公开边界（battle view / intent / events、party、save schema）  
- CLI 体验打磨（帮助、颜色、种子/debug）  

### Milestone 4 — 第二壳（可选）：桌面

- 仅适配器：订阅同一 `events`、发同一 `intent`  
- 像素/动画是加分项；**先能完成与 CLI 同构的一战与组队**  
- 技术选型在 M3 边界稳定后做 spike，避免过早绑死  

### 内容与世代

- 默认 **Gen3 规则味道**（已有 PRNG），内容可用关都子集或虚构小镇  
- 「像正作」优先保证 **个体与战斗数字可信**；剧情与地图可用原创，降低 IP/数据压力  

---

## 7. 和「只做库」路线的关系

| | 只做 Living 库 | 文本游戏 + 可换壳 core（本路线） |
|--|----------------|----------------------------------|
| 成功标准 | `Pokemon(...)` 数值对 | `play` 能愉快玩完一小环 |
| CLI | 调试/load | **主产品** |
| 对战 | 可选 | **MVP 必需（可极简）** |
| 桌面 | 无关 | 第二 presentation，复用 core |
| 现有代码 | 直接当产品 | **零件**，要补 session/battle/save |

库式 API 仍应存在（`from pokemaster2.core import Pokemon, Battle`），方便测试与日后桌面；**用户第一口是游戏**。

---

## 8. 技术债（续作顺手）

1. IV 范围应为 0–31  
2. `nature_modifiers` 无返回值  
3. DB URI：`sqlite:///` vs peewee 路径  
4. CSV 多余列 vs 模型字段  
5. 模块级全局 `PRNG` → 注入  
6. click 的 `type=bool`  
7. 工具链现代化（见 M0）  

---

## 9. 近期任务拆分

1. Milestone 0：工程复活  
2. 极简 dex + `Pokemon` 个体 + 伤害公式测试  
3. `Battle` + `pokemaster2 play` 最小一战  
4. 遭遇 / 捕捉 / 存档 → 短征程  
5. （可选）桌面适配器 spike  

---

## 10. 总结

- **初衷**是 **CLI 文本宝可梦游戏**，不是 PyPI 上又一个图鉴包装库。  
- **底层架构**应建成 **无 UI 的 game core**，这样 **桌面养成/对战是同一意图上的第二个壳**，而不是另一套项目。  
- **秩序**必须是：先 M1 命令行里能打完一场 → 再短征程 → 再冻 core API → 才谈桌面。  
- 现有 PRNG/Stats/灌库是有用遗产；从「库模板」扭到「游戏 + core」，产品叙事与目录边界要一起改。  

**下一步最有意义的一步**：复活工程后，尽早做出 `pokemaster2 play` 的最小对战环——这是验证架构能否同时服务 CLI 与未来桌面的试金石。
