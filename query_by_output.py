from utils import decision_tree
from utils import query
import csv


def example():
    """
    This function builds a simple example and shows the process by starting from an dummy table
    """
    joined_table = [[1900, 170, 10], [0, 120, 10], [0, 120, 100], [2010, 120, 10], [1650, 200, 10]]
    remove_columns = [2]
    example_table = [[1900, 170], [0, 120]]

    annotated_table = query.decorate_table(example_table, remove_columns, joined_table)

    joined_schema = ["I SHOULD NOT BE VISIBLE", "birth", "height"]  # the decorator column should never be in the output
    tree = decision_tree.make_tree(annotated_table)

    print(tree)
    print(query.where_segment(joined_schema, tree))


def load(file_name):
    """
    Loads a csv file and separates the attribute names from the actual rows
    :param file_name:
    :return:
    """
    with open(file_name, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    schema = [x.strip() for x in data[0]]
    table = [[int(el) for el in row] for row in data[1:]]

    return schema, table


def process(db_file, example_file, table_names):
    print()
    print("----------Loading: " + db_file + "," + example_file + " tables: " + str(table_names) + "----------")
    (db_schema, db_table) = load(db_file)
    (example_schema, example_table) = load(example_file)

    print("------DB-------")
    print(db_schema)
    print(db_table)

    print("------EXAMPLE------")
    print(example_table)
    print(example_schema)

    # finds which columns are to be projected away
    missing = [index for (index, x) in enumerate(db_schema) if x not in example_schema]
    annotated_table, ok = query.decorate_table(example_table, missing, db_table)

    if not ok:
        print("No query can be found to match a row in the example: ")
        print(str(annotated_table))
        return

    print("------DECORATED TABLE------")
    # print(missing)
    print(annotated_table)

    db_schema.insert(0, "I SHOULD NOT BE VISIBLE")

    tree = decision_tree.make_tree(annotated_table)

    print("-------TREE-------")
    print(tree)
    print(query.tree_to_query(example_schema, table_names, db_schema, tree))


if __name__ == '__main__':
    table_names = ["master", "batting"]
    process("db.csv", "example.csv", table_names)
    print(
        "Example 1 is the example of the paper, as you can see the output is very similar, although not equal, "
        "as we consider pID to be numerical")

    table_names = ["people"]
    process("db2.csv", "example2.csv", table_names)
    print(
        "Example 2 shows that the algorithm is able to find opposite conditions depending on the specific subtree. "
        "See where weight is first selected >75 and then <=75 in the right subtree")

    table_names = ["people"]
    process("db3.csv", "example3.csv", table_names)
    print(
        "Example 3 shows that the algorithm is able to find the best attribute that can select the desired queries, "
        "reducing considerably the query size")

    table_names = ["people"]
    process("db4.csv", "example4.csv", table_names)
    print(
        "Example 4 shows that if a query doesn't exist (impossible rows), it is not possible to find a query")
