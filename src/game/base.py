from typing import Optional

class TextObject:
    """文字冒险游戏中的基础对象类"""

    def __init__(self, 
                 name: str, 
                 symbol: str, 
                 x: int = 0, 
                 y: int = 0, 
                 interactable: bool = False):
        """
        :param name: 对象名称（如“墙”、“玩家”、“门”）
        :param symbol: 在文字地图上显示的字符
        :param x: 横坐标
        :param y: 纵坐标
        :param interactable: 是否可交互
        """
        self.name = name
        self.symbol = symbol
        self.x = x
        self.y = y
        self.interactable = interactable
        self.visible = True  # 是否可见
        self.color = None

    def render(self) -> str:
        """返回在地图上显示的字符"""
        return self.symbol if self.visible else " "

    def update(self, world) -> None:
        """每回合刷新逻辑（子类可重写）"""
        pass

    def interact(self, actor) -> Optional[str]:
        """
        与玩家或其他对象交互（子类可重写）
        :param actor: 进行交互的对象（通常是玩家）
        :return: 交互结果（文字描述）
        """
        if not self.interactable:
            return f"{self.name} 似乎没什么反应。"
        return None

    def move_to(self, x: int, y: int) -> None:
        """移动对象到指定位置"""
        self.x = x
        self.y = y

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name} ({self.x},{self.y})>"