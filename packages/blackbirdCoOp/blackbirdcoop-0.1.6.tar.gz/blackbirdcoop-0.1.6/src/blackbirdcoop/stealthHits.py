"""
LIFT - UCSC iGEM 2024

Module: StealthHits

Author: Vibhitha Nandakumar
"""


class StealthHits:

    """
    Class to find stealth hits within a given sequence

    Input: Stealth list file in text format and the insert sequence as a string

    Output: Returns an embedded list with the hit sequence and its position within the sequence

    """

    def __init__(self, stealthList, iSeq):
        self.stealthList = stealthList
        self.iSeq = iSeq

    def find_hits(self):
        indexes = []

        for hit in self.stealthList:
            length = len(hit)
            start = 0

            while start < len(self.iSeq):
                index = self.iSeq.find(hit, start)
                if index == -1:
                    break
                indexes.append([index, hit])
                start = index + length
        indexes.sort(key=lambda x: x[0])
        return indexes
