#!/usr/bin/env python
import urllib2, json, os, sys, getopt, shutil
from subprocess import Popen
from fp_lib_table import read_fp_lib_table, write_fp_lib_table

def usage():
  print """Usage: %s <local folder>
  
  Clones/updates all the .pretty repos from the KiCAD github account
  into the specified local folder.

  Options:

    -h, --help    Print this help and exit
    -v, --verbose Print full git output for each repository
    -q, --quiet   Don't print anything at all
    -t, --table   Update/overwrite ~/fp-lib-table for the current user.  The 
                  first run will move fp-lib-table to fp-lib-table-old and 
                  replace it, auto generated rows will have the option
                  "auto=true" added.  Future runs will only update/remove rows
                  marked as auto.  The <local folder> is assumed to be in
                  environment $KISYSMOD, use -a to force absolute paths.
    -a, --absolute
                  The uri for the library will be an absolute path instead of
                  respecting $KISYSMOD.""" % sys.argv[0]

try:
  opts, args = getopt.getopt(sys.argv[1:], "hqvta", ["help", "quiet", "verbose", "table", "absolute"])
except getopt.GetoptError as err:
  print str(err)
  usage()
  sys.exit(-2)

git_output = open("/dev/null", "w")
git_quiet = False
update_table = False
absolute = False
for o, a in opts:
  if o in ("-h", "--help"):
    usage()
    sys.exit(0)
  elif o in ("-v", "--verbose"):
    git_output.close()
    git_output = None
  elif o in ("-q", "--quiet"):
    git_quiet = True
  elif o in ("-a", "--absolute"):
    absolute = True
  elif o in ("-t", "--table"):
    update_table = True
  else:
    print "Unhandled option,", o
    usage()
    sys.exit(-2)

if len(args) < 1:
  try:
    kisysmod = os.environ['KISYSMOD']
  except KeyError:
    print "No local folder specified, and couldn't read KISYSMOD environment variable"
    usage()
    sys.exit(-2)
else:
  kisysmod = args[0]

if not os.path.isdir(kisysmod):
  os.makedirs(kisysmod)

full_list = []
page = 1
while True:
  req = urllib2.Request('https://api.github.com/users/kicad/repos?page=%d' % page)
  req.add_header('Accept', 'application/vnd.github.v3+json')
  req.add_header('User-Agent', 'hairymnstr-kicad-fetcher')

  res = urllib2.urlopen(req)

  repos = json.loads(res.read())

  for repo in repos:
    full_list.append(repo['clone_url'])
  
  if len(repos) < 30:
    break

  page += 1

for repo in full_list:
  repo_name = repo.rsplit('/', 1)[1]
  
  if repo_name.split(".", 1)[1] == "pretty.git":
    if os.path.isdir(os.path.join(kisysmod, repo_name.rstrip(".git"))):
      if not git_quiet:
        print "Pulling repo", repo_name
      pr = Popen(["git", "pull"], cwd=os.path.join(kisysmod, repo_name.rstrip(".git")), stdout=git_output)
      pr.wait()
    else:
      cmd = ["git", "clone", repo]
      if not git_quiet:
        print "Cloning repo", repo_name
      if not git_output == None:
        # verbose mode
        cmd.append("-q")
      pr = Popen(cmd, cwd=kisysmod, stdout=git_output)
      pr.wait()
  else:
    if not git_quiet:
      print "ignore:", repo_name

if update_table:
  if os.path.exists(os.path.expanduser("~/fp-lib-table")):
    libs = read_fp_lib_table()

    found_auto = False
    new_libs = []
    for lib in libs:
      if lib['options'].find("auto=true") > -1:
        found_auto = True
      else:
        # keep all manual entries
        new_libs.append(lib)

    if not found_auto:
      print "No auto update libraries found, (is this a first run?)"
      print "Replacing fp-lib-table, old one will be stored at ~/fp-lib-table-old"

      shutil.copy2(os.path.expanduser("~/fp-lib-table"), os.path.expanduser("~/fp-lib-table-old"))

      # dump the library list
      new_libs = []
  else:
    print "No fp-lib-table found, creating from scratch"
    new_libs = []

  # now add the newly cloned/updated repos to the list
  for repo in full_list:
    if repo.find(".pretty") > -1:
      lib = {}
      lib['name'] = repo.rsplit('/', 1)[1].split(".")[0]
      lib['type'] = u'KiCad'
      if absolute:
        lib['uri'] = os.path.abspath(os.path.join(kisysmod, lib['name'] + ".pretty"))
      else:
        lib['uri'] = "${KISYSMOD}/" + lib['name'] + ".pretty"
      lib['options'] = u'auto=true'
      lib['descr'] = u'""'

      new_libs.append(lib)

  # finally, save the new fp-lib-table
  write_fp_lib_table(new_libs)

