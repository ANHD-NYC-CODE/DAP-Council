"""
Functions to standardize address strings
in HPD contacts data
"""
import re

STREETS = [
    (r'(?<= )AVE(NUE)?$', 'AVENUE'),
    (r'(?<= )(STREET|STR|(ST\.?))', 'STREET'),
    (r'(?<= )PL(ACE)?$', 'PLACE'),  # plaza / place?
    (r'(?<= )(ROAD|(?<!\d)RD\.?)', 'ROAD'),
    (r'(?<= )(LA(NE)?|LN)', 'LANE'),
    (r'(?<= )CT|CRT', 'COURT'),
    (r'(?<= )DR(IVE)?$', 'DRIVE'),
    (r'(?<= )(BOULEVARD|BLVD)', 'BOULEVARD'),
    (r'(?<= )(PKWY|PARKWY)', 'PARKWAY'),
    (r'(?<= )PK$', 'PARK'),
    (r'(?<= )BCH$', 'BEACH'),
    (r'(?<= )TERR(ACE)?$', 'TERRACE'),
    (r'(^|(?<= ))(BDWAY|BDWY|BROAD WAY)', 'BROADWAY')
]


# Look for direction abbrivation as the start of the string or a space, but NOT 'AVENUE '
# this is to avoid lettered avenues such as "AVENUE W"
DIR_START = "(^|(?<=[ ]))(?<!AVENUE )"
DIR_END = "((?=[ ])|$)"


def dir_regex(x): return DIR_START + x + DIR_END


DIRECTIONS = [
    (dir_regex(r'N\.?'), 'NORTH'),
    (dir_regex(r'SO?\.?'), 'SOUTH'),
    (dir_regex(r'E\.?'), 'EAST'),
    (dir_regex(r'W\.?'), 'WEST')
]

ALIASES = [
    ('ADAM CLAYTON POWELL( JR)?( (BLVD|BOULEVARD))?', 'ADAM CLAYTON POWELL JR BOULEVARD'),
    ('AVENUE OF( THE)? AMERICAS', 'AVENUE OF THE AMERICAS'),
    (r'COLLEGE PT\.? (BLVD|BOULEVARD)', 'COLLEGE POINT BOULEVARD'),
    ('CO-OP CITY', 'COOP CITY')
]

REMOVE = [
    ('(BKLYN|BROOKLYN|QUEENS|BRONX|MANHATTAN|NEW YORK|NYC|SI)$', ''),
    ('(BENSONHURST|CORONA)$', ''),
    (r'\(.+\)$', '')
]

REGEX_REPLACEMENTS = STREETS + DIRECTIONS + REMOVE

# Str, Str -> Lambda


def number_to_text(number):
    if number == '1':
        suffix = 'ST'
    elif number == '2':
        suffix = 'ND'
    elif number == '3':
        suffix = 'RD'
    elif number == '11':
        suffix = 'TH'
    elif number == '12':
        suffix = 'TH'
    elif number == '13':
        suffix = 'TH'
    elif len(number) == 1:
        suffix = 'TH'
    elif len(number) >= 2 and number[-1:] == '1':
        suffix = 'ST'
    elif len(number) >= 2 and number[-1:] == '2':
        suffix = 'ND'
    elif len(number) >= 2 and number[-1:] == '3':
        suffix = 'RD'
    else:
        suffix = 'TH'

    return number + suffix


def replace_func(pattern, replacement):
    return lambda s: re.sub(pattern, replacement, s)


ALIASES_FUNCS = list(map(lambda x: replace_func(*x), ALIASES))
REGEX_FUNCS = list(map(lambda x: replace_func(*x), REGEX_REPLACEMENTS))

WORD_NUMBERS = ['0TH', '1ST', '2ND', '3RD',
                '4TH', '5TH', '6TH', '7TH',
                '8TH', '9TH', '10TH']
SUFFIXES = {
    '0': 'TH',
    '1': 'ST',
    '2': 'ND',
    '3': 'RD',
    '4': 'TH',
    '5': 'TH',
    '6': 'TH',
    '7': 'TH',
    '8': 'TH',
    '9': 'TH'
}


def format_number(matchobj):
    n = matchobj.group('number')
    rest = matchobj.group('rest')
    if int(n) < 11:
        return WORD_NUMBERS[int(n)] + rest
    else:
        tens_digit = str(n)[-2:-1]

        if tens_digit == '1':
            return str(n) + 'TH' + rest
        else:
            return n + SUFFIXES[n[-1]] + rest


