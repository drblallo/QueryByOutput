from utils import decision_tree
from utils import query

def example():
    joined_table = [[1900, 170, 10], [0, 120, 10], [0, 120, 100], [2010, 120, 10], [1650, 200, 10]]
    remove_columns = [2]
    example_table = [[1900, 170], [0, 120]]

    annotated_table = query.decorate_table(example_table, remove_columns, joined_table)

    joined_schema = ["I SHOULD NOT BE VISIBLE", "birth", "height"]
    tree = decision_tree.make_tree(annotated_table)

    print(tree)
    print(query.where_segment(joined_schema, tree))


if __name__ == '__main__':
    example()
