from enum import Enum
from typing import Optional, List
from pydantic import Field
from .base import Text_BaseModel


class GameObjectType(str, Enum):
    """游戏对象类型枚举"""
    EMPTY = "empty"
    WALL = "wall"
    PLAYER = "player"
    DOOR = "door"
    KEY = "key"
    MONSTER = "monster"
    TREASURE = "treasure"
    NPC = "npc"
    ITEM = "item"


class Direction(str, Enum):
    """方向枚举"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Position(Text_BaseModel):
    """位置坐标"""
    x: int = Field(description="X坐标")
    y: int = Field(description="Y坐标")

    def __add__(self, other: 'Position') -> 'Position':
        """位置相加"""
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __eq__(self, other: object) -> bool:
        """位置相等比较"""
        if not isinstance(other, Position):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """使位置可哈希，用作字典键"""
        return hash((self.x, self.y))


class GameObject(Text_BaseModel):
    """基础游戏对象类"""
    type: GameObjectType = Field(description="对象类型")
    name: str = Field(description="对象名称")
    symbol: str = Field(description="显示符号")
    position: Position = Field(description="位置")
    interactive: bool = Field(default=False, description="是否可交互")
    passable: bool = Field(default=False, description="是否可通过")

    @classmethod
    def get_example_instance(cls) -> 'GameObject':
        """创建示例实例"""
        return GameObject(
            type=GameObjectType.WALL,
            name="Wall",
            symbol="wall",
            position=Position(x=0, y=0),
            interactive=False,
            passable=False
        )


class Player(Text_BaseModel):
    """玩家角色类"""
    position: Position = Field(description="当前位置")
    gold: int = Field(default=0, description="金币数量")
    has_key: bool = Field(default=False, description="拥有钥匙")
    health: int = Field(default=100, description="生命值")
    max_health: int = Field(default=100, description="最大生命值")
    inventory: List[str] = Field(default_factory=list, description="背包物品")

    def move(self, dx: int, dy: int, world) -> str:
        """按方向移动玩家"""
        new_pos = Position(x=self.position.x + dx, y=self.position.y + dy)
        return world.move_player_to(new_pos)

    @classmethod
    def get_example_instance(cls) -> 'Player':
        """创建示例实例"""
        return Player(
            position=Position(x=1, y=1),
            gold=0,
            has_key=False,
            health=100,
            max_health=100,
            inventory=[]
        )


class GameCell(Text_BaseModel):
    """游戏格子"""
    position: Position = Field(description="位置")
    game_object: Optional[GameObject] = Field(default=None, description="格子中的游戏对象")

    @classmethod
    def get_example_instance(cls) -> 'GameCell':
        """创建示例实例"""
        return GameCell(
            position=Position(x=0, y=0),
            game_object=GameObject(
                type=GameObjectType.WALL,
                name="Wall",
                symbol="wall",
                position=Position(x=0, y=0)
            )
        )


class InteractionResult(Text_BaseModel):
    """交互结果"""
    success: bool = Field(description="交互是否成功")
    message: str = Field(description="结果消息")
    game_state_changed: bool = Field(default=False, description="游戏状态是否改变")

    @classmethod
    def get_example_instance(cls) -> 'InteractionResult':
        """创建示例实例"""
        return InteractionResult(
            success=True,
            message="交互成功",
            game_state_changed=True
        )