"""Use nbconvert to generate pdfs of an assignment.
    
"""

import os
import shutil
import pwd
import argparse
import stat

import nbformat as nbf

findex = open('./docs/index.html','w')

opener = """
<!DOCTYPE html>
<html>
<head></head>
<body><p>ES103 Spring 2021 Materials</p>

"""

closer = """
</body>
</html>
"""

findex.write(opener)

alphabet = "._ !0123456789MWFABCDEGHIJKLMNOPQRSTUVXYZabcdefghijklmnopqrstuvwxyz"


def set_permissions(path, uid, gid):
    os.chown(path, uid, gid)
    if os.path.isdir(path):
        os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IXUSR | stat.S_IXGRP)
    else:
        os.chmod(path, stat.S_IRUSR | stat.S_IRGRP)


def main():
    source_dir = os.path.abspath(".")
    docdir = os.path.relpath("./docs")
    for root, dirs, files in os.walk(source_dir):
        dirs.sort(key=lambda word: [alphabet.index(c) for c in word])
        for file in files:
            rel_dir = os.path.relpath(root, source_dir)
            if file.endswith(".ipynb") and not "checkpoint" in file :
                # print(rel_dir,file)
                dst = os.path.join(docdir,rel_dir)
                convertcmdpre = "jupyter nbconvert "+" --to html --output-dir "+dst+" "+os.path.join(rel_dir,file)
                #convertcmdpre = "jupyter nbconvert  "+dst+"/*.ipynb"+" --to webpdf --output-dir "+dst

                #print (convertcmdpre)
                os.system(convertcmdpre)
                link = "<a href="+str(os.path.join(rel_dir,file[0:-5]+"html"))+">"+file[0:-6]+"</a>"
                findex.write("<p>\r\n")
                findex.write(link+"\r\n")
                findex.write("</p>\r\n")

    findex.write(closer)
    findex.close()

                


if __name__ == "__main__":
    main()
