import uuid
from semawal.models.cluster import Cluster
# Generate a network that contains clusters
class Network:
    def __init__(self, name, description) -> None:
        """Generate a network.
        Args:
            name ([str]): Name of the network.
            description ([str]): Description of the network.
        """
        self.__id = str(uuid.uuid4())
        self.__name = name
        self.__description = description
        self.__clusters = {}
    def __str__(self) -> str:
        """String representation of the network.
        Returns: [str]
        """
        return "%:%" % (self.__id, self.__name)
    def __repr__(self) -> str:
        """String representation of the network.
        Returns: [str]
        """
        return self.__str__()
    def __setattr__(self, name, value) -> bool:
        """Set the network attribute.
        Args:
            name ([str]): Attribute name.
            value ([any]): Attribute value.
        Returns: [bool]
        """
        if not name.startswith('_'):
            return False
        # set the attribute
        self.__dict__[name] = value
    def __delattr__(self, name) -> bool:
        """Drop the network attribute.
        Args:
            name ([str]): Attribute key.
        Returns: [bool]
        """
        if not name.startswith('_'):
            return False
        # drop the attribute
        del self.__dict__[name]
    def __iter__(self)-> any:
        """Iterate over the clusters.
        Returns: [Iterator]
        """
        return iter(self.__clusters)
    def __getitem__(self, key)-> Cluster|None:
        """Get the cluster by key.
        Args:
            key ([str]): Cluster key.
        Returns: [Cluster]
        """
        return self.__clusters[key]
    def __len__(self) -> int:
        """Get the number of clusters.
        Returns: [int]
        """
        return len(self.__clusters)

    # Getters
    def get_id(self) -> str:
        """Get the network id.
        Returns: [str]
        """
        return self.__id
    def get_name(self) -> str:
        """Get the network name.
        Returns: [str]
        """
        return self.__name
    def get_description(self) -> str:
        """Get the network description.
        Returns: [str]
        """
        return self.__description
    def get_clusters(self) -> dict:
        """Get the clusters.
        Returns: [dict]
        """
        return self.__clusters
    def get_cluster(self, key: str) -> Cluster|None:
        """Get the cluster by key.
        Args:
            key ([str]): Cluster key.
        Returns: [Cluster]
        """
        return self.__clusters[key] if key in self.__clusters else None

    # Setters
    def set_name(self, name: str) -> bool:
        """Set the network name.
        Args:
            name ([str]): Name of the network.
        Returns: [bool]
        """
        self.__name = name
        return True
    def set_description(self, description: str) -> bool:
        """Set the network description.
        Args:
            description ([str]): Description of the network.
        Returns: [bool]
        """
        self.__description = description
        return True

    # Adders
    def add_cluster(self, cluster: Cluster) -> bool:
        """Add a cluster to the network.
        Args:
            cluster ([Cluster]): Cluster to add.
        Returns: [bool]
        """
        if cluster.get_id() in self.__clusters:
            return False
        self.__clusters[cluster.get_id()] = cluster
        return True

    # Removers
    def remove_cluster(self, key: str) -> bool:
        """Remove a cluster from the network.
        Args:
            key ([str]): Cluster key.
        Returns: [bool]
        """
        if key not in self.__clusters:
            return False
        del self.__clusters[key]
        return True

    # Resetters
    def reset_clusters(self, full_reset = False) -> bool:
        """Reset the clusters.
        Returns: [bool]
        """
        if full_reset:
            self.__name = ""
            self.__description = ""
        self.__clusters = {}
        return True

