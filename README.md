# EasyBooking



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
=============================================================================================================== tests coverage ===============================================================================================================
______________________________________________________________________________________________ coverage: platform linux, python 3.12.11-final-0 ______________________________________________________________________________________________

Name                                             Stmts   Miss  Cover
--------------------------------------------------------------------
src/easy_booking/api/v1/__init__.py                  9      0   100%
src/easy_booking/api/v1/auth.py                     11      0   100%
src/easy_booking/api/v1/booking.py                  29      2    93%
src/easy_booking/api/v1/room.py                     26      1    96%
src/easy_booking/api/v1/user.py                     28      2    93%
src/easy_booking/auth/__init__.py                    0      0   100%
src/easy_booking/auth/auth.py                        6      1    83%
src/easy_booking/daos/base.py                       17      4    76%
src/easy_booking/daos/booking.py                    43      0   100%
src/easy_booking/daos/room.py                       39      0   100%
src/easy_booking/daos/user.py                       50      2    96%
src/easy_booking/db.py                               9      2    78%
src/easy_booking/dependencies.py                    12      3    75%
src/easy_booking/exceptions/__init__.py              1      0   100%
src/easy_booking/exceptions/base.py                 15      0   100%
src/easy_booking/exceptions/booking.py               9      0   100%
src/easy_booking/exceptions/cli.py                   2      0   100%
src/easy_booking/exceptions/room.py                  9      0   100%
src/easy_booking/exceptions/user.py                  9      0   100%
src/easy_booking/main.py                            15      2    87%
src/easy_booking/models/__init__.py                  3      0   100%
src/easy_booking/models/base.py                      3      0   100%
src/easy_booking/models/booking.py                  15      0   100%
src/easy_booking/models/room.py                     12      0   100%
src/easy_booking/models/user.py                     17      0   100%
src/easy_booking/schemas/booking.py                 20      0   100%
src/easy_booking/schemas/page.py                     8      0   100%
src/easy_booking/schemas/room.py                    13      0   100%
src/easy_booking/schemas/user.py                    30      0   100%
src/easy_booking/services/booking.py                45      0   100%
src/easy_booking/services/room.py                   42      0   100%
src/easy_booking/services/user.py                   51     10    80%
src/easy_booking/settings.py                        27      0   100%
src/easy_booking/utils.py                           23      2    91%
tests/__init__.py                                    0      0   100%
tests/conftest.py                                   66      3    95%
tests/daos/__init__.py                               0      0   100%
tests/daos/test_booking.py                          99      4    96%
tests/daos/test_room.py                             59      0   100%
tests/daos/test_user.py                             61      0   100%
tests/exceptions/__init__.py                         0      0   100%
tests/exceptions/test_base.py                       18      0   100%
tests/exceptions/test_booking.py                    34      0   100%
tests/exceptions/test_room.py                       34      0   100%
tests/exceptions/test_user.py                       34      0   100%
tests/integration/__init__.py                        0      0   100%
tests/integration/test_workflows.py                233      0   100%
tests/performance/test_services_performance.py     391     48    88%
tests/routers/__init__.py                            0      0   100%
tests/routers/test_booking.py                      104      0   100%
tests/routers/test_room.py                         100      0   100%
tests/routers/test_user.py                          42      0   100%
tests/services/__init__.py                           0      0   100%
tests/services/test_booking.py                     136      0   100%
tests/services/test_room.py                         90      0   100%
tests/services/test_user.py                        115      0   100%
tests/utils/__init__.py                              0      0   100%
tests/utils/fake_data_generator.py                  79     34    57%
--------------------------------------------------------------------
TOTAL                                             2343    120    95%

