# Returns a Composition Polynomial. Channel provides the coef
def get_CP(channel,poly):

    coef = [channel.receive_random_field_element() for i in range(len(poly))]

    return [alpha*p for alpha,p in zip(coef,poly)][0]

## Returns a list of images from the CP
def CP_eval(cp, eval_domain):
    #CP = get_CP(channel,p0,p1,p2)
    return [cp(d) for d in eval_domain]