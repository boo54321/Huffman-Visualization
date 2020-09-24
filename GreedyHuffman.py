import sys
import re
import networkx as nx
import math
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
from matplotlib import pyplot as plt
import pygraphviz
import random


class Node(object):
    def __init__(self, Character=None, Frequency=0.0, LeftChild=None, RightChild=None):
        self.Character = Character
        self.Frequency = Frequency
        self.lChild = LeftChild
        self.rChild = RightChild

    # Very important it will return the frequency when the class is called
    def __repr__(self):
        return "{}: {}".format(self.Character, self.Frequency)


class MinHeapForHuffman:

    def __init__(self, Size=sys.maxsize):
        self.HeapSize = Size
        self.Heap = []

    @staticmethod
    def Parent(Index):
        return (Index - 1) // 2

    @staticmethod
    def LeftChild(Index):
        return 2 * Index + 1

    @staticmethod
    def RightChild(Index):
        return 2 * Index + 2

    def HeapifyDown(self, Parent):
        smallest, lChild, rChild = Parent, self.LeftChild(Parent), self.RightChild(Parent)
        if lChild < len(self.Heap) and self.Heap[lChild].Frequency <= self.Heap[smallest].Frequency:
            smallest = lChild
        if rChild < len(self.Heap) and self.Heap[rChild].Frequency <= self.Heap[smallest].Frequency:
            smallest = rChild
        if smallest is not Parent:
            self.Heap[smallest], self.Heap[Parent] = self.Heap[Parent], self.Heap[smallest]
            self.HeapifyDown(smallest)

    def HeapifyUp(self, Index):
        while Index is not 0 and self.Heap[Index].Frequency <= self.Heap[self.Parent(Index)].Frequency:
            self.Heap[Index], self.Heap[self.Parent(Index)] = self.Heap[self.Parent(Index)], self.Heap[Index]
            Index = self.Parent(Index)

    def ExtractMin(self):
        if len(self.Heap) is 1:
            return self.Heap.pop(0)
        else:
            Temp, self.Heap[0] = self.Heap[0], self.Heap[len(self.Heap) - 1]
            self.Heap.pop()
            self.HeapifyDown(0)
            return Temp

    def DeleteNode(self, Index):
        self.Heap[Index].Frequency = - sys.maxsize - 1
        # This is as follows
        # The largest negative integer is -maxint-1 —
        # the asymmetry results from the use of 2’s complement binary arithmetic
        self.HeapifyUp(Index)
        self.ExtractMin()

    def ChangeKey(self, Index, Value_to_change_with):
        self.Heap[Index].Frequency = Value_to_change_with
        self.HeapifyDown(Index)

    # iterative approach of this gives top down construction of heap
    def AddKey(self, Value):
        if len(self.Heap) != self.HeapSize:
            self.Heap.append(Value)
            self.HeapifyUp(len(self.Heap) - 1)

    def Bottom_Up_Constructor(self, List):
        self.Heap = List[:]
        i = self.Parent(len(self.Heap) - 1)
        while i >= 0:
            self.HeapifyDown(i)
            i -= 1


def TextReader(Text: str):
    Dict = {}
    while len(Text) != 0:
        i = Text[0]
        Dict[i] = Text.count(i)
        # Text = re.sub("[{}]".format(i), "", Text)
        Text = Text.replace(i, "")
        # print(Text, Text.count(i), len(Text))
    return Dict


def HuffManTree(Text: str):
    Dict = TextReader(Text)
    Heap = MinHeapForHuffman()
    for i in Dict.keys():
        Heap.AddKey(Node(i, ((Dict[i] / sum(Dict.values())) * 100)))
    if __name__ == "__main__":
        DrawHeap(Heap, "Heap Insertions")
    while len(Heap.Heap) is not 1:
        lChild, rChild = Heap.ExtractMin(), Heap.ExtractMin()
        Heap.AddKey(Node(Frequency=lChild.Frequency + rChild.Frequency, LeftChild=lChild, RightChild=rChild))
        if __name__ == "__main__":
            for N in Heap.Heap:
                if N.Character is None:
                    DrawHuffman(N, len(Heap.Heap))
    if Heap.Heap[0].Frequency == 100:
        print("HuffManTree Created Successfully")
    else:
        print("Problem while creating Huffman")
    List = []
    for i in range(len(Dict)):
        List.append(0)
    EncodedText = {}
    printHuffman(Heap.Heap[0], List, 0, EncodedText)
    print("Character Codes: {}".format(EncodedText))
    Buffer = ""
    # for k in sorted(EncodedText.keys()):
    #     Text = Text.replace(str(k), str(EncodedText[k]))
    #     print(Text)
    for i in Text:
        Buffer += EncodedText[i]
    if __name__ == "__main__":
        print("Character with Frequencies : {}".format(Dict))
        print("Encoded Data: {}".format(Buffer))
    return Buffer, EncodedText


