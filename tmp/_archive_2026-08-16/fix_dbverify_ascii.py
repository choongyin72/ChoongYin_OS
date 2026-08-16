import io

f = r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/libraries/DbVerify.py"
text = io.open(f, encoding="utf-8").read()
orig = text
text = text.replace("\u2014", " - ")
text = text.replace("  -  ", " - ")
if text != orig:
    io.open(f, "w", encoding="utf-8").write(text)
    print("fixed")
else:
    print("no change")
