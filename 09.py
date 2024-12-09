from aoc import *

blocks = [int(n) for n in data]

File = namedtuple("File", "pos,id,size")
FreeSpace = namedtuple("FreeSpace", "pos,size")

free_space = deque()
files = []
pos = 0
for i, nblocks in enumerate(blocks):
    if i % 2 == 0:
        files.append(File(pos, len(files), nblocks))
        pos += files[-1].size
    else:
        free_space.append(FreeSpace(pos, nblocks))
        pos += free_space[-1].size

while free_space and free_space[0][0] < files[-1][0]:
    space = free_space.popleft()
    file = files.pop()

    moved_file = File(space.pos, file.id, min(space.size, file.size))
    insort(files, moved_file, key=attrgetter("pos"))

    remaining_space = space.size - moved_file.size
    if remaining_space > 0:
        free_space.appendleft(
            space._replace(pos=space.pos + moved_file.size, size=remaining_space)
        )
    remaining_file = file.size - moved_file.size
    if remaining_file > 0:
        files.append(file._replace(size=remaining_file))

    new_space = FreeSpace(file.pos + remaining_file, moved_file.size)
    free_space.append(new_space)


def checksum():
    s = 0
    for pos, fileid, size in files:
        for i in range(size):
            s += (pos + i) * fileid
    return s


print(checksum())


free_space = []
files.clear()
pos = 0
for i, nblocks in enumerate(blocks):
    if i % 2 == 0:
        files.append(File(pos, len(files), nblocks))
        pos += files[-1].size
    else:
        free_space.append(FreeSpace(pos, nblocks))
        pos += free_space[-1].size

files_by_id = {f.id: f for f in files}
for fileid in reversed(range(len(files))):
    file = files_by_id[fileid]
    space = None
    for i in range(len(free_space)):
        if free_space[i].pos > file.pos:
            break
        if free_space[i].size >= file.size:
            space = free_space.pop(i)
            break
    if space is None:
        continue

    moved_file = File(space.pos, file.id, min(space.size, file.size))
    files_by_id[fileid] = moved_file

    remaining_space = space.size - moved_file.size
    if remaining_space > 0:
        insort(
            free_space,
            space._replace(pos=space.pos + moved_file.size, size=remaining_space),
            key=attrgetter("pos"),
        )

    new_space = FreeSpace(file.pos, moved_file.size)
    insort(free_space, new_space, key=attrgetter("pos"))

files = sorted(files_by_id.values(), key=attrgetter("pos"))
print(checksum())
