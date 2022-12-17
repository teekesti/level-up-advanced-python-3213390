def pairwise_offset(sequence, fillvalue='*', offset=0):
    orig = list(sequence)
    shifted_orig = orig + [fillvalue]*offset
    seq_copy = [fillvalue]*offset + orig
    return list(zip(shifted_orig, seq_copy))
