from utils import decision_tree 

def from_segment(tables):
    return "FROM " + " JOIN ".join(tables) + " " 

def select_segment(input_schema):
    return "SELECT " + ", ".join(input_schema) + " "

def tree_to_where(joined_schema, tree):
    if not isinstance(tree, decision_tree.Tree):
        if tree == 1:
            return ("", True)
        return ("FALSE", False)

    attributeName = joined_schema[tree.attributeColumn] 
    (lquery, lres) = tree_to_where(joined_schema, tree.left)
    (rquery, rres) = tree_to_where(joined_schema, tree.right)

    if lquery != "":
        lquery = " AND " + lquery  

    if rquery != "":
        rquery = " AND " + rquery 

    if not lres and not rres:
        return ("FALSE", False)
    
    squery = "("
    if lres:
        squery = squery + "(" + attributeName + " <= " + str(tree.threshold) 
        squery = squery + lquery + ")"


    if lres and rres:
        squery = squery  + " OR "

    if rres:
        squery = squery + "(" + attributeName + " > " + str(tree.threshold)
        squery = squery + rquery + ")"
    squery = squery + ")"

    return (squery, True)

def where_segment(joined_schema, tree):
    return "WHERE " + tree_to_where(joined_schema, tree)[0]

def tree_to_query(input_schema, tables, joined_schema, tree):   
    select = select_segment(input_schema)
    frm = from_segment(tables) 
    where = where_segment(joined_schema, tree)

    return select + frm + where

def projected_table(remove_columns, joined_table):
    cloned_table = [] 
    for row in joined_table:
        cloned_table.append(row.copy())
        for column in reversed(remove_columns):
            del cloned_table[-1][column] 

    return cloned_table


def decorate_table(example_table, remove_columns, joined_table):
    kinds = [-1] * len(joined_table)

    cloned_table = projected_table(remove_columns, joined_table)
    print("-----CLONED-------")
    print(cloned_table)

    for row in example_table:
        ls = []
        for (index, join_row) in enumerate(cloned_table):
            if join_row == row:
                ls.append(index)
        for index in ls:
            kinds[index] = 1 if len(ls) == 1 else 0

    print(kinds)
    for (row, kind) in zip(joined_table, kinds):
        row.insert(0, kind)

    return joined_table
