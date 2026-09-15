# Problem and tests are good quality (AI, up to 1 min)

Failed

Summary: Tests need to change to cover the described behavior; problem description is fine.

1. No Test Leakage [OK]: Problem description does not mention or depend on test files or logic from the patch; the Test assumptions properly declare minimal required interfaces.

2. Tests Cover Required Behavior [ERROR]: The tests only verify API presence via compilation and do not validate coordinator affinity across pages, default and custom policy eligibility, preferred-target ordering and suppression, retry winner updates, continuation lifecycle, raw PagingState compatibility, or preservation of request behavior.

3. Tests Focus on Behavior [OK]: Tests do not enforce internal implementation details, but they need observable behavioral assertions.

4. Sanity Check [OK]: Patch appears coherent and executable; the base filter should remain stable.
