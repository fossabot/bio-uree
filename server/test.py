class lol():
    def __init__(self):
        self.a = "a"

    class abc():
        def __init__(self):
            self.b = "b"

        def bah(self):
            print(self.a)

Lol = lol()
ABC = Lol.abc()
ABC.bah()