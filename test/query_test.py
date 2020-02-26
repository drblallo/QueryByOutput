from utils import query
from utils import decision_tree

def test_from_segment():
    assert query.from_segment(["city", "region"]) == "FROM city JOIN region "

def test_select_segment():
    assert query.select_segment(["cap", "size"]) == "SELECT cap, size "

def test_where_segment():
    table = [[1, 1900, 170], [1, 0, 120], [-1, 2000, 190], [-1, 2010, 120], [-1, 1650, 200]]

    clf = decision_tree.make_tree(table)

    joined_schema = ["I SHOULD NOT BE VISIBLE", "birth", "height"]

    assert query.where_segment(joined_schema, clf) == "WHERE ((birth <= 1950.0 AND ((birth <= 825.0) OR (birth > 825.0 AND ((birth > 1775.0))))))"
    
