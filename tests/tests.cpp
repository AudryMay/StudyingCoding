#include <iostream>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <vector>
#include <algorithm>
#include <string>
#include <stack>
#include <utility>
#include <sstream>
using namespace std;

struct ListNode {
    int val;
    ListNode *next;
    ListNode() : val(0), next(nullptr) {}
    ListNode(int x) : val(x), next(nullptr) {}
    ListNode(int x, ListNode *next) : val(x), next(next) {}
};


 void reorderList(ListNode* head) {
        
        ListNode* tmp = head;
        while(tmp&&tmp->next){
          ListNode* findSecondToTheLast = tmp;
          while(findSecondToTheLast->next  && findSecondToTheLast->next->next) findSecondToTheLast = findSecondToTheLast->next;
          if (findSecondToTheLast == tmp->next) break;
          findSecondToTheLast->next->next = tmp->next;
          tmp->next= findSecondToTheLast->next;
          findSecondToTheLast->next = nullptr;
          tmp = tmp->next->next;

        }

       // return head;
}

int main() {
    // Creating nodes
    ListNode *node1 = new ListNode(1);
    ListNode *node2 = new ListNode(2);
    ListNode *node3 = new ListNode(3);
    ListNode *node4 = new ListNode(4);
    ListNode *node5 = new ListNode(5);

    // Linking nodes to create the linked list
    node1->next = node2;
    node2->next = node3;
    node3->next = node4;
   // node4->next = node5;

    // Print the linked list values
    reorderList(node1);
    ListNode *current = node1;
    while (current != nullptr) {
        std::cout << current->val << " ";
        current = current->next;
    }

    // Clean up: delete allocated nodes
    delete node1;
    delete node2;
    delete node3;
    delete node4;
    delete node5;

    return 0;
}