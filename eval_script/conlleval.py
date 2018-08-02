# coding:utf8
import argparse
import re

import sys

from collections import defaultdict


def startOfChunk(prevTag, tag, prevType, type):
    '''
    用于判断一个单词是不是chunk的开头
    参考：http://www.cnts.ua.ac.be/conll2000/chunking/
    :param prevTag:上一个单词的tag，比如B 或者 I
    :param tag: 这个单词的tag，比如B 或者 I
    :param prevType: 上一个单词的type，比如NP 或者 VP
    :param type: 这个单词的type，比如NP 或者 VP
    :return: bool
    '''
    chunkStart = False
    if prevTag == 'B' and tag == 'B': chunkStart = True
    if prevTag == 'I' and tag == 'B': chunkStart = True
    if prevTag == 'O' and tag == 'B': chunkStart = True
    if prevTag == 'O' and tag == 'I': chunkStart = True

    if prevTag == 'E' and tag == 'E': chunkStart = True
    if prevTag == 'E' and tag == 'I': chunkStart = True
    if prevTag == 'O' and tag == 'E': chunkStart = True
    if prevTag == 'O' and tag == 'I': chunkStart = True

    if tag != 'O' and tag != '.' and prevType != type:
        chunkStart = True

    if tag == '[': chunkStart = True
    if tag == ']': chunkStart = True

    return chunkStart


def endOfChunk(prevTag, tag, prevType, type):
    '''
    用于判断一个单词是不是chunk的结尾
    功能类似startOfChunk函数
    :param prevTag:
    :param tag:
    :param prevType:
    :param type:
    :return:
    '''
    chunkEnd = False
    if  prevTag == 'B' and tag == 'B' : chunkEnd = True
    if  prevTag == 'B' and tag == 'O' : chunkEnd = True
    if  prevTag == 'I' and tag == 'B' : chunkEnd = True
    if  prevTag == 'I' and tag == 'O' : chunkEnd = True

    if  prevTag == 'E' and tag == 'E' : chunkEnd = True
    if  prevTag == 'E' and tag == 'I' : chunkEnd = True
    if  prevTag == 'E' and tag == 'O' : chunkEnd = True
    if  prevTag == 'I' and tag == 'O' : chunkEnd = True

    if prevTag != 'O' and prevTag != '.' and prevType != type:
        chunkEnd = True

    if prevTag == ']': chunkEnd = True
    if prevTag == '[': chunkEnd = True

    return chunkEnd


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='r',
                        help='Assume raw output tokens, that is without the prefixes B- and I-. In this case each word will be counted as one chunk.',
                        action='store_true'
                        )
    parser.add_argument('-l', dest='l',
                        help='Generate output as part of a LaTeX table.',
                        action='store_true'
                        )
    parser.add_argument('-d', dest='d',
                        help='On each line, use char rather than whitespace as delimiter between tokens.',
                        metavar='char',
                        )
    parser.add_argument('-o', dest='o',
                        help='Use token as output tag for items that are outside of chunks or other classes. This option only works when -r is used as well. The default value for the outside output tag is O.',
                        metavar='token',
                        )
    return parser

boundary = "-*-"
boundary_b = "BOS"  # sentence boundary
boundary_e = "EOS"  # snetence boundary
# my $correct;              # current corpus chunk tag (I,O,B)
correctChunk = 0  # number of correctly identified chunks
correctTags = 0  # number of correct chunk tags
# my $correctType;          # type of current corpus chunk tag (NP,VP,etc.)
delimiter = ' '  # field delimiter
FB1 = 0.0  # FB1 score (Van Rijsbergen 1979)
# my $firstItem;            # first feature (for sentence boundary checks)
foundCorrect = 0  # number of chunks in corpus
foundGuessed = 0  # number of identified chunks
# my $guessed;              # current guessed chunk tag
# my $guessedType;          # type of current guessed chunk tag
# my $i;                    # miscellaneous counter
inCorrect = False  # currently processed chunk is correct until now
lastCorrect = 'O'  # previous chunk tag in corpus
latex = False  # generate LaTeX formatted output
lastCorrectType = ''  # type of previously identified chunk tag
lastGuessed = 'O'  # previously identified chunk tag
lastGuessedType = ''  # type of previous chunk tag in corpus
# my $lastType;             # temporary storage for detecting duplicates
# my $line;                 # line
nbrOfFeatures = -1  # number of features per line
precision = 0.0  # precision score
oTag = "O"  # outside tag, default O
raw = False  # raw input: add B to every token
recall = 0.0  # recall score
tokenCounter = 0  # token counter (ignores sentence breaks)
#
correctChunk_dict = defaultdict(lambda: 0)  # number of correctly identified chunks per type
foundCorrect_dict = defaultdict(lambda: 0)  # number of chunks in corpus per type
foundGuessed_dict = defaultdict(lambda: 0)  # number of identified chunks per type
#
# my @features;             # features on line
# my @sortedTypes;          # sorted list of chunk type names


