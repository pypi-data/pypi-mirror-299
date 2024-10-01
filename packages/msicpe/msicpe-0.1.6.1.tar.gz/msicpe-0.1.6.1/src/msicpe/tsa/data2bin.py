import struct
import numpy as np


def data2bin(s,dtype='int'):
    """Convert data s of type dtype into binary representation

    Args:
        s (np.array): data 
        dtype (str, optional): datatype. Defaults to 'int'.
    """
        
    def _binary(num):
        return ''.join('{:0>8b}'.format(c) for c in struct.pack('!i', num))


    def _float_to_bin(value):  # For testing.
        """ Convert float to 32-bit binary string. """
        [d] = struct.unpack("!I", struct.pack("!f", value))
        return '{:032b}'.format(d)
    binary_repr_v=None
    
    if dtype=='int':
        binary_repr_v = np.vectorize(_binary)
    elif dtype=='float':
        binary_repr_v = np.vectorize(_float_to_bin)
# Conversion de la chaine de caractère (représentation binaire) en suite d'int
    return np.array([[int(x) for i in binary_repr_v(s) for x in i]])