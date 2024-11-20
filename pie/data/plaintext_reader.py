from .base_reader import BaseReader


class PlainTextReader(BaseReader):
    """
    Reader for plain text format (txt files)
    
    Segmentation is be performed based on end of lines and/or split into self.max_sent_len words (separated with blank space)
    """
    def __init__(self, settings, fpath):
        super(PlainTextReader, self).__init__(settings, fpath)
        self.max_sent_len = settings.max_sent_len

    def parselines(self):
        """
        Generator over sentences in a single file

        Yields tuples:
            - list of raw tokens
            - None (gap filler for the dict of tasks that are absent in plain text files)
        """
        inp = []

        for inp in self.get_sents():
            while len(inp) > self.max_sent_len:
                inp_ = inp[:self.max_sent_len]
                yield inp_, None
                inp = inp[self.max_sent_len:]
            yield inp, None

    def get_tasks(self):
        """
        All conll tasks (as in proiel files) in expected order
        """
        return set()

    def get_sents(self):
        lines = 0
        with open(self.fpath) as f:            
            for line in f:
                if not line.strip():
                    continue
                # Tokenize on whitespaces
                line_tokens = line.strip().split()
                lines += 1
                yield line_tokens       
