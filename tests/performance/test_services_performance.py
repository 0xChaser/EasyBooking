"""
Performance tests for UserService, RoomService and BookingService using pytest-benchmark.

pytest-benchmark is synchronous by default, so we use asyncio.run() or
event_loop.run_until_complete() to execute async functions within benchmarks.

Run with:
    pytest tests/performance/test_services_performance.py --benchmark-only -v

Note: pytest-benchmark should NOT be run with pytest-xdist (-n auto) as
benchmarks need to run serially for accurate timing measurements.
"""
import asyncio
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from easy_booking.services.user import UserService
from easy_booking.services.room import RoomService
from easy_booking.services.booking import BookingService
from easy_booking.daos.user import UserDao
from easy_booking.daos.room import RoomDao
from easy_booking.daos.booking import BookingDao
from easy_booking.models.base import Base
from tests.utils.fake_data_generator import FakeDataGenerator


@pytest.fixture(scope="function")
def perf_event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def perf_engine(perf_event_loop):
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False,
    )
    
    async def setup_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    perf_event_loop.run_until_complete(setup_db())
    yield engine
    
    async def teardown_db():
        await engine.dispose()
    
    perf_event_loop.run_until_complete(teardown_db())


@pytest.fixture(scope="function")
def perf_session_factory(perf_engine):
    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=perf_engine,
        expire_on_commit=False,
    )


class TestUserServicePerformance:

    def test_create_user_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark the time it takes to create a single user.
        
        This measures the full cycle of:
        - Generating fake user data
        - Creating the user via UserDao
        - Database commit
        """
        async def create_user():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                data = FakeDataGenerator.fake_user()
                user = await user_dao.create(data)
                return user

        def run_create_user():
            return perf_event_loop.run_until_complete(create_user())

        result = benchmark(run_create_user)
        assert result is not None
        assert result.id is not None

    def test_get_all_users_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark retrieving a page of users (10 users from a set of 50).
        
        This measures:
        - Database query for paginated results
        - Count query for total
        - Pydantic model validation
        """
        async def setup_users():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                for _ in range(50):
                    await user_dao.create(FakeDataGenerator.fake_user())

        perf_event_loop.run_until_complete(setup_users())

        async def get_users():
            async with perf_session_factory() as session:
                return await UserService.get_all(0, 10, session)

        def run_get_users():
            return perf_event_loop.run_until_complete(get_users())

        result = benchmark(run_get_users)
        assert result is not None
        assert result.total == 50
        assert len(result.items) == 10

    def test_get_user_by_id_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark retrieving a single user by ID.
        
        This measures the time to fetch one specific user from the database.
        """
        created_user_id = None

        async def setup_user():
            nonlocal created_user_id
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                data = FakeDataGenerator.fake_user()
                user = await user_dao.create(data)
                created_user_id = user.id

        perf_event_loop.run_until_complete(setup_user())

        async def get_user():
            async with perf_session_factory() as session:
                return await UserService.get_user_by_id(created_user_id, session)

        def run_get_user():
            return perf_event_loop.run_until_complete(get_user())

        result = benchmark(run_get_user)
        assert result is not None
        assert result.id == created_user_id

    def test_delete_user_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark deleting a user by ID.
        
        Note: This test creates a new user before each benchmark iteration
        since the user is deleted during the benchmark.
        """
        created_user_ids = []

        async def setup_users_for_deletion():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                for _ in range(100):
                    data = FakeDataGenerator.fake_user()
                    user = await user_dao.create(data)
                    created_user_ids.append(user.id)

        perf_event_loop.run_until_complete(setup_users_for_deletion())

        iteration = [0]

        async def delete_user():
            if iteration[0] < len(created_user_ids):
                user_id = created_user_ids[iteration[0]]
                iteration[0] += 1
                async with perf_session_factory() as session:
                    return await UserService.delete_by_id(user_id, session)
            return None

        def run_delete_user():
            return perf_event_loop.run_until_complete(delete_user())

        result = benchmark.pedantic(run_delete_user, iterations=1, rounds=50)