# sanity check
parser = build_parser()
options = parser.parse_args()

if options.l: latex = True
if options.r: raw = True
if options.d is not None: delimiter = options.d
if options.o is not None: oTag = options.o

# process input
for line in sys.stdin:
    if line == '\n': continue

    features = line[:-1].split(delimiter)

    if nbrOfFeatures < 0:
        nbrOfFeatures = len(features) - 1
    elif nbrOfFeatures != len(features) - 1 and len(features) != 0:
        print 'unexpected number of features: {} ({})\n'.format(len(features), nbrOfFeatures + 1),
        sys.exit(1)

    if len(features) == 0 or features[0] == boundary_b or features[0] == boundary_e:
        features = [boundary, 'O', 'O']

    if len(features) < 2:
        sys.exit('conlleval: unexpected number of features in line %s\n' % (line))

    if raw:
        if features[-1] == oTag: features[-1] = 'O'
        if features[-2] == oTag: features[-2] = 'O'
        if features[-1] != 'O':
            features[-1] = 'B-' + features[-1]
        if features[-2] != 'O':
            features[-2] = 'B-' + features[-2]

    pattern = re.compile(r'^([^-]*)-(.*)$')
    if pattern.match(features[-1]):
        guessed, guessedType = pattern.match(features[-1]).groups()
    else:
        guessed, guessedType = features[-1], ''

    features.pop()

    if pattern.match(features[-1]):
        correct, correctType = pattern.match(features[-1]).groups()
    else:
        correct, correctType = features[-1], ''

    features.pop()

    guessedType = guessedType if guessedType else ''
    correctType = correctType if correctType else ''
    firstItem = features.pop(0)

    if firstItem == boundary: guessed = 'O'

    if inCorrect:
        if endOfChunk(lastCorrect, correct, lastCorrectType, correctType) and \
                endOfChunk(lastGuessed, guessed, lastCorrectType, guessedType) and \
                        lastGuessedType == lastCorrectType:
            inCorrect = False
            correctChunk += 1
            correctChunk_dict[lastCorrectType] = correctChunk_dict[lastCorrectType] + 1 if correctChunk_dict[
                lastCorrectType] else 1

        elif endOfChunk(lastCorrect, correct, lastCorrectType, correctType) != \
                endOfChunk(lastGuessed, guessed, lastGuessedType, guessedType) or \
                        guessedType != correctType:

            inCorrect = False

    if startOfChunk(lastCorrect, correct, lastCorrectType, correctType) and \
            startOfChunk(lastGuessed, guessed, lastGuessedType, guessedType) and \
                    guessedType == correctType:
        inCorrect = True

    if startOfChunk(lastCorrect, correct, lastCorrectType, correctType):
        foundCorrect += 1
        foundCorrect_dict[correctType] = foundCorrect_dict[correctType] + 1 if foundCorrect_dict[correctType] else 1

    if startOfChunk(lastGuessed, guessed, lastGuessedType, guessedType):
        foundGuessed += 1
        foundGuessed_dict[guessedType] = foundGuessed_dict[guessedType] + 1 if foundGuessed_dict[guessedType] else 1

    if firstItem != boundary:
        if correct == guessed and guessedType == correctType:
            correctTags += 1
        tokenCounter += 1

    lastGuessed = guessed
    lastCorrect = correct
    lastGuessedType = guessedType
    lastCorrectType = correctType

