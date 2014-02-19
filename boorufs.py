import os
import urllib
import fuse
import requests
import stat

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

    def readdir(self, path, offset):
        dirs = self.olddirs
        if path != self.oldpath:
            dirs = []
            self.files = {}
            if path == "/":
                r = requests.get("http://danbooru.donmai.us/posts.json")
            else:
                r = requests.get("http://danbooru.donmai.us/posts.json?tags=" + path.split("/")[-1])
            for i in r.json():
                try:
                    dirs.append(str(i["large_file_url"].split("/")[-1]))
                    self.files[str(i["large_file_url"].split("/")[-1])] = i["file_size"]
                except KeyError:
                    try:
                        dirs.append(str(i["file_url"].split("/")[-1]))
                        self.files[str(i["file_url"].split("/")[-1])] = i["file_size"]
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
            st.st_size = self.files[path.split("/")[-1]]
        return st

    def read(self, path, size, offset):
        filename = path.split("/")[-1]
        if not os.path.exists("/tmp/"+filename):
            if filename[0:6] == "sample":
                r = urllib.urlretrieve("http://danbooru.donmai.us/data/sample/" + filename, "/tmp/" + filename)
            else:
                r = urllib.urlretrieve("http://danbooru.donmai.us/data/" + filename, "/tmp/" + filename)
        f = os.open("/tmp/"+filename, os.O_RDONLY)
        return os.read(f, os.path.getsize("/tmp/"+filename))[offset:offset+size]

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