import os

def p():
    for root, dirs, files in os.walk('.'):
        print("**@", root, dirs, files)
        return files
        
print(p())