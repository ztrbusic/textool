from pathlib import Path
import regex as re
from pypdf import PdfReader
from stdnum.hr import oib

def is_valid_jmbg(candidate_jmbg: str) -> bool:
	jmbg_digits = []
	for d in candidate_jmbg:
		jmbg_digits.append(int(d))
	S = (
	7 * (jmbg_digits[0] + jmbg_digits[6])
	+ 6 * (jmbg_digits[1] + jmbg_digits[7])
	+ 5 * (jmbg_digits[2] + jmbg_digits[8])
	+ 4 * (jmbg_digits[3] + jmbg_digits[9])
	+ 3 * (jmbg_digits[4] + jmbg_digits[10])
	+ 2 * (jmbg_digits[5] + jmbg_digits[11])
	)
	K = 11 - (S % 11)
	if K > 9:
		K = 0
	return K == jmbg_digits[12]

def is_valid_mbo(candidate_mbo: str) -> bool:
	mbo_digits = []
	for d in candidate_mbo:
		mbo_digits.append(int(d))
	S = (
		7 * mbo_digits[0]
		+ 6 * mbo_digits[1]
		+ 5 * mbo_digits[2]
		+ 4 * mbo_digits[3]
		+ 3 * mbo_digits[4]
		+ 2 * mbo_digits[5]
		+ 7 * mbo_digits[6]
		+ 6 * mbo_digits[7]
		)
	K = 11 - (S % 11)
	if K == 11:
		K = 0
	if K == 10:
		return False
	return K == mbo_digits[8]

def scan_pii(path: Path) -> dict:
# TXT and PDF - reading the file
	try:
		if path.suffix.lower() in [".txt"]:
			try:
				with path.open("r", encoding="utf-8") as f:
					text = f.read()
			except UnicodeDecodeError:
				with path.open("r", encoding="latin-1") as f:
					text = f.read()
		else:
			reader = PdfReader(str(path))
			text = ""
			for page in reader.pages:
				text += page.extract_text()

# OIB  - extraction and validation
		candidates_oib = re.findall(r"\d{11}", text)
		valid_oibs = []
		for c in candidates_oib:
			if oib.is_valid(c):
				valid_oibs.append(c)

# JMBG - extraction and validation
		candidates_jmbg = re.findall(r"\d{13}", text)
		valid_jmbgs = []
		for c in candidates_jmbg:
			if is_valid_jmbg(c) == True:
				dd = int(c[:2])
				mm = int(c[2:4])
				if 1 <= mm <= 12 and 1 <= dd <= 31:
					valid_jmbgs.append(c)

		return {"file": str(path), "status": "ok", "pii": {"OIBs": valid_oibs, "JMBGs": valid_jmbgs}}

	except Exception as e:
			return {"file": str(path), "status": "error", "message": str(e)}