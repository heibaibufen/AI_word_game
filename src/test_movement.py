#!/usr/bin/env python3
"""测试移动功能"""

from game.world import World
from game.types import Position, GameObject, GameObjectType

def create_test_world():
    """创建一个简单的测试世界"""
    # 创建一个简单的5x5地图，边界有墙
    map_text = """
#####
#我 #
# 钥#
#####
"""

    world = World.from_text(map_text)
    return world

def test_movement():
    """测试基本移动功能"""
    print("=== 测试移动功能 ===\n")

    world = create_test_world()
    player = world.player

    print("1. 初始状态:")
    print(f"   玩家位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    print("2. 测试移动到空白空间:")
    print("   向右移动:")
    result = player.move(1, 0, world)
    print(f"   结果: {result}")
    print(f"   新位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    print("3. 测试移动到墙:")
    print("   向右移动（撞墙）:")
    result = player.move(1, 0, world)
    print(f"   结果: {result}")
    print(f"   位置: ({player.position.x}, {player.position.y})")
    print()

    print("4. 测试向下移动:")
    print("   向下移动:")
    result = player.move(0, 1, world)
    print(f"   结果: {result}")
    print(f"   新位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    print("5. 测试移动到钥匙:")
    print("   向右移动（朝向钥匙）:")
    result = player.move(1, 0, world)
    print(f"   结果: {result}")
    print(f"   新位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    print("6. 测试与钥匙的交互:")
    print("   向前交互:")
    result = world.interact_forward()
    print(f"   结果: {result}")
    print(f"   玩家有钥匙: {player.has_key}")
    print()

if __name__ == "__main__":
    test_movement()