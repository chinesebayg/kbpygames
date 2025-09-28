import random

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
    
    def is_alive(self):
        """检查是否存活"""
        return self.is_alive
    
    def attack(self, target):
        """攻击目标 - 基类方法，子类需要重写"""
        if not self.is_alive or not target.is_alive:
            return 0
        
        damage = random.randint(self.damage - 5, self.damage + 5)
        actual_damage = target.take_damage(damage)
        return actual_damage
    
    def __str__(self):
        """字符串表示"""
        status = "存活" if self.is_alive else "死亡"
        return f"{self.name} (HP: {self.hp}/{self.max_hp}, 状态: {status})"


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
            print(f"💥 {self.name} 发动暴击！造成 {actual_damage} 点伤害！")
            return actual_damage
        else:
            damage = random.randint(self.damage - 5, self.damage + 5)
            actual_damage = target.take_damage(damage)
            return actual_damage


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
            print(f"🔥 {self.name} 施放强力法术！造成 {actual_damage} 点伤害！")
            return actual_damage
        else:
            damage = random.randint(self.damage - 3, self.damage + 7)
            actual_damage = target.take_damage(damage)
            return actual_damage


def create_character():
    """创建角色"""
    print("\n=== 角色创建 ===")
    name = input("请输入角色名字: ")
    
    print("请选择职业:")
    print("1. 战士 (高HP，中等伤害)")
    print("2. 法师 (低HP，高伤害)")
    
    while True:
        choice = input("请输入选择 (1/2): ")
        if choice == "1":
            return Warrior(name)
        elif choice == "2":
            return Mage(name)
        else:
            print("无效选择，请重新输入！")


def battle_round(player1, player2):
    """一回合战斗逻辑"""
    print(f"\n--- 战斗回合 ---")
    print(f"{player1}")
    print(f"{player2}")
    
    # 随机决定攻击顺序
    if random.random() < 0.5:
        attacker, defender = player1, player2
        print(f"\n{player1.name} 先攻！")
    else:
        attacker, defender = player2, player1
        print(f"\n{player2.name} 先攻！")
    
    # 第一轮攻击
    if attacker.is_alive and defender.is_alive:
        damage = attacker.attack(defender)
        if damage > 0:
            print(f"{attacker.name} 攻击 {defender.name}，造成 {damage} 点伤害！")
    
    # 第二轮攻击（如果双方都还活着）
    if attacker.is_alive and defender.is_alive:
        damage = defender.attack(attacker)
        if damage > 0:
            print(f"{defender.name} 反击 {attacker.name}，造成 {damage} 点伤害！")


def main():
    """主函数 - 控制整个战斗流程"""
    print("🎮 欢迎来到RPG战斗模拟器！")
    print("=" * 50)
    
    # 角色创建
    print("\n玩家1创建角色:")
    player1 = create_character()
    
    print("\n玩家2创建角色:")
    player2 = create_character()
    
    print(f"\n战斗开始！")
    print(f"玩家1: {player1.name} ({player1.character_class})")
    print(f"玩家2: {player2.name} ({player2.character_class})")
    print("=" * 50)
    
    # 回合制战斗
    round_count = 1
    while player1.is_alive and player2.is_alive:
        print(f"\n第 {round_count} 回合")
        battle_round(player1, player2)
        round_count += 1
        
        # 检查战斗是否结束
        if not player1.is_alive:
            print(f"\n🏆 战斗结束！{player2.name} 获胜！")
            break
        elif not player2.is_alive:
            print(f"\n🏆 战斗结束！{player1.name} 获胜！")
            break
    
    print("\n游戏结束，感谢游玩！")


if __name__ == "__main__":
    main()
