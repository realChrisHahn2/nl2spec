from statistics import mode


def get_overlaps(explain_dict_list, k):
    overlaps = []
    for dict in explain_dict_list:
        if k in dict:
            overlaps.append(dict[k])
    return overlaps


def merge_dicts(explain_dict_list):
    merge_dict = {}
    for dict in explain_dict_list:
        for k in dict:
            if k.lower() not in merge_dict:
                merge_dict[k.lower()] = [dict[k]]
            else:
                merge_dict[k.lower()].append(dict[k])
    return merge_dict


def all_equal(l):
    return all(x == l[0] for x in l)


def fill_with_none(dict, n):
    for k in dict:
        i = 0
        while len(dict[k]) < n:
            dict[k].append("None" + str(i))
            i += 1
    return dict


def most_freq(l):
    if len(l) == 0:
        return "No output"
    try:
        res = mode(l)
    except:
        res = l[0]
    return res


def count_occurences(l, el):
    count = 0
    for e in l:
        if e == el:
            count += 1
    return count


def calc_certainty_score(l, el, n):
    occ = count_occurences(l, el)
    return occ / n


def ambiguity_detection_ast():
    return


def add_certainty_and_reduce(merge_d, n):
    reduced = {}
    for k, v in merge_d.items():
        certainty_list = []
        for e in v:
            score = calc_certainty_score(v, e, n)
            if not e.startswith("None"):
                certainty_list.append((e, round(score * 100, 2)))
        certainty_list = list(set(certainty_list))
        certainty_list = sorted(certainty_list, key=lambda x: x[1], reverse=True)
        reduced[k] = certainty_list
    return reduced


def ambiguity_detection_translations(explain_dict_list, n, locked_translations):
    merge_d = merge_dicts(explain_dict_list)
    merge_d = fill_with_none(merge_d, n)
    reduced_d = add_certainty_and_reduce(merge_d, n)
    reduced_d = add_locked_subtranslation(reduced_d, locked_translations)
    certainty_triple_list = [
        (
            k,
            [e[0] for e in reduced_d[k]],
            [e[1] for e in reduced_d[k]],
            [e[2] for e in reduced_d[k]],
        )
        for k in reduced_d.keys()
    ]
    return sorted(certainty_triple_list, key=lambda x: max(x[2]))


def add_locked_subtranslation(model_subt, locked_subt):
    model_subt = {k: [(e[0], e[1], False) for e in model_subt[k]] for k in model_subt}
    for k in locked_subt:
        if k in model_subt:
            elem = None
            for e in model_subt[k]:
                if e[0] == locked_subt[k]:
                    elem = e
            if elem is None:
                model_subt[k] = [(locked_subt[k], 0.0, True)] + model_subt[k]
            else:
                model_subt[k].remove(elem)
                model_subt[k] = [(locked_subt[k], elem[1], True)] + model_subt[k]
        else:
            model_subt[k] = [(locked_subt[k], 0.0, True)]
    return model_subt


def ambiguity_final_translation(parsed_result_formulas, n):
    mf = most_freq(parsed_result_formulas)
    cert = calc_certainty_score(parsed_result_formulas, mf, n)
    return (mf, cert)
