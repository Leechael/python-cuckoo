'''
Example usage. Modeled after https://github.com/efficient/cuckoofilter/blob/master/example/test.cc
'''

import cuckoofilter
import gzip

if __name__ == '__main__':
    total_items = 100000
    cf = cuckoofilter.CuckooFilter(total_items, 2)

    num_inserted = 0
    for i in range(total_items):
        cf.insert(str(i))
        num_inserted = num_inserted + 1

    for i in range(num_inserted):
        assert cf.contains(str(i))

    total_queries = 0
    false_queries = 0
    for i in range(total_items, 2 * total_items):
        if cf.contains(str(i)):
            false_queries = false_queries + 1
        total_queries = total_queries + 1

    serialized = cf.serialize().read()

    print('False positive rate is {:%}'.format(false_queries / total_queries))
    print("size after serialize: {:}".format(len(serialized)))
    print("size after serialize + gzip: {:}".format(len(gzip.compress(serialized))))
