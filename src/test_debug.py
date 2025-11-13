#!/usr/bin/env python3
"""调试移动问题"""

from game.world import World
from game.types import Position

def debug_movement():
    """调试移动功能"""
    print("=== 调试移动 ===\n")

    # 创建一个简单的5x5地图，边界有墙
    map_text = """
#####
#我 #
# 钥#
#####
"""

    world = World.from_text(map_text)
    player = world.player

    print("1. 初始状态:")
    print(f"   玩家位置: ({player.position.x}, {player.position.y})")
    print("   世界渲染:")
    print(world.render())
    print()

    # 测试位置(2, 1)有什么 - 应该是空的
    test_pos = Position(x=2, y=1)
    print(f"2. 检查位置({test_pos.x}, {test_pos.y})有什么:")

    # 检查位置是否有效
    is_valid = world.game_map.is_valid_position(test_pos)
    print(f"   位置有效: {is_valid}")

    if is_valid:
        # 检查该位置有什么对象
        obj = world.game_map.get_object_at(test_pos)
        print(f"   位置上的对象: {obj}")

        # 检查位置是否可通行
        is_passable = world.game_map.is_passable(test_pos)
        print(f"   位置可通行: {is_passable}")

    print()

    # 检查位置(1, 1)有什么 - 当前玩家位置
    current_pos = player.position
    print(f"3. 检查当前玩家位置({current_pos.x}, {current_pos.y})有什么:")

    obj = world.game_map.get_object_at(current_pos)
    print(f"   位置上的对象: {obj}")

    is_passable = world.game_map.is_passable(current_pos)
    print(f"   位置可通行: {is_passable}")

    print()

    # 测试地图上所有对象
    print("4. 地图上的所有对象:")
    for pos, obj in world.game_map.objects.items():
        print(f"   位置({pos.x}, {pos.y}): {obj.type} - {obj.symbol} - 可通行: {obj.passable}")

if __name__ == "__main__":
    debug_movement()