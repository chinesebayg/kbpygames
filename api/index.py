"""
Vercel serverless function for the web games
"""
import json
import random
import os
from datetime import datetime

# RPG战斗游戏类定义
class Character:
    """角色基类 - 所有角色的通用属性和方法"""
    
    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.damage = damage
        self.is_alive = True
    
    def take_damage(self, damage):
        """受到伤害"""
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.is_alive = False
        return damage
    
    def attack(self, target):
        """攻击目标 - 基类方法，子类需要重写"""
        if not self.is_alive or not target.is_alive:
            return 0
        
        damage = random.randint(self.damage - 5, self.damage + 5)
        actual_damage = target.take_damage(damage)
        return actual_damage
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'name': self.name,
            'hp': self.hp,
            'max_hp': self.max_hp,
            'damage': self.damage,
            'is_alive': self.is_alive,
            'character_class': getattr(self, 'character_class', '未知')
        }


class Warrior(Character):
    """战士类 - 高HP，中等伤害"""
    
    def __init__(self, name):
        super().__init__(name, hp=120, damage=25)
        self.character_class = "战士"
    
    def attack(self, target):
        """战士攻击 - 重写基类方法"""
        if not self.is_alive or not target.is_alive:
            return 0
        
        # 战士有30%概率造成暴击
        if random.random() < 0.3:
            damage = random.randint(self.damage + 10, self.damage + 20)
            actual_damage = target.take_damage(damage)
            return actual_damage, True  # 返回伤害和是否暴击
        else:
            damage = random.randint(self.damage - 5, self.damage + 5)
            actual_damage = target.take_damage(damage)
            return actual_damage, False


class Mage(Character):
    """法师类 - 低HP，高伤害"""
    
    def __init__(self, name):
        super().__init__(name, hp=80, damage=35)
        self.character_class = "法师"
    
    def attack(self, target):
        """法师攻击 - 重写基类方法"""
        if not self.is_alive or not target.is_alive:
            return 0
        
        # 法师有20%概率施放强力法术
        if random.random() < 0.2:
            damage = random.randint(self.damage + 15, self.damage + 25)
            actual_damage = target.take_damage(damage)
            return actual_damage, True  # 返回伤害和是否强力法术
        else:
            damage = random.randint(self.damage - 3, self.damage + 7)
            actual_damage = target.take_damage(damage)
            return actual_damage, False


# 20行游戏状态管理
class CaveGame:
    def __init__(self):
        self.state = "start"
        self.message = "Welcome to the game! You are in a dark cave"
        self.choices = ["left", "right"]
        self.previous_choice = None
    
    def make_choice(self, choice):
        if self.state == "start":
            if choice == "left" or choice == "right":
                self.state = "room"
                self.message = "You are in a room with a table and a chair"
                self.choices = ["sit down", "stand up"]
                self.previous_choice = choice
            else:
                self.message = "Invalid choice. Please choose 'left' or 'right'."
        
        elif self.state == "room":
            if choice == "sit down":
                self.state = "sitting"
                self.message = "You are sitting down. You need to find the magic stone"
                self.choices = ["restart"]
            elif choice == "stand up":
                self.state = "standing"
                if self.previous_choice == "right":
                    self.message = "You are standing up. You did it! You are a wizard!"
                else:
                    self.message = "You are standing up. You need to find the magic stone"
                self.choices = ["restart"]
            else:
                self.message = "Invalid choice. Please choose 'sit down' or 'stand up'."
        
        elif self.state in ["sitting", "standing"]:
            if choice == "restart":
                self.__init__()
            else:
                self.message = "Game over. Choose 'restart' to play again."


# 全局游戏状态存储（在serverless环境中使用内存存储）
games = {}
characters = {}


