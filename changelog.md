# Changelog
## 2.0.1 (2022-11-17)
- Renamed *debot.py* to *csb_debot.py* in anticipation of generalising the debotting program.
## 2.0 (2022-11-17)
- Prepped for export to executable. User-friendly print statements added for general usage.
- Removed deprecated priority controls.
- Updated remaining priority control's conditionals to match desired purging criteria.
- Properly annotated everything so people can actually understand what I'm doing.
- Program now outputs both cleaned and rejected data for review.
## 1.1.1 (2022-11-06)
- Fixed *student_status()* to eliminate over-assigning the 'missing' status.
- Added *alt_student_status()* function as an alternative status checker. Currently have 9 entries that return different results between the two functions. Verifying why manually.
## 1.1 (2022-11-04)
- Added *student_status()* function to sort responses by undergrad/grad/both/missing.
## 1.0 (2022-11-03)
- Initial version
