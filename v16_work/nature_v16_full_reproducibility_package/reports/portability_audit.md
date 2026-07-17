# Portability audit
- Scanned execution-critical source (.py, .sh, .lean, .mns, manuscript .md/.tex,
  Makefile) for forbidden absolute user paths (/home/user, /mnt/data, /Users/):
  **none found** (verified by verify_package.py).
- The manuscript renderer references the system font dir /usr/share/fonts/...
  (a standard, distro-portable Linux path), not a user-specific path.
- Figure references in manuscripts are package-relative (../source_figures/...).
- Recurrence/experiment code resolves paths from the script location or --out.
