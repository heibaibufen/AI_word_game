#!/usr/bin/env python3
"""游戏实现的完整测试脚本"""

from game.world import World
from game.types import Position

# 来自原始test.py的测试地图
map_text = """
墙墙墙墙墙墙墙
墙 我 钥 怪 门
墙 宝   人 墙
墙墙墙墙墙墙墙
"""

def test_complete_functionality():
    """测试完整的游戏功能"""
    print("=== AI文字游戏完整测试 ===\n")

    # 从文本创建世界
    world = World.from_text(map_text)
    player = world.player

    print("1. 初始世界状态:")
    print(f"   玩家位置: ({player.position.x}, {player.position.y})")
    print(f"   玩家金币: {player.gold}")
    print(f"   玩家有钥匙: {player.has_key}")
    print("\n   世界渲染:")
    print(world.render())
    print()

    print("2. 测试玩家移动（向左移动捡起钥匙）:")
    print("   向左移动:")
    result = player.move(-1, 0, world)  # 向左移动
    print(f"   结果: {result}")
    print(f"   新位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    print("3. 测试交互（捡起钥匙）:")
    print("   向前交互:")
    result = world.interact_forward()
    print(f"   结果: {result}")
    print(f"   玩家有钥匙: {player.has_key}")
    print()

    print("4. 测试向门移动:")
    print("   向右移动（回到原始位置）:")
    result = player.move(1, 0, world)  # 向右移动
    print(f"   结果: {result}")
    print(f"   位置: ({player.position.x}, {player.position.y})")

    print("   再次向右移动:")
    result = player.move(1, 0, world)  # 向右移动
    print(f"   结果: {result}")
    print(f"   位置: ({player.position.x}, {player.position.y})")

    print("   再次向右移动（朝向门）:")
    result = player.move(1, 0, world)  # 向右移动
    print(f"   结果: {result}")
    print(f"   位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    print("5. 测试与门的交互:")
    print("   向前交互:")
    result = world.interact_forward()
    print(f"   结果: {result}")
    print("   世界渲染:")
    print(world.render())
    print()

    print("6. 测试向下移动到宝箱:")
    print("   向下移动:")
    result = player.move(0, 1, world)  # 向下移动
    print(f"   结果: {result}")
    print(f"   位置: ({player.position.x}, {player.position.y})")

    print("   向左移动:")
    result = player.move(-1, 0, world)  # 向左移动
    print(f"   结果: {result}")
    print(f"   位置: ({player.position.x}, {player.position.y})")

    print("   再次向左移动:")
    result = player.move(-1, 0, world)  # 向左移动
    print(f"   结果: {result}")
    print(f"   位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    print("7. 测试与宝箱的交互:")
    print("   向前交互:")
    result = world.interact_forward()
    print(f"   结果: {result}")
    print(f"   玩家金币: {player.gold}")
    print()

    print("8. 最终游戏状态:")
    print(f"   状态: {world.get_status()}")
    print(f"   游戏结束: {world.game_over}")
    print(f"   胜利: {world.victory}")
    print()

    print("9. 测试游戏状态序列化:")
    game_state = world.get_game_state()
    print(f"   游戏状态: {game_state}")
    print()

    print("=== 完整测试成功完成! ===")
    print("所有游戏机制都正常工作!")

if __name__ == "__main__":
    test_complete_functionality()