class MaxHeap:
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left_child(self, i):
        return 2 * i + 1

    def right_child(self, i):
        return 2 * i + 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def insert(self, item):
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def extract_max(self):
        if self.is_empty():
            return None
        self.swap(0, len(self.heap) - 1)
        max_item = self.heap.pop()
        self._sift_down(0)
        return max_item

    def is_empty(self):
        return len(self.heap) == 0

    def _sift_up(self, i):
        while i > 0 and self.heap[i] > self.heap[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def _sift_down(self, i):
        n = len(self.heap)
        max_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        if left < n and self.heap[left] > self.heap[max_index]:
            max_index = left
        if right < n and self.heap[right] > self.heap[max_index]:
            max_index = right

        if i != max_index:
            self.swap(i, max_index)
            self._sift_down(max_index)
