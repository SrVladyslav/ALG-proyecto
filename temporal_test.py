import collections
import re
from spellsuggest import SpellSuggester
from spellsuggest import TrieSpellSuggester
import time

if __name__ == "__main__":
    vocab_file_path = "./corpora/quijote.txt"
    tokenizer = re.compile("\W+")
    with open(vocab_file_path, "r", encoding='utf-8') as fr:
        c = collections.Counter(tokenizer.split(fr.read().lower()))
        if '' in c:
            del c['']
        reversed_c = [(freq, word) for (word,freq) in c.items()]
        sorted_reversed = sorted(reversed_c, reverse=True)
        sorted_vocab = [word for (freq,word) in sorted_reversed]
    
    suggester = SpellSuggester(vocab_file_path)
    trie_suggester = TrieSpellSuggester(vocab_file_path)
    
    for t in [10, 100, 1000, 10000]:
        print("Size " + str(t))
        testVoc = sorted([sorted_vocab[i] for i in range(0,t)])
        suggester.changeVocabulary(testVoc)
        trie_suggester.changeVocabulary(testVoc)
        
        funcs = ["levenshtein", "restricted", "intermediate"]
        for f in range(0, len(funcs)):
            print("\tFunction: " + funcs[f])
            totalT = 0.0
            for w in testVoc:
                startT = time.process_time()
                res = suggester.suggest(w, funcs[f], 4)
                endT = time.process_time()
                totalT += endT - startT
            totalT /= len(w)
            print("\t\t Normal version: t = " + str(totalT))
            totalT = 0.0
            for w in testVoc:
                startT = time.process_time()
                res = trie_suggester.suggest(w, funcs[f], 4)
                endT = time.process_time()
                totalT += endT - startT
            totalT /= len(w)
            print("\t\t Trie version: t = " + str(totalT))
        
