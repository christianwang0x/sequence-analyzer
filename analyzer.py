from statistics import *


MAX_DEGREE = 1


# Object for a column of data bytes.
# That is, a byte at a specific index
#   for every row in a 2d table of bytes
# The initialization parameters determine the desired
#   two sets of values (residuals, uniformities),
#   which can be called as soon as the object
#   has been instantiated.
class Column:
    def __init__(self, sequence, index):
        self.maximum_degree = MAX_DEGREE
        self.row_count = len(sequence)
        self.byte_list = self.get_byte_list(sequence, index)
        self.entry_list = self.get_byte_list(sequence, index, False)
        self.frequencies = self.get_frequencies()
        self.entry_count = self.get_entry_count()
        self.longest_slice = self.get_longest_entry_slice()

    def __call__(self):
        residual = self.get_scaled_residual()
        uniformity_score = self.get_uniformity_score()
        return residual, uniformity_score

    # Gets a series of bytes from a sequence at a specified
    #   index.
    @staticmethod
    def get_byte_list(sequence, index, fill=True):
        byte_list = []
        for row in sequence:
            if index > len(row)-1:
                if fill:
                    byte_list.append(None)
                else:
                    pass
            else:
                byte_list.append(row[index])
        return byte_list

    # Find the longest continuous series of bytes in
    #   a column. This comes in handy when not all of
    #   the input rows are of the same length.
    def get_longest_entry_slice(self):
        start = 0
        stop = 0
        new_start = 0
        new_stop = new_start
        while new_start < self.row_count:
            while new_stop < self.row_count:
                if self.byte_list[new_stop] is None:
                    if new_stop - new_start > stop - start:
                        start = new_start
                        stop = new_stop
                    new_start = new_stop+1
                    new_stop = new_start
                    break
                else:
                    new_stop += 1
            else:
                if new_stop - new_start > stop - start:
                    start = new_start
                    stop = new_stop
                break
        return slice(start, stop)

    # Get the frequency of each byte found in a column.
    # Returns a dictionary mapping the byte to its count.
    def get_frequencies(self):
        byte_list = self.byte_list
        frequencies = dict()
        for b in byte_list:
            if frequencies.get(b):
                frequencies[b] += 1
            else:
                frequencies[b] = 1
        return frequencies

    # Gets the number of actual values in a column.
    # If some columns are shorter than others, their
    #   ending bytes are added as None objects to
    #   self.byte_list
    def get_entry_count(self):
        byte_list = self.byte_list
        entry_count = 0
        for b in byte_list:
            if b is not None:
                entry_count += 1
        return entry_count

    # Takes the longest continuous series of bytes in
    #   a column and finds the best polynomial to fit.
    # The residual is scaled to compensate for a lack
    #   of bytes at some indexes.
    def get_scaled_residual(self):
        cbl = self.byte_list[self.longest_slice]
        start = self.longest_slice.start
        stop = self.longest_slice.stop
        length = stop - start
        int_pairs = [(i, self.byte_list[i]) for i in range(start, stop)]
        x, y = zip(*int_pairs)
        degree = get_best_fit_degree(x, y, self.maximum_degree)
        residual = round(get_residual(x, y, degree), 2)
        multiplier = length / self.row_count
        scaled_residual = residual / multiplier
        return scaled_residual

    # Get a score that represents the uniformity
    #   of a column. Uses an online variance algorithm
    def get_uniformity_score(self):
        n = 0
        mean = 0
        m2 = 0
        variance = None
        for b in range(256):
            x = self.frequencies.get(b, 0)
            n = n + 1
            delta = x - mean
            mean = mean + delta / n
            m2 = m2 + delta * (x - mean)
            try:
                variance = m2 / (n - 1)
            except ZeroDivisionError:
                pass
        y = (variance / (self.entry_count ** 2)) * 250
        return y
