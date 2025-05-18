


#include<algorithm>
#include <iostream>
#include <vector>
using namespace std;

class BSTNode {
public:
    int request_id;
    string username;
    BSTNode* left;
    BSTNode* right;

    BSTNode(int _id, string _name) {
        this->request_id = _id;
        this->username = _name;
        this->left = nullptr;
        this->right = nullptr;
    }
};

class BST {
private:
    BSTNode* root;

    int node_counter(BSTNode* node) {
        if (node == nullptr) return 0;
        return 1 + node_counter(node->left) + node_counter(node->right);
    }

    void printInOrder(BSTNode* node) {
        if (node) {
            printInOrder(node->left);
            cout << "ID: " << node->request_id << ", Name: " << node->username << endl;
            printInOrder(node->right);
        }
    }

public:
    BST() {
        this->root = nullptr;
    }

    bool contains_id(int request_id) {
        BSTNode* pointer = root;
        while (pointer != nullptr) {
            if (request_id == pointer->request_id) return true;
            else if (request_id < pointer->request_id) pointer = pointer->left;
            else pointer = pointer->right;
        }
        return false;
    }

    void add_node_to_bst(int request_id, string username) {
        if (contains_id(request_id)) {
            cout << "Request ID " << request_id << " already exists!\n";
            return;
        }

        if (root == nullptr) {
            root = new BSTNode(request_id, username);
            return;
        }

        BSTNode* pointer = root;
        BSTNode* parent = nullptr;

        while (pointer != nullptr) {
            parent = pointer;
            if (request_id < pointer->request_id)
                pointer = pointer->left;
            else if (request_id > pointer->request_id)
                pointer = pointer->right;
        }

        if (request_id < parent->request_id)
            parent->left = new BSTNode(request_id, username);
        else
            parent->right = new BSTNode(request_id, username);
    }

    BSTNode* find_by_id(int request_id) {
        BSTNode* pointer = root;
        while (pointer != nullptr) {
            if (request_id == pointer->request_id) return pointer;
            else if (request_id < pointer->request_id) pointer = pointer->left;
            else pointer = pointer->right;
        }
        return nullptr;
    }

    void remove_node_by_id(int request_id) {
        BSTNode* pointer = root;
        BSTNode* parent = nullptr;

        while (pointer != nullptr && pointer->request_id != request_id) {
            parent = pointer;
            if (request_id < pointer->request_id)
                pointer = pointer->left;
            else
                pointer = pointer->right;
        }

        if (pointer == nullptr) {
            cout << "Request ID " << request_id << " not found in BST!\n";
            return;
        }

        if (pointer->left == nullptr && pointer->right == nullptr) {
            if (pointer == root) root = nullptr;
            else if (parent->left == pointer) parent->left = nullptr;
            else parent->right = nullptr;
        }
        else if (pointer->left == nullptr || pointer->right == nullptr) {
            BSTNode* child = (pointer->left != nullptr) ? pointer->left : pointer->right;
            if (pointer == root) root = child;
            else if (parent->left == pointer) parent->left = child;
            else parent->right = child;
        }
        else {
            BSTNode* successorParent = pointer;
            BSTNode* successor = pointer->right;

            while (successor->left != nullptr) {
                successorParent = successor;
                successor = successor->left;
            }

            pointer->request_id = successor->request_id;
            pointer->username = successor->username;

            if (successorParent->left == successor)
                successorParent->left = successor->right;
            else
                successorParent->right = successor->right;
        }

        delete pointer;
        cout << "Request ID " << request_id << " has been deleted from BST.\n";
    }

    void printBST() {
        cout << "BST (In-order Traversal - Sorted by ID):\n";
        if (root == nullptr) {
            cout << "BST is empty.\n";
            return;
        }
        printInOrder(root);
    }

    bool isEmptyBST() {
        return root == nullptr;
    }

    int sizeBST() {
        return node_counter(root);
    }
};

class MaxHeap {
private:
    struct Request {
        int request_id, priority;
    };

    vector<Request> heap;

    void maxHeapify(int idx) {
        int largest = idx;
        int left = 2 * idx + 1;
        int right = 2 * idx + 2;

        if (left < heap.size() && heap[left].priority > heap[largest].priority) largest = left;
        if (right < heap.size() && heap[right].priority > heap[largest].priority) largest = right;

        if (largest != idx) {
            swap(heap[idx], heap[largest]);
            maxHeapify(largest);
        }
    }

    int findIndexById(int request_id) {
        for (int idx = 0; idx < heap.size(); idx++) {
            if (heap[idx].request_id == request_id) return idx;
        }
        return -1;
    }

public:
    MaxHeap() {}

    void insertHeap(int request_id, int priority) {
        Request newRequest = { request_id, priority };
        heap.push_back(newRequest);
        int idx = heap.size() - 1;

        while (idx > 0 && heap[(idx - 1) / 2].priority < heap[idx].priority) {
            swap(heap[idx], heap[(idx - 1) / 2]);
            idx = (idx - 1) / 2;
        }
    }

    void deleteFromHeap(int request_id) {
        int idx = findIndexById(request_id);
        if (idx == -1) {
            cout << "Request ID " << request_id << " not found in Heap!\n";
            return;
        }

        heap[idx] = heap.back();
        heap.pop_back();

        if (!heap.empty()) {
            maxHeapify(idx);
        }

        cout << "Request ID " << request_id << " has been deleted from Heap.\n";
    }

    void deleteMaxHeap() {
        if (heap.empty()) {
            cout << "Heap is empty!\n";
            return;
        }
        cout << "Deleted request: " << heap[0].request_id << " with priority " << heap[0].priority << endl;
        heap[0] = heap.back();
        heap.pop_back();

        if (!heap.empty()) {
            maxHeapify(0);
        }
    }

