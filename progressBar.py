    def runprogress():
        testlist = ["one","two","three","four","five"]
        progress = 100/len(testlist)
        for i,c in zip(testlist, range(len(testlist))):
            print i
            time.sleep(5)
            tb1.setValue((c+1)*progress)
        tb1.setValue(100)
    runprogress()
