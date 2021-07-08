import re
from typing import Text 
import Levenshtein as lev
import os

TEST_DATA = '''
P. MARSHEL BRITTO
 +971- 524305132| blueberry.mg.147@gmail.com| Dubai
Marketing Specialist ~ RELATIONSHIP MANAGEMENT
 Dedicated banking professional offering 7+ years of experience in the banking sector
with sound knowledge of various financial products, investment policies & market
dynamics.
 Managing portfolios of HNIs/UHNIs of UAE and NRIs across the globe by providing them
with a platform to invest in different market territories and currencies.
 Expert in Business Development, Wealth Management and Service Follow-up to ensure
revenue generation and enhanced profitability to meet client expectations.
 Significant experience in managing the business cycle process from client consultation
to closing including identifying opportunities, developing focus, and providing tacti cal
business solutions
 Relationship m anagement skills with an ability to m anage customer centric operations ,
ensuring customer satisfaction by achieving delivery & service quality norms.
 Decisive leader with proven people management skills, proficient in managing multiple
team’s resources by using strong organizational skills, out-of-the-box thinking, and
innovative problem-solving abilities.
Financial Planning &
Analysis
Revenue Growth
Client Relationship
Management
Customer On-boarding
Productivity Improvement
Promotional Strategies
Client Acquisition
Product Research
Team Management
Cross Selling
Portfolio Management
SELECTED CAREER ACCOMPLISHMENTS
Standard chartered
Marketing specialist
April 2016 – Present

 Managing Portfolios of HNIs/UHNIs of UAE and NRIs across the globe by providing them with a platform to invest in different
market territories and currencies.
 Dealing in AUM account opening (min fund of 200k USD), customized Wealth accumulation/management strategies by
partnering with global fund managers . Asset allocation strategies, 360 Degree liability need for the clients.
 Managing USD/GBP/EUR denominated investment portfolios of HNIs .
 Delivered complex in-country and cross-country initiatives, managing in a diverse environment, supervising people directly
or through influence.
 Current Account Opening, Personal Loan, Credit Cards, Car loan & Wealth Referrals.
Key Accomplishments:
Received 2018 most excellent Business development Manager in UAE – Retail Segment
Indusind Bank, Tamil Nadu
Senior Relationship Manager – Priority Banking
(Mar 2015-Apr 2016)
Assist ant Manager- Retail Banking
 Provide financial solutions to the Priority customers and ensure value added services. Increase liabilities size of relations hip via



balances in accounts of existing customers and enhance customer profitability by capturi ng larger share of wallet.
Work closely with clients to develop a customized goals-based financial plan based on their unique financial situation and managed
their portfolio to help reach their financial goals.
Responsible for developing the acquisitions portfolio through internal and external calling efforts to prospect and existing customers.
In addition, provided day to day branch operations support and managed the branch as needed.
Ensured adherence to Bank policies and guidelines such as KYC & AML.
Ensured successful on boarding of the customer for a smooth transition to branch banking team.
Handled activation of customer and ensured that customer maintains required balances & starts transactions in his accounts.
Kotak Mahindra Bank, Tamil Nadu
 Dec 2013-March 2015
Assistant Manager – Gold loan
Division
Developed business plans and sales strategy to ensure attainment of company sales goals & profitability for leading Gold L oans.
chemistry Forecasted sales activity and revenue achievement while creating satisfied customers. Evolved market segmentation & penetr ation
strategies & identified key/institutional accounts and secured profitable business.
Drove new client acquisition efforts for maximizing revenue through Deployment services and Activities.
Pepsi Co Beverages, Tamil Nadu
Marketing Promoter
Worked as “Marketing Promoter” in Beverages Department.
Presales representative attending outlets
Handling distributers
May 2011- Dec 2013
Education :
Sri Krishna College of Arts & Science – Coimbatore | 2011 |Bachelor of Computer Applications.



Date of Birth
Language Proficiency
Address
P ERSONAL INFORMATION
th
: 7 Dec 1990
: English, Tamil and Malayalam.
: A-104, al wasal Towers, Business Bay, Dubai, UAE.
chemistry

'''




# create ngram sets
def ngram_sets(PATTERNS):
    PATTERNS_NGRAMS = {}

    for pat in PATTERNS:
        key = pat.count(' ')+1
        if key in PATTERNS_NGRAMS:
            PATTERNS_NGRAMS[key].append(pat)
        else:
            PATTERNS_NGRAMS[key]= [pat]
    return PATTERNS_NGRAMS