class TestUserServiceBulkPerformance:

    def test_create_multiple_users_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark creating 10 users in sequence.
        
        This measures the overhead of multiple sequential database operations.
        """
        async def create_multiple_users():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                users = []
                for _ in range(10):
                    data = FakeDataGenerator.fake_user()
                    user = await user_dao.create(data)
                    users.append(user)
                return users

        def run_create_multiple():
            return perf_event_loop.run_until_complete(create_multiple_users())

        result = benchmark(run_create_multiple)
        assert len(result) == 10

    def test_get_all_users_pagination_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark pagination through a larger dataset.
        
        This creates 100 users and retrieves them in pages of 20.
        """
        async def setup_many_users():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                for _ in range(100):
                    await user_dao.create(FakeDataGenerator.fake_user())

        perf_event_loop.run_until_complete(setup_many_users())

        async def paginate_users():
            results = []
            async with perf_session_factory() as session:
                for offset in range(0, 100, 20):
                    page = await UserService.get_all(offset, 20, session)
                    results.append(page)
            return results

        def run_pagination():
            return perf_event_loop.run_until_complete(paginate_users())

        result = benchmark(run_pagination)
        assert len(result) == 5


class TestRoomServicePerformance:

    def test_create_room_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark the time it takes to create a single room.
        """
        async def create_room():
            async with perf_session_factory() as session:
                room_dao = RoomDao(session)
                data = FakeDataGenerator.fake_room()
                room = await room_dao.create(data)
                return room

        def run_create_room():
            return perf_event_loop.run_until_complete(create_room())

        result = benchmark(run_create_room)
        assert result is not None
        assert result.id is not None

    def test_get_all_rooms_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark retrieving a page of rooms (10 rooms from a set of 50).
        """
        async def setup_rooms():
            async with perf_session_factory() as session:
                room_dao = RoomDao(session)
                for _ in range(50):
                    await room_dao.create(FakeDataGenerator.fake_room())

        perf_event_loop.run_until_complete(setup_rooms())

        async def get_rooms():
            async with perf_session_factory() as session:
                return await RoomService.get_all_room(0, 10, session)

        def run_get_rooms():
            return perf_event_loop.run_until_complete(get_rooms())

        result = benchmark(run_get_rooms)
        assert result is not None
        assert result.total == 50
        assert len(result.items) == 10

    def test_get_room_by_id_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark retrieving a single room by ID.
        """
        created_room_id = None

        async def setup_room():
            nonlocal created_room_id
            async with perf_session_factory() as session:
                room_dao = RoomDao(session)
                data = FakeDataGenerator.fake_room()
                room = await room_dao.create(data)
                created_room_id = room.id

        perf_event_loop.run_until_complete(setup_room())

        async def get_room():
            async with perf_session_factory() as session:
                return await RoomService.get_by_id(created_room_id, session)

        def run_get_room():
            return perf_event_loop.run_until_complete(get_room())

        result = benchmark(run_get_room)
        assert result is not None
        assert result.id == created_room_id

    def test_delete_room_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark deleting a room by ID.
        """
        created_room_ids = []

        async def setup_rooms_for_deletion():
            async with perf_session_factory() as session:
                room_dao = RoomDao(session)
                for _ in range(100):
                    data = FakeDataGenerator.fake_room()
                    room = await room_dao.create(data)
                    created_room_ids.append(room.id)

        perf_event_loop.run_until_complete(setup_rooms_for_deletion())

        iteration = [0]

        async def delete_room():
            if iteration[0] < len(created_room_ids):
                room_id = created_room_ids[iteration[0]]
                iteration[0] += 1
                async with perf_session_factory() as session:
                    return await RoomService.delete_by_id(room_id, session)
            return None

        def run_delete_room():
            return perf_event_loop.run_until_complete(delete_room())

        benchmark.pedantic(run_delete_room, iterations=1, rounds=50)