def replace_number(string):
    return re.sub(r"(^|(?<=[ ]))(?P<number>\d+)(TH|ST|ND|RD)?(?P<rest>(\b|[ ]).*)", format_number, string)


HOLY_SAINTS = ['JOSEPH', 'MARKS', 'LAWRENCE', 'JAMES',
               'NICHOLAS', 'HOLLIS', 'JOHNS', "JOHN's"]

SAINTS_REGEX = r"ST\.?[ ](?P<street_name>({}))".format('|'.join(HOLY_SAINTS))


def saints(s):
    def repl(matchobj): return "SAINT " + matchobj.group('street_name')
    return re.sub(SAINTS_REGEX, repl, s)


STREET_FUNCS = ALIASES_FUNCS + [replace_number, saints] + REGEX_FUNCS

# list(of functions), str -> str


def func_chain(funcs, val):
    if len(funcs) == 0:
        return val
    else:
        return func_chain(funcs[1:], funcs[0](val))


def remove_extra_spaces(s):
    return ' '.join([x for x in s.split(' ') if x != ''])


def prepare(s):
    return remove_extra_spaces(s).strip().upper().replace('"', '').replace('-', '')


def normalize_street(street):
    if street is None:
        return None

    s = prepare(street)

    if s == '':
        return None

    return func_chain(STREET_FUNCS, s).replace('.', '').strip()


# remove dashes or spaces...sorry Queens!
def normalize_street_number(number):
    if number is None or number == '':
        return None
    return re.sub(r'(?<=\d)(-|[ ])(?=\d)', '', number).replace('-', '').strip()


APT_STRINGS_TO_REMOVE = ['.', '_', '#', '{', '}', '/']


def clean_apt_str(s):
    s = prepare(s)
    for char_to_remove in APT_STRINGS_TO_REMOVE:
        s = s.replace(char_to_remove, '')
    return s


APT_NUM = r'(?<=\d)(ST|TH|ND|RD)'
# "12F" becomes 12F
# "12TH F" becomes 12FLOOR
EDGE_CASE_FLOOR = APT_NUM + '[ ]F$'
FLOOR_REGEX = r'(?<=\d)[ ]?((FL(OOR|O|R)?)|FW)$'


def normalize_apartment(string):
    if string is None:
        return None

    s = clean_apt_str(string)

    if s == '':
        return None

    s = re.sub(EDGE_CASE_FLOOR, 'FLOOR', s)
    s = re.sub(APT_NUM, '', s)
    s = re.sub(FLOOR_REGEX, 'FLOOR', s)

    return s.replace(' ', '')


