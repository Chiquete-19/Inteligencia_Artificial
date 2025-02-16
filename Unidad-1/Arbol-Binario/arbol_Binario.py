class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def Print (self):
        if self.left:
            self.left.Print()
        print (self.data),
        if self.right:
            self.right.Print()

def Search(root, data):
    if root is None or root.data == data:
        return root
    if root.data < data:
        return Search(root.right, data)
    return Search(root.left, data)

root = Node(12)
root.insert(10)
root.insert(4)
root.insert(9)
root.insert(3)
root.Print()

print("Found" if Search(root, 4) else "Not Found")
