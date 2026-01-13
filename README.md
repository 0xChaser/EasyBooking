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
root@ba3d2114f0e7:/app# pytest --cov
============================================================================================================ test session starts =============================================================================================================
platform linux -- Python 3.12.11, pytest-9.0.2, pluggy-1.6.0
benchmark: 5.2.3 (defaults: timer=time.perf_counter disable_gc=False min_rounds=5 min_time=0.000005 max_time=1.0 calibration_precision=10 warmup=False warmup_iterations=100000)
rootdir: /app
configfile: pyproject.toml
testpaths: tests
plugins: Faker-40.1.0, anyio-4.12.1, xdist-3.8.0, monitor-1.6.6, cov-7.0.0, benchmark-5.2.3, asyncio-1.3.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 144 items

tests/auth/test_auth.py ......                                                                                                                                                                                                         [  4%]
tests/daos/test_booking.py ...                                                                                                                                                                                                         [  6%]
tests/daos/test_room.py ...                                                                                                                                                                                                            [  8%]
tests/daos/test_user.py ...                                                                                                                                                                                                            [ 10%]
tests/exceptions/test_auth.py ............                                                                                                                                                                                             [ 18%]
tests/exceptions/test_base.py ...                                                                                                                                                                                                      [ 20%]
tests/exceptions/test_booking.py .....                                                                                                                                                                                                 [ 24%]
tests/exceptions/test_room.py .....                                                                                                                                                                                                    [ 27%]
tests/exceptions/test_user.py .....                                                                                                                                                                                                    [ 31%]
tests/integration/test_auth_workflows.py .......                                                                                                                                                                                       [ 36%]
tests/integration/test_workflows.py ..............                                                                                                                                                                                     [ 45%]
tests/performance/test_services_performance.py ..................                                                                                                                                                                      [ 58%]
tests/routers/test_auth.py .............                                                                                                                                                                                               [ 67%]
tests/routers/test_booking.py .......                                                                                                                                                                                                  [ 72%]
tests/routers/test_room.py ........                                                                                                                                                                                                    [ 77%]
tests/routers/test_user.py ....                                                                                                                                                                                                        [ 80%]
tests/services/test_booking.py .........                                                                                                                                                                                               [ 86%]
tests/services/test_room.py .........                                                                                                                                                                                                  [ 93%]
tests/services/test_user.py ..........                                                                                                                                                                                                 [100%]

============================================================================================================== warnings summary ==============================================================================================================
tests/auth/test_auth.py::TestAuthBackend::test_bearer_transport_scheme_name
  tests/auth/test_auth.py:12: PytestWarning: The test <Function test_bearer_transport_scheme_name> is marked with '@pytest.mark.asyncio' but it is not an async function. Please remove the asyncio mark. If the test is not marked explicitly, check for global marks applied via 'pytestmark'.
    def test_bearer_transport_scheme_name(self):

tests/auth/test_auth.py::TestAuthBackend::test_get_jwt_strategy_returns_jwt_strategy
  tests/auth/test_auth.py:15: PytestWarning: The test <Function test_get_jwt_strategy_returns_jwt_strategy> is marked with '@pytest.mark.asyncio' but it is not an async function. Please remove the asyncio mark. If the test is not marked explicitly, check for global marks applied via 'pytestmark'.
    def test_get_jwt_strategy_returns_jwt_strategy(self):

tests/auth/test_auth.py::TestAuthBackend::test_auth_backend_configuration
  tests/auth/test_auth.py:21: PytestWarning: The test <Function test_auth_backend_configuration> is marked with '@pytest.mark.asyncio' but it is not an async function. Please remove the asyncio mark. If the test is not marked explicitly, check for global marks applied via 'pytestmark'.
    def test_auth_backend_configuration(self):

tests/auth/test_auth.py::TestAuthBackend::test_auth_backend_strategy_getter
  tests/auth/test_auth.py:44: PytestWarning: The test <Function test_auth_backend_strategy_getter> is marked with '@pytest.mark.asyncio' but it is not an async function. Please remove the asyncio mark. If the test is not marked explicitly, check for global marks applied via 'pytestmark'.
    def test_auth_backend_strategy_getter(self):

