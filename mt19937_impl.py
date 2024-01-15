# this is simply a python implementation of a standard Mersenne Twister PRNG.
# the parameters used, implement the MT19937 variant of the PRNG, based on the
# Mersenne prime 2^19937−1
# see https://en.wikipedia.org/wiki/Mersenne_Twister for a very good explanation
# of the math behind this...

# class Mt19937():
#     u, d = 11, 0xFFFFFFFF
#     s, b = 7, 0x9D2C5680
#     t, c = 15, 0xEFC60000
#     l = 18
#     # n = 624
#     n = 127

#     def my_int32(self, x):
#         return (x & 0xFFFFFFFF)

#     def __init__(self, seed):
#         w = 32
#         r = 31
#         f = 1812433253
#         self.m = 397
#         self.a = 0x9908B0DF
#         self.MT = [0] * self.n
#         self.index = self.n + 1
#         self.lower_mask = (1 << r) - 1
#         self.upper_mask = self.my_int32(~self.lower_mask)
#         self.MT[0] = self.my_int32(seed)
#         for i in range(1, self.n):
#             self.MT[i] = self.my_int32(
#                 (f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (w - 2))) + i))

#     def extract_number(self):
#         if self.index >= self.n:
#             self.twist()
#             self.index = 0
#         y = self.MT[self.index]
#         # this implements the so-called "tempering matrix"
#         # this, functionally, should alter the output to
#         # provide a better, higher-dimensional distribution
#         # of the most significant bits in the numbers extracted
#         y = y ^ ((y >> self.u) & self.d)
#         y = y ^ ((y << self.s) & self.b)
#         y = y ^ ((y << self.t) & self.c)
#         y = y ^ (y >> self.l)
#         self.index += 1
#         return self.my_int32(y)

#     def twist(self):
#         for i in range(0, self.n):
#             x = (self.MT[i] & self.upper_mask) + \
#                 (self.MT[(i + 1) % self.n] & self.lower_mask)
#             xA = x >> 1
#             if (x % 2) != 0:
#                 xA = xA ^ self.a
#             self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
