boorufs
=======

Easy/shitty fs based on FUSE to browse danbooru from your favourite filemanager/image viewer.

Usage:

`python boorufs.py MOUNTPOINT`

- `MOUNTPOINT` is any directory where you can write

Once it's mounted, open `MOUNTPOINT/any_tags` to browse a tag.

`fusermount -u -z MOUNTPOINT` to close/delete the mountpoint

Require:
- [Requests](http://docs.python-requests.org/en/latest/)
- [fuse-python](https://pypi.python.org/pypi/fuse-python)

Shortcomings:
- Danbooru is hardcoded
- Only display 10 items at time
- Cache images on /tmp/
- No way to navigate, needs to open directly the tag 
- Buggy