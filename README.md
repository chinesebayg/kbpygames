# 游戏合集 Web 应用

这是一个基于 Flask 的 Web 游戏应用，包含两个经典游戏：

1. **RPG战斗模拟器** - 回合制战斗游戏
2. **洞穴探险** - 文字冒险游戏

## 功能特色

### RPG战斗模拟器
- 🎮 基于面向对象编程设计
- ⚔️ 两种职业：战士（高HP，暴击）和法师（高伤害，强力法术）
- 🔄 回合制战斗系统
- 📊 实时战斗日志和状态显示
- 💥 特殊技能和随机伤害

### 洞穴探险
- 🏔️ 经典的文字冒险游戏
- 🎯 多分支剧情选择
- 🧙‍♂️ 寻找魔法石的冒险
- 📈 游戏进度可视化
- 🔄 可重复游玩

## 技术特性

- 🌐 现代化响应式 Web 界面
- 📱 支持各种设备访问
- ⚡ 无需刷新页面的实时交互
- 🎨 美观的 UI 设计和动画效果
- 🔧 基于 Flask 的后端 API

## 安装和运行

### 方法一：简化版本（推荐，无需安装额外依赖）

直接运行简化版服务器：

```bash
python simple_web_games.py
```

或者双击运行 `start_games.bat` 文件（Windows）

### 方法二：Flask版本（需要安装Flask）

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
python app.py
```

### 访问游戏

打开浏览器访问：
- **简化版本**：http://localhost:8000
- **Flask版本**：http://localhost:5000

## 游戏玩法

### RPG战斗模拟器
1. 创建两个角色（输入名字并选择职业）
2. 点击"开始战斗"开始回合制战斗
3. 观看战斗过程和结果
4. 可以重新开始新的战斗

### 洞穴探险
1. 点击"开始游戏"开始冒险
2. 根据提示做出选择（向左/向右，坐下/站起来）
3. 尝试不同的选择组合找到魔法石
4. 成为强大的魔法师！

## 项目结构

```
├── app.py                 # Flask 应用主文件
├── requirements.txt       # Python 依赖
├── README.md             # 项目说明
├── templates/            # HTML 模板
│   ├── base.html         # 基础模板
│   ├── index.html        # 首页
│   ├── rpg_game.html     # RPG 游戏页面
│   └── cave_game.html    # 洞穴探险页面
├── 20linegame.py         # 原始洞穴游戏代码
└── rpg_battle_simulator.py # 原始 RPG 游戏代码
```

## 开发说明

- 使用 Flask 作为 Web 框架
- 前端使用 Bootstrap 5 和 Font Awesome 图标
- JavaScript 处理前端交互
- Session 存储游戏状态
- RESTful API 设计

## 扩展功能

可以考虑添加的功能：
- 更多职业和技能
- 装备系统
- 存档功能
- 多人对战
- 音效和背景音乐
- 成就系统

享受游戏吧！🎮