tests/daos/test_booking.py: 3 warnings
tests/daos/test_room.py: 3 warnings
tests/daos/test_user.py: 3 warnings
tests/exceptions/test_auth.py: 12 warnings
tests/exceptions/test_base.py: 3 warnings
tests/exceptions/test_booking.py: 5 warnings
tests/exceptions/test_room.py: 5 warnings
tests/exceptions/test_user.py: 5 warnings
tests/integration/test_auth_workflows.py: 7 warnings
tests/integration/test_workflows.py: 14 warnings
tests/performance/test_services_performance.py: 18 warnings
tests/routers/test_auth.py: 13 warnings
tests/routers/test_booking.py: 7 warnings
tests/routers/test_room.py: 8 warnings
tests/routers/test_user.py: 4 warnings
tests/services/test_booking.py: 9 warnings
tests/services/test_room.py: 9 warnings
tests/services/test_user.py: 10 warnings
  /usr/local/lib/python3.12/multiprocessing/popen_fork.py:66: DeprecationWarning: This process (pid=8730) is multi-threaded, use of fork() may lead to deadlocks in the child.
    self.pid = os.fork()

tests/exceptions/test_auth.py: 11 warnings
tests/integration/test_auth_workflows.py: 9 warnings
tests/routers/test_auth.py: 16 warnings
  /usr/local/lib/python3.12/site-packages/sqlalchemy/sql/schema.py:3624: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
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
src/easy_booking/daos/booking.py                    49      0   100%
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
src/easy_booking/services/booking.py                55      1    98%
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
tests/integration/test_workflows.py                272      0   100%
tests/performance/test_services_performance.py     396     48    88%
tests/routers/__init__.py                            0      0   100%
tests/routers/test_auth.py                         132      0   100%
tests/routers/test_booking.py                      104      0   100%
tests/routers/test_room.py                         100      0   100%
tests/routers/test_user.py                          42      0   100%
tests/services/__init__.py                           0      0   100%
tests/services/test_booking.py                     137      0   100%
tests/services/test_room.py                         90      0   100%
tests/services/test_user.py                        115      0   100%
tests/utils/__init__.py                              0      0   100%
tests/utils/fake_data_generator.py                  79     34    57%
--------------------------------------------------------------------
TOTAL                                             2904    115    96%

