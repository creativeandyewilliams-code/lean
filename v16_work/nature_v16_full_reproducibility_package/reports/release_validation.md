# Release validation
- ZIP name: nature_v16_full_reproducibility_package.zip; root dir:
  nature_v16_full_reproducibility_package/ (exact).
- `unzip -t`: OK (no corrupt entries).
- Fresh extraction to a clean directory + `python3 verify_package.py`: **PASS**
  (required paths present; no broken symlinks; no forbidden absolute user paths;
  no sorry/admit/axiom-decl in .lean; no unapproved placeholders; Gate Zero
  crosswalk 12/12 exact with matching model/registry hashes; recurrence
  table/summary consistent; receiver second-generation success with 0 author
  repairs and formal>prose identity recovery; both manuscript PDFs render with
  >0 pages; MANIFEST.sha256 sample verified with 0 mismatches).
- package size ~16 MB unpacked; ZIP ~14 MB; 119 tracked files.
