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
