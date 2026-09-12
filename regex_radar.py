#!/usr/bin/env python3
"""
regex-radar: Visual regex pattern tester and cheat-sheet reference CLI.
"""
import argparse, re, sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass

__version__ = "1.0.0"

CHEAT_SHEET = {
    "\d": "Any digit [0-9]",
    "\w": "Any word character [a-zA-Z0-9_]",
    "\s": "Any whitespace character",
    "^": "Start of string / line",
    "$": "End of string / line",
    "+": "1 or more occurrences",
    "*": "0 or more occurrences",
    "?": "0 or 1 occurrence (optional)",
    "{n,m}": "Between n and m times",
    "(?i)": "Case-insensitive flag",
    "(?<=...)": "Positive lookbehind"
}

def test_regex(pattern, text, replace=None):
    try:
        compiled = re.compile(pattern)
        matches = list(compiled.finditer(text))
        result = {
            "valid": True,
            "match_count": len(matches),
            "matches": [{"span": m.span(), "match": m.group(0), "groups": m.groups()} for m in matches]
        }
        if replace is not None:
            result["replaced"] = compiled.sub(replace, text)
        return result
    except re.error as e:
        return {"valid": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="🎯 regex-radar: Visual Regex Tester & Reference")
    parser.add_argument("--pattern", help="Regular expression pattern")
    parser.add_argument("--text", help="Target input string to match against")
    parser.add_argument("--replace", help="Replacement string")
    parser.add_argument("--cheat-sheet", action="store_true", help="Print regex reference cheat sheet")
    args = parser.parse_args()
    
    if args.cheat_sheet or (not args.pattern and not args.text):
        print("=" * 60)
        print("🎯 REGEX-RADAR CHEAT SHEET REFERENCE")
        print("=" * 60)
        for token, desc in CHEAT_SHEET.items():
            print(f"  {token:<10} ➔ {desc}")
        print("=" * 60)
        if not args.pattern:
            return
            
    res = test_regex(args.pattern, args.text or "Sample text with email user@domain.com and numbers 12345.")
    print("\n" + "=" * 60)
    print("🎯 REGEX MATCHING RESULTS")
    print("=" * 60)
    print(f"Pattern : /{args.pattern}/")
    print(f"Input   : \"{args.text}\"")
    if not res["valid"]:
        print(f"❌ Regex Syntax Error: {res['error']}")
    else:
        print(f"✅ Found {res['match_count']} match(es):")
        for idx, m in enumerate(res["matches"], 1):
            print(f"  [{idx}] '{m['match']}' at index {m['span']}")
            if m["groups"]:
                print(f"      Groups: {m['groups']}")
        if "replaced" in res:
            print(f"🔄 Replaced output: \"{res['replaced']}\"")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
