class Node(object):
    
    def __init__(self, name, props={}, type="regular"):
        """
        type in ["regular", "root", "leaf"]
        """
        self.__name = name
        self.legacy = dict()
        self.links = dict()
        if type(props) != type({}):
            print('[*] Node propreties should be of type Dict.')
            self.properties = dict()
        else:
            self.properties = props
        if type in ["regular", "root", "leaf"]:
            self.type = type
        attribute = ""
        mode=1
        power=1
        print("[!] Created node ", name)

    def __str__(self):
        return self.__name

    def __r(self):
        d = dict()

        for relation in self.legacy.keys():
            if relation not in d.keys():
                d[relation] = list()
        for relation in self.links.keys():
            if relation not in d.keys():
                d[relation] = list()

        for relation in self.legacy.keys():
            for elem in self.legacy[relation]:
                d[relation].append(elem)

        for relation in self.links.keys():
            for elem in self.links[relation]:
                b = True
                for e in d[relation]:
                    if e[0] != elem[0]:
                        continue
                    if  e[2] == 1:
                        b = False
                        break
                    else:
                        e[1] = elem[1]
                        e[2] = elem[2]
                        b = False
                        break
                if b:
                    d[relation].append(elem)
        return d

    def r(self):
        return self.__r()

    def rename(newname):
        self.__name = newname
        return self

    def addProp(key, value):
        return self

    def dropProp(key):
        return self

    def getProp(key):
        pass

    def checkProp(key, value):
        pass

    def extends(self, node):
        if length(self.links) > 0:
            print('[*] Node ', self.name, " can't extend another node since it already has links with other nodes.")
            return self
        self.legacy = node.links
        self.links["extends"] = [[node,1,1]]

    def check_relation(self, r1, r2):
        if r1[0] != r2[0]:
            return 0
        if r2[2] == 1:
            return -1
        return 1

    def link(self, attribute, node, mode=1, power=1):
        """Summary or Description of the Function

            Parameters:
            mode (int): 0=negative, 1=positive
            power (int): 0=none strict, 1=strict
        """
        if attribute not in self.legacy.keys():
            if attribute not in self.links.keys():
                self.links[attribute] = list()
            self.links[attribute].append([node, mode, power])

        else:
            co = 0
            c = 5
            while (co < len(self.legacy[attribute]) and c != 0):
                c = self.check_relation([node, power], self.legacy[attribute][co])
                co=co+1

            if c == -1:
                print("Cant link", self.__name, " to ", node.__name,  " using relation: '", attribute,"', a legacy strict link exist.")
                return False
            if c == 0:
                if attribute not in self.links.keys():
                    self.links[attribute] = list()
                self.links[attribute].append([node, mode, power])
            if c == 1:
                if attribute not in self.links.keys():
                    self.links[attribute] = list()
                for e in self.links[attribute]:
                    if e[0] == node:
                        e[1] = mode
                        e[2] = power
                        return True
                self.links[attribute].append([node, mode, power])
        
        return self;

    def andWith(self, node, attribute="", mode="", power=""):
        if attribute == "":
            attribute = self.attribute
        if mode=="":
            mode = self.mode
        if power=="":
            power = self.power
        
        return self.link(attribute=attribute, node=node, mode=mode, power=power)

    def mutual_link(self, attribute, node, mode=1, power=1):
        node.link(attribute=attribute, node=self,  mode=mode, power=power)
        return self.link(attribute=attribute, node= node, mode=mode, power=power)

    def showLinks(self):
        rlnk = self.__r()
        for key in rlnk.keys():
            for elem in rlnk[key]:
                n = elem[0]
                mode = elem[1]
                power = elem[2]
                print(self.__name, "\t|  ", key , "\t|  ", n, " mode: ", mode, " strict: ", power) 

    def connections(self, all = True):
        r = []
        rlnk = self.__r()
        for key in rlnk.keys():
            for elem in rlnk[key]:
                if not all and elem[1] == 0:
                    continue
                r.append(elem[0])
        return set(r)

    def relationsWith(self, node):
        r = []
        rlnk = self.__r()
        for key in rlnk.keys():
            for nd in rlnk[key]:
                if node in nd:
                    r.append(key)
        return r
    
    def check(self, attribute, node, mode=1):
        rlnk = self.__r()
        if attribute not in rlnk.keys():
            return False
        for nd in rlnk[attribute]:
            if node == nd[0] and nd[1] == mode:
                return True
        return False