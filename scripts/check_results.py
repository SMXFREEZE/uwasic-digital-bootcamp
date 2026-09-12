"""Fail CI if Cocotb reports failures or produces no test cases"""
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
cases = root.findall(".//testcase")
failed = [case for case in cases if case.find("failure") is not None or case.find("error") is not None]
if not cases or failed:
    raise SystemExit(f"Failed verification: {len(cases)} tests and {len(failed)} failures")
print(f"Passed {len(cases)} tests")
