"""
 The function gets an index and a channel, and sends over the channel the relevant data for verifying the correctness of the FRI layers. 
 More specifically, it iterates over fri_layers and fri_merkles and in each iteration it sends the following data (in the stated order):
"""
def decommit_on_fri_layers(idx, channel, fri_layers, fri_merkles):
    for layer, merkle in zip(fri_layers[:-1], fri_merkles[:-1]):
        length = len(layer)
        idx = idx % length
        sib_idx = (idx + length // 2) % length        
        channel.send(str(layer[idx]))
        channel.send(str(merkle.get_authentication_path(idx)))
        channel.send(str(layer[sib_idx]))
        channel.send(str(merkle.get_authentication_path(sib_idx)))       
    channel.send(str(fri_layers[-1][0]))


"""
To prove that indeed the FRI layers we decommit on were generated from evaluation of the composition polynomial, we must also send:

1. The value 𝑓(𝑥) with its authentication path.
2. The value 𝑓(𝑔𝑥) with its authentication path.
3. The value 𝑓(𝑔2𝑥) with its authentication path.
The verifier, knowing the random coefficients of the composition polynomial, can compute its evaluation at 𝑥, 
and compare it with the first element sent from the first FRI layer.

decommit_on_query sends (1, 2, and 3) over the channel, and then call decommit_on_fri_layers
"""
def decommit_on_query(idx, channel, fri_layers, fri_merkles, f_eval, f_merkle): 
    assert idx + 16 < len(f_eval), f'query index: {idx} is out of range. Length of layer: {len(f_eval)}.'
    channel.send(str(f_eval[idx])) # f(x).
    channel.send(str(f_merkle.get_authentication_path(idx))) # auth path for f(x).
    channel.send(str(f_eval[idx + 8])) # f(gx).
    channel.send(str(f_merkle.get_authentication_path(idx + 8))) # auth path for f(gx).
    channel.send(str(f_eval[idx + 16])) # f(g^2x).
    channel.send(str(f_merkle.get_authentication_path(idx + 16))) # auth path for f(g^2x).
    decommit_on_fri_layers(idx, channel,fri_layers, fri_merkles)  

# To finish the proof, the prover gets a set of random queries from the channel, i.e., indices between 0 to 8191, and decommits on each query.
def decommit_fri(channel, fri_layers, fri_merkles, f_eval, f_merkle):
    for query in range(3):
        # Get a random index from the verifier and send the corresponding decommitment.
        decommit_on_query(channel.receive_random_int(0, 8191-16), channel, fri_layers, fri_merkles, f_eval, f_merkle)

