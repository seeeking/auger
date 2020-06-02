
def add(a, b):
    c = a + b
    return c


def update_dict(origin, to_update):
    origin.update(to_update)

# def mutate_dict(origin):
#     return {f'{k}_mutated': v for k, v in origin.items()}
#
# # Auger cannot handle args reassignment, tracer doesn't record the old reference
# # I don't know how to fix this without changing the architecture completely
# # it's a bad habit anyway, so be able to capture real mutation matters more to me
# # If we do not use a tracer or profiler, e.g. if we use a invasive annotation approach, we may be able to fix this
# def update_dict_reassign(origin):
#     origin = mutate_dict(origin)
#     return origin