def ConstructHeapTree(Heap, Index, Root, G):
    if Heap.LeftChild(Index) < len(Heap.Heap):
        G.add_node(Heap.Heap[Heap.LeftChild(Index)])
        G.add_edge(Root, Heap.Heap[Heap.LeftChild(Index)])
        ConstructHeapTree(Heap, Heap.LeftChild(Index), Heap.Heap[Heap.LeftChild(Index)], G)
    if Heap.RightChild(Index) < len(Heap.Heap):
        G.add_node(Heap.Heap[Heap.RightChild(Index)])
        G.add_edge(Root, Heap.Heap[Heap.RightChild(Index)])
        ConstructHeapTree(Heap, Heap.RightChild(Index), Heap.Heap[Heap.RightChild(Index)], G)
    # return G




def ConstructTree(G, Root, Label):
    if Root.lChild:
        G.add_node(Root.lChild)
        G.add_edge(Root, Root.lChild)
        Label[(Root, Root.lChild)] = 1
        ConstructTree(G, Root.lChild, Label)
    if Root.rChild:
        G.add_node(Root.rChild)
        G.add_edge(Root, Root.rChild)
        Label[(Root, Root.rChild)] = 0
        ConstructTree(G, Root.rChild, Label)


def DrawHeap(Heap, Name):
    # Root = ConstructTree(Heap, 0, N(Heap.Heap[0].Frequency))
    G = nx.DiGraph()
    G.add_node(Heap.Heap[0])
    ConstructHeapTree(Heap, 0, Heap.Heap[0], G)
    global i
    write_dot(G, "Plot/Heap.dot")
    # same layout using matplotlib with no labels
    pos = hierarchy_pos(G, Heap.Heap[0])
    plt.figure(figsize=(38.40, 21.60))
    plt.title(Name, color="red", size=72)
    # nx.draw_networkx_nodes(G, pos, node_size=2500)
    nx.draw(G, pos, with_labels=True, arrows=True, node_shape="o", node_size=2500)
    plt.draw()
    plt.savefig("Outputs/{}".format('Heap.png'))
    i = str(int(i) + 1)
    # print(Root)
    # [print() for i in range(20)]


def DrawHuffman(Root, Name):
    G = nx.DiGraph()
    G.add_node(Root)
    Label = {}
    ConstructTree(G, Root, Label)
    global i
    write_dot(G, "Plot/{}".format(i + ' Plot.dot'))
    # same layout using matplotlib with no labels
    pos = hierarchy_pos(G, Root)
    plt.figure(figsize=(38.40, 21.60))
    plt.title(Name, color="red", size=72)
    nx.draw(G, pos, with_labels=True, arrows=True, node_shape="o", node_size=2500, linewidth=20)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=Label, font_color="blue", font_size=72)
    plt.draw()
    plt.savefig("Outputs/{}".format(i + ' Iter.png'))
    i = str(int(i) + 1)


def printHuffman(Root: Node, List: list, Top, Dict):
    if Root.lChild:
        List[Top] = 1
        printHuffman(Root.lChild, List, Top + 1, Dict)
    if Root.rChild:
        List[Top] = 0
        # print(List)
        printHuffman(Root.rChild, List, Top + 1, Dict)
    if Root.rChild == Root.lChild is None:
        Dict["{}".format(Root.Character)] = re.sub("[, []", "", str(List[:Top])).strip("]")
        # print("{}: {}".format(Root.Character, List[:Top]))


def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=2., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


if __name__ == "__main__":
    i = "0"
    EncodedText = HuffManTree("hi i am the guy")
