import re
import demjson
import os

INDENT = '    '


class Conf(object):
    def __init__(self, *args):
        self.blocks = list(args)
        self.servers = []
        self.upd()
        self.__name__ = 'Conf'

    def add(self, *args):
        self.blocks.extend(args)
        self.upd()
        return self.blocks

    def remove(self, *args):
        for x in args:
            self.blocks.remove(x)
        self.upd()
        return self.blocks

    def filter(self, btype='', name=''):
        flist = []
        for x in self.blocks:
            if name and isinstance(x, Key) and x.name == name:
                flist.append(x)
            elif isinstance(x, Container) and x.__class__.__name__ == btype and x.value == name:
                flist.append(x)
            elif not name and btype and x.__class__.__name__ == btype:
                flist.append(x)
        return flist

    def upd(self):
        svr = []
        for x in self.blocks:
            if isinstance(x, Server):
                svr.append(x)
        self.servers = svr

    def all(self):
        return self.blocks

    def as_list(self):
        ret = []
        for x in self.blocks:
            ret.append(x.as_list())
        return ret

    def as_dict(self):
        return {'conf': [x.as_dict() for x in self.blocks]}

    def as_block(self):
        ret = []
        for x in self.blocks:
            if isinstance(x, (Key, Comment)):
                ret.append(x.as_block())
            else:
                for y in x.as_block():
                    ret.append(y)
        return ret


class Server(object):
    def __init__(self, *args):
        self.blocks = list(args)
        self.locations = []
        self.comments = []
        self.keys = []
        self.upd()
        self.__name__ = 'Server'

    def add(self, *args):
        self.blocks.extend(args)
        self.upd()
        return self.blocks

    def remove(self, *args):
        for x in args:
            self.blocks.remove(x)
        self.upd()
        return self.blocks

    def filter(self, btype='', name=''):
        flist = []
        for x in self.blocks:
            if name and isinstance(x, Key) and x.name == name:
                flist.append(x)
            elif isinstance(x, Container) and x.__class__.__name__ == btype and x.value == name:
                flist.append(x)
            elif not name and btype and x.__class__.__name__ == btype:
                flist.append(x)
        return flist

    def upd(self):
        l, c, k = [], [], []
        for x in self.blocks:
            if isinstance(x, Location):
                l.append(x)
            elif isinstance(x, Comment):
                c.append(x)
            elif isinstance(x, Key):
                k.append(x)
        self.locations, self.comments, self.keys = l, c, k

    def all(self):
        return self.blocks

    def as_list(self):
        ret = []
        for x in self.blocks:
            ret.append(x.as_list())
        return ['server', '', ret]

    def as_dict(self):
        return {'server': [x.as_dict() for x in self.blocks]}

    def as_block(self):
        ret = []
        ret.append('server {\n')
        for x in self.blocks:
            if isinstance(x, (Key, Comment)):
                ret.append(INDENT + x.as_block())
            elif isinstance(x, Container):
                y = x.as_block()
                ret.append('\n'+INDENT+y[0])
                for z in y[1:]:
                    ret.append(INDENT+z)
        ret.append('}\n')
        return ret

class MainArgs(object):
    def __init__(self, *args):
        self.blocks = list(args)
        self.keys = []
        self.upd()
        self.__name__ = 'MainArgs'

    def add(self, *args):
     #   self.blocks.insert(i-1,args)
      #  self.blocks.extend(args)
        self.upd()
        return self.blocks

    def ll(self,*args):
        return self.blocks.index(args)

    def remove(self, *args):
        for x in args:
            self.blocks.remove(x)
        self.upd()
        return self.blocks

    def filter(self, btype='', name=''):
        flist = []
        for x in self.blocks:
            if name and isinstance(x, Key) and x.name == name:
                flist.append(x)
            elif isinstance(x, Container) and x.__class__.__name__ == btype and x.value == name:
                flist.append(x)
            elif not name and btype and x.__class__.__name__ == btype:
                flist.append(x)
        return flist

    def upd(self):
        k = []
        for x in self.blocks:
            if isinstance(x, Key):
                k.append(x)
        self.keys = k

    def all(self):
        return self.blocks

    def as_list(self):
        ret = []
        for x in self.blocks:
            ret.append(x.as_list())
        return ['MainArgs', '', ret]

    def as_dict(self):
        return {'MainArgs': [x.as_dict() for x in self.blocks]}

    def as_block(self):
        ret = []
        ret.append('\n')
        for x in self.blocks:
            if isinstance(x, (Key, Comment)):
                ret.append(INDENT + x.as_block())
        ret.append('\n')
        return ret


