# CIE A Level 9702 物理中英双语讲义

面向 CIE A Level 物理（9702）的中英双语讲义网站（Redutech 版），覆盖 AS 与 A2 全部章节。本仓库为 [Redutech Global Apps Centre](https://redutechglobal.com/apps/) 9702 讲义的生产版本镜像。

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**在线访问：** https://redutechglobal.com/apps/9702

---

## 内容概览

| 项目 | 数量 |
|---|---|
| 章节 | 27 章（第 1–26 章 + 附录 A） |
| 小节 | 176 个 |
| 例题 | 202 道 |
| 练习 | 311 道（含真题来源标签） |
| 插图 | 249 张 PNG |

### 章节列表

| # | 章节 | Chapter |
|---|---|---|
| 1 | 物理量与单位 | Physical quantities and units |
| 2 | 运动学 | Kinematics |
| 3 | 动力学 | Dynamics |
| 4 | 力、密度与压强 | Forces, density and pressure |
| 5 | 功、能量与功率 | Work, energy and power |
| 6 | 固体的形变 | Deformation of solids |
| 7 | 波 | Waves |
| 8 | 叠加 | Superposition |
| 9 | 电学 | Electricity |
| 10 | 直流电路 | D.C. circuits |
| 11 | 粒子物理 | Particle physics |
| 12 | 圆周运动 | Motion in a circle |
| 13 | 引力场 | Gravitational fields |
| 14 | 温度 | Temperature |
| 15 | 理想气体 | Ideal gases |
| 16 | 热力学 | Thermodynamics |
| 17 | 振动 | Oscillations |
| 18 | 电场 | Electric fields |
| 19 | 电容 | Capacitance |
| 20 | 磁场 | Magnetic fields |
| 21 | 交流电 | Alternating currents |
| 22 | 量子物理 | Quantum physics |
| 23 | 核物理 | Nuclear physics |
| 24 | 医学物理 | Medical physics |
| 25 | 天体物理与宇宙学 | Astronomy and cosmology |
| 26 | 实验技能（Paper 3 & 5） | Practical skills |
| A | 附录：数据、公式与术语 | Data, formulae and glossary |

---

## 技术说明

整个站点是**单文件** `index.html`（约 1.5 MB），所有章节内嵌其中，通过 JavaScript 切换视图，无构建步骤、无外部依赖：

- 数学公式：[MathJax](https://www.mathjax.org/) 渲染 LaTeX（行内 `$...$`、独立块 `$$...$$`）
- 插图：统一引用 `images/` 下的 PNG，**不使用内联 SVG**
- 样式与脚本全部内联，可直接双击本地打开或部署到任意静态托管

### 目录结构

```
9702/
├── index.html              # 站点主体（全部内容）
├── images/                 # 249 张插图，命名 ch<章>_fig|example|practice<...>.png
├── update_chapter.py       # 章节更新自动化脚本
├── Redutech_logotrans.png  # 站点 Logo
├── favicon.* / apple-touch-icon.png
└── .claude/skills/update-chapter.md
```

---

## 本地使用

无需安装任何依赖，直接打开：

```bash
xdg-open index.html   # 或浏览器拖入文件
```

如需本地服务：

```bash
python3 -m http.server 8000
```

---

## 更新章节流程

章节内容通过 `update_chapter.py` 三步流水线更新：

```bash
# 1. 抽取当前章节 HTML
python3 update_chapter.py prepare <N>

# 2. 编写新章节 HTML → /tmp/ch<N>_new.html
#    插图一律用 <img src="images/...">，禁止内联 SVG

# 3. 校验并写入 ruiqi 站点的 index.html（自动校验标签闭合、LaTeX $ 配对、SVG 策略）
python3 update_chapter.py apply <N> /tmp/ch<N>_new.html
```

`apply` 会直接写入生产站点 `/home/bill/nas/ruiqi_website/9702/index.html`，自动生成 `index.html.bak_ch<N>` 安全备份，并在校验失败时中止。更新后执行 `./deploy.sh` 同步到本仓库。

在 Claude Code 中亦可直接使用技能：`/update-chapter <N>`。

---

## 版本管理

一键提交并推送：

```bash
./deploy.sh                  # 自动生成提交信息
./deploy.sh "更新第 5 章"     # 指定提交信息
```

脚本会自动检测 mihomo 代理（7890）连通性、检查 GitHub 是否可达、提示超过 50 MB 的文件；若没有改动则直接退出。

也可以手动：

```bash
git add -A && git commit -m "更新第 N 章" && git push
```

以下内容不纳入版本控制（见 `.gitignore`）：

- `backups/` — 历史 `index.html.bak_*` 备份
- `screenshot*/` — 更新过程截图
- `__pycache__/`、`*.log`

---

## 许可证

本项目自有内容（讲义整理、插图、代码）采用
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-Hans) 许可：

- **署名** — 转载需注明来源并链接回本仓库
- **非商业性使用** — 不得用于商业目的（如付费课程、付费讲义）
- **相同方式共享** — 修改后的作品须以相同许可证发布

详见 [LICENSE](LICENSE)。

### 双许可 / 商业授权

本项目的**版权人（项目作者）自身不受上述 NonCommercial 条款限制**，可自由地将本项目内容用于商业用途。

如需**商业使用**本项目，请联系作者获取商业授权：

- GitHub：[@BillWANG0312](https://github.com/BillWANG0312)

> 说明：商业授权仅涵盖本项目作者享有版权的部分（讲义整理、插图、代码）；文中引用的 Cambridge 试题与教材素材需由使用者另行取得 Cambridge 授权。

> **例外：** 文中引用的 CIE / Cambridge 试题与教材素材版权归 Cambridge International 所有，**不适用本许可证**，仅作教学参考使用；如需商用请自行取得授权。
