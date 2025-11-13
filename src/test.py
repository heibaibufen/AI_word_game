from game.world import World


map_text = """
墙墙墙墙墙墙墙
墙 我 钥 怪 门
墙 宝   人 墙
墙墙墙墙墙墙墙
"""

world = World.from_text(map_text)
player = world.player

print("=== 欢迎来到 AI 文字冒险 Demo ===")
print("指令：上 下 左 右 看 互助 状态 退出\n")
print(world.render())

while True:
    cmd = input("\n> ").strip()
    if cmd in ("退出", "q"):
        print("游戏结束。")
        break
    elif cmd == "看":
        print(world.render())
    elif cmd in ("上", "下", "左", "右"):
        dx, dy = 0, 0
        if cmd == "上": dy = -1
        if cmd == "下": dy = 1
        if cmd == "左": dx = -1
        if cmd == "右": dx = 1
        print(player.move(dx, dy, world))
        print(world.render())
    elif cmd in ("查", "互动"):
        print(world.interact_forward())
    elif cmd == "状态":
        print(f"金币: {player.gold}, 有钥匙: {player.has_key}")
    else:
        print("未知指令。")