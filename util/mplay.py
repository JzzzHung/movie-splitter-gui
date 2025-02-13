class mPlay():

    def __init__(self, display):
        self.display = display
        self.counter = 0
        self.playList = [
            'There is no video to split.',
            'There is no video to split! Please select at least one video.',
            'NO VIDEO LA!!!',
            '(╯°Д°)╯ ┻┻',
            "┳┳ ╭( ' - '╭)"
                         ]

    def play(self):
        if self.counter < 3:
            self.display(self.playList[self.counter], 0)
        else:
            if self.counter % 2 != 0:
                # @REF https://facemood.grtimed.com/classification/%E6%86%A4%E6%80%92
                self.display(self.playList[3], 0)
            else:
                # @REF https://facemood.grtimed.com/classification/%E7%84%A1%E5%A5%88
                # @REF https://www.compart.com/en/unicode/U+256D
                self.display(self.playList[4], 0)
        self.counter += 1

    def resetCounter(self):
        self.counter = 0