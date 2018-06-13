#ft_params = {'init_acc':0.5, 'nb_bel_ratio':1e-3, 'threshold':{'low':0.51, 'high':0.8}}

def ft_algo(ans,nb_json, ft_degree,ft_params):
    # ft_degree: 0 off, 1 low, 2 high 
    # ft_degree always legal
    total = 0
    answers = []
    accset = []
    if len(ans)>1:
        # print('length: ')
        # print(len(ans))
        for i in ans:
            if i[1] not in answers :
                # print(i[1])
                if i[4] < ft_params['nb_bel_ratio']:
                    answers.append(i[1])
                    accset.append(ft_params['init_acc'])
                    total += ft_params['init_acc']
                else:
                    answers.append(i[1])
                    accset.append(i[3]/i[4])
                    total += i[3]/i[4]
            else:
                if i[4] <ft_params['nb_bel_ratio']:
                    accset[answers.index(i[1])] += ft_params['init_acc']
                    total += ft_params['init_acc']
                else:
                    accset[answers.index(i[1])] += i[3]/i[4]
                    total += i[3]/i[4]
        if max(accset)/total >= threshold:
            coranswer = answers[accset.index(max(accset))]
            answerset = []
            for an in ans:
                if an[1] == coranswer:
                    answerset.append(an[0])
            # print(total)
            # print(k/total)
            return answerset
    else :
        return None