'''
class Events(Container):
    def __init__(self, value, *args):
        super(Events, self).__init__(value, *args)
        self.name = ''
'''

class Http(object):
    def __init__(self, *args):
        self.blocks = list(args)
        self.keys = []
        self.upd()
        self.__name__ = 'Http'

    def add(self, *args):
        self.blocks.extend(args)
        self.upd()
        return self.blocks

    def remove(self, *args):
        for x in args:
            self.blocks.remove(x)
        self.upd()
        return self.blocks

    def filter(self, btype='', name=''):
        flist = []
        for x in self.blocks:
            if name and isinstance(x, Key) and x.name == name:
                flist.append(x)
            elif isinstance(x, Container) and x.__class__.__name__ == btype and x.value == name:
                flist.append(x)
            elif not name and btype and x.__class__.__name__ == btype:
                flist.append(x)
        return flist

    def upd(self):
        k = []
        for x in self.blocks:
            if isinstance(x, Key):
                k.append(x)
        self.keys = k

    def all(self):
        return self.blocks

    def as_list(self):
        ret = []
        for x in self.blocks:
            ret.append(x.as_list())
        return ['http', '', ret]

    def as_dict(self):
        return {'http': [x.as_dict() for x in self.blocks]}

    def as_block(self):
        ret = []
        ret.append('http {\n')
        for x in self.blocks:
            if isinstance(x, (Key, Comment)):
                ret.append(INDENT + x.as_block())
        ret.append('}\n')
        return ret

class Events(object):
    def __init__(self, *args):
        self.blocks = list(args)
        self.keys = []
        self.upd()
        self.__name__ = 'Events'

    def add(self, *args):
        self.blocks.extend(args)
        self.upd()
        return self.blocks

    def remove(self, *args):
        for x in args:
            self.blocks.remove(x)
        self.upd()
        return self.blocks

    def filter(self, btype='', name=''):
        flist = []
        for x in self.blocks:
            if name and isinstance(x, Key) and x.name == name:
                flist.append(x)
            elif isinstance(x, Container) and x.__class__.__name__ == btype and x.value == name:
                flist.append(x)
            elif not name and btype and x.__class__.__name__ == btype:
                flist.append(x)
        return flist

    def upd(self):
        k = []
        for x in self.blocks:
            if isinstance(x, Key):
                k.append(x)
        self.keys = k

    def all(self):
        return self.blocks

    def as_list(self):
        ret = []
        for x in self.blocks:
            ret.append(x.as_list())
        return ['events', '', ret]

    def as_dict(self):
        return {'events': [x.as_dict() for x in self.blocks]}

    def as_block(self):
        ret = []
        ret.append('events {\n')
        for x in self.blocks:
            if isinstance(x, (Key, Comment)):
                ret.append(INDENT + x.as_block())
        ret.append('}\n')
        return ret

class Container(object):
    def __init__(self, value, *args):
        self.name = ''
        self.value = value
        self.comments = []
        self.keys = []
        self.blocks = list(args)
        self.upd()


    def add(self, *args):
        self.blocks.extend(args)
        self.upd()
        return self.blocks

    def remove(self, *args):
        for x in args:
            self.blocks.remove(x)
        self.upd()
        return self.blocks

    def upd(self):
        c, k = [], []
        for x in self.blocks:
            if isinstance(x, Comment):
                c.append(x)
            elif isinstance(x, Key):
                k.append(x)
        self.comments, self.keys = c, k

    def all(self):
        return self.blocks

    def as_list(self):
        ret = []
        for x in self.blocks:
            ret.append(x.as_list())
        return [self.name, self.value, ret]

    def as_dict(self):
        return {self.name+' '+self.value: [x.as_dict() for x in self.blocks]}

    def as_block(self):
        ret = []
        ret.append(self.name + ' ' + self.value + ' {\n')
        for x in self.blocks:
            if isinstance(x, (Key, Comment)):
                ret.append(INDENT + x.as_block())
            elif isinstance(x, Container):
                y = x.as_block()
                ret.append('\n'+INDENT+INDENT+y[0])
                for z in y[1:]:
                    ret.append(INDENT+z)
            else:
                y = x.as_block()
                ret.append(INDENT+y)
        ret.append('}\n')
        return ret


