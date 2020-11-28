class MyRange:
    def __init__(self, *args):
        flag = [all(self.is_number(i) for i in args)]
        if flag:
            self.start = 0
            self.step = 1
            if len(args) == 1:
                self.stop = args[0]
            elif 2 <= len(args) <= 3:
                self.start = args[0]
                self.stop = args[1]
                if len(args) == 3:
                    self.step = args[2]
            else:
                print("Incorrect parameters")
        else:
            raise Exception

    def __next__(self):
        if self.start < self.stop and self.step > 0:
            res = self.start
            self.start += self.step
            return res
        elif self.start > self.stop and self.step < 0:
            res = self.start
            self.start += self.step
            return res
        else:
            raise StopIteration

    def __iter__(self):
        return self

    @staticmethod
    def is_number(i):
        try:
            int(i)
            return True
        except ValueError:
            return False
.format()

print("This is python range")
for i in range(1, 10, -2):
    print(i)
print("This is my range")
for i in MyRange(10, 2, -2):
    print(i)