import os

def read_fp_lib_table():
  fr = open(os.path.expanduser("~/fp-lib-table"), "r")
  d = fr.read()
  fr.close()

  d = d[d.find("(fp_lib_table") + len("(fp_lib_table"):]

  d = d.strip()
  libs = []
  while d.find("(lib") > -1:
    d = d[d.find("(lib") + 4:].strip()

    lib = {}
    while True:
      tok, d = d.split(")", 1)
      if tok == "":
        break

      tok = tok.strip("(")
      key, val = tok.split(None, 1)

      lib[key] = val

    libs.append(lib)

  return libs

def write_fp_lib_table(libs):
  fw = open(os.path.expanduser("~/fp-lib-table"), "w")

  fw.write("(fp_lib_table\n")

  for lib in libs:
    fw.write("  (lib (name %s)(type %s)(uri %s)(options %s)(descr %s))\n" % (lib['name'], lib['type'], lib['uri'], lib['options'], lib['descr']))

  fw.write(")\n")

  fw.close()

if __name__ == "__main__":

  libs = read_fp_lib_table()

  write_fp_lib_table(libs)

