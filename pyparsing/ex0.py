from pyparsing import Word, StringEnd, alphas

noEnd = Word(alphas)
print(noEnd.parseString('Dorking...'))

withEnd = Word(alphas) + StringEnd()
print(withEnd.parseString('Dorking...'))
