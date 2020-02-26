from utils import decision_tree

def example():
    table = [[1, 1900, 170], [1, 0, 120], [-1, 2000, 190], [-1, 2010, 120], [-1, 1650, 200]]

    return decision_tree.make_tree(table)


if __name__ == '__main__':
    print(example())