class Comment(object):
    def __init__(self, comment):
        self.comment = comment

    def as_list(self):
        return [self.comment]

    def as_dict(self):
        return {'#': self.comment}

    def as_block(self):
        return '# ' + self.comment + '\n'


class Location(Container):
    def __init__(self, value, *args):
        super(Location, self).__init__(value, *args)
        self.name = 'location'


class LimitExcept(Container):
    def __init__(self, value, *args):
        super(LimitExcept, self).__init__(value, *args)
        self.name = 'limit_except'


class Types(Container):
    def __init__(self, value, *args):
        super(Types, self).__init__(value, *args)
        self.name = 'types'


class If(Container):
    def __init__(self, value, *args):
        super(If, self).__init__(value, *args)
        self.name = 'if'


class Upstream(Container):
    def __init__(self, value, *args):
        super(Upstream, self).__init__(value, *args)
        self.name = 'upstream'


class Key(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def as_list(self):
        return [self.name, self.value]

    def as_dict(self):
        return {self.name: self.value}

    def as_block(self):
        return self.name + ' ' + " ".join(self.value) + ';\n'



def remove_reg(line):
    xline = ""
    if len(line)>0:
        b = re.findall(r"{.*?}",line)
        if b:
            for x in b :
                xline = line.replace(x,"")
            return xline
        else:
            return line
    else:
        return ""

__CLASS_LIST__ = (Conf.__name__,Http.__name__,Events.__name__,Server.__name__,MainArgs.__name__)

def loads(data, conf=True):
    f = Conf() if conf else []
    lopen = []
    for line in data.split('\n'):
        if re.match('\s*server\s*\{', line):
            s = Server()
            lopen.insert(0, s)
        if re.match('\s*location.*\{', line):
            lpath = re.match('\s*location\s*(.*\S+)\s*\{', line).group(1)
            l = Location(lpath)
            lopen.insert(0, l)
        if re.match('\s*if.*\{', line):
            ifs = re.match('\s*if\s*(.*\S+)\s*\{', line).group(1)
            ifs = If(ifs)
            lopen.insert(0, ifs)
        if re.match('\s*upstream.*\{', line):
            ups = re.match('\s*upstream\s*(.*\S+)\s*\{', line).group(1)
            u = Upstream(ups)
            lopen.insert(0, u)
        if re.match('^\#.*',line):
            lopen.insert(0,Comment(line))
        if re.match('.*;', line):
            kname, kval = re.match('.*(?:^|^\s*|{\s*)(\S+)\s(.+);', line).group(1, 2)
            k = Key(kname, [x for x in kval.split() if len(x)>0])
            lopen[0].add(k)
        #if re.match('.*}', line) and re.match('.*}', remove_reg(line)):
        if re.match('.*}', remove_reg(line)):
            closenum = len(re.findall('}',remove_reg(line)))
            while closenum > 0:
                if isinstance(lopen[0], Server):
                    f.add(lopen[0]) if conf else f.append(lopen[0])
                    lopen.pop(0)
                elif isinstance(lopen[0], Container):
                    c = lopen[0]
                    lopen.pop(0)
                    if lopen:
                        lopen[0].add(c)
                    else:
                        f.add(c) if conf else f.append(c)
                closenum = closenum - 1
        if re.match('\s*#\s*', line):
            c = Comment(re.match('\s*#\s*(.*)$', line).group(1))
            if len(lopen):
                lopen[0].add(c)
            else:
                f.add(c) if conf else f.append(c)
    return f

def read_no_conf(data):
    data = open(data).read()
    finished_one = 0
    f = Conf()
    lopen = []
    max_count = 0
    for line in data.split('\n'):
        if re.match('\s*events\s*\{', line):
            s = Events()
            lopen.insert(max_count, s)
            max_count = max_count + 1
        if re.match('\s*http.*\{', line):
            s = Http()
            lopen.insert(max_count, s)
            max_count = max_count + 1
        if re.match('.*;', line):
            kname, kval = re.match('.*(?:^|^\s*|{\s*)(\S+)\s(.+);', line).group(1, 2)
            k = Key(kname, [x for x in kval.split() if len(x)>0])
            if max_count == 0:
                s = MainArgs()
                lopen.insert(max_count,s)
                lopen[max_count].add(k)
                max_count = max_count + 1
            else:
                lopen[max_count-1].add(k)
        if re.match('.*}', remove_reg(line)):
            finished_one = 1
    for x in lopen:
        f.add(x)
    return f

def _nginx_data_to_reg(data):
    if data:
        num = 0
        temp_list = r"^\s*"
        for x in data.split("|||"):
            temp_list = temp_list + "(" + str(x) + ")" + r"\s+\S{0,1}"
            num = num +1
        temp_list = temp_list.rstrip("\s+") + r"((\S{0,3}\s*)|(\s*))"
        return (temp_list,num)
    else:
        return ""




def nginx_del(obj,data):
    func = data.split("|||")
    k = Key(str(func[1]),func[2:])
    print k.value
    print k.name
    if len(func)<5:
        if func[0] in __CLASS_LIST__:
            for x in obj.blocks:
                if x.__name__ == func[0]:
                    for y in x.keys:
                        if y.name == k.name and y.value == k.value:
                            x.remove(y)
    return obj

##update
def nginx_update(obj,data):
    func = data.split("|||")
    if len(func) < 5:
        if func[0] in __CLASS_LIST__:
            for x in obj.blocks:
                if x.__name__ == func[0]:
                    for y in x.blocks :
                        if isinstance(y,Key):
                            if y.name == func[1] and len(y.value) == 1:
                                k = Key(str(func[1]),[func[2]])

                              #  x.remove(y)
                              #  x.add(k)
                                x.upd()
                            elif y.name == func[1] and len(y.value) == 2:
                                if y.value[0] == func[2]:
                                    k = Key(str(func[1]),func[2:])
                                    x.remove(y)
                                    x.add(k)
                                    x.upd()
                        if isinstance(y,Location):
                            lpath = " ".join([y.name,y.value])
                            if lpath == func[1]:
                                k = Location(y.value)
                                for temp_list in func[2:]:
                                    temp = temp_list.split("||")
                                    temp_k = Key(temp[0], temp[1:])
                                    k.add(temp_k)
                                x.remove(y)
                                x.add(k)
                        if isinstance(y,If):
                            lpath = " ".join([y.name,y.value])
                            if lpath == func[1]:
                                k = Location(y.value)
                                for i in range(2,len(func),2):
                                    temp_k = Key(func[i], [x for x in func[i+1].split() if len(x)>0])
                                    k.add(temp_k)
                                x.remove(y)
                                x.add(k)
                        if isinstance(y,Comment):
                            pass
    return obj

## add
def nginx_add(obj,data):
    func = data.split("|||")
    k = Key(str(func[1]),func[2:])
    c = []
    b = []
    if len(func)<5:
        if func[0] in __CLASS_LIST__:
            for x in obj.blocks:
                if x.__name__ == func[0]:
                    for y in x.keys:
                        c.append(y.name)
                        b.append(y.value)
                    if k.value not in b and k.name not in c:
                        x.add(k)
    return obj

##search set
def nginx_search_set(f,data):
    b = f.as_dict()
    func = data.split("|||")
    for dict_x in  b.get("conf"):
        for keys_y in dict_x.keys():
            keys_y_strip = keys_y.strip("}").strip("{").strip()
            if func[0].strip() == keys_y_strip:
                for dict_z in dict_x.get(keys_y):
                    if dict_z.has_key(func[1].strip()):
                        if len(dict_z.get(func[1].strip())) == 1:
                            return True
                        elif len(dict_z.get(func[1].strip())) > 1:
                            print func[2:-1]
                            if dict_z.get(func[1].strip())[0:-1] == func[2:-1]:
                                func[1].strip()
                                return True
    return False


##search set&value -_-!! Do it later...How a dict can be so hard to decode.
def nginx_search_all(fboject, data):
    pass

##reload nginx , just for fun......
def nginx_reload(nginx_path):
    if not os.system(str(nginx_path) + " -s reload"):
        return True
    else:
        return False


def load(fobj):
    return loads(fobj.read())

def loadf(path):
    return load(open(path, 'r'))

def dumps(obj):
    return ''.join(obj.as_block())

def dump(obj, fobj):
    fobj.write(dumps(obj))
    return fobj

def dumpf(obj, path):
    dump(obj, open(path, 'w'))
    return path
