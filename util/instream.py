import sys
import urllib.request as urllib
import re

class InStream:

    def __init__(self, fileOrUrl):
        self._buffer = ''
        self._stream = None
        self._readingWebPage = False

        # Try to open a file, then a URL.
        try:
            self._stream = open(fileOrUrl, 'r', encoding='utf-8')
        except IOError:
            try:
                self._stream = urllib.urlopen(fileOrUrl)
                self._readingWebPage = True
            except IOError:
                raise IOError('No such file or URL: ' + fileOrUrl)

    #-------------------------------------------------------------------

    def _readRegExp(self, regExp):
        if self.isEmpty():
            raise EOFError()
        compiledRegExp = re.compile(r'^\s*' + regExp)
        match = compiledRegExp.search(self._buffer)
        if match is None:
            raise ValueError()
        s = match.group()
        self._buffer = self._buffer[match.end():]
        return s.lstrip()

    #-------------------------------------------------------------------

    def isEmpty(self):
        while self._buffer.strip() == '':
            line = self._stream.readline()
            if sys.hexversion < 0x03000000 or self._readingWebPage:
                line = line.decode('utf-8')
            if line == '':
                return True
            self._buffer += str(line)
        return False

    #-------------------------------------------------------------------

    def readInt(self):
        s = self._readRegExp(r'[-+]?(0[xX][\dA-Fa-f]+|0[0-7]*|\d+)')
        radix = 10
        strLength = len(s)
        if (strLength >= 1) and (s[0:1] == '0'): radix = 8
        if (strLength >= 2) and (s[0:2] == '-0'): radix = 8
        if (strLength >= 2) and (s[0:2] == '0x'): radix = 16
        if (strLength >= 2) and (s[0:2] == '0X'): radix = 16
        if (strLength >= 3) and (s[0:3] == '-0x'): radix = 16
        if (strLength >= 3) and (s[0:3] == '-0X'): radix = 16
        return int(s, radix)

    def readAllInts(self):
        strings = self.readAllStrings()
        ints = []
        for s in strings:
            i = int(s)
            ints.append(i)
        return ints

    #-------------------------------------------------------------------

    def readFloat(self):
        s = self._readRegExp(r'[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')
        return float(s)

    def readAllFloats(self):
        strings = self.readAllStrings()
        floats = []
        for s in strings:
            f = float(s)
            floats.append(f)
        return floats

    #-------------------------------------------------------------------

    def readBool(self):
        s = self._readRegExp(r'(True)|(False)|1|0')
        if (s == 'True') or (s == '1'):
            return True
        return False

    def readAllBools(self):
        strings = self.readAllStrings()
        bools = []
        for s in strings:
            b = bool(s)
            bools.append(b)
        return bools


    #-------------------------------------------------------------------

    def readString(self):
        s = self._readRegExp(r'\S+')
        return s

    def readAllStrings(self):
        strings = []
        while not self.isEmpty():
            s = self.readString()
            strings.append(s)
        return strings

    #-------------------------------------------------------------------

    def hasNextLine(self):
        if self._buffer != '':
            return True
        else:
            self._buffer = self._stream.readline()
            if sys.hexversion < 0x03000000 or self._readingWebPage:
                self._buffer = self._buffer.decode('utf-8')
            if self._buffer == '':
                return False
            return True

    #-------------------------------------------------------------------

    def readLine(self):
        if not self.hasNextLine():
            raise EOFError()
        s = self._buffer
        self._buffer = ''
        return s.rstrip('\n')

    def readAllLines(self):
        lines = []
        while self.hasNextLine():
            line = self.readLine()
            lines.append(line)
        return lines

    #-------------------------------------------------------------------

    def readAll(self):
        s = self._buffer
        self._buffer = ''
        for line in self._stream:
            if sys.hexversion < 0x03000000 or self._readingWebPage:
                line = line.decode('utf-8')
            s += line
        return s

    #-------------------------------------------------------------------

    def __del__(self):
        if self._stream is not None:
            self._stream.close()