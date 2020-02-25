from sklearn import tree

def find_threshold(table, attributeColumn):
    clf = tree.DecisionTreeClassifier()
    
    dataset = ([x[attributeColumn]] for x in table)
    target = (x[0] for x in table) 

    clf = clf.fit(list(dataset), list(target))
    
    threshold = clf.tree_.threshold[0]
    return threshold

def divide(table, attributeColumn):
    threshold = find_threshold(table, attributeColumn)
    
    left = list(filter(lambda row: row[attributeColumn] <= threshold, table))
    right = list(filter(lambda row: row[attributeColumn] > threshold, table))

    return left, right, threshold

def purity_kind(table):
    if len(table) == 0:
        assert False

    first = table[0][0]

    sameKind = list((x for x in table if x[0] == first))
    if len(sameKind) == len(table):
        return first

    return 0

class Tree:
    def __init__(self, left, right, threshold, attributeColumn):
        self.left = left
        self.right = right
        self.threshold = threshold
        self.attributeColumn = attributeColumn

def make_tree(table, attributeColumn):
    kind = purity_kind(table)
    if kind != 0 or attributeColumn >= len(table):
        return kind

    (left, right, threshold) = divide(table, attributeColumn)

    left = make_tree(left, attributeColumn + 1)
    right = make_tree(right, attributeColumn + 1)

    return Tree(left, right, threshold, attributeColumn) 
    
