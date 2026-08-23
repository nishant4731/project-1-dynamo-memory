import re
p = "/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate/adversary.sh"
s = open(p).read()
start = s.index('case_run "report pretty-printed instead of canonical"')
end = s.index('case_run "supplied plumbing edited by the agent"')
new = '''# The agent renders the report itself, pretty-printed, instead of using the
# read-only plumbing.  The old form sed-ed a separators= call that now lives in
# dragnet_io.py, so it patched nothing and always read reward 1.
case_run "agent renders its own pretty-printed report" '
  python3 /patch/pretty.py && python3 /app/dragnet_restitch.py /app/data/dragnet'
'''
open(p, "w").write(s[:start] + new + s[end:])

# the mutation, kept in its own file so no shell quoting is involved
open("/Users/utkarsha/Documents/Project 1/.cache/dragnet-gate/pretty.py", "w").write(
    's = open("/solution/dragnet_restitch.py").read()\n'
    'new = (\'import json as _json\\n\'\n'
    '       \'def render_report(report):\\n\'\n'
    '       \'    return (_json.dumps(report, sort_keys=True, indent=2) + "\\\\n").encode("ascii")\')\n'
    'out = s.replace("render_report = dragnet_io.render_report", new)\n'
    'assert out != s, "anchor missing"\n'
    'open("/app/dragnet_restitch.py", "w").write(out)\n')
print("patched")
