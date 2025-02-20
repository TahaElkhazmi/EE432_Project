import tkinter as tk
from tkinter import ttk, messagebox

# Task class
class Task:
    def __init__(self, desc, priority, done=False):
        self.description = desc
        self.priority = priority
        self.is_completed = done

# LinkedList
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, task):
        n = Node(task)
        n.next = self.head
        self.head = n

    def remove(self, desc):
        cur = self.head
        prev = None
        while cur:
            if cur.task.description == desc:
                if not prev:
                    self.head = cur.next
                else:
                    prev.next = cur.next
                return True
            prev = cur
            cur = cur.next
        return False

    def get_all(self):
        tasks = []
        cur = self.head
        while cur:
            tasks.append(cur.task)
            cur = cur.next
        return tasks

# HashTable
class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [[] for _ in range(size)]
    def _hash(self, key):
        return sum(ord(x) for x in key) % self.size
    def insert(self, task):
        idx = self._hash(task.description)
        for pair in self.table[idx]:
            if pair[0] == task.description:
                pair[1] = task
                return
        self.table[idx].append([task.description, task])
    def search(self, desc):
        idx = self._hash(desc)
        for pair in self.table[idx]:
            if pair[0] == desc:
                return pair[1]
        return None
    def remove(self, desc):
        idx = self._hash(desc)
        chain = self.table[idx]
        for i, pair in enumerate(chain):
            if pair[0] == desc:
                chain.pop(i)
                return True
        return False

# BST
class BSTNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def _p(self, pr):
        p = pr.lower()
        if p == 'high':
            return 3
        elif p == 'medium':
            return 2
        return 1

    def insert(self, task):
        if not self.root:
            self.root = BSTNode(task)
        else:
            self._insert(self.root, task)

    def _insert(self, node, task):
        newp = self._p(task.priority)
        curp = self._p(node.task.priority)
        if newp < curp:
            if not node.left:
                node.left = BSTNode(task)
            else:
                self._insert(node.left, task)
        else:
            if not node.right:
                node.right = BSTNode(task)
            else:
                self._insert(node.right, task)

    def in_order(self):
        result = []
        self._in(self.root, result)
        return result

    def _in(self, node, res):
        if node:
            self._in(node.left, res)
            res.append(node.task)
            self._in(node.right, res)

    def remove_priority(self, pr):
        self.root = self._remove(self.root, pr)

    def _remove(self, node, pr):
        if not node:
            return None
        curp = self._p(node.task.priority)
        tp = self._p(pr)
        if tp < curp:
            node.left = self._remove(node.left, pr)
        elif tp > curp:
            node.right = self._remove(node.right, pr)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            m = self._min(node.right)
            node.task = m.task
            node.right = self._remove(node.right, m.task.priority)
        return node

    def _min(self, node):
        while node and node.left:
            node = node.left
        return node

# GUI
# https://docs.python.org/3/library/tkinter.html
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple ToDo")

        self.ll = LinkedList()
        self.ht = HashTable()
        self.bst = BST()

        fr = tk.Frame(root, padx=10, pady=10)
        fr.pack()

        tk.Label(fr, text="Desc:").grid(row=0, column=0)
        self.e_desc = tk.Entry(fr, width=25)
        self.e_desc.grid(row=0, column=1, padx=5)

        tk.Label(fr, text="Priority:").grid(row=0, column=2)
        self.var_p = tk.StringVar(value="Medium")
        op = ttk.OptionMenu(fr, self.var_p, "Medium", "High", "Medium", "Low")
        op.grid(row=0, column=3, padx=5)

        self.var_c = tk.BooleanVar()
        cbtn = tk.Checkbutton(fr, text="Done?", variable=self.var_c)
        cbtn.grid(row=0, column=4)

        btn_add = tk.Button(fr, text="Add Task", command=self.add_task)
        btn_add.grid(row=0, column=5, padx=5)

        fr2 = tk.Frame(root, padx=10, pady=5)
        fr2.pack()

        tk.Label(fr2, text="Search by Desc:").grid(row=0, column=0)
        self.e_search = tk.Entry(fr2, width=25)
        self.e_search.grid(row=0, column=1, padx=5)

        b_search = tk.Button(fr2, text="Search", command=self.search_task)
        b_search.grid(row=0, column=2)

        b_del = tk.Button(fr2, text="Delete by Desc", command=self.del_task)
        b_del.grid(row=0, column=3, padx=5)

        fr3 = tk.Frame(root, padx=10, pady=10)
        fr3.pack()

        self.txt = tk.Text(fr3, width=60, height=10)
        self.txt.pack()

        fr4 = tk.Frame(root, padx=10, pady=5)
        fr4.pack()

        btn_all = tk.Button(fr4, text="Show All (LL)", command=self.show_all)
        btn_all.pack(side=tk.LEFT, padx=5)

        btn_bst = tk.Button(fr4, text="Show BST", command=self.show_bst)
        btn_bst.pack(side=tk.LEFT, padx=5)

    def add_task(self):
        d = self.e_desc.get().strip()
        if not d:
            messagebox.showwarning("Warning", "Empty desc")
            return
        pr = self.var_p.get()
        dn = self.var_c.get()
        t = Task(d, pr, dn)
        self.ll.add(t)
        self.ht.insert(t)
        self.bst.insert(t)
        messagebox.showinfo("Added", "Task added")
        self.e_desc.delete(0, tk.END)
        self.var_p.set("Medium")
        self.var_c.set(False)

    def show_all(self):
        self.txt.delete("1.0", tk.END)
        for t in self.ll.get_all():
            self.txt.insert(tk.END, f"{t.description} / {t.priority} / {t.is_completed}\n")

    def show_bst(self):
        self.txt.delete("1.0", tk.END)
        tasks = self.bst.in_order()
        for t in reversed(tasks):
            self.txt.insert(tk.END, f"{t.description} / {t.priority} / {t.is_completed}\n")

    def search_task(self):
        s = self.e_search.get().strip()
        self.txt.delete("1.0", tk.END)
        if not s:
            messagebox.showwarning("Warning", "Empty search")
            return
        t = self.ht.search(s)
        if t:
            self.txt.insert(tk.END, f"Found: {t.description} / {t.priority} / {t.is_completed}\n")
        else:
            self.txt.insert(tk.END, "Not found\n")

    def del_task(self):
        s = self.e_search.get().strip()
        if not s:
            messagebox.showwarning("Warning", "Empty desc")
            return
        found = self.ht.search(s)
        if not found:
            messagebox.showwarning("Warning", "Not found")
            return
        rll = self.ll.remove(s)
        rht = self.ht.remove(s)
        self.bst.remove_priority(found.priority)
        if rll and rht:
            messagebox.showinfo("Deleted", "Task deleted")
        else:
            messagebox.showwarning("Deleted", "Error or not found")

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
