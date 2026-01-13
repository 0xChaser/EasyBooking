# EasyBooking

## Links :

- Frontend : https://easybooking.flo-isk.fr
- Backend : https://easybooking-api.flo-isk.fr

### Frontend Technologies : 

- React
- Shadcn UI
- Tailwind CSS

### Backend Technologies: 

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- Uvicorn
- SQLite
- Bandit (for security analysis)
- Pytest (for unitary testing)
- Pytest Benchmark (for performance testing)
- Pytest xdist (for parallel testing)

### Useful Commands

- Run bandit :

    ```bash
    bandit -r src/
    ```

- Run pytest : 

    ```bash
    pytest
    ```

- Run pytest with coverage :

    ```bash
    pytest --cov
    ```

### Console Output Example

```console
root@ba3d2114f0e7:/app# pytest --cov
=============================================================================================================== tests coverage ===============================================================================================================
______________________________________________________________________________________________ coverage: platform linux, python 3.12.11-final-0 ______________________________________________________________________________________________

Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
src/easy_booking/api/v1/__init__.py                  9      0   100%
src/easy_booking/api/v1/auth.py                     11      0   100%
src/easy_booking/api/v1/booking.py                  29      1    97%
src/easy_booking/api/v1/room.py                     26      1    96%
src/easy_booking/api/v1/user.py                     28      1    96%
src/easy_booking/auth/__init__.py                    0      0   100%
src/easy_booking/auth/auth.py                        6      0   100%
src/easy_booking/daos/base.py                       17      4    76%
src/easy_booking/daos/booking.py                    53      0   100%
src/easy_booking/daos/room.py                       39      0   100%
src/easy_booking/daos/user.py                       50      2    96%
src/easy_booking/db.py                               9      2    78%
src/easy_booking/dependencies.py                    12      0   100%
src/easy_booking/exceptions/__init__.py              1      0   100%
src/easy_booking/exceptions/base.py                 19      0   100%
src/easy_booking/exceptions/booking.py               9      0   100%
src/easy_booking/exceptions/cli.py                   2      0   100%
src/easy_booking/exceptions/room.py                 13      0   100%
src/easy_booking/exceptions/user.py                  9      0   100%
src/easy_booking/main.py                            15      2    87%
src/easy_booking/models/__init__.py                  3      0   100%
src/easy_booking/models/base.py                      3      0   100%
src/easy_booking/models/booking.py                  22      0   100%
src/easy_booking/models/room.py                     18      0   100%
src/easy_booking/models/user.py                     17      0   100%
src/easy_booking/schemas/booking.py                 31      0   100%
src/easy_booking/schemas/page.py                     8      0   100%
src/easy_booking/schemas/room.py                    24      0   100%
src/easy_booking/schemas/user.py                    30      0   100%
src/easy_booking/services/booking.py                59      1    98%
src/easy_booking/services/room.py                   42      0   100%
src/easy_booking/services/user.py                   51     10    80%
src/easy_booking/settings.py                        27      0   100%
src/easy_booking/utils.py                           23      2    91%
tests/__init__.py                                    0      0   100%
tests/auth/__init__.py                               0      0   100%
tests/auth/test_auth.py                             36      0   100%
tests/conftest.py                                   66      3    95%
tests/daos/__init__.py                               0      0   100%
tests/daos/test_booking.py                          99      4    96%
tests/daos/test_room.py                             59      0   100%
tests/daos/test_user.py                             61      0   100%
tests/exceptions/__init__.py                         0      0   100%
tests/exceptions/test_auth.py                      101      0   100%
tests/exceptions/test_base.py                       18      0   100%
tests/exceptions/test_booking.py                    34      0   100%
tests/exceptions/test_room.py                       34      0   100%
tests/exceptions/test_user.py                       34      0   100%
tests/integration/__init__.py                        0      0   100%
tests/integration/test_auth_workflows.py           188      0   100%
tests/integration/test_workflows.py                287      0   100%
tests/performance/test_services_performance.py     396     48    88%
tests/routers/__init__.py                            0      0   100%
tests/routers/test_auth.py                         132      0   100%
tests/routers/test_booking.py                      129      0   100%
tests/routers/test_room.py                         100      0   100%
tests/routers/test_user.py                          42      0   100%
tests/services/__init__.py                           0      0   100%
tests/services/test_booking.py                     137      0   100%
tests/services/test_room.py                         90      0   100%
tests/services/test_user.py                        115      0   100%
tests/utils/__init__.py                              0      0   100%
tests/utils/fake_data_generator.py                  79     32    59%
--------------------------------------------------------------------
TOTAL                                             2952    113    96%

------------------------------------------------------------------------------------------------------------- benchmark: 18 tests -------------------------------------------------------------------------------------------------------------
Name (time in us)                                        Min                     Max                    Mean                 StdDev                 Median                    IQR            Outliers         OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_get_room_by_id_performance                     571.4390 (1.0)        1,038.9220 (1.0)          693.4122 (1.0)          93.8709 (1.0)         674.8930 (1.0)         144.0360 (1.0)         159;2  1,442.1437 (1.0)         498           1
test_get_user_by_id_performance                     621.1450 (1.09)       2,175.9240 (2.09)         794.4562 (1.15)        186.8577 (1.99)        728.9330 (1.08)        201.3260 (1.40)        34;13  1,258.7226 (0.87)        282           1
test_delete_room_performance                        967.2160 (1.69)      13,904.0990 (13.38)      1,655.3323 (2.39)      1,984.7516 (21.14)     1,147.3145 (1.70)        235.7830 (1.64)          2;8    604.1083 (0.42)         50           1
test_get_all_users_performance                    1,058.9210 (1.85)       2,098.2600 (2.02)       1,362.1549 (1.96)        163.3095 (1.74)      1,361.3270 (2.02)        216.6175 (1.50)         80;5    734.1309 (0.51)        276           1
test_get_all_rooms_performance                    1,103.1700 (1.93)       2,176.5910 (2.10)       1,318.5069 (1.90)        169.5315 (1.81)      1,294.2050 (1.92)        235.4512 (1.63)         92;6    758.4336 (0.53)        305           1
test_create_user_performance                      1,421.9920 (2.49)       2,931.6480 (2.82)       1,876.7580 (2.71)        299.3025 (3.19)      1,829.2270 (2.71)        342.9670 (2.38)         27;4    532.8337 (0.37)        101           1
test_create_room_performance                      1,484.4900 (2.60)       2,761.4880 (2.66)       1,746.2728 (2.52)        215.7676 (2.30)      1,694.8160 (2.51)        250.3985 (1.74)         30;5    572.6482 (0.40)        137           1
test_delete_user_performance                      1,641.9840 (2.87)       5,401.8960 (5.20)       2,045.1988 (2.95)        559.3637 (5.96)      1,866.1855 (2.77)        432.1100 (3.00)          3;1    488.9500 (0.34)         50           1
test_get_booking_by_id_performance                2,318.2110 (4.06)     253,481.5420 (243.99)     4,490.7259 (6.48)     14,574.2177 (155.26)    2,896.3570 (4.29)        810.9720 (5.63)         1;47    222.6811 (0.15)        299           1
test_get_all_bookings_performance                 3,510.0450 (6.14)       7,344.2860 (7.07)       4,422.1228 (6.38)        681.1179 (7.26)      4,274.3930 (6.33)        574.8973 (3.99)        36;12    226.1357 (0.16)        147           1
test_delete_booking_performance                   3,781.5770 (6.62)       5,927.5020 (5.71)       4,411.1462 (6.36)        523.7135 (5.58)      4,199.2495 (6.22)        654.3940 (4.54)         13;2    226.6984 (0.16)         50           1
test_get_all_users_pagination_performance         4,610.4220 (8.07)       7,051.3380 (6.79)       5,257.4974 (7.58)        472.6484 (5.04)      5,137.5300 (7.61)        384.9340 (2.67)        35;13    190.2046 (0.13)        141           1
test_create_booking_performance                   5,088.3640 (8.90)       8,018.3030 (7.72)       5,771.5483 (8.32)        520.0685 (5.54)      5,699.9055 (8.45)        668.6435 (4.64)         23;2    173.2637 (0.12)         76           1
test_get_all_rooms_pagination_performance         5,795.0480 (10.14)     15,185.0540 (14.62)      7,542.8253 (10.88)     1,675.0939 (17.84)     7,077.6905 (10.49)     1,352.0780 (9.39)         13;8    132.5763 (0.09)        114           1
test_create_multiple_users_performance           12,204.7830 (21.36)     24,768.6780 (23.84)     14,700.5572 (21.20)     2,556.8204 (27.24)    13,925.6820 (20.63)     2,338.0230 (16.23)         1;1     68.0246 (0.05)         24           1
test_create_multiple_rooms_performance           12,328.9450 (21.58)     16,399.4700 (15.79)     14,138.4197 (20.39)     1,075.8395 (11.46)    14,134.1745 (20.94)     1,695.8370 (11.77)        16;0     70.7293 (0.05)         48           1
test_get_all_bookings_pagination_performance     19,349.6180 (33.86)    142,327.8320 (137.00)    36,140.9461 (52.12)    24,100.8184 (256.74)   27,053.0570 (40.08)    15,101.9737 (104.85)        4;4     27.6694 (0.02)         43           1
test_create_multiple_bookings_performance        59,817.2490 (104.68)   218,382.5150 (210.20)   106,023.9144 (152.90)   42,906.7439 (457.08)   99,729.7750 (147.77)   56,367.1608 (391.34)        3;1      9.4318 (0.01)         13           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
===================================================================================================== 145 passed, 179 warnings in 35.05s =====================================================================================================
root@ba3d2114f0e7:/app#
```

```console
root@ba3d2114f0e7:/app# bandit -r src/
[main]	INFO	profile include tests: None
[main]	INFO	profile exclude tests: None
[main]	INFO	cli include tests: None
[main]	INFO	cli exclude tests: None
[main]	INFO	running on Python 3.12.11
Run started:2026-01-13 10:33:50.305257+00:00

Test results:
	No issues identified.

Code scanned:
	Total lines of code: 1026
	Total lines skipped (#nosec): 0

Run metrics:
	Total issues (by severity):
		Undefined: 0
		Low: 0
		Medium: 0
		High: 0
	Total issues (by confidence):
		Undefined: 0
		Low: 0
		Medium: 0
		High: 0
Files skipped (0):
root@ba3d2114f0e7:/app#
```
