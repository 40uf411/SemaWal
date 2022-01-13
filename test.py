from semawal.models import Node

nodeA = Node(
    name="A",
    description="A node",
    type="root",
    attributes = {
        "key": "value"
    },
    parent = None,
    num_workers = 4
) 
print(nodeA.get_name())
# print(nodeA)