if inCorrect:
    correctChunk += 1
    correctChunk_dict[lastCorrectType] = correctChunk_dict[lastCorrectType] + 1 if correctChunk_dict[
        lastCorrectType] else 1

if not latex:
    # compute overall precision, recall and FB1 (default values are 0.0)
    if foundGuessed > 0: precision = 100 * float(correctChunk) / foundGuessed
    if foundCorrect > 0: recall = 100 * float(correctChunk) / foundCorrect
    if precision + recall > 0: FB1 = 2 * precision * float(recall) / (precision + recall)

    # print overall performance
    print 'processed {} tokens with {} phrases;'.format(tokenCounter, foundCorrect),
    print 'found: {} phrases; correct: {}.\n'.format(foundGuessed, correctChunk),
    if tokenCounter > 0:
        print 'accuracy: %6.2f%%; ' % (100 * float(correctTags) / tokenCounter),
        print '%d %d %d ' % (correctChunk, foundCorrect, foundGuessed),
        print 'precision: %6.2f%%; ' % (precision),
        print 'recall: %6.2f%%; ' % (recall),
        print 'FB1: %6.2f\n' % (FB1),

# sort chunk type names
lastType = None
sortedTypes = []
for i in sorted(foundCorrect_dict.keys() + foundGuessed_dict.keys()):
    if lastType is None or lastType != i:
        sortedTypes.append(i)
    lastType = i

# print performance per chunk type
if (not latex):
    for i in sortedTypes:
        correctChunk_dict[i] = correctChunk_dict[i] if correctChunk_dict[i] else 0

        if not foundGuessed_dict[i]:
            foundGuessed_dict[i] = 0
            precision = 0.0
        else:
            precision = 100 * float(correctChunk_dict[i]) / foundGuessed_dict[i]

        if not foundCorrect_dict[i]:
            recall = 0.0
        else:
            recall = 100 * float(correctChunk_dict[i]) / foundCorrect_dict[i]

        if precision + recall == 0.0:
            FB1 = 0.0
        else:
            FB1 = 2 * float(precision) * recall / (precision + recall)

        print '%17s: ' % (i),
        print '% 4d % 4d % 4d ' % (correctChunk_dict[i], foundCorrect_dict[i], foundGuessed_dict[i]),
        print 'precision: %6.2f%%; ' % (precision),
        print 'recall: %6.2f%%; ' % (recall),
        print 'FB1: %6.2f  %d\n' % (FB1, foundGuessed_dict[i]),

else:
    print "        & Precision &  Recall  & F\$_{\\beta=1} \\\\\\hline",
    for i in sortedTypes:
        correctChunk_dict[i] = correctChunk_dict[i] if correctChunk_dict[i] else 0

        if not foundGuessed_dict[i]:
            precision = 0.0
        else:
            precision = 100 * float(correctChunk_dict[i]) / foundGuessed_dict[i]

        if not foundCorrect_dict[i]:
            recall = 0.0
        else:
            recall = 100 * float(correctChunk_dict[i]) / foundCorrect_dict[i]

        if precision + recall == 0.0:
            FB1 = 0.0
        else:
            FB1 = 2 * float(precision) * recall / (precision + recall)
        print '\n%-7s &  %6.2f\\%% & %6.2f\\%% & %6.2f \\\\' % (i, precision, recall, FB1),

    print '\\hline\n',
    precision = 0.0
    recall = 0
    FB1 = 0.0
    if foundGuessed > 0: precision = 100 * float(correctChunk) / foundGuessed
    if foundCorrect > 0: recall = 100 * float(correctChunk) / foundCorrect
    if precision + recall > 0: FB1 = 2 * float(precision) * recall / (precision + recall)

    print "Overall &  %6.2f\\%% & %6.2f\\%% & %6.2f \\\\\\hline\n" % (precision, recall, FB1),
