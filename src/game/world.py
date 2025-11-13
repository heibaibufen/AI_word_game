from typing import List, Optional, Type
from collections import defaultdict

from game import game_map
from game.base import TextObject
from game.types import Door, Player, Wall


class World:
    """文字冒险游戏的核心世界类"""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.objects: List['TextObject'] = []  # 世界中的所有对象
        self.grid = defaultdict(list)  # 方便快速查询某格子里的对象
        self.player: Optional['Player'] = None

    # -----------------------------
    # 对象管理
    # -----------------------------
    def add_object(self, obj: 'TextObject'):
        """向世界中添加一个对象"""
        self.objects.append(obj)
        self.grid[(obj.x, obj.y)].append(obj)
        if obj.__class__.__name__ == "Player":
            self.player = obj

    def remove_object(self, obj: 'TextObject'):
        """从世界中移除一个对象"""
        self.objects.remove(obj)
        self.grid[(obj.x, obj.y)].remove(obj)

    def move_object(self, obj: 'TextObject', new_x: int, new_y: int):
        """更新对象位置"""
        if (obj.x, obj.y) in self.grid:
            self.grid[(obj.x, obj.y)].remove(obj)
        obj.move_to(new_x, new_y)
        self.grid[(new_x, new_y)].append(obj)

    # -----------------------------
    # 逻辑判断
    # -----------------------------
    def get_objects_at(self, x: int, y: int) -> List['TextObject']:
        """返回该坐标下的所有对象"""
        return self.grid.get((x, y), [])

    def is_blocked(self, x: int, y: int) -> bool:
        """判断该位置是否被阻挡"""
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return True
        for obj in self.get_objects_at(x, y):
            if obj.name == "墙":
                return True
        return False

    # -----------------------------
    # 交互与更新
    # -----------------------------
    def update(self):
        """更新所有对象的状态"""
        for obj in self.objects:
            obj.update(self)

    def interact_at(self, x: int, y: int):
        """尝试与指定位置的对象交互"""
        objs = self.get_objects_at(x, y)
        for o in objs:
            if o.interactable:
                result = o.interact(self.player)
                if result:
                    return result
        return "那里似乎没什么可以互动的。"

    # -----------------------------
    # 渲染系统
    # -----------------------------
    @classmethod
    def from_text(cls, text: str) -> 'World':
        """从文本地图创建世界"""
        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        height = len(lines)
        width = max(len(line) for line in lines)

        world = cls(width, height)

        # 定义字符 -> 类映射表
        symbol_map = game_map.symbol_map

        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch.strip() == "":
                    continue
                if ch in symbol_map:
                    obj_class = symbol_map[ch]
                    obj = obj_class(x, y)
                    # 特殊处理门：默认为未上锁
                    if isinstance(obj, Door):
                        obj.locked = False
                    world.add_object(obj)
        return world

    def render(self) -> str:
        """生成文字地图"""
        canvas = [["  " for _ in range(self.width)] for _ in range(self.height)]
        for obj in self.objects:
            if 0 <= obj.x < self.width and 0 <= obj.y < self.height and obj.visible:
                canvas[obj.y][obj.x] = obj.render()
        return "\n".join("".join(row) for row in canvas)
    def interact_forward(self):
        dx, dy = 0, 0
        if self.player is None:
            return "没有玩家。"
        # 假设朝向为上
        dx, dy = 0, -1
        target_x, target_y = self.player.x + dx, self.player.y + dy
        objs = self.get_objects_at(target_x, target_y)
        if not objs:
            return "前方什么都没有。"
        for o in objs:
            if o.interactable:
                return o.interact(self.player)
        return "没有可互动的对象。"
