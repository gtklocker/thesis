from helpers import compact_list_repr

def normalized_block_id(maybe_block_id):
    if isinstance(maybe_block_id, str):
        return bytearray.fromhex(maybe_block_id)[::-1]
    return maybe_block_id

class Interlink:
    def __init__(self, genesis, blocks=None):
        self.genesis = normalized_block_id(genesis)
        self.blocks = [] if blocks is None else blocks

    def update(self, block_id, level):
        block_id = normalized_block_id(block_id)
        blocks = self.blocks.copy()
        for i in range(0, level+1):
            if i < len(blocks):
                blocks[i] = block_id
            else:
                blocks.append(block_id)
        return Interlink(genesis=self.genesis, blocks=blocks)

    def as_array(self):
        return self.blocks + [self.genesis]

    def __str__(self):
        return compact_list_repr(bytearr[::-1].hex() for bytearr in self.as_array())
