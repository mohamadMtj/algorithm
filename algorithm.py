

class BSTNode:
    def __init__(this, id, name):
        this.id = id
        this.name = name
        this.left = None
        this.right = None


class BST:
    def __init__(this):
        this.root = None

    def node_counter(this, node):
        if not node:
            return 0
        return 1 + this.node_counter(node.left) + this.node_counter(node.right)

    def _print_in_order(this, node):
        if node:
            this._print_in_order(node.left)
            print(f"ID: {node.id}, Name: {node.name}")
            this._print_in_order(node.right)

    def _print_preorder(this, node):
        if node:
            print(f"ID: {node.id}, Name: {node.name}")
            this._print_preorder(node.left)
            this._print_preorder(node.right)

    def contains_id(this, id):
        pointer = this.root
        while pointer:
            if id == pointer.id:
                return True
            elif id < pointer.id:
                pointer = pointer.left
            else:
                pointer = pointer.right
        return False

    def add_node_to_bst(this, id, name):
        if this.contains_id(id):
            print(f"Request ID {id} already exists!")
            return

        new_node = BSTNode(id, name)
        if not this.root:
            this.root = new_node
            return

        pointer = this.root
        parent = None
        while pointer:
            parent = pointer
            if id < pointer.id:
                pointer = pointer.left
            else:
                pointer = pointer.right

        if id < parent.id:
            parent.left = new_node
        else:
            parent.right = new_node

    def find_by_id(this, id):
        pointer = this.root
        while pointer:
            if id == pointer.id:
                return pointer
            elif id < pointer.id:
                pointer = pointer.left
            else:
                pointer = pointer.right
        return None

    def _delete_node(this, node, id):
        if not node:
            print(f"Request ID {id} not found in BST!")
            return None

        if id < node.id:
            node.left = this._delete_node(node.left, id)
        elif id > node.id:
            node.right = this._delete_node(node.right, id)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            p = this.find_min_node(node.right)
            node.id, node.name = p.id, p.name
            node.right = this._delete_node(node.right, p.id)

        return node

    def remove_node_by_id(this, id):
        this.root = this._delete_node(this.root, id)

    def find_min_node(this, node):
        pointer = node
        while pointer.left:
            pointer = pointer.left
        return pointer

    def print_bst(this):
        print("BST (In-order Traversal - Sorted by ID):")
        if not this.root:
            print("BST is empty.")
        else:
            this._print_in_order(this.root)

    def print_bst_preorder(this):
        print("BST (Pre-order Traversal):")
        if not this.root:
            print("BST is empty.")
        else:
            this._print_preorder(this.root)

    def is_empty_bst(this):
        return this.root is None

    def size_bst(this):
        return this.node_counter(this.root)


