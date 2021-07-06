import re
from typing import Text 


# 
def RemoveSyncategorematic(text):
    return re.sub('(\s+)(a|an|and|the|of)(\s+)', ' ', text) 


def SuggestShortForms(sentense):
    text = RemoveSyncategorematic(sentense)
    text = re.sub('\(.+?\)', '', text)
    regex = [
        '\W{}\W'.format('.'.join([i[0].upper() for i in text.split(' ') if i])),
        '{}\W+?{}\W+?'.format(sentense, '\.'.join([i[0].upper() for i in text.split(' ') if i])),
        '\W{}\W'.format(''.join([i[0].upper() for i in text.split(' ') if i])),
        '{}\W?\({}\)\W?'.format(sentense, ''.join([i[0].upper() for i in text.split(' ') if i])),
    ]+[i.replace('(', '').replace(')', '') for i in re.findall('\(.+?\)',re.sub('\(.+?\)', '', sentense) )]
    return list(set(regex))


def LooseShortFullMatcher(sentense):
    regex = []
    regex.append(re.escape(sentense))
    regex.append(re.sub('\(.+?\)', '', sentense).replace(' ', '\W?'))
    [regex.append(i) for i in SuggestShortForms(sentense)]    
    return '|'.join(["({})".format(i) for i in regex])


def MatchMiner(patterns, data):
    result = []
    regex = '|'.join(LooseShortFullMatcher(i) for i in patterns)
    print(regex)
    regex  = re.compile(regex, re.I)
    for out in regex.findall(data):
        for x in out:
            if x:
                result.append(x)
    return result



# main function
def main():
    exp = 'Bachelor of Medicine and surgery'
    samples= [
        ' BMS ',
        'B.M.S',
    ]
    
    for data in samples:
        print(MatchMiner([exp], data)) 

if __name__=='__main__':
    main()