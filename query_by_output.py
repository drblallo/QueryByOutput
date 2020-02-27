from utils import decision_tree
from utils import query
import csv

def example():
    joined_table = [[1900, 170, 10], [0, 120, 10], [0, 120, 100], [2010, 120, 10], [1650, 200, 10]]
    remove_columns = [2]
    example_table = [[1900, 170], [0, 120]]

    annotated_table = query.decorate_table(example_table, remove_columns, joined_table)

    joined_schema = ["I SHOULD NOT BE VISIBLE", "birth", "height"]
    tree = decision_tree.make_tree(annotated_table)

    print(tree)
    print(query.where_segment(joined_schema, tree))

def load(file_name):
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    schema = [x.strip() for x in data[0]]
    table = [[int(el) for el in row] for row in data[1:]]

    return schema, table


if __name__ == '__main__':
    (db_schema, db_table) = load("db.csv")
    (example_schema, example_table) = load("example.csv")
    table_names = ["master", "batting"]

    print("------DB-------")
    print(db_schema)
    print(db_table)

    print("------EXAMPLE------")
    print(example_table)
    print(example_schema)

    missing = [index for (index, x) in enumerate(db_schema) if x not in example_schema]
    annotated_table = query.decorate_table(example_table, missing, db_table)

    print("------EXTRA------")
    print(missing)
    print(annotated_table)

    db_schema.insert(0, "I SHOULD NOT BE VISIBLE")

    tree = decision_tree.make_tree(annotated_table)
    print(tree)
    print(query.tree_to_query(example_schema, table_names, db_schema, tree))
