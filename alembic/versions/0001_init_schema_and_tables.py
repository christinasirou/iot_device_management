"""init schema and tables

Revision ID: 0001
Revises: 
Create Date: 2025-10-05
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from config import settings

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
	# Ensure schema exists
	schema = settings.db_schema
	op.execute(f"CREATE SCHEMA IF NOT EXISTS {schema}")

	# device_types
	op.create_table(
		'device_types',
		sa.Column('id', sa.Integer(), primary_key=True),
		sa.Column('name', sa.String(length=100), nullable=False),
		sa.Column('description', sa.Text()),
		sa.Column('manufacturer', sa.String(length=100)),
		sa.Column('model', sa.String(length=100)),
		sa.Column('is_active', sa.Boolean(), server_default=sa.text('true')),
		sa.Column('created_at', sa.DateTime(timezone=True)),
		sa.Column('updated_at', sa.DateTime(timezone=True)),
		schema=schema
	)
	op.create_index('ix_device_types_id', 'device_types', ['id'], unique=False, schema=schema)
	op.create_index('ix_device_types_name', 'device_types', ['name'], unique=False, schema=schema)

	# devices
	op.create_table(
		'devices',
		sa.Column('id', sa.Integer(), primary_key=True),
		sa.Column('name', sa.String(length=100), nullable=False),
		sa.Column('description', sa.Text()),
		sa.Column('location', sa.String(length=200)),
		sa.Column('latitude', sa.Float()),
		sa.Column('longitude', sa.Float()),
		sa.Column('is_active', sa.Boolean(), server_default=sa.text('true')),
		sa.Column('is_online', sa.Boolean(), server_default=sa.text('false')),
		sa.Column('last_seen', sa.DateTime(timezone=True)),
		sa.Column('device_type_id', sa.Integer(), sa.ForeignKey(f"{schema}.device_types.id")),
		sa.Column('created_at', sa.DateTime(timezone=True)),
		sa.Column('updated_at', sa.DateTime(timezone=True)),
		schema=schema
	)
	op.create_index('ix_devices_id', 'devices', ['id'], unique=True, schema=schema)
	op.create_index('ix_devices_name', 'devices', ['name'], unique=False, schema=schema)

	# sensors
	op.create_table(
		'sensors',
		sa.Column('id', sa.Integer(), primary_key=True),
		sa.Column('name', sa.String(length=100), nullable=False),
		sa.Column('sensor_id', sa.String(length=50), nullable=False, unique=True),
		sa.Column('sensor_type', sa.String(length=50), nullable=False),
		sa.Column('unit', sa.String(length=20)),
		sa.Column('min_value', sa.Float()),
		sa.Column('max_value', sa.Float()),
		sa.Column('is_active', sa.Boolean(), server_default=sa.text('true')),
		sa.Column('is_online', sa.Boolean(), server_default=sa.text('false')),
		sa.Column('last_reading', sa.DateTime(timezone=True)),
		sa.Column('device_id', sa.Integer(), sa.ForeignKey(f"{schema}.devices.id")),
		sa.Column('created_at', sa.DateTime(timezone=True)),
		sa.Column('updated_at', sa.DateTime(timezone=True)),
		schema=schema
	)
	op.create_index('ix_sensors_id', 'sensors', ['id'], unique=False, schema=schema)
	op.create_index('ix_sensors_name', 'sensors', ['name'], unique=False, schema=schema)
	op.create_index('ix_sensors_sensor_id', 'sensors', ['sensor_id'], unique=True, schema=schema)

	# sensor_data
	op.create_table(
		'sensor_data',
		sa.Column('id', sa.Integer(), primary_key=True),
		sa.Column('sensor_id', sa.Integer(), sa.ForeignKey(f"{schema}.sensors.id"), nullable=False),
		sa.Column('value', sa.Float(), nullable=False),
		sa.Column('unit', sa.String(length=20)),
		sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
		sa.Column('meta', sa.Text()),
		sa.Column('quality_score', sa.Float()),
		schema=schema
	)
	op.create_index('idx_sensor_timestamp', 'sensor_data', ['sensor_id','timestamp'], unique=False, schema=schema)
	op.create_index('idx_timestamp', 'sensor_data', ['timestamp'], unique=False, schema=schema)


def downgrade() -> None:
	schema = settings.db_schema
	op.drop_index('idx_timestamp', table_name='sensor_data', schema=schema)
	op.drop_index('idx_sensor_timestamp', table_name='sensor_data', schema=schema)
	op.drop_table('sensor_data', schema=schema)

	op.drop_index('ix_sensors_sensor_id', table_name='sensors', schema=schema)
	op.drop_index('ix_sensors_name', table_name='sensors', schema=schema)
	op.drop_index('ix_sensors_id', table_name='sensors', schema=schema)
	op.drop_table('sensors', schema=schema)

	op.drop_index('ix_devices_name', table_name='devices', schema=schema)
	op.drop_index('ix_devices_id', table_name='devices', schema=schema)
	op.drop_table('devices', schema=schema)

	op.drop_index('ix_device_types_name', table_name='device_types', schema=schema)
	op.drop_index('ix_device_types_id', table_name='device_types', schema=schema)
	op.drop_table('device_types', schema=schema)

