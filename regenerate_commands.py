import re


inpath = "commands/commands_TCP.txt"
outpath = "commands.txt"
pat = re.compile(r'^\s*\d+\s*:\s*')
systemName = 'TCP'
with open(inpath, "r") as inf, open(outpath, "w") as outf:
    for line in inf:
        s = line.strip()
        if not s:
            continue
        s = pat.sub("", s)                # remove leading "N :"
        parts = s.split()
        if len(parts) < 4:
            continue
        seed = parts[2]                   # third token after header removal
        trail = parts[-2]                 # second to last
        walk = parts[-1]                  # last
        outf.write(f"python3 Run_SAT_afterEDSMallRed.py {seed} result_BiasedAllRedSAT {systemName} {trail} {walk}\n")
