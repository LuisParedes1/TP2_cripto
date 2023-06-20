from polynomial import Polynomial
from merkle import MerkleTree

# function that takes the previous domain as an argument, and outputs the next one.
def next_fri_domain(fri_domain):
    return [x ** 2 for x in fri_domain[:len(fri_domain) // 2]]

# takes as arguments a polynomial and a field element (the one we referred to as 𝛽), and returns the "folded" next polynomial.
def next_fri_polynomial(poly,  beta):
    odd_coefficients = poly.poly[1::2]
    even_coefficients = poly.poly[::2]
    odd = beta * Polynomial(odd_coefficients)
    even = Polynomial(even_coefficients)
    return odd + even

# function that takes a polynomial, a domain, and a field element (𝛽), 
# and returns the next polynomial, the next domain, and the evaluation of 
# this next polynomial on this next domain
def next_fri_layer(poly, domain, beta):
    next_poly = next_fri_polynomial(poly, beta)
    next_domain = next_fri_domain(domain)
    next_layer = [next_poly(x) for x in next_domain]
    return next_poly, next_domain, next_layer


"""
cp: The composition polynomial, that is also the first FRI polynomial.
domain: The coset of order 8192 (la traza extendida) that is also the first FRI domain, that is - eval_domain.
cp_eval: The evaluation of cp over domain, which is also the first FRI layer 
cp_merkle: The first Merkle tree (we will have one for each FRI layer) constructed from these evaluation
channel: The channel is used to get random field elements (the values the verifier would supply)
"""
def FriCommit(cp, domain, cp_eval, cp_merkle, channel):    
    fri_polys = [cp]
    fri_domains = [domain]
    fri_layers = [cp_eval]
    fri_merkles = [cp_merkle]

    while fri_polys[-1].degree() > 0:
        beta = channel.receive_random_field_element()
        next_poly, next_domain, next_layer = next_fri_layer(fri_polys[-1], fri_domains[-1], beta)
        fri_polys.append(next_poly)
        fri_domains.append(next_domain)
        fri_layers.append(next_layer)
        fri_merkles.append(MerkleTree(next_layer))
        channel.send(fri_merkles[-1].root)

    channel.send(str(fri_polys[-1].poly[0])) # send over the channel the constant (i.e. - the polynomial's free term)

    return fri_polys, fri_domains, fri_layers, fri_merkles