# Pokemaster2 续作盘点与路线图

> 对「封尘多年」仓库的现状勘察结论，以及如何接着做的建议。  
> 代码、标识符、路径保持原文；说明用简体中文。

## 1. 项目是什么

**一句话**：在 Python 里造出「和正作游戏一样」的宝可梦——有种族、等级、IV/EV、性格、特性、性别、招式、持有物，并能升级、进化、学招等。

| 项目 | 说明 |
|------|------|
| 包名 | `pokemaster2` |
| 口号 | Get Real, Living™ Pokémon in Python |
| 版本 | `21.12.3`（CalVer：`year.month.minor`） |
| 状态 | PyPI 上 **Pre-Alpha** |
| 仓库 | https://github.com/kipyin/pokemaster2 |
| 前身 | https://github.com/kipyin/pokemaster（README 已指向本仓库） |
| 最后有效功能提交 | 约 2021-12 |
| 最后合并活动 | 2022-01 Dependabot；之后仅有未合并依赖 PR（至 2023-02） |

**与前身的关系**

- v1（`pokemaster`）依赖外部 [veekun/pokedex](https://github.com/veekun/pokedex)（SQLAlchemy + 全量 CSV/SQLite），公开 API 已是 `Pokemon(national_id=1, level=5)`。
- v2 目标是**摆脱对外部 pokedex 运行时依赖**：用 **peewee + 自带 CSV** 建库，并重写领域模型；脚手架来自 `fedejaure/cookiecutter-modern-pypackage`。

理想用法（来自 v1，v2 尚未接通）：

```python
from pokemaster import Pokemon
bulbasaur = Pokemon(national_id=1, level=5)
eevee = Pokemon("eevee", level=10, gender="female")
```

---

## 2. 仓库结构（现状）

```
src/pokemaster2/
  __init__.py          # 仅版本元数据，无公开 API
  cli.py               # click：`load` 把 CSV 灌进 SQLite
  prng.py              # 第 3 世代 LCG，可生成 PID / IV 基因
  pokemon.py           # Stats + 未完成的 BasePokemon
  db/
    tables.py          # Pokemon, PokemonSpecies（peewee）
    io.py              # load / get_database / get_csv_dir
    default.py         # 默认 DB URI、CSV 路径（环境变量可覆盖）
src/data/csv/
  pokemon.csv          # ~964 行（veekun 风格）
  pokemon_species.csv  # ~807 行
tests/                 # PRNG / Stats / CLI / db 基础测试
docs/                  # Sphinx + furo，usage 几乎为空
```

工具链：Poetry、nox、invoke、pre-commit、towncrier、bump2version、GitHub Actions（tests / release / CodeQL / pre-commit 自动更新）。

---

## 3. 已完成 vs 未完成

### 3.1 已经可用（有代码 + 测试）

| 模块 | 能力 | 成熟度 |
|------|------|--------|
| `prng.PRNG` | Gen3 LCG；`generate_pid_and_iv(method=1\|2\|4)`；`reset` / `next_` / `random` | 高；与 Smogon 文档对齐，测试扎实 |
| `pokemon.Stats` | 逐点 `+ - * //`、从 gene 拆 IV、`zeros` | 中高；IV 上界写成 0–32（游戏实为 0–31） |
| `db.tables` | `Pokemon` / `PokemonSpecies` 两表 + `get_pokemon(identifier)` | 中；多数字段 FK 被注释掉 |
| `db.io.load` | CSV → SQLite 批插入，支持 drop/safe/recursive | 中；与「模型列 vs CSV 列」未对齐时会炸 |
| CLI `pokemaster2 load` | 包装 `io.load` | 能跑；产品面几乎只有这一条命令 |

### 3.2 骨架已有、主体被注释或未接线

| 位置 | 意图 | 缺口 |
|------|------|------|
| `BasePokemon` | 活体宝可梦领域对象 | 几乎整段 `_from_pokedex_by_id` / `evolve` / `level_up` 注释掉 |
| `Stats.nature_modifiers` | 性格修正 1.1 / 0.9 / 1.0 | 函数体注释掉且**无 return** |
| `_calc_stats` | 正式能力值公式 | 依赖未完成的 `nature_modifiers` |
| 图鉴查询层 | v1 的 `_database.get_*` | v2 仅有极简 `get_pokemon` |
| 公开 API | `from pokemaster2 import Pokemon` | `__init__` 未导出任何领域类型 |
| 招式 / 道具 / 战斗 | v1 部分存在 | v2 无 |

### 3.3 数据层缺口（相对「能造一只完整宝可梦」）

当前 CSV **只有 2 张表**。要接通 v1 已写过的逻辑，至少还需要（名称按 veekun 惯例）：

| 数据 | 用途 |
|------|------|
| `stats` / `pokemon_stats` | 种族值、努力值产出 |
| `natures` | 性格及升降项 |
| `abilities` / `pokemon_abilities` | 特性池与 PID 映射 |
| `experience` / `growth_rates` | 等级 ↔ 经验 |
| `types` / `pokemon_types` | 属性 |
| `moves` / `pokemon_moves` / `pokemon_move_methods` | 等级招式、默认 4 招 |
| `items` / `pokemon_items`（可选） | 野生持有物 |
| `version_groups` 等（可选） | 按版本过滤学习面 |

`pokemon_species.csv` 表头含 `generation_id`、`evolution_chain_id`、`color_id`、`growth_rate_id` 等，**模型里对应字段多为注释**；`io.load` 用 `DictReader` 整行 `insert_many` 时，多出来的键会与 peewee 模型冲突——**全量灌库路径目前不可靠**。

默认库路径：`default.db_uri_with_origin()` 返回 `sqlite:///.../pokedex.sqlite3`，而 `io.get_database` 把 URI **原样**交给 `peewee.SqliteDatabase(uri)`。peewee 期望的是**文件路径**（或特殊名），不是 SQLAlchemy 风格 URI → **默认连接方式有设计债**。仓库内也**没有**打包好的 `pokedex.sqlite3`，只有 CSV。

---

## 4. 工程健康度（2026 视角）

| 项 | 现状 | 风险 |
|----|------|------|
| Python | `>=3.8,<3.11` | 3.8/3.9 已 EOL；本机常见 3.12+ 装不上 |
| Poetry | 旧式 `dev-dependencies` | 需迁到 `group.dev.dependencies` |
| flakehell | 已停更且与新 flake8 不兼容 | lint 链路易碎 |
| black / mypy / pre-commit | 2021 钉死版本 | CI 与本地难复现 |
| Actions | `actions/checkout@v2` 等 | 应用新 major；大量 Dependabot PR 未合 |
| flake8-annotations 等 | 偏严 | 对半成品领域代码阻力大 |
| 覆盖率门槛 | fail_under = 70 | 合理；领域代码补齐时要同步测 |
| README Quickstart | TODO | 新人零上手路径 |
| 文档 usage | 仅 `import pokemaster2` | 与真实能力不符 |

**结论**：不先做一轮「能安装、能测、能 lint」的现代化，功能开发会反复被工具链打断。

---

## 5. 已知技术债 / 小坑（续作时顺手修）

1. **IV 合法范围**：`validate_iv` 写 0–32 inclusive，游戏为 **0–31**。
2. **`nature_modifiers` 无返回值**：调用 `_calc_stats` 会得到 `None` 再崩。
3. **DB URI 格式**：去掉 `sqlite:///` 前缀，或统一用 path / `playhouse.db_url`。
4. **CSV 列 ⊇ 模型字段**：load 前应按模型字段过滤，或补全模型 + 迁移脚本。
5. **`Pokemon.species` FK**：在类外赋值 `Pokemon.species = ForeignKeyField(...)`，且 CSV/`species_id` 与关系字段命名需理清，避免双重含义。
6. **模块级 `prng = PRNG()`**（`pokemon.py`）：全局可变种子，测试与多实例会踩脚；宜注入或挂在类上（v1 是 `Pokemon._prng`）。
7. **`PRNG._generator`**：每次 `__call__` 新建 generator，靠改 `self.seed` 凑效；可改成单例 iterator，行为保持不变。
8. **stat 命名**：v2 用 `atk`/`def_`/`spatk`…，v1/veekun 用 `attack`/`special-attack`；对外 API 建议尽早定一种，内部可做映射（已有 `STAT_NAMES_FULL`）。
9. **CLI `load` 的 bool 选项**：`type=bool` 对 click 不友好（非空字符串都是 True）；宜用 `is_flag` 或明确 choice。

---

## 6. 建议产品切片（推荐顺序）

原则：**先恢复「一只可查询、可生成的宝可梦」竖切**，再横向加招式/战斗；工具链与竖切可并行，但 **Milestone 0 应挡在大量功能 PR 之前**。

### Milestone 0 — 复活工程（约 0.5–1 天）

- [ ] Python 支持改为 `>=3.10,<3.14`（或至少 3.10–3.12）
- [ ] 升级 Poetry 元数据、锁文件；替换/移除 flakehell
- [ ] 刷新 pre-commit、black、ruff（可用 ruff 替代 flake8 全家桶）、mypy、pytest
- [ ] 修好 CI Actions major 版本；矩阵含 3.10–3.12
- [ ] 本地：`poetry install` → `pytest` 全绿
- [ ] 修正 `get_database` 路径/URI；CSV load 只写入模型字段
- [ ] README：真实安装与 `pokemaster2 load` 示例

**验收**：干净 clone 后 10 分钟内装好并测通。

### Milestone 1 — 最小活体宝可梦（核心价值）

目标 API（可微调命名）：

```python
from pokemaster2 import Pokemon

p = Pokemon(national_id=1, level=5)
assert p.species == "bulbasaur"
assert 1 <= p.level <= 100
assert p.iv is not None and p.stats.hp >= 1
```

工作项：

- [ ] 从 veekun 拉取/裁剪 CSV：`pokemon_stats`, `stats`, `natures`, `experiences`, `growth_rates`, `types`, `pokemon_types`, `abilities`, `pokemon_abilities`（Gen3 子集也可先做）
- [ ] peewee 模型与 `MODELS` 注册；可选生成并**提交或构建时生成** `pokedex.sqlite3`
- [ ] 查询模块（恢复 v1 `_database` 职责）：`get_pokemon` / `get_experience` / `get_nature` / `get_ability` / `get_gender`
- [ ] 完成 `Stats.nature_modifiers`、`_calc_stats`、IV 范围
- [ ] 实现 `Pokemon`（或完工 `BasePokemon` + 薄包装）：PID、性格、特性、性别、种族值、IV/EV、能力值
- [ ] 测试：固定 PRNG seed 的快照；妙蛙种子 Lv5 能力值与已知公式一致
- [ ] 包导出与简短 usage 文档

**验收**：不手写 SQL，三行代码得到一只数值正确的妙蛙种子。

### Milestone 2 — 成长与招式

- [ ] 经验获得 / 升级 / `exp_to_next_level`
- [ ] `pokemon_moves` + 默认最多 4 招；学习/遗忘 API
- [ ] 进化链（`evolves_from_species_id` 已有字段）与 `evolve()` 骨架
- [ ] CLI：`pokemaster2 show bulbasaur --level 5`（调试友好）

### Milestone 3 — 游戏行为（按兴趣选）

- [ ] 持有物、亲密度、球种/捕获率（数据向）
- [ ] 简易对战数值：`BattleStats`、能力等级、命中/回避（v1 有雏形）
- [ ] 多世代 PRNG（Gen4+）
- [ ] 版本组（`emerald` 等）过滤学习面与遭遇

### Milestone 4 — 发布与生态

- [ ] 文档站点内容与 API autodoc 对齐
- [ ] 版本 CalVer 新一轮（如 `26.x.y`）
- [ ] PyPI 发布说明；CHANGELOG / towncrier
- [ ] 明确 Gen 范围与「非官方、非任天堂」免责声明

---

## 7. 架构建议（少踩坑）

```
                    ┌─────────────┐
  CSV (veekun) ──►  │  db.io.load │ ──► SQLite
                    └──────┬──────┘
                           │ peewee models
                    ┌──────▼──────┐
                    │  db.query   │  纯数据：种族、经验表、性格…
                    └──────┬──────┘
                           │
              ┌────────────▼────────────┐
              │  Pokemon / Stats / PRNG │  领域：一只「活」的怪
              └────────────┬────────────┘
                           │
                    ┌──────▼──────┐
                    │  cli / __init__ 公开 API
                    └─────────────┘
```

- **深模块**：对外只暴露 `Pokemon`、`Stats`、`PRNG`、以及「session/db 初始化」；peewee 表结构不泄漏到用户代码。
- **数据与规则分离**：公式（能力值、性别比、特性槽）放领域层；表行只当查表。
- **可测性**：PRNG 可注入；测能力值时固定 seed 与 IV。
- **数据来源**：继续 veekun CSV 许可与归属说明写进 README；可用子模块或脚本同步，避免手工改数值。

---

## 8. 三条续作路径（怎么选）

| 路径 | 适合 | 做法 |
|------|------|------|
| **A. 复兴 v2（推荐）** | 想要独立包、可控制依赖 | 按 Milestone 0 → 1 → 2 推进 |
| **B. 冷启动调用 v1 + pokedex** | 只想尽快玩 API | 维护 `pokemaster` + 钉住 pokedex 提交；与 v2 目标相悖 |
| **C. 换数据后端** | 不愿维护 CSV | 例如 pokeapi / 其他静态 JSON；要重写 query 层，PRNG/Stats 仍可留 |

推荐 **A**：v2 的 PRNG 与 Stats 已经是对的底座，缺的是「图鉴数据宽度」和「把注释掉的 Pokemon 工厂接上」。

---

## 9. 建议的近期任务拆分（可直接开 todo）

1. **工程现代化**：Python 版本、ruff、CI、Poetry 锁（Milestone 0）
2. **修复 DB 默认路径与 CSV 安全 load**（过滤未知列）
3. **导入最小 veekun 表集**并写模型
4. **实现 `Pokemon(...)` 构造 + 能力值测试**
5. **README Quickstart + usage 文档**
6. （随后）升级、招式、进化、CLI show

---

## 10. 总结

`pokemaster2` 不是空壳：它是一次**方向正确的重写**——用自带数据 + peewee 替换外部 pokedex，并保留了游戏向 PRNG 与数值骨架。停更时停在「脚手架完整、领域模型半成品、数据表仅 2 张」。

**最小有意义的下一步**：  
先让仓库在现代 Python 上可安装可测，再灌入造一只怪所需的表，把 `BasePokemon` / `Pokemon` 工厂从注释里救出来，用固定 seed 锁定妙蛙种子的能力值。

做到 Milestone 1，这个项目就重新「活」了；其余都是在 Living™ 上面加厚度。
