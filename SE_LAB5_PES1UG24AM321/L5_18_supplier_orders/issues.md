\# Issues Found and Fixed — supplier\_orders.py



\*\*Before:\*\* Pylint 2.41/10, Bandit 3 issues (1 High, 1 Medium, 1 Low), Flake8 4 issues

\*\*After:\*\* Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues



Line numbers refer to the original file (see `reports/before/`).



| Issue | Type | Line(s) | Description | Fix Approach |

|-------|------|---------|-------------|--------------|

| Shell injection (Bandit B605, High) | Security | 21 | `os.system()` passes the supplier name to the operating system shell, so a name like `Acme \& del \*.\*` would run a second, malicious command. | Replaced `os.system("echo ...")` with `print()`, which only displays text, and removed the unused `import os`. |

| SQL injection (Bandit B608, Medium) | Security / Bug | 11 | The INSERT query is built with `%` string formatting, so user text becomes part of the SQL. A supplier like `O'Brien Metals` crashes the query, and crafted input could change it. | Used a parameterised query with `?` placeholders and passed the values as a separate tuple, so SQLite always treats them as data. |

| try/except/pass (Bandit B110, Low) | Error handling | 27-28 | `except Exception: pass` silently hides every error, so a failed cleanup (or a bug) would never be noticed. | Catch only `sqlite3.Error` and print the error message so failures are visible. |

| Global variable order\_total (Pylint W0603) | Design | 6, 10, 12 | A global counter is modified inside a function with `global`. It is separate from the database, so it can drift out of sync with the real data and makes functions hard to test. | Removed the global. A new `order\_total(conn)` function calculates `SUM(quantity)` directly from the database. |

| Unused argument remarks (Pylint W0613) | Bug | 16 | `markReceived` accepts a `remarks` argument but never uses it, so delivery remarks are silently lost. | Added a `remarks` column to the table and saved the value in the UPDATE query. |

| Redefining conn from outer scope (Pylint W0621) | Design | 4, 9, 16, 24, 31 | A global `conn` is created when the file is imported, and every function parameter named `conn` shadows it, which is confusing. | Moved database creation into `create\_store()`, called from `main()`, and added an `if \_\_name\_\_ == "\_\_main\_\_":` guard. |

| camelCase function names (Pylint C0103) | Style | 9, 16, 20, 31 | Names like `placeOrder` break PEP 8, the Python naming convention, which uses snake\_case for functions. | Renamed to `place\_order`, `mark\_received`, `notify\_warehouse` and `pending\_count`, and updated the calls in `main()`. |

| Missing docstrings (Pylint C0114/C0116) | Documentation | 1, all functions | There is no description of what the module or any function does. | Added a module docstring and a one-line docstring to every function. |

| Lines too long (Flake8 E501) | Style | 5, 11, 32 | Lines of 87-122 characters exceed the 79-character PEP 8 limit and are hard to read. | Split the SQL strings across several lines inside brackets, since Python joins adjacent strings automatically. |

| Missing whitespace around operator (Flake8 E225) | Style | 12 | `order\_total+=quantity` has no spaces around `+=`. | Changed to `order\_total += quantity` (this line was later removed with the global variable). |