def clean_number_and_streets(string):
    # Beach
    string = string.upper().replace("BEAC H", 'BEACH')
    string = string.upper().replace("BEA CH", 'BEACH')
    string = string.upper().replace("BE ACH", 'BEACH')
    string = string.upper().replace("B EACH", 'BEACH')

    # Street
    string = string.upper().replace("STREE T", 'STREET')
    string = string.upper().replace("STR EET", 'STREET')
    string = string.upper().replace("ST REET", 'STREET')
    string = string.upper().replace("STRE ET", 'STREET')
    string = string.upper().replace("S TREET", 'STREET')
    string = string.upper().replace("STREE", "STREET")
    string = string.upper().replace("STR ", "STREET")

    # PLACE
    string = string.upper().replace("PLAC E", 'PLACE')
    string = string.upper().replace("PLA CE", 'PLACE')
    string = string.upper().replace("PL ACE", 'PLACE')
    string = string.upper().replace("P LACE", 'PLACE')

    # ROAD
    string = string.upper().replace("ROA D", 'ROAD')
    string = string.upper().replace("RO AD", 'ROAD')
    string = string.upper().replace("R OAD", 'ROAD')

    # AVENUE
    string = string.upper().replace("AVENU E", 'AVENUE')
    string = string.upper().replace("AVEN UE", 'AVENUE')
    string = string.upper().replace("AVE NUE", 'AVENUE')
    string = string.upper().replace("AV ENUE", 'AVENUE')
    string = string.upper().replace("A VENUE", 'AVENUE')
    string = string.upper().replace("AVNUE", 'AVENUE')
    string = string.upper().replace("AVENU", 'AVENUE')
    string = string.upper().replace("AVENE", 'AVENUE')
    string = string.upper().replace("AVNEUE", 'AVENUE')

    # PARKWAY
    string = string.upper().replace("P ARKWAY", 'PARKWAY')
    string = string.upper().replace("PA RKWAY", 'PARKWAY')
    string = string.upper().replace("PAR KWAY", 'PARKWAY')
    string = string.upper().replace("PARK WAY", 'PARKWAY')
    string = string.upper().replace("PARKWA Y", 'PARKWAY')
    string = string.upper().replace("PARKWA", 'PARKWAY')
    string = string.upper().replace("PARKWAYY", 'PARKWAY')
    string = string.upper().replace("PKW Y", "PARKWAY")

    # EXPRESSWAY
    string = string.upper().replace("EXP RESSWAY", "EXPRESSWAY")

    # HIGHWAY
    string = string.upper().replace("HWY", 'HIGHWAY')
    # NORTH
    string = string.upper().replace("N ORTH", 'NORTH')
    string = string.upper().replace("NOR TH", 'NORTH')
    # SOUTH
    string = string.upper().replace("SOUT H", 'SOUTH')
    string = string.upper().replace("S OUTH", 'SOUTH')
    string = string.upper().replace("SOU TH", 'SOUTH')
    # BOULEVARD
    string = string.upper().replace("BOULEVAR D", 'BOULEVARD')
    string = string.upper().replace("BOULEVA RD", 'BOULEVARD')
    string = string.upper().replace("BOULEV ARD", 'BOULEVARD')
    string = string.upper().replace("BOULE VARD", 'BOULEVARD')
    string = string.upper().replace("BOUL EVARD", 'BOULEVARD')
    string = string.upper().replace("BOU LEVARD", 'BOULEVARD')
    string = string.upper().replace("B OULEVARD", 'BOULEVARD')
    string = string.upper().replace("BOUELEVARD", 'BOULEVARD')
    string = string.upper().replace("BOULEV ", 'BOULEVARD')

    # BLVD
    string = string.upper().replace("BLVD", 'BOULEVARD')
    string = string.upper().replace("BLV D", 'BOULEVARD')
    string = string.upper().replace("BL VD", 'BOULEVARD')
    string = string.upper().replace("B LVD", 'BOULEVARD')

    # TERRACE
    string = string.upper().replace("TERRAC E", 'TERRACE')
    string = string.upper().replace("TERRA CE", 'TERRACE')
    string = string.upper().replace("TERR ACE", 'TERRACE')
    string = string.upper().replace("TER RACE", 'TERRACE')
    string = string.upper().replace("TE RRACE", 'TERRACE')
    string = string.upper().replace("T ERRACE", 'TERRACE')

    # CONCOURSE

    string = string.upper().replace("CONC OURSE", "CONCOURSE")

    # remove double space
    string = string.upper().replace("  ", " ")
    string = string.upper().replace("   ", " ")
    string = string.upper().replace("    ", " ")
    string = string.upper().replace("     ", " ")

    # rmove +
    string = string.upper().replace("+", '')

    # remove all periods
    string = string.upper().replace('.', '')

    # remove space dash space
    string = string.upper().replace(' - ', ' ')

    # other typos
    string = re.sub(r"\bP OLITE\b", "POLITE", string)
    string = re.sub(r"\bDEREIMER\b", "DE REIMER", string)
    string = re.sub(r"\bBAYRIDGE\b", "BAY RIDGE", string)
    string = re.sub(r"\bAVESOUTH\b", "AVE SOUTH", string)
    string = re.sub(r"\bPARKHILL\b", "PARK HILL", string)
    string = re.sub(r"\bSTJOHNS\b", "SAINT JOHNS", string)
    string = re.sub(r"\bSTMARKS\b", "SAINT MARKS", string)
    string = re.sub(r"\bSTNICHOLAS\b", "SAINT NICHOLAS", string)
    string = re.sub(r"\bSTPAULS\b", "SAINT PAULS", string)
    string = re.sub(r"\bSTLAWRENCE\b", "SAINT LAWRENCE", string)
    string = re.sub(r"\bWILLIAMSBRID GE\b", "WILLIAMSBRIDGE", string)
    string = re.sub(r"\bATLANT IC\b", "ATLANTIC", string)
    string = re.sub(r"\bWTREMONT\b", "WEST TREMONT", string)
    string = re.sub(r"\bREVERAND\b", "REV", string)
    string = re.sub(r"\bPENNSYLVAN IA\b", "PENNSYLVANIA", string)
    string = re.sub(r"\bRID GE\b", "RIDGE", string)
    string = re.sub(r"\bHARDIN G\b", "HARDING", string)
    string = re.sub(r"\bCHESTNU T\b", "CHESTNU T", string)
    string = re.sub(r"\bFRANCIS LEWI S\b", "FRANCIS LEWIS", string)
    string = re.sub(r"\bWASHINGTO\b", "WASHINGTON", string)
    string = re.sub(r"\bPARK WE ST\b", "PARK WEST", string)
    string = re.sub(r"\bTHOMAS SBOYLAND\b", "THOMAS SOUTH BOYLAND", string)
    string = re.sub(r"\bPAEDERGAT\b", "PAERDEGAT", string)
    string = re.sub(r"\bVALENTI NE\b", "VALENTINE", string)
    string = re.sub(r"\bSOUTHE RN\b", "SOUTHERN", string)

    # Replace Street Appreviations
    HOLY_SAINTS = ['JOSEPH', 'MARKS', 'LAWRENCE', 'JAMES',
                   'NICHOLAS', 'HOLLIS', 'JOHNS', "JOHN's", "EDWARDS", "GEORGES"]

    # replace ST MARKS etc with SAINT MARKS
    for saint in HOLY_SAINTS:
        string = re.sub(r"(?=.*ST {})(\bST {}\b)".format(saint, saint), "SAINT {}".format(saint), string)

    string = re.sub(r"\bFT\b", "FORT", string)
    string = re.sub(r"\bRV\b", "RIVER", string)
    string = re.sub(r"\bCT\b", "COURT", string)
    string = re.sub(r"\bTER\b", "TERRACE", string)
    string = re.sub(r"\bLN\b", "LANE", string)
    string = re.sub(r"\bPL\b", "PLACE", string)
    string = re.sub(r"\bDR\b", "DRIVE", string)
    string = re.sub(r"\bRD\b", "ROAD", string)
    string = re.sub(r"\bAV\b", "AVENUE", string)
    string = re.sub(r"\bAVE\b", "AVENUE", string)
    string = re.sub(r"\bBLVD\b", "BOULEVARD", string)
    string = re.sub(r"\bBDWAY\b", "BROADWAY", string)
    string = re.sub(r"\bBDWY\b", "BROADWAY", string)
    string = re.sub(r"\bPKWY\b", "PARKWAY", string)
    string = re.sub(r"\bPKWAY\b", "PARKWAY", string)
    string = re.sub(r"\bEXPWY\b", "EXPRESSWAY", string)
    string = re.sub(r"\bEXP WY\b", "EXPRESSWAY", string)
    string = re.sub(r"\bEXPR ESSWAY\b", "EXPRESSWAY", string)

    string = re.sub(r"(?!{})(?=\bST\b)(\bST\b)".format(
        ".*" + saint + "|" for saint in HOLY_SAINTS), "STREET", string)

    # Join MAC DOUGAL and others into MACDOUGAL

    string = re.sub(r"(\bMAC \b)", r"MAC", string)
    string = re.sub(r"(\bMC \b)", r"MC", string)

    # replace THIRD and similar with 3rd
    string = re.sub(r"\bFIRST\b", "1ST", string)
    string = re.sub(r"\bSECOND\b", "2ND", string)
    string = re.sub(r"\bTHIRD\b", "3RD", string)
    string = re.sub(r"\bFOURTH\b", "4TH", string)
    string = re.sub(r"\bFIFTH\b", "5TH", string)
    string = re.sub(r"\bSIXTH\b", "6TH", string)
    string = re.sub(r"\bSEVENTH\b", "7TH", string)
    string = re.sub(r"\bEIGHTH\b", "8TH", string)
    string = re.sub(r"\bNINTH\b", "9TH", string)
    string = re.sub(r"\bTENTH\b", "10TH", string)
    string = re.sub(r"\bELEVENTH\b", "11TH", string)
    string = re.sub(r"\bTWELTH\b", "12TH", string)

    # Replace Compass appreviations
    string = re.sub(r"\bN\b", "NORTH", string)
    string = re.sub(r"\bE\b", "EAST", string)
    string = re.sub(r"\bS\b", "SOUTH", string)
    string = re.sub(r"\bW\b", "WEST", string)

    # replace 143 street with 143rd st
    match = re.search(r"(?<!^)(?=\s\d+ (STREET|AVENUE))( \d+ (STREET|AVENUE))", string)
    if match:
        original = match.group().strip()
        number, rest = original.split(' ', 1)
        match = " ".join([number_to_text(number), rest])
        string = string.upper().replace(original, match)

    # remove dashes from street-names-with-dashes (but not 12-14 number dashes)
    string = re.sub(r"(?=[a-zA-Z]*\-[a-zA-Z])\-", " ", string)
    return string