# ROOM SERVICE PERFORMANCE TESTS
class TestRoomServiceBulkPerformance:

    def test_create_multiple_rooms_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark creating 10 rooms in sequence.
        """
        async def create_multiple_rooms():
            async with perf_session_factory() as session:
                room_dao = RoomDao(session)
                rooms = []
                for _ in range(10):
                    data = FakeDataGenerator.fake_room()
                    room = await room_dao.create(data)
                    rooms.append(room)
                return rooms

        def run_create_multiple():
            return perf_event_loop.run_until_complete(create_multiple_rooms())

        result = benchmark(run_create_multiple)
        assert len(result) == 10

    def test_get_all_rooms_pagination_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark pagination through a larger dataset of rooms.
        """
        async def setup_many_rooms():
            async with perf_session_factory() as session:
                room_dao = RoomDao(session)
                for _ in range(100):
                    await room_dao.create(FakeDataGenerator.fake_room())

        perf_event_loop.run_until_complete(setup_many_rooms())

        async def paginate_rooms():
            results = []
            async with perf_session_factory() as session:
                for offset in range(0, 100, 20):
                    page = await RoomService.get_all_room(offset, 20, session)
                    results.append(page)
            return results

        def run_pagination():
            return perf_event_loop.run_until_complete(paginate_rooms())

        result = benchmark(run_pagination)
        assert len(result) == 5

# BOOKING SERVICE PERFORMANCE TESTS

class TestBookingServicePerformance:

    def test_create_booking_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark the time it takes to create a single booking.
        
        This requires creating a user and room first (as foreign keys).
        """
        user_id = None
        room_id = None

        async def setup_dependencies():
            nonlocal user_id, room_id
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                room_dao = RoomDao(session)
                user = await user_dao.create(FakeDataGenerator.fake_user())
                room = await room_dao.create(FakeDataGenerator.fake_room())
                user_id = user.id
                room_id = room.id

        perf_event_loop.run_until_complete(setup_dependencies())

        async def create_booking():
            async with perf_session_factory() as session:
                booking_in = FakeDataGenerator.fake_booking_in({"room_id": room_id})
                booking = await BookingService.add_booking(booking_in, session, user_id)
                return booking

        def run_create_booking():
            return perf_event_loop.run_until_complete(create_booking())

        result = benchmark(run_create_booking)
        assert result is not None
        assert result.id is not None

    def test_get_all_bookings_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark retrieving a page of bookings (10 bookings from a set of 50).
        """
        async def setup_bookings():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                room_dao = RoomDao(session)
                booking_dao = BookingDao(session)
                
                users = []
                rooms = []
                for _ in range(10):
                    user = await user_dao.create(FakeDataGenerator.fake_user())
                    room = await room_dao.create(FakeDataGenerator.fake_room())
                    users.append(user)
                    rooms.append(room)
                
                for i in range(50):
                    user = users[i % len(users)]
                    room = rooms[i % len(rooms)]
                    booking_data = FakeDataGenerator.fake_booking_data(user.id, room.id)
                    await booking_dao.create(booking_data)

        perf_event_loop.run_until_complete(setup_bookings())

        async def get_bookings():
            async with perf_session_factory() as session:
                return await BookingService.get_all_booking(0, 10, session)

        def run_get_bookings():
            return perf_event_loop.run_until_complete(get_bookings())

        result = benchmark(run_get_bookings)
        assert result is not None
        assert result.total == 50
        assert len(result.items) == 10

    def test_get_booking_by_id_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark retrieving a single booking by ID (includes eager loading of user and room).
        """
        created_booking_id = None

        async def setup_booking():
            nonlocal created_booking_id
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                room_dao = RoomDao(session)
                booking_dao = BookingDao(session)
                
                user = await user_dao.create(FakeDataGenerator.fake_user())
                room = await room_dao.create(FakeDataGenerator.fake_room())
                booking_data = FakeDataGenerator.fake_booking_data(user.id, room.id)
                booking = await booking_dao.create(booking_data)
                created_booking_id = booking.id

        perf_event_loop.run_until_complete(setup_booking())

        async def get_booking():
            async with perf_session_factory() as session:
                return await BookingService.get_by_id(created_booking_id, session)

        def run_get_booking():
            return perf_event_loop.run_until_complete(get_booking())

        result = benchmark(run_get_booking)
        assert result is not None
        assert result.id == created_booking_id

    def test_delete_booking_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark deleting a booking by ID.
        """
        created_booking_ids = []

        async def setup_bookings_for_deletion():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                room_dao = RoomDao(session)
                booking_dao = BookingDao(session)
                
                users = []
                rooms = []
                for _ in range(10):
                    user = await user_dao.create(FakeDataGenerator.fake_user())
                    room = await room_dao.create(FakeDataGenerator.fake_room())
                    users.append(user)
                    rooms.append(room)
                
                for i in range(100):
                    user = users[i % len(users)]
                    room = rooms[i % len(rooms)]
                    booking_data = FakeDataGenerator.fake_booking_data(user.id, room.id)
                    booking = await booking_dao.create(booking_data)
                    created_booking_ids.append(booking.id)

        perf_event_loop.run_until_complete(setup_bookings_for_deletion())

        iteration = [0]

        async def delete_booking():
            if iteration[0] < len(created_booking_ids):
                booking_id = created_booking_ids[iteration[0]]
                iteration[0] += 1
                async with perf_session_factory() as session:
                    return await BookingService.delete_by_id(booking_id, session)
            return None

        def run_delete_booking():
            return perf_event_loop.run_until_complete(delete_booking())

        benchmark.pedantic(run_delete_booking, iterations=1, rounds=50)


