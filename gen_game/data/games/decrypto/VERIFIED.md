# Verification of decrypto

## Every model call, in order

| n | step | model | seconds | sent | reply | |
|---|---|---|---|---|---|---|
| 01 | design | claude-opus-5-5 | 60.4 | 975 chars | 10979 chars |  |
| 02 | critic | claude-opus-5-5 | 51.7 | 4518 chars | 6597 chars |  |
| 03 | design | claude-opus-5-5 | 60.8 | 9673 chars | 12325 chars |  |
| 04 | critic | claude-opus-5-5 | 43.7 | 5689 chars | 4900 chars |  |
| 05 | spec | claude-opus-5-5 | 77.5 | 4693 chars | 16362 chars |  |
| 06 | scenarios | claude-opus-5-5 | 61.1 | 19100 chars | 8432 chars |  |
| 07 | scenarios | claude-opus-5-5 | 41.2 | 29581 chars | 9400 chars |  |
| 08 | coder | claude-opus-5-5 | 120.8 | 34900 chars | 28491 chars |  |
| 09 | coder | claude-opus-5-5 | 85.3 | 59422 chars | 31858 chars |  |
| 10 | coder | claude-opus-5-5 | 85.1 | 59907 chars | 31767 chars |  |
| 11 | coder | claude-opus-5-5 | 100.2 | 59440 chars | 31261 chars |  |
| 12 | coder | claude-opus-5-5 | 106.1 | 60223 chars | 32664 chars |  |
| 13 | triage | claude-opus-5-5 | 18.1 | 14412 chars | 1575 chars |  |
| 14 | coder | claude-opus-5-5 | 151.9 | 36011 chars | 32002 chars |  |
| 15 | coder | claude-opus-5-5 | 86.8 | 61018 chars | 31817 chars |  |
| 16 | coder | rl-muse-spark-1-3-sglang-playground | 99.6 | 60533 chars | 31265 chars |  |
| 17 | coder | claude-opus-5-5 | 290.0 | 60551 chars | 24901 chars |  |
| 18 | coder | claude-opus-5-5 | 81.0 | 61342 chars | 24789 chars |  |
| 19 | triage | claude-opus-5-5 | 12.5 | 16186 chars | 1300 chars |  |
| 20 | coder | claude-opus-5-5 | 117.3 | 35818 chars | 31834 chars |  |
| 21 | coder | claude-opus-5-5 | 97.1 | 60340 chars | 32773 chars |  |
| 22 | coder | claude-opus-5-5 | 139.0 | 61105 chars | 32522 chars |  |
| 23 | coder | claude-opus-5-5 | 112.8 | 60358 chars | 32335 chars |  |
| 24 | coder | claude-opus-5-5 | 126.3 | 61129 chars | 33546 chars |  |
| 25 | triage | claude-opus-5-5 | 13.1 | 8501 chars | 1389 chars |  |
| 26 | scenarios | claude-opus-5-5 | 69.1 | 20016 chars | 10587 chars |  |
| 27 | scenarios | claude-opus-5-5 | 50.6 | 32169 chars | 11432 chars |  |
| 28 | triage | claude-opus-5-5 | 14.0 | 6500 chars | 1427 chars |  |
| 29 | design | claude-opus-5-5 | 88.5 | 2596 chars | 11677 chars |  |
| 30 | critic | claude-opus-5-5 | 61.7 | 4094 chars | 5518 chars |  |
| 31 | spec | claude-opus-5-5 | 65.1 | 3099 chars | 16840 chars |  |
| 32 | scenarios | claude-opus-5-5 | 61.9 | 20049 chars | 10100 chars |  |
| 33 | coder | claude-opus-5-5 | 120.4 | 34588 chars | 34917 chars |  |
| 34 | coder | claude-opus-5-5 | 101.7 | 59601 chars | 35088 chars |  |
| 35 | coder | claude-opus-5-5 | 116.1 | 59086 chars | 35944 chars |  |
| 36 | coder | claude-opus-5-5 | 98.6 | 59263 chars | 35784 chars |  |
| 37 | triage | claude-opus-5-5 | 9.5 | 5641 chars | 1330 chars |  |
| 38 | design | claude-opus-5-5 | 67.7 | 2547 chars | 11860 chars |  |
| 39 | critic | claude-opus-5-5 | 53.7 | 4762 chars | 6597 chars |  |
| 40 | design | claude-opus-5-5 | 61.0 | 7564 chars | 13283 chars |  |
| 41 | critic | claude-opus-5-5 | 48.9 | 5678 chars | 6278 chars |  |
| 42 | spec | claude-opus-5-5 | 70.4 | 4683 chars | 15961 chars |  |
| 43 | scenarios | claude-opus-5-5 | 65.6 | 18305 chars | 7722 chars |  |
| 44 | coder | claude-opus-5-5 | 113.4 | 35721 chars | 31869 chars |  |
| 45 | coder | claude-opus-5-5 | 94.9 | 60219 chars | 32433 chars |  |
| 46 | coder | claude-opus-5-5 | 86.2 | 60210 chars | 32272 chars |  |
| 47 | coder | claude-opus-5-5 | 102.4 | 61206 chars | 32056 chars |  |
| 48 | coder | claude-opus-5-5 | 89.3 | 60219 chars | 32540 chars |  |
| 49 | triage | claude-opus-5-5 | 11.6 | 9024 chars | 1259 chars |  |

## The prompt the coder was given

- `CODER_PROMPT.md`: sha256 2e5d13c04d5e9947, 35721 chars. MATCHES call 44: this is exactly what was sent.
- the coder was called 24 time(s); the last was call 48

