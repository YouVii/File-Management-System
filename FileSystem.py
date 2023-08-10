import datetime
import shutil

class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.content = ''
        self.creation_time = datetime.datetime.now()

class FileSystemCLI:
    def __init__(self):
        self.root = Node('/')
        self.current_node = self.root
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'mkdir': self.mkdir,
            'rmdir': self.rmdir,
            'touch': self.touch,
            'rm': self.rm,
            'pwd': self.pwd,
            'write': self.write,
            'read': self.read,
            'mv': self.mv,
            'cp': self.cp
        }

    def start(self):
        while True:
            raw_command = input('> ')
            command = raw_command.strip().split(' ')
            cmd, args = command[0], command[1:]

            if cmd in self.commands:
                self.commands[cmd](*args)
            elif cmd == 'exit':
                break
            else:
                print(f'Unknown command: {cmd}')

    def ls(self):
        for child in self.current_node.children.values():
            print(f'{child.name}\t{len(child.content)}B\t{child.creation_time}')

    def cd(self, directory):
        if directory in self.current_node.children:
            self.current_node = self.current_node.children[directory]
        elif directory == '..':
            if self.current_node.parent is not None:
                self.current_node = self.current_node.parent
        else:
            print(f'No such directory: {directory}')

    def mkdir(self, directory):
        if directory not in self.current_node.children:
            self.current_node.children[directory] = Node(directory, parent=self.current_node)
        else:
            print(f'Directory already exists: {directory}')

    def rmdir(self, directory):
        if directory in self.current_node.children:
            if len(self.current_node.children[directory].children) == 0:
                del self.current_node.children[directory]
            else:
                print(f"Directory '{directory}' is not empty.")
        else:
            print(f'No such directory: {directory}')

    def touch(self, filename):
        if filename not in self.current_node.children:
            self.current_node.children[filename] = Node(filename, parent=self.current_node)
        else:
            print(f'File already exists: {filename}')

    def rm(self, filename):
        if filename in self.current_node.children:
            del self.current_node.children[filename]
        else:
            print(f'No such file: {filename}')

    def pwd(self):
        path = []
        node = self.current_node
        while node is not None:
            path.append(node.name)
            node = node.parent
        print('/'.join(reversed(path)) or '/')

    def write(self, filename, *content):
        content = ' '.join(content)
        if filename in self.current_node.children:
            self.current_node.children[filename].content = content
        else:
            print(f'No such file: {filename}')

    def read(self, filename):
        if filename in self.current_node.children:
            print(self.current_node.children[filename].content)
        else:
            print(f'No such file: {filename}')

    def mv(self, oldname, newname):
        if oldname in self.current_node.children:
            if newname not in self.current_node.children:
                self.current_node.children[newname] = self.current_node.children[oldname]
                self.current_node.children[newname].name = newname
                del self.current_node.children[oldname]
            else:
                print(f'Name already exists: {newname}')
        else:
            print(f'No such file or directory: {oldname}')

    def cp(self, oldname, newname):
        if oldname in self.current_node.children:
            if newname not in self.current_node.children:
                self.current_node.children[newname] = Node(newname, self.current_node)
                self.current_node.children[newname].content = self.current_node.children[oldname].content
            else:
                print(f'Name already exists: {newname}')
        else:
            print(f'No such file or directory: {oldname}')

if __name__ == "__main__":
    cli = FileSystemCLI()
    cli.start()
