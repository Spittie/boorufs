import os
import urllib
import fuse
import requests
import stat
import ConfigParser

fuse.fuse_python_api = (0, 2)


class MyStat(fuse.Stat):
    def __init__(self):
        self.st_mode = stat.S_IFDIR | 0755
        self.st_ino = 0
        self.st_dev = 0
        self.st_nlink = 2
        self.st_uid = 0
        self.st_gid = 0
        self.st_size = 4096
        self.st_atime = 0
        self.st_mtime = 0
        self.st_ctime = 0


class BooruFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        fuse.Fuse.__init__(self, *args, **kw)

        self.files = {}
        self.oldpath = ""
        self.olddirs = ['.', '..']
        self.config = ConfigParser.RawConfigParser()
        self.config.read("booru.cfg")

    def readdir(self, path, offset):
        dirs = self.olddirs
        if path != self.oldpath:
            dirs = []
            self.files = {}
            if path == "/":
                for section in self.config.sections():
                    dirs.append(str(section))

            elif path.split("/")[-2] == '':
                booru = path.split("/")[-1]
                url = self.config.get(booru, "url")
                limit = self.config.get(booru, "limit")
                # Default to danbooru
                r = requests.get(url + "/posts.json" + "?limit=" + str(limit))
                if self.config.get(booru, "type") == "danbooru":
                    r = requests.get(url + "/posts.json" + "?limit=" + str(limit))
                if self.config.get(booru, "type") == "moebooru":
                    r = requests.get(url + "/post.json" + "?limit=" + str(limit))
                for i in r.json():
                    try:
                        dirs.append(str(i["file_url"].split("/")[-1]))
                        self.files[str(i["file_url"].split("/")[-1])] = {}
                        self.files[str(i["file_url"].split("/")[-1])].update({"file_url": i["file_url"]})
                        self.files[str(i["file_url"].split("/")[-1])].update({"booru": booru})
                        self.files[str(i["file_url"].split("/")[-1])].update({"file_size": i["file_size"]})
                    except KeyError:
                        pass

            else:
                booru = path.split("/")[1]
                url = self.config.get(booru, "url")
                search = path.split("/")[2]
                limit = self.config.get(booru, "limit")
                r = requests.get(url + "/posts.json" + "?limit=" + str(limit) + "&tags=" + search)
                if self.config.get(booru, "type") == "danbooru":
                    r = requests.get(url + "/posts.json" + "?limit=" + str(limit) + "&tags=" + search)
                if self.config.get(booru, "type") == "moebooru":
                    r = requests.get(url + "/post.json" + "?limit=" + str(limit) + "&tags=" + search)
                for i in r.json():
                    try:
                        dirs.append(str(i["file_url"].split("/")[-1]))
                        self.files[str(i["file_url"].split("/")[-1])] = {}
                        self.files[str(i["file_url"].split("/")[-1])].update({"file_url": i["file_url"]})
                        self.files[str(i["file_url"].split("/")[-1])].update({"booru": booru})
                        self.files[str(i["file_url"].split("/")[-1])].update({"file_size": i["file_size"]})
                    except KeyError:
                        pass

        self.oldpath = path
        self.olddirs = dirs
        for d in dirs:
            yield fuse.Direntry(d)

    def getattr(self, path):
        st = MyStat()
        if path.__contains__("."):
            st.st_mode = stat.S_IFREG | 0666
            st.st_nlink = 1
            st.st_size = self.files[str(path.split("/")[-1])]["file_size"]
        return st

    def read(self, path, size, offset):
        filename = str(path.split("/")[-1])
        booru = self.files[filename]["booru"]
        url = self.files[filename]["file_url"]
        if not os.path.exists("/tmp/boorufs"):
            os.makedirs("/tmp/boorufs")
        if not os.path.exists("/tmp/boorufs/"+filename):
            if self.config.get(booru, "type") == "danbooru":
                if url[0:2] == "//":
                    r = urllib.urlretrieve("http:" + url, "/tmp/boorufs/" + filename)
                else:
                    r = urllib.urlretrieve(str(self.config.get(booru, "url")) + self.files[filename]["file_url"],
                                           "/tmp/boorufs/" + filename)
            if self.config.get(booru, "type") == "moebooru":
                r = urllib.urlretrieve(url, "/tmp/boorufs/" + filename)
        f = os.open("/tmp/boorufs/"+filename, os.O_RDONLY)
        return os.read(f, os.path.getsize("/tmp/boorufs/"+filename))[offset:offset+size]

    def mknod(self, path, mode, dev):
        return 0

    def unlink(self, path):
        return 0

    def write(self, path, buff, offset):
        return 0

    def release(self, path, flags):
        return 0

    def open(self, path, flags):
        return 0

    def truncate(self, path, size):
        return 0

    def utime(self, path, times):
        return 0

    def mkdir(self, path, mode):
        return 0

    def rmdir(self, path):
        return 0

    def rename(self, pathfrom, pathto):
        return 0

    def fsync(self, path, isfsyncfile):
        return 0


def main():
    server = BooruFS()
    server.parse(errex=1)
    server.main()


if __name__ == "__main__":
    main()