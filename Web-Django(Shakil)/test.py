class A:
    def method(self):
        print("A method")

class B(A):
    def method(self):
        print("B method")

obj = B()
obj.method()