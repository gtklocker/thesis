* hash functions
	- H(x) ~ U(0, 2^n)
	- sha256
	- ripemd160
* public key cryptography
	- public key
	- private key
	- sign(priv, m)
	- verify(pub, sig, m)
	- forall m. verify(pub, sign(priv, m), m) == true
	- encrypt(pub, m)
	- decrypt(priv, m)
	- forall m. decrypt(priv, encrypt(m)) == m
	- bitcoin uses ecdsa
* merkle trees
	- choose hash function, for bitcoin is sha256(sha256(\_))
	- many types, we study bitcoin style
	- point
		- ability to commit to a set of elements using only a single hash (merkle tree root or mtr)
		- generate log(n)-sized proofs of inclusion as needed which one can verify while only knowing the mtr
	- tree generation
		- initialize the lowest, leaf level as the hashes of the elements we wish to include in our set
		- starting from leaf level combine each element with its next, concat and hash
		- if an element doesn't have a next, assume its next is itself (last element on a level of odd length)
	- proof generation (we have the tree and want to prove the existence of a leaf)
		- generate the path of siblings starting from leafs to the root with a bit on each level to denote left/right
	- proof verification (we have the leaf, path, l/r bits and merkle tree root)
		- hash the concat of each element of the path and the last hash generated
		- concat has to be in the correct order utilizing the l/r bit
		- base case hash is the leaf
		- if the last hash matches the merkle tree root 
* bloom filters
	- probabilistic data structure
	- used to test whether an element is a member of a set
	- may have false positives but not false negatives
	- compact representation as array
* addresses
	- encoded form of public key
	- looks like 15Xk2qNwdcYRLijDrJzBFZcKtHXmrkPqEM
	- bitcoin cash looks like qqcmpeefj6wte0yyzrgtwz842avtugd0kv3t2chg24
