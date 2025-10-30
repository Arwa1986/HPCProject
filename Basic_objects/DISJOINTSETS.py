class DisjointSet:
    def __init__(self):
        self.parent = {}  # Dictionary to store the parent of each element
        self.s1 = -1
        self.s2= -1
        self.merging_score = 0
        self.biased_by = 0
        self.biased_score = 0

    # disjointset1 == disjointset2
    # if both ave the same representative
    # and the sma e values for each set
    # values could be stored in different order within the set
    # example:
    # ds1={1:[1,3,4], 2:[2,5,6], 7:[7]}
    # ds2={2:[5,2,6], 1:[3,1,4], 7:[7]}
    # ds1 == ds2 is True
    def __eq__(self, other):
        result = True
        if self.parent.keys() == other.parent.keys():
            for key in self.parent.keys():
                self_set = set(self.get_set(key))
                other_set = set(other.get_set(key))
                # if self_set != other_set and len(self_set) == len(other_set):
                #     result = all(item in other_set for item in self_set)
                result= self_set == other_set
                if not result:
                    return False
        else:
            result = False
        return result

    def to_string(self):
        all_sets_str = ''
        all_sets = self.get_sets()
        for representative, elements in all_sets.items():
            all_sets_str += f"{representative}: {elements}\n"
        return all_sets_str

    def make_set(self, element):
        # Create a new set with a single element
        self.parent[element] = element

    def find(self, element):
        # Find the representative element (root) of the set
        if self.parent[element] == element:
            return element
        return self.find(self.parent[element])

    def union(self, element1, element2):
        # Merge two sets by making one the parent of the other
        root1 = self.find(element1)
        root2 = self.find(element2)
        if root1 != root2:
            self.parent[root2]=root1
            return True
        return False
    def get_set(self, node):
        #for a given node, return the set that contains this node
        root = self.find(node)
        nodes_list=[]
        for element in self.parent:
            if root == self.find(element):
                nodes_list.append(element)
        return nodes_list

    def get_sets(self):
        sets = {}  # Dictionary to store sets and their representatives
        for element in self.parent:
            root = self.find(element)
            if root not in sets:
                sets[root] = [element]
            else:
                sets[root].append(element)
        return sets

    def is_representative(self, node):
        representative = self.find(node)
        if node == representative:
            return True
        else:
            return False

    def get_percentage_of_decreasing_score(self):
        if self.merging_score == 0:
            return 0
        return abs(self.merging_score - self.biased_score) / self.merging_score * 100

    def print(self):
        all_sets = self.get_sets()
        for representative, elements in all_sets.items():
            print(f"Set with representative {representative}: {elements}")