def handler(request):
    """Vercel serverless function handler"""
    from http.server import BaseHTTPRequestHandler
    from urllib.parse import urlparse, parse_qs
    
    # 解析请求
    parsed_url = urlparse(request.get('url', ''))
    path = parsed_url.path
    method = request.get('method', 'GET')
    
    # 设置响应头
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    
    try:
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # 处理RPG游戏API
        if path == '/api/rpg/create_character' and method == 'POST':
            data = request.get('json', {})
            name = data.get('name')
            char_class = data.get('class')
            
            if char_class == 'warrior':
                character = Warrior(name)
            elif char_class == 'mage':
                character = Mage(name)
            else:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Invalid character class'})
                }
            
            characters[name] = character.to_dict()
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps(character.to_dict(), ensure_ascii=False)
            }
        
        elif path == '/api/rpg/battle' and method == 'POST':
            data = request.get('json', {})
            player1_name = data.get('player1')
            player2_name = data.get('player2')
            
            if player1_name not in characters or player2_name not in characters:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Character not found'})
                }
            
            # 重新创建角色对象
            p1_data = characters[player1_name]
            p2_data = characters[player2_name]
            
            if p1_data['character_class'] == '战士':
                player1 = Warrior(p1_data['name'])
            else:
                player1 = Mage(p1_data['name'])
            
            if p2_data['character_class'] == '战士':
                player2 = Warrior(p2_data['name'])
            else:
                player2 = Mage(p2_data['name'])
            
            # 恢复HP状态
            player1.hp = p1_data['hp']
            player1.is_alive = p1_data['is_alive']
            player2.hp = p2_data['hp']
            player2.is_alive = p2_data['is_alive']
            
            # 随机决定攻击顺序
            if random.random() < 0.5:
                attacker, defender = player1, player2
                first_attacker = player1_name
            else:
                attacker, defender = player2, player1
                first_attacker = player2_name
            
            battle_log = []
            
            # 第一轮攻击
            if attacker.is_alive and defender.is_alive:
                result = attacker.attack(defender)
                if isinstance(result, tuple):
                    damage, is_special = result
                    if is_special:
                        if attacker.character_class == '战士':
                            battle_log.append(f"💥 {attacker.name} 发动暴击！造成 {damage} 点伤害！")
                        else:
                            battle_log.append(f"🔥 {attacker.name} 施放强力法术！造成 {damage} 点伤害！")
                    else:
                        battle_log.append(f"{attacker.name} 攻击 {defender.name}，造成 {damage} 点伤害！")
                else:
                    battle_log.append(f"{attacker.name} 攻击 {defender.name}，造成 {result} 点伤害！")
            
            # 第二轮攻击（如果双方都还活着）
            if attacker.is_alive and defender.is_alive:
                result = defender.attack(attacker)
                if isinstance(result, tuple):
                    damage, is_special = result
                    if is_special:
                        if defender.character_class == '战士':
                            battle_log.append(f"💥 {defender.name} 发动暴击！造成 {damage} 点伤害！")
                        else:
                            battle_log.append(f"🔥 {defender.name} 施放强力法术！造成 {damage} 点伤害！")
                    else:
                        battle_log.append(f"{defender.name} 反击 {attacker.name}，造成 {damage} 点伤害！")
                else:
                    battle_log.append(f"{defender.name} 反击 {attacker.name}，造成 {result} 点伤害！")
            
            # 更新角色状态
            characters[player1_name] = player1.to_dict()
            characters[player2_name] = player2.to_dict()
            
            # 检查胜负
            winner = None
            if not player1.is_alive:
                winner = player2_name
            elif not player2.is_alive:
                winner = player1_name
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'battle_log': battle_log,
                    'player1': player1.to_dict(),
                    'player2': player2.to_dict(),
                    'first_attacker': first_attacker,
                    'winner': winner
                }, ensure_ascii=False)
            }
        
        # 处理洞穴游戏API
        elif path == '/api/cave/init' and method == 'POST':
            game = CaveGame()
            game_id = str(datetime.now().timestamp())
            games[game_id] = game
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'state': game.state,
                    'message': game.message,
                    'choices': game.choices,
                    'previous_choice': game.previous_choice,
                    'game_id': game_id
                }, ensure_ascii=False)
            }
        
        elif path == '/api/cave/make_choice' and method == 'POST':
            data = request.get('json', {})
            game_id = data.get('game_id')
            choice = data.get('choice')
            
            if game_id not in games:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Game not found'})
                }
            
            game = games[game_id]
            game.make_choice(choice)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'state': game.state,
                    'message': game.message,
                    'choices': game.choices,
                    'previous_choice': game.previous_choice
                }, ensure_ascii=False)
            }
        
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Not found'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