* how does money sending work
	- alice wishes to send 0.5 btc to bob
	- alice signs a certificate stating the value (0.5 btc) and the recipient (bob's public key), called an output
	- alice places the output in a transaction and publishes it on the network
	- bob now has a balance of 0.5 btc
* transactions
	- contains list of inputs and list of outputs
	- transaction id (txid) is the hash of its contents
	- corollary: changing the contents changes the txid
* blocks
	- prevent double spend
	- contains a header (always) and a list of txs
	- the txs are ordered topologically (a tx input may use another tx's output, and the other tx may be in the same block)
	- block header contains
		- merkle tree root of txids
		- pointer to the previous block hash (previd)
		- a nonce
		- misc. information such as version number
		- in tuple form (previd, mtr, nonce)
	- block hash (block id) is the hash of the header
	- blocks form a DAG
	- there may be forks: always choose the longest chain
	- block base case is the genesis
* utxo
	- unspent transaction outputs
	- balance of an address is the sum of values of the txs in the utxo that reference it
* consensus
* proof of work
	- miners create blocks
	- need to prove they spent time creating them
	- a block is considered valid iff it is well-formed and its hash, H(B) <= T, T is called target
	- mining algorithm: starting with the nonce of 0, increment the nonce until the block is valid
	- Pr[miner mines a block] = T/2^k, where k is the # of bits of the hash fn
	- difficulty: 1/T, as target decreases it's more difficult to mine a block
	- constant difficulty setting: T is constant
	- variable difficulty setting: T varies so that one or more conditions are met
		- for bitcoin, the condition is that a block has to be mined every 10 minutes
		- difficulty adjusts every 2016 blocks
		- if for the last 2016 blocks there were more than 1 block per 10 minutes on average difficulty increases (T decreases)
		- otherwise difficulty decreases (T increases)
* coinbase transaction
	- money to compensate miners, 12.5 btc
	- halves every 210,000 blocks
	- base case of inputs
* genesis block
	- base case block in the blockchain
	- only thing that needs to be hardcoded in software
* outputs
	- can also contain auxillary data, but limited in size
* spending outputs as inputs
* bitcoin script
* pay 2 public key hash
* spv proofs
	- model
		- prover with access to the bitcoin network
		- verifier is offline with no such access, only knows the chain genesis id, but turing complete
	- proving a block B has occured
		- can be proved by supplying a copy of the whole block chain headers from B up to the genesis
	- proving a tx is included in a specific block, assuming the verifier knows the block header & that the block is valid
		- can be proved by supplying the tx, a merkle proof for the txid
		- can be verified by calculating the txid and verifying the merkle proof for the mtr inside the known block header
	- proving a tx (in block B) is included somewhere in the whole block chain
		- prover has to provide proof that B has occured, and proof that the tx is included in B
		- verifier has to check both proofs
		- most useful kind of proof
		- example: convincing someone you've sent them or burnt money
		- linear in the size of the chain
	- problems
		- someone may supply a proof for a block linked to genesis but not on the longest chain
			- mitigation
				- assuming at least one honest prover will partake
				- require the headers for the full chain the block belongs in
				- allow for a contestation period
				- if someone contesting provides a larger chain the original proof is invalid
		- no verification that the tx is actually valid
			- a malicious miner may have added a tx which spend money that does not exist
			- block won't be accepted by any honest full node but the offline verifier can't know that
			- can't be mitigated without knowing the full block history
* full nodes
	- know
		- the full utxo set
		- the longest chain (whole blocks)
	- is the default kind of actor in the network
* lite nodes
	- know
		- txs concerning only their address
		- the longest chain (only headers)
	- how it works
		- lite node announces a bloom filter which matches txs for its address
		- full nodes in the network make sure to notify the lite node for txs in the utxo that match the bloom filter and are not false positives
* upgrades
	- soft fork
	- hard fork
	- velvet fork
	- user activated velvet fork
* nipopows
	- spv proofs require linear space, we wish for this to be smaller
	- intuition: instead of supplying the whole chain on most proofs, we supply a sample of blocks
	- nipopows accomplish logarithmic proofs instead of linear
	- assumptions
		- constant difficulty
		- header contains interlink
		- bitcoin does not satisfy these assumptions
* levels
	- half the blocks are expected to have hash <= T/2
	- a fourth of the blocks are expected to have hash <= T/4
	- a block B is of level i if H(B) <= T/2^i
	- corollary: a block of level i+1 is also of level i
	- a block of level μ is also called a μ-superblock
	- intuition: some blocks
		- are more *important* than others
		- carry more proof-of-work than others
		- more difficult for an adversary to fake than others
* interlink
	- a vector which is assumed to exist inside the block header similar to previd
	- at the i-th position contains the hash of the previous i-superblock
	- corollary: hash at 0-th position is always the same as the previd
* notation
	- upchain: C↑μ, the sub-block chain of C containing only the blocks of level μ
	- C[i] gives the i-th block 
		- if i is negative then the i-th block from the end
		- C[0] is the genesis, denoted G or Gen
	- C[i:j] gives the blocks in sequence from the i-th up to (but not including) the j-th
		- i may be ommited, means i=0
		- j may be ommited, means j=len(C)
	- C{B:} gives the part of the chain from the block B and on
* suffix proof
	- security parameters: k, m
	- proves that a chain (π) with the suffix of length k (χ) claimed is actually a valid chain (not longest!)
	- generation
		- assuming a genesis G
		- χ = C[-k:]
		- π = []
		- let maxμ be the largest level on C[:-k]
		- B = G
		- for μ = maxμ..0
			- let a = C↑μ{B:}
			- π += a[:-m]
			- B = a[-m]
		- return (π, χ)
	- validation
		- the proof needs to be traversable from its last block up until the known genesis
		- traversal happens through the interlinks
	- proofs can be compared so that a proof of a longer chain is better than a proof of a smaller chain
	- proof comparison (in nipopows called verification) will not be covered here
	- but if a verifier wishes to know the longest chain
		- they can offer a contestation period (similar to an spv verifier)
		- and compare proofs submitted to find the best
* infix proof
	- security parameters: k, m
	- proof for general predicates on a block
	- essentially a suffix proof augmented to include
		- a specific set of blocks of interest
		- any auxillary data required for deciding the predicate on that set of blocks
	- how to augment
		- assume an existing suffix proof on the chain where a block of interest B resides, (π, χ)
		- assume A, C in π, where A is the first block before B in π and C is the first block after B in π
			```
			A-------C     level μ


			    B         level μ-λ

			```
		- need to make sure C links back to B in the proof for the proof to be valid
		- need to make sure B links back to A in the proof for the proof to be valid
		- we "follow down" from C to B and from B to A to include those intermediate blocks which contain the interlinks necessary
			- following down is starting from a block and following the pointer in the interlink without moving past our desired block
			- we include those paths in our suffix proof
		- final proof
			```
			A-------C     level μ
			\--\  /
			   | /
			   -B         level μ-λ

			```
	- examples
		- prove there is a specific tx on the chain
* nipopows on bitcoin
	- constant difficulty problem
		- an unsolved problem for nipopows
		- we assume the constant T to be the highest-possible variable T value for bitcoin
		- this value is obtained as the hash value of the genesis block, but is also part of the protocol rules
		- authors have indicated this is correct but the protocol is not proved under this assumption yet (ongoing work)
	- no interlinks in block headers
		- most viable alternative for the timeframe of this work was a user-activated velvet fork
		- we aim (and show that it is possible) to include a transaction on every single block including its interlink
		- need to spend money for this, but for bitcoin cash the amount is modest
		- in this way we can do everything like the interlink was really in the header
		- construction is resistant to blocks where we missed transactions or adversarially posted interlinks
		- suffix and infix proof generation needs to be slightly modified to account for cases where a block doesn't have any or a valid interlink
		- is provably secure per the nipopows paper
* velvet fork nipopows
	- what changes now that we may not have a valid interlink inside a block
	- changes to suffix proof generation, infix proof generation, follow down
* this work
	- implementation of software which does the velvet fork called the *interlinker* (have 2 implementations, one lite and one full node)
		- connects to the bitcoin cash network
		- computes the interlink to be included in the upcoming block
		- creates a transaction containing the mtr of the interlink
		- publishes the transaction for inclusion in the upcoming block
		- use of spv tagged outputs: lite clients only need to download the blk headers & interlink txs & proofs for them only
	- deployment of the interlinker on bitcoin cash testnet
	- statistics of the deployment
	- implementation of a lite client called the *prover* which
		- connects to the bitcoin cash network
		- obtains the chain
		- obtains the interlinks for each block
		- computes the correct interlinks for each block locally and keeps only the velvet transactions with interlinks that match
		- can construct velvet suffix and infix proofs
		- builds on top of the nodejs bcash package
	- interlink compression (block *set* instead of block list)
	- partial use of the interlink with compressed interlinks
		- in cases where a tx ends up on a future block, other than the intended one, most pointers should still be ok
		- prover should keep a cache of all interlink commitments