class MaxHeap:
    def __init__(this):
        this.heap = []

    def insert_heap(this, id, priority):
        this.heap.append({'id': id, 'priority': priority})
        this._heapify_up(len(this.heap) - 1)

    def _heapify_up(this, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if this.heap[parent]['priority'] < this.heap[idx]['priority']:
                this.heap[parent], this.heap[idx] = this.heap[idx], this.heap[parent]
                idx = parent
            else:
                break

    def _heapify_down(this, idx):
        size = len(this.heap)
        largest = idx
        left = 2 * idx
        right = 2 * idx + 1

        if left < size and this.heap[left]['priority'] > this.heap[largest]['priority']:
            largest = left
        if right < size and this.heap[right]['priority'] > this.heap[largest]['priority']:
            largest = right

        if largest != idx:
            this.heap[largest], this.heap[idx] = this.heap[idx], this.heap[largest]
            this._heapify_down(largest)

    def find_index_by_id(this, id):
        for idx, item in enumerate(this.heap):
            if item['id'] == id:
                return idx
        return -1

    def delete_from_heap(this, id):
        idx = this.find_index_by_id(id)
        if idx == -1:
            print(f"Request ID {id} not found in Heap!")
            return

        this.heap[idx] = this.heap[-1]
        this.heap.pop()
        if idx < len(this.heap):
            this._heapify_down(idx)
        print(f"Request ID {id} has been deleted from Heap.")

    def delete_max_heap(this):
        if not this.heap:
            print("Heap is empty!")
            return
        print(f"Deleted request: {this.heap[0]['id']} with priority {this.heap[0]['priority']}")
        this.heap[0] = this.heap[-1]
        this.heap.pop()
        if this.heap:
            this._heapify_down(0)

    def process_highest_priority_request(this, bst):
        if not this.heap:
            print("No requests to process!")
            return

        top = this.heap[0]
        print("Processing request...")
        print(f"Request ID: {top['id']} | Priority: {top['priority']}")
        this.delete_max_heap()
        bst.remove_node_by_id(top['id'])
        print(f"Request ID {top['id']} has been removed from both MaxHeap and BST.")

    def increase_priority(this, id, new_priority):
        idx = this.find_index_by_id(id)
        if idx == -1:
            print(f"Request ID {id} not found!")
            return

        if new_priority <= this.heap[idx]['priority']:
            print("New priority must be greater than current priority!")
            return

        this.heap[idx]['priority'] = new_priority
        this._heapify_up(idx)
        print(f"Priority for request ID {id} updated to {new_priority}.")

    def display_heap(this):
        print("MaxHeap (Sorted by Priority - Highest First):")
        if not this.heap:
            print("Heap is empty.")
            return

        for item in sorted(this.heap, key=lambda x: x['priority'], reverse=True):
            print(f"ID: {item['id']}, Priority: {item['priority']}")

    def is_empty_heap(this):
        return len(this.heap) == 0

    def size_max_heap(this):
        return len(this.heap)



def selectOption():
    menuItems = '''\nHOW CAN I HELP YOU?\n
1) View all requests
2) Insert request
3) Increase priority
4) Process request
5) Search request
6) Delete request
7) Print BST (Preorder)
8) Visualize system overview
9) Exit'''
    print(menuItems)
    while True:
        choice = input("\nEnter your choice (1-9): ")
        if choice.isdigit() and 1 <= int(choice) <= 9:
            return int(choice)
        else:
            print("Invalid, try again.")


def getValue(mode):
    while True:
        try:
            value = int(input(f"Enter {mode} (as a number): "))
            return value
        except ValueError:
            print(f"Invalid input. Please enter a numeric value for {mode}.")


bst = BST()
heap = MaxHeap()

list_data = [
    (1, "mohamad", 60),
    (2, "ali", 40),
    (3, "arash", 80),
    (4, "poya", 70),
    (5, "hani", 100)
]
for id, name, priority in list_data:
    bst.add_node_to_bst(id, name)
    heap.insert_heap(id, priority)


def viewRequests():
    bst.print_bst()
    heap.display_heap()


def insertRequest():
    while True:
        name = input("Enter request name: ")
        id = getValue("request ID")
        priority = getValue("priority")
        if bst.contains_id(id):
            print(f"\n❌ Request ID {id} already exists.")
        else:
            bst.add_node_to_bst(id, name)
            heap.insert_heap(id, priority)
            print("\n✅ Request inserted.")
        if input("\nPress [R] to return or [Enter] to insert another: ").lower() == 'r':
            break


def increasePriority():
    while True:
        id = getValue("request ID")
        priority = getValue("new priority")
        heap.increase_priority(id, priority)
        if input("\nPress [R] to return or [Enter] to continue: ").lower() == 'r':
            break


def processRequest():
    while True:
        heap.process_highest_priority_request(bst)
        if input("\nPress [R] to return or [Enter] to continue: ").lower() == 'r':
            break


def searchRequest():
    while True:
        id = getValue("request ID")
        result = bst.find_by_id(id)
        if result:
            print(f"\nRequest found: {result.name}")
        else:
            print("\nRequest not found.")
        if input("\nPress [R] to return or [Enter] to search again: ").lower() == 'r':
            break


def deleteRequest():
    while True:
        id = getValue("request ID")
        bst.remove_node_by_id(id)
        heap.delete_from_heap(id)
        if input("\nPress [R] to return or [Enter] to delete another: ").lower() == 'r':
            break


def printPreorder():
    bst.print_bst_preorder()
    
def processRequest():
    while True:
        heap.process_highest_priority_request(bst)
        if input("\nPress [R] to return or [Enter] to continue: ").lower() == 'r':
            break    


while True:
    option = selectOption()
    print()
    if option == 1:
        viewRequests()
    elif option == 2:
        insertRequest()
    elif option == 3:
        increasePriority()
    elif option == 4:
        processRequest()
    elif option == 5:
        searchRequest()
    elif option == 6:
        deleteRequest()
    elif option == 7:
        printPreorder()
    elif option ==8 :
        processRequest()
    else:
        print("Goodbye!")
        break
    input("\nPress [Enter] to continue...")
