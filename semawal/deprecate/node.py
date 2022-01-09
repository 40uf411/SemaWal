class Node(object):
    
    def __init__(self, name, props={}, type="regular"):
        """
        type in ["regular", "root", "leaf"]
        """
        
        self.__name = name
        self.linksVersion = 0
        self.parentLinksVersion = -1

        self.links = dict()
        self.staticLinks = dict()
        self.staticLinksVersion = 0
        self.attribute = ""
        self.mode=1
        self.power=1
        self._parent = None
        if type in ["regular", "root", "leaf"]:
            self._type = type

        if not isinstance(props, dict):
            print('[*] Node propreties should be of type Dict.')
            self.properties = dict()
        else:
            self.properties = props

        print("[!] Created node:", name)

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name
        
    def __getattr__(self, name):
        def function():
            print("You tried to call a method named: %s" % name)
        return function
    
    def reset(self):
        self.linksVersion = 0
        self.parentLinksVersion = -1

        self.links = dict()
        self.staticLinks = dict()
        self.staticLinksVersion = 0
        self.attribute = ""
        self.mode=1
        self.power=1
        self._parent = None

        print("[!] Node '", self, "' has been reseted.")
    
    def type(self):
        return str(self._type)

    def name(self): 
        return self.__name

    def rename(self, newname):
        self.__name = newname
        return self

    def getProperties(self):
        return dict(self.properties)
    
    def addProp(self, key, value):
        self.properties[key] = value
        return self

    def dropProp(self, key):
        self.properties[key] = None
        return self

    def getProp(self, key): 
        return self.properties[key]

    def validateProps(self, pattern):
        for pKey in pattern.keys():
            if pKey not in self.properties: 
                return False
            else:
                v = self.properties[pKey]
                for condition in pattern[pKey]:
                    if condition[0] == "==":
                        if v != condition[1] : return False
                    elif condition[0] == "!=":
                        if v == condition[1] : return False
                    elif condition[0] == ">=":
                        if v < condition[1] : return False
                    elif condition[0] == "<=":
                        if v > condition[1] : return False
                    elif condition[0] == ">":
                        if v <= condition[1] : return False
                    elif condition[0] == "<":
                        if v >= condition[1] : return False
        return True

    def parent(self):
        return self._parent

    def root(self, depth=0):
        d = 1
        p = self.parent()
        if p == None:
            return None
        else:
            po = self
            while p != None and (depth<=0 or d<depth):
                po = p
                p = po.parent()
                d=d+1
            return po
    
    def extends(self, node, generate = True):
        if node.type() == "leaf":
            print("[*] Node", node, " is of type 'leaf' and cannot make links.")
            return self

        if isinstance(self.parent(), Node):
            print('[*] Node ', self.name, " can't extend another node since it already has links with other nodes.")
            return self
        self._parent = node
        p = node.getProperties()
        for prop in self.properties.keys():
            p[prop] = self.properties[prop]
        self.properties = p
        
        if generate:
            self.generateStaticLinks()
        self.parentLinksVersion = node.linksVersion
        self.linksVersion = self.linksVersion + 1
        return self

    def getLinks(self, generate = True):
        if generate:
            self.generateStaticLinks()
        return dict(self.staticLinks)
    
    def commit(self):
        return self.generateStaticLinks()

    def generateStaticLinks(self):
        # if no change has been made, leave.
        if self.staticLinksVersion == self.linksVersion and (not isinstance(self.parent(), Node) or self.parent().linksVersion == self.parentLinksVersion):
            return self
        # adding parent links
        # tmp links
        tmp = dict() 
        # if parent's links has changed
        if isinstance(self.parent(), Node):
            # parent links
            self.staticLinks = tmp = self.parent().getLinks().copy()
            self.parentLinksVersion = self.parent().linksVersion

        lLinks = self.links

        for attribute in lLinks: 
            # if attribute not on the tmp list, add all items from local list [attribute]           
            if attribute not in tmp.keys():
                tmp[attribute] = list()
                for elem in lLinks[attribute]:
                    tmp[attribute].append(elem)
            else:
                for node in lLinks[attribute]:
                    for elem in tmp[attribute]:
                        if elem[0] == node[0]:
                            if elem[2] >= node[2]:
                                self.dropLink(attribute=attribute, node=node[0], generate=False)
                                print("[*] A change to the parent of node", self, " caused the drop of a local link to ", node[0] ,"(mostly due to the parent link having higher power).")
                            else:
                                tmp[attribute].remove(elem)
                                tmp[attribute].append(node)
        self.staticLinks = tmp
        # adding compatible local links
        self.staticLinksVersion = self.linksVersion = max(self.staticLinksVersion, self.linksVersion) + 1
        return self

    def checkCompatibility(self, attribute, node, power, generate = True, checkOnly = "all"):
        """
        checkOnly = ["all", "local", "parent"]
        """
        # static
        #it force generates the parents links
        sLinks = self.getLinks()
        p = self.parent()
        sAttributes = sLinks.keys()
        # local
        if not generate:
            lLinks = self.links
            lAttributes = lLinks.keys()
        if attribute not in sAttributes and (generate or attribute not in lAttributes):
            return 0
        else:
            # if generate (the static links are updated) check only the static links, else check the unsaved links as well
            notInSLinks = False
            for sAttribute in sAttributes:
                for link in sLinks[sAttribute]:
                    if link[0] == node:
                        if link[2] >= power:
                            return -1
                        else:
                            notInSLinks = True 
                            break
            if not generate:
                for lAttribute in lAttributes:
                    for link in lLinks[lAttribute]:
                        if link[0] == node: 
                            return 2
            return 0 if notInSLinks else 1
        
    def link(self, attribute, node, mode=1, power=1, generate=True):
        """Summary or Description of the Function

            Parameters:
            mode (int): 0=negative, 1=positive
            power (int): 0=none strict, 1=strict
        """
        if self.type() == "leaf":
            print("[*] Node", self, " is of type 'leaf' and cannot make links.")
            return self
        elif node.type == "root":
            print("[*] Node", ndoe, " is of type 'root' and cannot be linked with.")
            return self

        # validating params
        if mode not in [0,1]:
            mode = 1
        if not isinstance(power, int) or power > 10 or power < 0:
            power = 1
        
        # save this params
        self.attribute = attribute
        self.mode = mode
        self.power = power
        #check if the link can be added
        compatibility = self.checkCompatibility(attribute=attribute, node=node, power=power, generate=generate)
        # link not compatable
        if compatibility == -1: 
            print("[*] Could not creat link between ", self, " and ", node, " on attribute: ", attribute)
        # link does not exist, or exist on static with lower power
        elif compatibility == 0 or compatibility == 1: 
            if attribute not in self.links.keys():
                self.links[attribute] = list()
            self.links[attribute].append([node, mode, power])
            self.linksVersion = self.linksVersion + 1
            if generate:
                self.generateStaticLinks()
            #
            if compatibility == 0:
                print("[!] A link from ", self, " to ", node, " has been made on attribute:", attribute)
            else:
                print("[!] A link from ", self, " to ", node, " has been updated on attribute:", attribute)
        # link exist in local with lower power
        elif compatibility == 2:
            for e in self.links[attribute]:
                if e[0] == node:
                    self.links[attribute].remove(e)
                    self.links[attribute].append([node, mode, power])
            print("[!] A link from ", self, " to ", node, " has been updated on attribute:", attribute)
            self.linksVersion = self.linksVersion + 1
            if generate:
                self.generateStaticLinks()
        return self;
        
        # if attribute not in self.legacy.keys():
        #     if attribute not in self.links.keys():
        #         self.links[attribute] = list()
        #     self.links[attribute].append([node, mode, power])

        # else:
        #     co = 0
        #     c = 5
        #     while (co < len(self.legacy[attribute]) and c != 0):
        #         c = self.check_relation([node, power], self.legacy[attribute][co])
        #         co=co+1

        #     if c == -1:
        #         print("Cant link", self.__name, " to ", node.__name,  " using relation: '", attribute,"', a legacy strict link exist.")
        #         return False
        #     if c == 0:
        #         if attribute not in self.links.keys():
        #             self.links[attribute] = list()
        #         self.links[attribute].append([node, mode, power])
        #     if c == 1:
        #         if attribute not in self.links.keys():
        #             self.links[attribute] = list()
        #         for e in self.links[attribute]:
        #             if e[0] == node:
        #                 e[1] = mode
        #                 e[2] = power
        #                 return True
        #         self.links[attribute].append([node, mode, power])
        
    def andWith(self, node, attribute="", mode="", power="", generate=False):
        if attribute == "":
            attribute = self.attribute
        if mode=="" or mode not in [0,1]:
            mode = self.mode
        if power=="" or not isinstance(power, int) or power > 10 or power < 0:
            power = self.power
        
        return self.link(attribute=attribute, node=node, mode=mode, power=power, generate=generate)

    def mutualLink(self, attribute, node, mode=1, power=1, generate=True):
        node.link(attribute=attribute, node=self,  mode=mode, power=power, generate=generate)
        return self.link(attribute=attribute, node= node, mode=mode, power=power, generate=generate)

    def dropLink(self, attribute, node, generate=True):
        tmp = dict()
        lList = self.links
        lattributes = lList.keys()
        for lattribute in lattributes:
            tmp[lattribute] = list()
        for lattribute in lattributes:
            if lattribute != attribute:
                tmp[lattribute] = lList[lattribute]
        for lNode in lList[attribute]:
            if lNode[0] != node:
                tmp[attribute].append(lList[lattribute])
        self.links = tmp
        self.linksVersion = self.linksVersion + 1
        if generate:
            self.generateStaticLinks()

    def showLinks(self, generate=True):
        if isinstance(self.parent(), Node):
            print(self.__name, "\t|  extends\t|  ", self.parent()) 
        rlnk = self.getLinks(generate=generate)
        for key in rlnk.keys():
            for elem in rlnk[key]:
                n = elem[0]
                mode = elem[1]
                power = elem[2]
                print(self.__name, "\t|  relation: ", key , "\t|  ", n, " \t| mode: ", mode, " power: ", power) 

    def getLinksAttributes(self):
        return list(self.getLinks().keys())

    def getConnections(self, attributes=[], props = [], mode = -1, minPower=0, maxPower=10):
        tmp = list()
        lLinks = self.getLinks()
        attributes = attributes if attributes != [] else lLinks.keys()
        for att in lLinks.keys():
            if att not in attributes:
                continue
            for elem in lLinks[att]:
                if not elem[0].validateProps(props):
                    continue
                if mode in [1, 0] and elem[1] != mode:
                    continue
                if elem[2] > maxPower or elem[2] < minPower:
                    continue
                tmp.append(elem[0])
        return list(set(tmp))
    
    def getRelationsWith(self, node):
        lLinks = self.getLinks()
        attributes = lLinks.keys()
        tmp = list()
        for attribute in attributes:
            for elem in lLinks[attribute]:
                if elem[0] == node:
                    tmp.append(attribute)
                    break
        return tmp

    def checkPattern(self, pattern, ignoreList=[]):
        ignoreList.append(self)
        if(len(pattern) == 0):
            return []
        else:
            paths = list()
            nodes = self.getConnections(attributes= pattern[0]["attributes"], 
                                        props=      pattern[0]["props"], 
                                        mode=       pattern[0]["mode"], 
                                        minPower=   pattern[0]["minPower"],
                                        maxPower=   pattern[0]["maxPower"])
            if pattern[0]["num"] > 0:
                if pattern[0]["num"] == 1:
                    pattern.pop(0)
                if(len(pattern) == 0):  
                    return [[self,node] for node in nodes and node not in ignoreList]
                else:
                    pattern[0]["num"] = pattern[0]["num"]-1
                    for node in nodes:
                        if node not in ignoreList:
                            paths.append(node.checkPattern(pattern=pattern, ignoreList=ignoreList))
            else: # pattern[0] < 0
                # check for "stat 0" of the pattern
                for node in nodes:
                    if node not in ignoreList:
                        paths.append(node.checkPattern(pattern=pattern, ignoreList=ignoreList))
                
                if(len(pattern) > 1): 
                    # check for the next stat
                    nodes_1 = self.getConnections(attributes= pattern[1]["attributes"], 
                                                  props=      pattern[1]["props"], 
                                                  mode=       pattern[1]["mode"], 
                                                  minPower=   pattern[1]["minPower"],
                                                  maxPower=   pattern[1]["maxPower"])
                    for node in nodes:
                        if node not in ignoreList:
                            paths.append(node.checkPattern(pattern=pattern[2:], ignoreList=ignoreList))
            if(len(paths) > 0):
                return [[self] + path for path in paths]
            else:
                return [self]
                    