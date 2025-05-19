
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


def show_display(bst, heap):
    print("\n========= SYSTEM OVERVIEW =========")
    print("BST Requests:")
    bst.print_bst()
    print("\nMaxHeap Requests:")
    heap.display_heap()
    print("===================================")


def display_menu():
    print("\n=================================")
    print("  REQUEST MANAGEMENT SYSTEM")
    print("=================================")
    print("1. Insert a new request")
    print("2. Delete request from BST")
    print("3. Search request in BST")
    print("4. Print BST (In-order)")
    print("5. Print BST (Pre-order)  ")
    print("6. Print MaxHeap")
    print("7. Process highest priority request")
    print("8. Increase priority of a request")
    print("9. Check if BST is empty")
    print("10. Check if Heap is empty")
    print("11. Get size of BST")
    print("12. Get size of Heap")
    print("13. Show system overview")
    print("14. Delete highest priority request   ")
    print("15. Exit")
    return input("Choose an option: ")


def main():
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

    while True:
        choice = display_menu()
        
        
        
        if choice == '1':
            id = int(input("Enter request ID: "))
            name = input("Enter user name: ")
            priority = int(input("Enter request priority: "))

            if bst.contains_id(id):
                print(f"❌ Request ID {id} already exists. Try a different ID.")
            else:
                bst.add_node_to_bst(id, name)
                heap.insert_heap(id, priority)
                print("✅ Request successfully inserted!")


        elif choice == '2':
            id = int(input("Enter request ID to delete: "))
            bst.remove_node_by_id(id)
            heap.delete_from_heap(id)

        elif choice == '3':
            id = int(input("Enter request ID to search: "))
            result = bst.find_by_id(id)
            if result:
                print(f"Request found - ID: {result.id}, Name: {result.name}")
            else:
                print("Request not found!")

        elif choice == '4':
            bst.print_bst()

        elif choice == '5':
            bst.print_bst_preorder()

        elif choice == '6':
            heap.display_heap()

        elif choice == '7':
            heap.process_highest_priority_request(bst)

        elif choice == '8':
            id = int(input("Enter request ID to increase priority: "))
            new_priority = int(input("Enter new priority: "))
            heap.increase_priority(id, new_priority)

        elif choice == '9':
            print("BST is empty." if bst.is_empty_bst() else "BST is not empty.")

        elif choice == '10':
            print("Heap is empty." if heap.is_empty_heap() else "Heap is not empty.")

        elif choice == '11':
            print(f"BST contains {bst.size_bst()} nodes.")

        elif choice == '12':
            print(f"Heap contains {heap.size_max_heap()} elements.")

        elif choice == '13':
            show_display(bst, heap)

        elif choice == '14':
            heap.delete_max_heap()

        elif choice == '15':
            print("Exiting program...")
            break

        else:
            print("Invalid option! Please try again.")
            


if "__main__" == __name__: main()