---------------------------------------------------------------------------------------------------------- benchmark: 18 tests ----------------------------------------------------------------------------------------------------------
Name (time in us)                                        Min                    Max                   Mean                StdDev                 Median                 IQR            Outliers         OPS            Rounds  Iterations
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_get_room_by_id_performance                     429.3260 (1.0)         767.6950 (1.0)         503.3848 (1.0)         30.6641 (1.0)         503.5740 (1.01)      17.1250 (1.0)       151;129  1,986.5517 (1.0)         782           1
test_get_user_by_id_performance                     431.7830 (1.01)      1,066.4390 (1.39)        513.6352 (1.02)        64.3978 (2.10)        496.1365 (1.0)       38.4370 (2.24)       103;85  1,946.9071 (0.98)        596           1
test_delete_room_performance                        685.7790 (1.60)      1,723.4690 (2.24)        826.0023 (1.64)       134.0476 (4.37)        808.0060 (1.63)      24.2900 (1.42)          2;9  1,210.6504 (0.61)         50           1
test_get_all_rooms_performance                      736.1110 (1.71)      1,174.9370 (1.53)        838.6519 (1.67)        65.4684 (2.14)        856.3590 (1.73)      91.9360 (5.37)        136;8  1,192.3898 (0.60)        452           1
test_get_all_users_performance                      776.4020 (1.81)      7,841.1890 (10.21)     1,002.7267 (1.99)       424.3511 (13.84)       914.8165 (1.84)     134.4560 (7.85)        15;21    997.2807 (0.50)        438           1
test_create_user_performance                        981.4820 (2.29)      1,620.5950 (2.11)      1,133.2918 (2.25)       102.6989 (3.35)      1,099.4800 (2.22)     123.9255 (7.24)         40;3    882.3853 (0.44)        139           1
test_create_room_performance                      1,012.5230 (2.36)      3,227.2740 (4.20)      1,240.6380 (2.46)       234.0820 (7.63)      1,163.1870 (2.34)     220.0277 (12.85)         8;3    806.0369 (0.41)        193           1
test_delete_user_performance                      1,126.1040 (2.62)      3,642.6830 (4.74)      1,397.6302 (2.78)       352.4506 (11.49)     1,390.3915 (2.80)     232.5370 (13.58)         2;1    715.4968 (0.36)         50           1
test_get_booking_by_id_performance                1,438.2240 (3.35)      2,324.2490 (3.03)      1,607.1474 (3.19)       142.1156 (4.63)      1,584.5340 (3.19)     263.5795 (15.39)       178;1    622.2205 (0.31)        472           1
test_delete_booking_performance                   1,855.3000 (4.32)      2,247.4590 (2.93)      1,930.6854 (3.84)        74.6716 (2.44)      1,904.8610 (3.84)      64.4150 (3.76)          6;3    517.9508 (0.26)         50           1
test_get_all_bookings_performance                 2,144.4190 (4.99)      2,988.2780 (3.89)      2,526.3865 (5.02)       125.5819 (4.10)      2,545.3490 (5.13)     109.3730 (6.39)        72;32    395.8222 (0.20)        274           1
test_create_booking_performance                   2,496.7040 (5.82)      3,663.1830 (4.77)      2,802.4007 (5.57)       214.2171 (6.99)      2,767.5740 (5.58)     217.2567 (12.69)       36;10    356.8369 (0.18)        175           1
test_get_all_rooms_pagination_performance         3,500.6860 (8.15)      5,598.3970 (7.29)      3,913.1251 (7.77)       368.8584 (12.03)     3,866.7205 (7.79)     387.1180 (22.61)        53;7    255.5502 (0.13)        206           1
test_get_all_users_pagination_performance         3,613.1010 (8.42)     12,548.9770 (16.35)     4,111.5688 (8.17)       915.0830 (29.84)     3,905.4490 (7.87)     424.7840 (24.80)       10;16    243.2162 (0.12)        192           1
test_create_multiple_users_performance            7,996.4780 (18.63)    14,152.5310 (18.44)     9,619.2060 (19.11)    1,254.3306 (40.91)     9,373.2440 (18.89)    890.2755 (51.99)        12;8    103.9587 (0.05)         60           1
test_create_multiple_rooms_performance            8,712.2570 (20.29)    10,755.4280 (14.01)     9,912.1882 (19.69)      541.9988 (17.68)    10,113.3970 (20.38)    450.2202 (26.29)        17;8    100.8859 (0.05)         61           1
test_get_all_bookings_pagination_performance     12,349.4820 (28.76)    52,290.5810 (68.11)    13,990.7140 (27.79)    4,828.2820 (157.46)   13,427.7530 (27.06)    926.3170 (54.09)         1;1     71.4760 (0.04)         66           1
test_create_multiple_bookings_performance        25,620.8630 (59.68)    32,676.9000 (42.56)    28,380.2377 (56.38)    1,621.3047 (52.87)    28,488.6430 (57.42)    847.2760 (49.48)       10;10     35.2358 (0.02)         33           1
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
===================================================================================================== 104 passed, 104 warnings in 17.77s =====================================================================================================
root@1306569e5fee:/app#
```