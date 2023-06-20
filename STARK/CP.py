# Returns a Composition Polynomial. Channel provides the coef
def get_CP(channel,p0,p1,p2):
    alpha0 = channel.receive_random_field_element()
    alpha1 = channel.receive_random_field_element()
    alpha2 = channel.receive_random_field_element()
    return alpha0*p0 + alpha1*p1 + alpha2*p2

## Returns a list of images from the CP
def CP_eval(cp, eval_domain):
    #CP = get_CP(channel,p0,p1,p2)
    return [cp(d) for d in eval_domain]