# 
def ngram(tokens, n):
    tokens = tokens.split()
    grams = [tokens[i:i+n] for i in range(len(tokens)-(n-1))]
    return grams

# matcher
def Matcher(NGRAM_TOKEN_PATTERNS, RAW_DATA, ERROR = 1):
    
    result = []
    for n, pattern_vals in NGRAM_TOKEN_PATTERNS.items():
        choices = ngram(RAW_DATA, n)
        for query in pattern_vals:
            for choice in choices:
                choice = ' '.join(choice)
                # exact match
                if choice.lower()==query.lower():
                    result.append([choice, query, 0])
                    continue
                
                # ratio match
                match = lev.ratio(choice.lower(), query.lower())

                # more than 80%
                if match>0.9:
                    result.append([choice, query, match])
                    continue
                
                # match = lev.distance(choice.lower(), query.lower())
                # if match<=ERROR:
                #     result.append([choice, query, match])
    return result

BASE_PATH = './../'

if __name__!='__main__':
    from django.conf import settings
    BASE_PATH = os.path.join(settings.BASE_DIR,'dashboard')


SKILLS_PATTERNS_NGRAMS = ngram_sets(open(os.path.join(BASE_PATH, 'KB/Skills.txt'),'r').read().split('\n'))
DESIGNATION_PATTERNS_NGRAMS = ngram_sets(open(os.path.join(BASE_PATH, 'KB/Designation.txt'),'r').read().split('\n'))
EDUCATION_PATTERNS_NGRAMS = ngram_sets(open(os.path.join(BASE_PATH, 'KB/Education.txt'),'r').read().split('\n'))
GENDER_PATTERNS_NGRAMS = ngram_sets(open(os.path.join(BASE_PATH, 'KB/Gender.txt'),'r').read().split('\n'))
NATIONALITY_PATTERNS_NGRAMS = ngram_sets(open(os.path.join(BASE_PATH, 'KB/Nationality.txt'),'r').read().split('\n'))


def KB_Extractor(DATA):
    result = {
        'SKILLS': Matcher(SKILLS_PATTERNS_NGRAMS, DATA),
        'DESIGNATION': Matcher(DESIGNATION_PATTERNS_NGRAMS, DATA),
        'EDUCATION': Matcher(EDUCATION_PATTERNS_NGRAMS, DATA),
        'GENDER': Matcher(GENDER_PATTERNS_NGRAMS, DATA),
        'NATIONALITY': Matcher(NATIONALITY_PATTERNS_NGRAMS, DATA),
    }
    return result

# main function
def main():
    print(KB_Extractor(TEST_DATA))
    
    
if __name__=='__main__':
    main()


# 
# def RemoveSyncategorematic(text):
#     return re.sub('(\s+)(a|an|and|the|of)(\s+)', ' ', text) 


# def SuggestShortForms(sentense):
#     text = RemoveSyncategorematic(sentense)
#     text = re.sub('\(.+?\)', '', text)
#     regex = [
#         '\W{}\W'.format('.'.join([i[0].upper() for i in text.split(' ') if i])),
#         '{}\W+?{}\W+?'.format(sentense, '\.'.join([i[0].upper() for i in text.split(' ') if i])),
#         '\W{}\W'.format(''.join([i[0].upper() for i in text.split(' ') if i])),
#         '{}\W?\({}\)\W?'.format(sentense, ''.join([i[0].upper() for i in text.split(' ') if i])),
#     ]+[i.replace('(', '').replace(')', '') for i in re.findall('\(.+?\)',re.sub('\(.+?\)', '', sentense) )]
#     return list(set(regex))


# def LooseShortFullMatcher(sentense):
#     regex = []
#     regex.append(re.escape(sentense))
#     regex.append(re.sub('\(.+?\)', '', sentense).replace(' ', '\W?'))
#     [regex.append(i) for i in SuggestShortForms(sentense)]    
#     return '|'.join(["({})".format(i) for i in regex])


# def MatchMiner(patterns, data):
#     result = []
#     regex = '|'.join(LooseShortFullMatcher(i) for i in patterns)
#     print(regex)
#     regex  = re.compile(regex, re.I)
#     for out in regex.findall(data):
#         for x in out:
#             if x:
#                 result.append(x)
#     return result