class TestBookingServiceBulkPerformance:

    def test_create_multiple_bookings_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark creating 10 bookings in sequence.
        """
        user_ids = []
        room_ids = []

        async def setup_dependencies():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                room_dao = RoomDao(session)
                for _ in range(10):
                    user = await user_dao.create(FakeDataGenerator.fake_user())
                    room = await room_dao.create(FakeDataGenerator.fake_room())
                    user_ids.append(user.id)
                    room_ids.append(room.id)

        perf_event_loop.run_until_complete(setup_dependencies())

        async def create_multiple_bookings():
            async with perf_session_factory() as session:
                bookings = []
                for i in range(10):
                    booking_in = FakeDataGenerator.fake_booking_in({"room_id": room_ids[i]})
                    booking = await BookingService.add_booking(booking_in, session, user_ids[i])
                    bookings.append(booking)
                return bookings

        def run_create_multiple():
            return perf_event_loop.run_until_complete(create_multiple_bookings())

        result = benchmark(run_create_multiple)
        assert len(result) == 10

    def test_get_all_bookings_pagination_performance(self, benchmark, perf_event_loop, perf_session_factory):
        """
        Benchmark pagination through a larger dataset of bookings.
        """
        async def setup_many_bookings():
            async with perf_session_factory() as session:
                user_dao = UserDao(session)
                room_dao = RoomDao(session)
                booking_dao = BookingDao(session)
                
                users = []
                rooms = []
                for _ in range(20):
                    user = await user_dao.create(FakeDataGenerator.fake_user())
                    room = await room_dao.create(FakeDataGenerator.fake_room())
                    users.append(user)
                    rooms.append(room)
                
                for i in range(100):
                    user = users[i % len(users)]
                    room = rooms[i % len(rooms)]
                    booking_data = FakeDataGenerator.fake_booking_data(user.id, room.id)
                    await booking_dao.create(booking_data)

        perf_event_loop.run_until_complete(setup_many_bookings())

        async def paginate_bookings():
            results = []
            async with perf_session_factory() as session:
                for offset in range(0, 100, 20):
                    page = await BookingService.get_all_booking(offset, 20, session)
                    results.append(page)
            return results

        def run_pagination():
            return perf_event_loop.run_until_complete(paginate_bookings())

        result = benchmark(run_pagination)
        assert len(result) == 5
