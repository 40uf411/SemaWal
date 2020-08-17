class Node(object):
    value = ""
    legacy = dict()
    links = dict()
    properties = dict()

    def __init__(self, value):
        self.value = value
        self.legacy = dict()
        self.links = dict()
        self.properties = dict()

    def __str__(self):
        return self.value

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

    def extends(self, node):
        self.legacy = node.links
        self.links["extends"] = [node,1,1]

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
                print("Cant link", self.value, " to ", node.value,  " using relation: '", attribute,"', a legacy strict link exist.")
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
                
    def mutual_link(self, attribute, node, mode=1, power=1):
        self.link(attribute=attribute, node= node, mode=mode, power=power)
        node.link(attribute, self, mode, power)

    def showLinks(self):
        rlnk = self.__r()
        for key in rlnk.keys():
            for elem in rlnk[key]:
                n = elem[0]
                mode = elem[1]
                power = elem[2]
                print(self.value, "\t|  ", key , "\t|  ", n, " mode: ", mode, " strict: ", power) 

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
    
    def answer(self, question, node, mode=1):
        rlnk = self.__r()
        if question not in rlnk.keys():
            return False
        for nd in rlnk[question]:
            if node == nd[0] and nd[1] == mode:
                return True
        return False