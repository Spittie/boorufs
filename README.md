boorufs
=======

Easy/shitty fs based on FUSE to browse danbooru from your favourite filemanager/image viewer.

## Usage:

`python boorufs.py MOUNTPOINT`

- `MOUNTPOINT` is any directory where you can write

Once it's mounted, open `MOUNTPOINT/any_tags` to browse a tag.

`fusermount -u -z MOUNTPOINT` to close/delete the mountpoint

## Config:
Configuring boorufs is simple, you just need to edit booru.cfg.

`[danbooru]` Name of the booru

`type = danbooru` type of the booru. danbooru and moebooru are supported so far

`url = http://danbooru.donmai.us` Url of the booru, with "http://" and without the ending "/"

`limit = 10` How many files to requests. Note that most booru are limited to 100

## Require:
- [Requests](http://docs.python-requests.org/en/latest/)
- [fuse-python](https://pypi.python.org/pypi/fuse-python)

## Shortcomings:
- Cache images on /tmp/boorufs/
- No way to navigate, needs to open directly the tag 
- Buggy

![boorufs](https://raw.github.com/Spittie/boorufs/master/boorufs.gif)