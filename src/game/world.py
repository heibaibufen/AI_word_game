from pydantic import Field
from .base import Text_BaseModel
from .types import GameObject, GameObjectType, Position, Player
from .game_map import GameMap


class World(Text_BaseModel):
    """管理游戏状态和逻辑的游戏世界类"""

    game_map: GameMap = Field(description="游戏地图")
    player: Player = Field(description="玩家角色")
    game_over: bool = Field(default=False, description="游戏结束状态")
    victory: bool = Field(default=False, description="胜利状态")

    def __init__(self, game_map: GameMap, player: Player, **data):
        """用地图和玩家初始化世界"""
        super().__init__(game_map=game_map, player=player, **data)

    @classmethod
    def get_example_instance(cls) -> 'World':
        """创建示例实例"""
        game_map = GameMap.get_example_instance()
        player = Player.get_example_instance()
        return cls(game_map=game_map, player=player)

    @classmethod
    def from_text(cls, map_text: str) -> 'World':
        """从文本表示创建世界"""
        game_map, player = GameMap.from_text(map_text)
        if player is None:
            # 如果在地图中没有找到玩家，则创建默认玩家
            player = Player(position=Position(x=1, y=1))
        return cls(game_map=game_map, player=player)

    def move_player_to(self, new_position: Position) -> str:
        """移动玩家到新位置"""
        if self.game_over:
            return "游戏已结束。"

        # 检查新位置是否有效
        if not self.game_map.is_valid_position(new_position):
            return "无法移动到该位置。"

        # 检查位置是否可通过
        if not self.game_map.is_passable(new_position):
            return "前方有障碍物。"

        # 移动玩家 - 仅更新位置，玩家不存储在地图对象中
        self.player.position = new_position
        return "移动成功。"

    def get_forward_position(self) -> Position:
        """获取玩家前方的位置（默认假设玩家面向右）"""
        # 为简单起见，假设前方是右方（x+1）
        return Position(x=self.player.position.x + 1, y=self.player.position.y)

    def interact_forward(self) -> str:
        """与玩家前方的对象交互"""
        if self.game_over:
            return "游戏已结束。"

        forward_pos = self.get_forward_position()
        game_object = self.game_map.get_object_at(forward_pos)

        if game_object is None:
            return "你前方没有可交互的对象。"

        if not game_object.interactive:
            return f"{game_object.name} 无法交互。"

        return self._handle_interaction(game_object, forward_pos)

    def _handle_interaction(self, game_object: GameObject, position: Position) -> str:
        """处理与不同对象类型的交互"""
        if game_object.type == GameObjectType.DOOR:
            if self.player.has_key:
                self.game_map.remove_object_at(position)
                self.player.has_key = False
                return "你用钥匙打开了门。"
            else:
                return "门是锁着的。你需要钥匙。"

        elif game_object.type == GameObjectType.KEY:
            self.player.has_key = True
            self.game_map.remove_object_at(position)
            return "你获得了一把钥匙。"

        elif game_object.type == GameObjectType.TREASURE:
            self.player.gold += 10
            self.game_map.remove_object_at(position)
            return "你获得了10个金币。"

        elif game_object.type == GameObjectType.MONSTER:
            self.game_over = True
            return "你被怪物击败了！游戏结束。"

        elif game_object.type == GameObjectType.NPC:
            return f"{game_object.name} 说：你好，冒险者！"

        else:
            return f"无法与 {game_object.name} 交互。"

    def render(self) -> str:
        """将游戏世界渲染为文本"""
        render_data = self.game_map.get_render_data()

        # 将渲染数据转换为字符串
        lines = []
        for row in render_data:
            line = ""
            for cell in row:
                line += cell
            lines.append(line)

        # 添加玩家位置（用玩家符号覆盖）
        px, py = self.player.position.x, self.player.position.y
        if 0 <= py < len(lines) and 0 <= px < len(lines[py]):
            # 将玩家位置的格子替换为玩家符号
            row = list(lines[py])
            row[px] = "我"  # 玩家符号
            lines[py] = "".join(row)

        # 用换行符连接行
        return "\n".join(lines)

    def get_status(self) -> str:
        """获取玩家状态"""
        return f"金币: {self.player.gold}, 有钥匙: {self.player.has_key}, 生命值: {self.player.health}/{self.player.max_health}"

    def check_victory(self) -> bool:
        """检查玩家是否获胜"""
        # 简单的胜利条件：收集50个金币
        if self.player.gold >= 50:
            self.victory = True
            self.game_over = True
            return True
        return False

    def get_game_state(self) -> dict:
        """获取当前游戏状态"""
        return {
            "player_position": {"x": self.player.position.x, "y": self.player.position.y},
            "player_gold": self.player.gold,
            "player_has_key": self.player.has_key,
            "player_health": self.player.health,
            "game_over": self.game_over,
            "victory": self.victory
        }