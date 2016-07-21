sentence = raw_input("Sentence: ")

screen_width = 80
text_width = len(sentence)
box_width = text_width+6
left_marge = (screen_width-box_width)//2

print
print ' ' * left_marge + '+'  + '-' * (box_width-2) +  '+'
print ' ' * left_marge + '| ' + ' ' * text_width    + '   |'
print ' ' * left_marge + '| ' + ' ' + sentence      + '  |'
print ' ' * left_marge + '| ' + ' ' * text_width    + '   |'
print ' ' * left_marge + '+'  + '-' * (box_width-2) +  '+'
