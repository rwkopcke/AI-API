import environ as env


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
cand_headers = env.GUB_REPORT_HEADERS

#input_addr = env.GUB_OUTPUT_TO_INPUT_ADDR
input_addr = env.GUB_OUTPUT_FLDR / 'chat_gub_response_2026_03_01.txt'

report_addr = env.GUB_REPORT_ADDR

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def read_file(addr):
    '''
        Separate report into a [str], each str a line of input
            [str], one str for each line of the introduction
            [str], one str for each candidate, combined 
            [str], one str for each line of the Notes
            [str]. one str for each line of the Comment
            [str]. one str for each line of the Suggest
        Input file:
        Blank lines separate these 4 blocks of information
        The 5th blank line ends the file
    '''
    num_blnk_lines = 0
    intro_lns = []
    cand_lns = []
    note_lns = []
    comment_lns = []
    suggest_lns = []

    with open(addr) as in_file:
        while num_blnk_lines < 5:
            line = in_file.readline().strip()
        
            if line:
                match num_blnk_lines:
                    case 0:
                        intro_lns.append(line)
                    case 1:
                        cand_lns.append(line)
                    case 2:
                        note_lns.append(line)
                    case 3:
                        comment_lns.append(line)
                    case 4:
                        suggest_lns.append(line)
            else:
                num_blnk_lines += 1
    return [intro_lns, cand_lns, note_lns, comment_lns, suggest_lns]


def cand_to_lst(line):
    '''
        separate line for each cand into into list of lines
        return candidates [str]; str has 4 fields
            0: name
            1: party
            2: 5 top issues, as a ;-delimited str
            3: web addresses
    '''
    # the first and last entries are empty
    lst1 = [item.strip()
            for item in line.split('|')]
    # splits last item in list1: top 5 from sources for a 2-item sublist
    lst2 = [item.strip()
            for item in lst1[-1].split('. (')]
    # 5-item output list:
    
    # first and last items are blanks
    return [*lst1[:-1], *lst2][1:-1]


def item_to_list(lst, sep):
    '''
    '''
    top_5_lst = lst.split(sep)
    return [
        item.strip() for item in top_5_lst
    ]
            
            
def print_(party, lst, rpt_file):
    '''
        Input [str] has 4 str
            0: name
            1: party
            2: 5 top issues, as a ;-delimited str
            3: web addresses
        skip party [1]
    '''
    with open(rpt_file, "a") as out_rpt:
        out_rpt.writelines(party.upper() + '\n')
        
        for cand in lst:
            out_rpt.writelines('\n' * 2)
            out_rpt.writelines(f'{cand[0]} ({party[0].upper()})\n')
            for item in item_to_list(cand[2], '; '):
                out_rpt.writelines('\t' + item + '\n')
            out_rpt.writelines(cand[3] + '\n')
        out_rpt.writelines('\n' * 3)
        
            
def combine_home_and_source(home, source):
    '''
        ensure that the home address is in the sources
    '''
    # remove leading ( and trailing )"
    src = source[1:-2]
    if not home in source:
        return f'[{home}] {src}'
    return src


def print_list(lns, rpt_file):
    '''
        Intro is a list with one str item
        Split the item lns[0] into senetences
        Print the senstences
    '''
    with open(rpt_file, "a") as out_rpt:
        for sent in lns:
            out_rpt.writelines(sent + '\n')
        out_rpt.writelines('\n')
        out_rpt.writelines('\n')
        
                
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# [line] all _ln
intro_lns, cand_lns, note_lns, comment_lns, suggest_lns = \
    read_file(input_addr)

# ignore first 2 ln of headers
candidates = list(map(cand_to_lst, cand_lns[2:]))

# find set of parties
party_set = {
    cand_lst[1] for cand_lst in candidates
}

print_list(intro_lns, report_addr)

for party in sorted(party_set):
    lst = [cand_lst 
           for cand_lst in candidates 
           if cand_lst[1] == party]

    # sort by last name (2nd word in x[0])
    lst = sorted(lst, 
                 key= lambda x: x[0].split(' ')[1])
    
    print_(party, lst, report_addr)

print_list(note_lns, report_addr)
print_list(comment_lns, report_addr)
print_list(suggest_lns, report_addr)
                