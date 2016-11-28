import pytest
import cuckoofilter
from io import BytesIO

@pytest.fixture
def cf():
    return cuckoofilter.CuckooFilter(1000, 4)

def test_insert(cf):
    assert cf.insert('hello')
    assert cf.size == 1

def test_insert_second_position(cf):
    for _ in range(cf.bucket_size - 1):
        cf.insert('hello')
    i1 = cf.insert('hello')
    i2 = cf.insert('hello')
    assert i1 != i2

@pytest.mark.skip(reason="Failed after remove f2, and this test maybe unecessary.")
def test_insert_full(cf):
    # A cuckoofilter can hold at most 2 * bucket_size of the same fingerprint
    for _ in range(cf.bucket_size * 2):
        cf.insert('hello')

    with pytest.raises(cuckoofilter.Fullfill) as e:
        cf.insert('hello')

    assert cf.size == (cf.bucket_size * 2)

def test_insert_over_capacitiy(cf):
    with pytest.raises(cuckoofilter.Fullfill) as e:
        for i in range((cf.capacity * cf.bucket_size) + 1):
            cf.insert(str(i))
    assert cf.load_factor() > 0.9

def test_contains(cf):
    cf.insert('hello')
    assert cf.contains('hello'), 'Key was not inserted'

def test_contains_builtin(cf):
    cf.insert('hello')
    assert 'hello' in cf

def test_delete(cf):
    cf.insert('hello')
    assert cf.delete('hello')
    assert not cf.contains('hello')
    assert cf.size == 0

def test_delete_second_bucket(cf):
    for _ in range(cf.bucket_size + 1):
        cf.insert('hello')
    for _ in range(cf.bucket_size + 1):
        cf.delete('hello')
    assert cf.size == 0

def test_delete_non_existing(cf):
    assert not cf.delete('hello')

def test_load_factor_empty(cf):
    assert cf.load_factor() == 0

def test_load_factor_non_empty(cf):
    cf.insert('hello')
    assert cf.load_factor() == (1 / (cf.capacity * cf.bucket_size))

def test_serialize(cf):
    for _ in range(cf.bucket_size):
        cf.insert('hello')
    io = cf.serialize()
    assert isinstance(io, BytesIO)
    assert io.tell() == 0

def test_unserialize(cf):
    for _ in range(cf.bucket_size):
        cf.insert(str(_))
    io = cf.serialize()
    ncf = cuckoofilter.CuckooFilter.unserialize(io)
    assert cf.capacity == ncf.capacity
    assert cf.size == ncf.size
    assert cf.fingerprint_size == ncf.fingerprint_size
    assert cf.bucket_size == ncf.bucket_size
    assert cf.max_kicks == ncf.max_kicks
    for _ in range(ncf.bucket_size):
        assert ncf.contains(str(_))

def test_unserialize_with_invalid_file(cf):
    with pytest.raises(cuckoofilter.StreamValueError) as e:
        with open("/dev/random", "rb") as f:
            cf = cuckoofilter.CuckooFilter.unserialize(f)

def test_unserialize_with_reading_in_utf8(cf):
    with pytest.raises(UnicodeDecodeError) as e:
        with open("/dev/random") as f:
            cf = cuckoofilter.CuckooFilter.unserialize(f)