    void processHighestPriorityRequest(BST& this_bst) {
        if (heap.empty()) {
            cout << "No requests to process!\n";
            return;
        }

        int request_id = heap[0].request_id;
        int priority = heap[0].priority;

        cout << "Processing request...\n";
        cout << "Request ID: " << request_id << " | Priority: " << priority << endl;

        deleteMaxHeap();
        this_bst.remove_node_by_id(request_id);

        cout << "Request ID " << request_id << " has been removed from both MaxHeap and BST.\n";
    }

    void increasePriority(int request_id, int newPriority) {
        int idx = findIndexById(request_id);
        if (idx == -1) {
            cout << "Request ID " << request_id << " not found!\n";
            return;
        }

        if (newPriority <= heap[idx].priority) {
            cout << "New priority must be greater than current priority!\n";
            return;
        }

        heap[idx].priority = newPriority;

        while (idx > 0 && heap[(idx - 1) / 2].priority < heap[idx].priority) {
            swap(heap[idx], heap[(idx - 1) / 2]);
            idx = (idx - 1) / 2;
        }

        cout << "Priority for request ID " << request_id << " updated to " << newPriority << ".\n";
    }

    void display_heap() {
        cout << "MaxHeap (Sorted by Priority - Highest First):\n";
        if (heap.empty()) {
            cout << "Heap is empty.\n";
            return;
        }

        vector<Request> p = heap;
        sort(p.begin(), p.end(), [](Request a, Request b) {
            return a.priority > b.priority;
            });

        for (const auto& request : p) {
            cout << "ID: " << request.request_id << ", Priority: " << request.priority << endl;
        }
    }

    bool isEmptyHeap() {
        return heap.empty();
    }

    int sizeMaxHeap() {
        return heap.size();
    }
};


void show_display(BST& this_bst, MaxHeap& this_heap) {
    cout << "\n========= SYSTEM OVERVIEW =========\n";
    cout << "BST Requests:\n";
    this_bst.printBST();
    cout << "\nMaxHeap Requests:\n";
    this_heap.display_heap();
    cout << "===================================\n";
}

void display_menu() {
    cout << "\n=================================\n";
    cout << "  REQUEST MANAGEMENT SYSTEM\n";
    cout << "=================================\n";
    cout << "1. Insert a new request\n";
    cout << "2. Delete request from BST\n";
    cout << "3. Search request in BST\n";
    cout << "4. Print BST\n";
    cout << "5. Print MaxHeap\n";
    cout << "6. Delete highest priority request\n";
    cout << "7. Process highest priority request\n";
    cout << "8. Increase priority of a request\n";
    cout << "9. Check if BST is empty\n";
    cout << "10. Check if Heap is empty\n";
    cout << "11. Get size of BST\n";
    cout << "12. Get size of Heap\n";
    cout << "13. Show system overview\n";
    cout << "14. Exit\n";
    cout << "Choose an option: ";
}

int main() {
    BST this_bst;
    MaxHeap this_heap;
    int choice;

    this_bst.add_node_to_bst(1, "Alice"); this_heap.insertHeap(1, 50);
    this_bst.add_node_to_bst(2, "Bob"); this_heap.insertHeap(2, 30);
    this_bst.add_node_to_bst(3, "Charlie"); this_heap.insertHeap(3, 70);
    this_bst.add_node_to_bst(4, "David"); this_heap.insertHeap(4, 60);
    this_bst.add_node_to_bst(5, "Eve"); this_heap.insertHeap(5, 90);

    while (true) {
        display_menu();
        cin >> choice;

        switch (choice) {
        case 1: {
            int request_id, priority;
            string username;
            cout << "Enter request ID: "; cin >> request_id;
            cout << "Enter user name: "; cin >> username;
            cout << "Enter request priority: "; cin >> priority;
            this_bst.add_node_to_bst(request_id, username);
            this_heap.insertHeap(request_id, priority);
            cout << "Request successfully inserted!\n";
            break;
        }
        case 2: {
            int request_id;
            cout << "Enter request ID to delete: "; cin >> request_id;
            this_bst.remove_node_by_id(request_id);
            this_heap.deleteFromHeap(request_id);
            break;
        }
        case 3: {
            int request_id;
            cout << "Enter request ID to search: "; cin >> request_id;
            BSTNode* result = this_bst.find_by_id(request_id);
            if (result != nullptr) {
                cout << "Request found - ID: " << result->request_id << ", Name: " << result->username << endl;
            }
            else {
                cout << "Request not found!\n";
            }
            break;
        }
        case 4:
            this_bst.printBST();
            break;
        case 5:
            this_heap.display_heap();
            break;
        case 6:
            this_heap.deleteMaxHeap();
            break;
        case 7:
            this_heap.processHighestPriorityRequest(this_bst);
            break;
        case 8: {
            int request_id, newPriority;
            cout << "Enter request ID to increase priority: "; cin >> request_id;
            cout << "Enter new priority: "; cin >> newPriority;
            this_heap.increasePriority(request_id, newPriority);
            break;
        }
        case 9:
            cout << "BST is " << (this_bst.isEmptyBST() ? "empty.\n" : "not empty.\n");
            break;
        case 10:
            cout << "Heap is " << (this_heap.isEmptyHeap() ? "empty.\n" : "not empty.\n");
            break;
        case 11:
            cout << "BST contains " << this_bst.sizeBST() << " nodes.\n";
            break;
        case 12:
            cout << "Heap contains " << this_heap.sizeMaxHeap() << " elements.\n";
            break;
        case 13:
            show_display(this_bst, this_heap);
            break;
        case 14:
            cout << "Exiting program...\n";
            return 0;
        default:
            cout << "Invalid option! Please try again.\n";
        }
    }
}
