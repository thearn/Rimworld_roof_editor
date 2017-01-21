import filecmp
from rim_map_roof import RimMapRoof

def test_file_unchanged():

    fn = 'data/Pottstown.rws'
    fn2 = 'data/Pottstown_same.rws'

    rm = RimMapRoof(fn)
    rm.write_image('data/Untitled.bmp')
    rm.read_image('data/Untitled.bmp')
    rm.save(fn2)

    assert filecmp.cmp(fn, fn2)

def test_file_changed():

    fn = 'data/Pottstown.rws'
    fn2 = 'data/Pottstown_same.rws'

    rm = RimMapRoof(fn)
    rm.read_image('data/edited.bmp')
    rm.save(fn2)

    assert not filecmp.cmp(fn, fn2)

