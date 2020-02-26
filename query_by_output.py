from utils import decision_tree
from utils import query

def example():
    table = [[1, 0, 170], [-1, 0, 195], [-1, 2000, 190], [-1, 2010, 120], [-1, 1650, 200]]

    joined_schema = ["I SHOULD NOT BE VISIBLE", "birth", "height"]
    tree = decision_tree.make_tree(table)

    print(tree)
    print(query.where_segment(joined_schema, tree))


if __name__ == '__main__':
    example()

