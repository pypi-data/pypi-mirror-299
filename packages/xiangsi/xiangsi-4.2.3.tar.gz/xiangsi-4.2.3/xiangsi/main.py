import math
import binascii
import hashlib
from . import func

funcs = func.Functions()

class Calculator(object):
    def __init__(self):
        self.feature = 64
        self.HashNums = 16
        self.prime = 4294967311


    def cossim(self, input1, input2):
        result1 = funcs.GetWeight(input1)
        result2 = funcs.GetWeight(input2)

        WordSet = list(set(result1.keys()).union(set(result2.keys())))
        DotProduct = 0
        sq1 = 0
        sq2 = 0

        for word in WordSet:
            # Get vector value of both documents
            vector1 = result1[word] if word in result1 else 0
            vector2 = result2[word] if word in result2 else 0
            
            # Calculate Cosine Similarity for this dimension
            DotProduct += vector1 * vector2
            sq1 += pow(vector1, 2)
            sq2 += pow(vector2, 2)

        try:
            FinalResult = DotProduct / (math.sqrt(sq1) * math.sqrt(sq2))
        except ZeroDivisionError:
            FinalResult = 0.0

        return FinalResult
    

    def jaccard(self, input1, input2):
        result1 = funcs.GetWeight(input1)
        result2 = funcs.GetWeight(input2)

        WordSet = list(set(result1.keys()).union(set(result2.keys())))
        TopSum = 0
        BottomSum = 0

        for word in WordSet:
            vector1 = result1[word] if word in result1 else 0
            vector2 = result2[word] if word in result2 else 0
            
            TopSum += min(vector1, vector2)
            BottomSum += max(vector1, vector2)

        try:
            FinalResult = TopSum / BottomSum
        except ZeroDivisionError:
            FinalResult = 0.0

        return FinalResult
    
    
    def simhash(self, input1, input2):
        result1 = funcs.GetWeight(input1)
        result2 = funcs.GetWeight(input2)

        tfidf1 = {k: result1[k] for k in sorted(result1, key=result1.get, reverse=True)[:self.feature]}
        tfidf2 = {k: result2[k] for k in sorted(result2, key=result2.get, reverse=True)[:self.feature]}

        product1 = [0] * self.feature
        product2 = [0] * self.feature

        for key, value in tfidf1.items():
            hashed = hashlib.md5(key.encode('utf-8')).hexdigest()
            vector = bin(int(hashed, 16))[-self.feature:]

            for i, x in enumerate(vector):
                product1[i] += value if (x == '1') else (value * -1)

        for key, value in tfidf2.items():
            hashed = hashlib.md5(key.encode('utf-8')).hexdigest()
            vector = bin(int(hashed, 16))[-self.feature:]

            for i, x in enumerate(vector):
                product2[i] += value if (x == '1') else (value * -1)


        fprint1 = ""
        fprint2 = ""
        for i in range(self.feature):
            fprint1 += '1' if product1[i] >= 0 else '0'
            fprint2 += '1' if product2[i] >= 0 else '0'

        FinalResult = sum(pos1 == pos2 for pos1, pos2 in zip(fprint1, fprint2)) / self.feature
        return FinalResult
    

    def minhash(self, input1, input2):
        result = funcs.GetWeight(input1)
        result2 = funcs.GetWeight(input2)

        coeff1 = funcs.HashAlg(self.HashNums)
        coeff2 = funcs.HashAlg(self.HashNums)

        signature = {}
        signature2 = {}

        MinhashNum = self.prime
        MinhashNum2 = self.prime
        for i in range(0, self.HashNums):
            for x in result.keys():
                crc = binascii.crc32(x.encode('utf-8')) & 0xffffffff
                # Generating Hash
                HashCode = (coeff1[i] * crc + coeff2[i]) % self.prime
                #  Track the lowest hash code seen.
                if HashCode < MinhashNum:
                    MinhashNum = HashCode
                
                if MinhashNum not in signature:
                    signature[MinhashNum] = result[x]

            for y in result2.keys():
                crc = binascii.crc32(y.encode('utf-8')) & 0xffffffff
                HashCode2 = (coeff1[i] * crc + coeff2[i]) % self.prime
                if HashCode2 < MinhashNum2:
                    MinhashNum2 = HashCode2
                
                if MinhashNum2 not in signature2:
                    signature2[MinhashNum2] = result2[y]
        
        intersect = 0
        total = 0
        for x, y in signature.items():
            if x in signature2:
                intersect += y
            total += y

        try:
            return intersect / total
        except ZeroDivisionError:
            return 0

