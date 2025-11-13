from game.base import TextObject


class Wall(TextObject):
    def __init__(self, x, y):
        super().__init__(name="墙", symbol="墙", x=x, y=y, interactable=False)

class Door(TextObject):
    def __init__(self, x, y, locked=True):
        super().__init__(name="门", symbol="门", x=x, y=y, interactable=True)
        self.locked = locked

    def interact(self, actor):
        if self.locked:
            return "门被锁住了。"
        else:
            return "你推开了门，通向新的房间。"

class Treasure(TextObject):
    def __init__(self, x, y, value=100):
        super().__init__(name="宝箱", symbol="箱", x=x, y=y, interactable=True)
        self.value = value
        self.taken = False

    def interact(self, actor):
        if self.taken:
            return "宝箱已经是空的。"
        self.taken = True
        return f"你打开了宝箱，获得了 {self.value} 金币！"


class KeyItem(TextObject):
    def __init__(self, x, y):
        super().__init__(name="钥匙", symbol="钥", x=x, y=y, interactable=True)
        self.taken = False

    def interact(self, actor):
        if self.taken:
            return "这里已经什么都没有了。"
        self.taken = True
        actor.has_key = True
        return "你捡起了一把闪亮的钥匙。"


class Monster(TextObject):
    def __init__(self, x, y, hp=30):
        super().__init__(name="怪物", symbol="怪", x=x, y=y, interactable=True)
        self.hp = hp

    def interact(self, actor):
        if self.hp <= 0:
            return "怪物已经被打败。"
        self.hp -= 10
        if self.hp > 0:
            return f"你攻击了怪物！它还剩 {self.hp} 生命。"
        else:
            return "你打败了怪物！"


class Npc(TextObject):
    def __init__(self, x, y, dialog="你好，旅行者。"):
        super().__init__(name="NPC", symbol="人", x=x, y=y, interactable=True)
        self.dialog = dialog

    def interact(self, actor):
        return self.dialog

class Player(TextObject):
    def __init__(self, x, y):
        super().__init__(name="我", symbol="我", x=x, y=y, interactable=True)
        self.has_key = False

    def move(self, dx, dy, world):
        new_x, new_y = self.x + dx, self.y + dy
        if world.is_blocked(new_x, new_y):
            return "那里被挡住了。"
        world.move_object(self, new_x, new_y)
        return "你移动了一步。"