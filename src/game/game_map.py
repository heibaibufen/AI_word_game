from typing import List, Dict, Optional, Tuple
from pydantic import Field
from .types import GameObject, GameObjectType, Position, GameCell, Player
from .base import Text_BaseModel


class GameMap(Text_BaseModel):
    """用于管理关卡数据的游戏地图类"""

    width: int = Field(description="地图宽度")
    height: int = Field(description="地图高度")
    cells: List[List[GameCell]] = Field(description="地图格子")
    objects: Dict[Position, GameObject] = Field(default_factory=dict, description="地图上的对象")

    def __init__(self, width: int, height: int, **data):
        """初始化游戏地图"""
        # 创建空格子
        cells = []
        for y in range(height):
            row = []
            for x in range(width):
                cell = GameCell(position=Position(x=x, y=y))
                row.append(cell)
            cells.append(row)

        super().__init__(width=width, height=height, cells=cells, **data)

    @classmethod
    def get_example_instance(cls) -> 'GameMap':
        """创建示例实例"""
        game_map = cls(width=10, height=10)

        # 添加一些墙
        for x in range(10):
            game_map.add_object(GameObject(
                type=GameObjectType.WALL,
                name="Wall",
                symbol="#",
                position=Position(x=x, y=0)
            ))
            game_map.add_object(GameObject(
                type=GameObjectType.WALL,
                name="Wall",
                symbol="#",
                position=Position(x=x, y=9)
            ))

        for y in range(10):
            game_map.add_object(GameObject(
                type=GameObjectType.WALL,
                name="Wall",
                symbol="#",
                position=Position(x=0, y=y)
            ))
            game_map.add_object(GameObject(
                type=GameObjectType.WALL,
                name="Wall",
                symbol="#",
                position=Position(x=9, y=y)
            ))

        return game_map

    def is_valid_position(self, position: Position) -> bool:
        """检查位置是否在地图边界内有效"""
        return 0 <= position.x < self.width and 0 <= position.y < self.height

    def get_object_at(self, position: Position) -> Optional[GameObject]:
        """获取特定位置的对象"""
        return self.objects.get(position)

    def add_object(self, game_object: GameObject) -> bool:
        """向地图添加对象"""
        if not self.is_valid_position(game_object.position):
            return False

        self.objects[game_object.position] = game_object
        self.cells[game_object.position.y][game_object.position.x].game_object = game_object
        return True

    def remove_object_at(self, position: Position) -> bool:
        """移除特定位置的对象"""
        if position in self.objects:
            del self.objects[position]
            self.cells[position.y][position.x].game_object = None
            return True
        return False

    def move_object(self, from_pos: Position, to_pos: Position) -> bool:
        """将对象从一个位置移动到另一个位置"""
        if not self.is_valid_position(to_pos):
            return False

        if from_pos in self.objects:
            game_object = self.objects[from_pos]
            del self.objects[from_pos]

            # 更新旧格子
            self.cells[from_pos.y][from_pos.x].game_object = None

            # 更新对象位置
            game_object.position = to_pos

            # 添加到新位置
            self.objects[to_pos] = game_object
            self.cells[to_pos.y][to_pos.x].game_object = game_object

            return True
        return False

    def is_passable(self, position: Position) -> bool:
        """检查位置是否可通过"""
        if not self.is_valid_position(position):
            return False

        game_object = self.get_object_at(position)
        if game_object is None:
            return True

        return game_object.passable

    def get_render_data(self) -> List[List[str]]:
        """获取用于显示的渲染数据"""
        render_data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                position = Position(x=x, y=y)
                game_object = self.get_object_at(position)

                if game_object:
                    row.append(game_object.symbol)
                else:
                    row.append(" ")  # 空白空间
            render_data.append(row)

        return render_data

    @classmethod
    def from_text(cls, map_text: str) -> Tuple['GameMap', Optional[Player]]:
        """从文本表示创建游戏地图"""
        lines = map_text.strip().split('\n')

        # 移除空行
        lines = [line for line in lines if line.strip()]

        if not lines:
            raise ValueError("地图文本为空")

        # 计算尺寸（每个字符是单独的格子）
        height = len(lines)
        width = max(len(line) for line in lines)

        game_map = cls(width=width, height=height)

        # 字符到对象类型的映射（使用单个字符）
        char_map = {
            "#": GameObjectType.WALL,
            "@": GameObjectType.PLAYER,
            "D": GameObjectType.DOOR,
            "K": GameObjectType.KEY,
            "M": GameObjectType.MONSTER,
            "T": GameObjectType.TREASURE,
            "N": GameObjectType.NPC,
        }

        # 用于原始测试的中文字符映射
        chinese_map = {
            "墙": GameObjectType.WALL,
            "我": GameObjectType.PLAYER,
            "门": GameObjectType.DOOR,
            "钥": GameObjectType.KEY,
            "怪": GameObjectType.MONSTER,
            "宝": GameObjectType.TREASURE,
            "人": GameObjectType.NPC,
        }

        player = None

        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if not char.strip():
                    continue

                pos = Position(x=x, y=y)

                # 先尝试中文字符映射
                if char in chinese_map:
                    obj_type = chinese_map[char]

                    if obj_type == GameObjectType.PLAYER:
                        # 单独创建玩家
                        player = Player(position=pos)
                    else:
                        # 创建游戏对象
                        game_object = GameObject(
                            type=obj_type,
                            name=obj_type.value,
                            symbol=char,
                            position=pos,
                            interactive=obj_type in [GameObjectType.DOOR, GameObjectType.KEY,
                                                   GameObjectType.TREASURE, GameObjectType.NPC],
                            passable=obj_type in [GameObjectType.EMPTY, GameObjectType.PLAYER]
                        )
                        game_map.add_object(game_object)

                # 尝试英文字符映射
                elif char in char_map:
                    obj_type = char_map[char]

                    if obj_type == GameObjectType.PLAYER:
                        # 单独创建玩家
                        player = Player(position=pos)
                    else:
                        # 创建游戏对象
                        game_object = GameObject(
                            type=obj_type,
                            name=obj_type.value,
                            symbol=char,
                            position=pos,
                            interactive=obj_type in [GameObjectType.DOOR, GameObjectType.KEY,
                                                   GameObjectType.TREASURE, GameObjectType.NPC],
                            passable=obj_type in [GameObjectType.EMPTY, GameObjectType.PLAYER]
                        )
                        game_map.add_object(game_object)

        return game_map, player