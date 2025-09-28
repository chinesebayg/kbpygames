@echo off
echo 🎮 启动游戏服务器...
echo.
echo 📍 服务器将在 http://localhost:8000 启动
echo 🎯 游戏列表:
echo    - 首页: http://localhost:8000
echo    - RPG战斗: http://localhost:8000/rpg
echo    - 洞穴探险: http://localhost:8000/cave
echo.
echo ⏹️  按 Ctrl+C 停止服务器
echo.
python simple_web_games.py
pause

