# functor - encapsulates chacksum logic



class CheckSummerFunctor:
    def __init__(self):
        self._checksum=0  # without two's compliment

    @property
    def result(self) -> int:
        # two's compliment it and the fly
        checksum_ = 256 - self._checksum
        return checksum_ #two's complimented

    # Attention: singleByte type is int
    def __call__(self, singleByte: int) -> None:
        if not isinstance(singleByte, int):
            raise TypeError("ChecksumFunctor chamado com tipo de valor invalido")
        else:
            self._checksum += singleByte
            while self._checksum > 255:
                self._checksum -= 256
            #print(f"checkcalc -> put[{singleByte}], acum:[{self._checksum}]")




if __name__=="__main__":

    # 1B 02 C1 50 61 02 1B 03 87
    # 1B 06 C1 50 00 00 1B 03 E6
    # 1B 02 01 82 34 35 1B 03 0F
    # 1B 06 01 82 1B 03 1B 03 56
    # 1B 06 01 89 14 00 1B 03 59

    d1_ = [2, 0xC1, 0x50, 0x61, 0x02, 3] #0x87
    d2_ = [6, 0xC1, 0x50, 0x00, 0x00, 3] #0xE6
    d3_ = [6, 0x01, 0x89, 0x14, 0x00, 3] #0x59

    proc = [d1_, d2_, d3_]
    expected = [0x87, 0xE6, 0x59]
    for data, checksum_expected in zip(proc, expected):
        #print(data, checksum_expected)
        calc = CheckSummerFunctor()
        #print(calc.result)
        sum = 0
        for byte in data:
            sum += byte
            calc(byte)

        assert (calc.result == checksum_expected)
        #print(f'Checksum -> Calculated: [{calc.result}], Expected: [{checksum_expected}], dif({calc.result-checksum_expected}], sum:[{sum}], mul255:[{sum/255}]')

