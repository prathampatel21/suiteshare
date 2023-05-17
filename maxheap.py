class MaxHeap:
    def __init__(self):
        # Initialize an empty heap
        self.heap = []  

    def parent(self, i):
        # Calculate the parent index of node i
        return (i - 1) // 2  

    # Calculate the index of the left child and of the right child of node i
    def left_child(self, i):
        return 2 * i + 1  

    def right_child(self, i):
        return 2 * i + 2  

    def swap(self, i, j):
        # Swap the elements at indices i and j
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]  

    def insert(self, item):
        self.heap.append(item) 
         # Restore the heap property by moving the item up
        self.heapify_up(len(self.heap) - 1)  

    def find_max(self):
        if self.is_empty():
            return None 
        # Swap the maximum item with the last item in the heap
        self.swap(0, len(self.heap) - 1)
          
        max_item = self.heap.pop()

        # Restore the heap property by moving the new root down
        self.heapify_down(0)  
        return max_item  

    def is_empty(self):
        return len(self.heap) == 0 

    def heapify_up(self, i):
        while i > 0 and self.heap[i] > self.heap[self.parent(i)]:
            # Swap the item with its parent if it disrupts the heap property
            self.swap(i, self.parent(i)) 
            # Move up to the parent index
            i = self.parent(i)  

    def heapify_down(self, i):
        n = len(self.heap)
        max_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        # Update the max index if the left child or right child is larger than the current maximum
        if left < n and self.heap[left] > self.heap[max_index]:
            max_index = left  
        if right < n and self.heap[right] > self.heap[max_index]:
            max_index = right  

        if i != max_index:
            # Swap the item with its largest child if it disrupts the heap property
            self.swap(i, max_index)
            # Recursively move down to the new position  
            self.heapify_down(max_index)  
