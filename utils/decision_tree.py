from sklearn import tree

def find_threshold(table, attributeColumn):
    clf = tree.DecisionTreeClassifier()
    
    dataset = ([x[attributeColumn]] for x in table)
    target = (x[0] for x in table) 

    clf = clf.fit(list(dataset), list(target))
    
    threshold = clf.tree_.threshold[0].item()
    gini = clf.tree_.impurity[0].item()
    return threshold, gini

def divide(table, attributeColumn):
    threshold, gini = find_threshold(table, attributeColumn)
    
    left = list(x for x in table if x[attributeColumn] <= threshold)
    right = list(x for x in table if x[attributeColumn] > threshold)

    return left, right, threshold, gini

def countOfClass(table, cls):
    return sum(1.0 if x[0] == cls else 0.0 for x in table) / len(table)

def singleGini(s):
    unass = countOfClass(s, 0) 
    pos = countOfClass(s, 1) 
    neg = countOfClass(s, -1) 

    gini = 1.0 - ((unass * unass) + (pos*pos) * (neg*neg))
    assert gini >= 0.0
    return gini

def splitGini(s1, s2):
    gini12 = (len(s1) * singleGini(s1)) + (len(s2) + singleGini(s2))
    gini12 = gini12 / (len(s1) + (len(s2)))

    assert gini12 >= 0.0
    return gini12

def best_attribute(table):
    def generate_attributes(table):
        for attr in range(1, len(table[0])):
            (_, gini) = find_threshold(table, attr)
            yield gini, attr

    (_, attr) = min(generate_attributes(table), key=lambda pair: pair[0])

    return attr 

def purity_kind(table):
    assert len(table) != 0

    sameKind = list((x for x in table if x[0] == table[0][0]))
    if len(sameKind) == len(table):
        return table[0][0]

    return 0

def childToString(child, nesting):
    return child.recursiveStr(nesting) if isinstance(child, Tree) else (" " * nesting) + str(child)

class Tree:
    def __init__(self, left, right, threshold, attributeColumn):
        self.left = left
        self.right = right
        self.threshold = threshold
        self.attributeColumn = attributeColumn

    def recursiveStr(self, nesting):
        me = "attribute: " + str(self.attributeColumn) + " threshold " + str(self.threshold)

        leftStr = childToString(self.left, nesting+1) 
        rightStr = childToString(self.right, nesting+1)

        return (" " * nesting) + me + "\n" + leftStr + "\n" + rightStr 

    def __str__(self):
        return self.recursiveStr(0)

def updateFree(table, newValue):
    for row in table:
        if row[0] == 0:
            row[0] = newValue

def make_tree(table):
    kind = purity_kind(table)
    if kind != 0: 
        return kind

    case = 1
    attributeColumn = best_attribute(table)
    (left, right, threshold, _) = divide(table, attributeColumn)

    if case == 1:
        updateFree(left, 1) 
        updateFree(right, 1)



    left = make_tree(left)
    right = make_tree(right)

    return Tree(left, right, threshold, attributeColumn) 
    