------------------------------------------------------------------------------------------------------------ benchmark: 18 tests -------------------------------------------------------------------------------------------------------------
Name (time in us)                                        Min                     Max                   Mean                 StdDev                 Median                    IQR            Outliers         OPS            Rounds  Iterations
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
test_get_room_by_id_performance                     537.6240 (1.0)        1,054.4140 (1.01)        626.2032 (1.0)          65.7883 (1.0)         605.1030 (1.0)          79.4170 (1.39)       128;17  1,596.9257 (1.0)         534           1
test_get_user_by_id_performance                     566.8320 (1.05)       1,046.4560 (1.0)         685.7413 (1.10)         85.1803 (1.29)        665.1650 (1.10)        105.2500 (1.84)       178;15  1,458.2758 (0.91)        566           1
test_delete_room_performance                        873.7900 (1.63)       1,981.6620 (1.89)        946.8645 (1.51)        157.4493 (2.39)        913.1230 (1.51)         57.3340 (1.0)           1;4  1,056.1174 (0.66)         50           1
test_get_all_rooms_performance                    1,010.4140 (1.88)       1,611.4130 (1.54)      1,115.8293 (1.78)        102.6979 (1.56)      1,073.2480 (1.77)        134.0625 (2.34)         68;8    896.1944 (0.56)        389           1
test_get_all_users_performance                    1,134.0390 (2.11)       2,296.9530 (2.19)      1,474.9072 (2.36)        208.4402 (3.17)      1,452.1220 (2.40)        295.2703 (5.15)         91;4    678.0088 (0.42)        241           1
test_delete_user_performance                      1,277.8300 (2.38)       3,977.6990 (3.80)      1,413.2575 (2.26)        384.9555 (5.85)      1,333.7050 (2.20)         78.9160 (1.38)          2;4    707.5851 (0.44)         50           1
test_create_room_performance                      1,310.4140 (2.44)       1,887.2870 (1.80)      1,468.6207 (2.35)        138.5520 (2.11)      1,427.7460 (2.36)        169.0305 (2.95)         35;6    680.9110 (0.43)        137           1
test_create_user_performance                      1,871.5790 (3.48)       4,707.7800 (4.50)      2,848.9202 (4.55)        724.6871 (11.02)     2,669.8275 (4.41)      1,005.5810 (17.54)        30;0    351.0102 (0.22)         82           1
test_get_booking_by_id_performance                2,320.8690 (4.32)      22,726.9060 (21.72)     4,342.8308 (6.94)      2,293.1794 (34.86)     3,919.8660 (6.48)      1,690.2772 (29.48)       38;30    230.2646 (0.14)        361           1
test_get_all_bookings_performance                 2,883.7440 (5.36)      14,650.0500 (14.00)     3,590.0819 (5.73)      1,504.6742 (22.87)     3,231.9510 (5.34)        198.5410 (3.46)        11;27    278.5452 (0.17)        206           1
test_delete_booking_performance                   3,620.0330 (6.73)       4,670.6980 (4.46)      3,848.2027 (6.15)        193.2306 (2.94)      3,805.0120 (6.29)        175.2490 (3.06)         10;3    259.8616 (0.16)         50           1
test_create_booking_performance                   4,457.2400 (8.29)       5,852.4440 (5.59)      4,873.2472 (7.78)        230.4752 (3.50)      4,847.0090 (8.01)        257.8320 (4.50)         16;3    205.2020 (0.13)         78           1
test_get_all_users_pagination_performance         4,624.8220 (8.60)       7,057.1920 (6.74)      5,417.6925 (8.65)        510.8636 (7.77)      5,396.7580 (8.92)        577.0820 (10.07)        33;6    184.5804 (0.12)        114           1
test_get_all_rooms_pagination_performance         4,847.9480 (9.02)       6,914.8170 (6.61)      5,420.6406 (8.66)        369.3739 (5.61)      5,353.3620 (8.85)        460.7380 (8.04)         30;4    184.4800 (0.12)        131           1
test_create_multiple_users_performance            9,793.4770 (18.22)     14,391.2580 (13.75)    10,884.9417 (17.38)       883.9657 (13.44)    10,547.6630 (17.43)       896.0390 (15.63)        13;3     91.8700 (0.06)         58           1
test_create_multiple_rooms_performance           10,732.6000 (19.96)     14,916.7570 (14.25)    12,192.6642 (19.47)     1,044.5201 (15.88)    11,993.6595 (19.82)     1,111.8730 (19.39)        14;3     82.0165 (0.05)         48           1
test_get_all_bookings_pagination_performance     26,150.7310 (48.64)     34,333.3360 (32.81)    27,603.4107 (44.08)     1,875.3118 (28.51)    26,900.8960 (44.46)       708.2688 (12.35)         4;5     36.2274 (0.02)         35           1
test_create_multiple_bookings_performance        67,084.0100 (124.78)   124,229.2940 (118.71)   82,294.3310 (131.42)   17,429.2793 (264.93)   77,258.5290 (127.68)   20,064.0167 (349.95)        2;1     12.1515 (0.01)         11           1
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Legend:
  Outliers: 1 Standard Deviation from Mean; 1.5 IQR (InterQuartile Range) from 1st Quartile and 3rd Quartile.
  OPS: Operations Per Second, computed as 1 / Mean
===================================================================================================== 144 passed, 178 warnings in 30.31s =====================================================================================================
root@ba3d2114f0e7:/app#
```