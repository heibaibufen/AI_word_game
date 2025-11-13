#!/usr/bin/env python3
"""游戏实现的基础测试脚本"""

from game.world import World
from game.types import Position

# 来自原始test.py的测试地图
map_text = """
墙墙墙墙墙墙墙
墙 我 钥 怪 门
墙 宝   人 墙
墙墙墙墙墙墙墙
"""

def test_basic_functionality():
    """测试基础游戏功能"""
    print("=== 测试AI文字游戏实现 ===\n")

    # 从文本创建世界
    world = World.from_text(map_text)
    player = world.player

    print("1. 测试从文本创建世界:")
    print(f"   玩家位置: ({player.position.x}, {player.position.y})")
    print(f"   玩家金币: {player.gold}")
    print(f"   玩家有钥匙: {player.has_key}")
    print()

    print("2. 测试世界渲染:")
    print(world.render())
    print()

    print("3. 测试玩家移动:")
    print("   向下移动:")
    result = player.move(0, 1, world)  # 向下移动
    print(f"   结果: {result}")
    print(f"   新位置: ({player.position.x}, {player.position.y})")
    print()

    print("4. 测试交互:")
    print("   向前交互:")
    result = world.interact_forward()
    print(f"   结果: {result}")
    print(f"   玩家有钥匙: {player.has_key}")
    print()

    print("5. 测试游戏状态:")
    print(f"   状态: {world.get_status()}")
    print(f"   游戏结束: {world.game_over}")
    print(f"   胜利: {world.victory}")
    print()

    print("6. 测试地图上的对象类型:")
    for y in range(world.game_map.height):
        for x in range(world.game_map.width):
            pos = world.game_map.objects.get(Position(x=x, y=y))
            if pos and pos.type != "wall":
                print(f"   在 ({x}, {y}) 发现 {pos.type} - 符号: {pos.symbol}")

    print("\n=== 基础功能测试完成 ===")
    print("所有核心类都正常工作！")

if __name__ == "__main__":
    test_basic_functionality()