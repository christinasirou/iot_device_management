from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.database import Base
from models.device import Device
from models.sensor import Sensor
from models.sensor_data import SensorData
from models.device_type import DeviceType
from config import settings
from sqlalchemy import text

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

"""Configure Alembic to use the runtime DB URL from settings."""
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
	fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
	"""Run migrations in 'offline' mode."""
	url = settings.database_url
	context.configure(
		url=url,
		target_metadata=target_metadata,
		literal_binds=True,
		compare_type=True,
		dialect_opts={"paramstyle": "named"},
	)

	with context.begin_transaction():
		context.run_migrations()


def run_migrations_online() -> None:
	"""Run migrations in 'online' mode.

	In this scenario we need to create an Engine
	and associate a connection with the context.

	"""
	configuration = config.get_section(config.config_ini_section, {})
	configuration["sqlalchemy.url"] = settings.database_url
	connectable = engine_from_config(
		configuration,
		prefix="sqlalchemy.",
		poolclass=pool.NullPool,
	)

	with connectable.connect() as connection:
		context.configure(
			connection=connection,
			target_metadata=target_metadata,
			compare_type=True,
		)

		with context.begin_transaction():
			context.run_migrations()


if context.is_offline_mode():
	run_migrations_offline()
else:
	run_migrations_online()
