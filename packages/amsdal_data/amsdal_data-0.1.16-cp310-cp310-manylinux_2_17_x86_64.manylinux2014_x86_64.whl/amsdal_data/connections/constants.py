ICEBERG_ALIAS = 'iceberg'
SQLITE_ALIAS = 'sqlite'
SQLITE_STATE_ALIAS = 'sqlite-state'
POSTGRES_STATE_ALIAS = 'postgres-state'
SQLITE_HISTORICAL_ALIAS = 'sqlite-historical'
SQLITE_IMMUTABLE_ALIAS = 'sqlite-immutable'
POSTGRES_HISTORICAL_ALIAS = 'postgres-historical'
POSTGRES_IMMUTABLE_ALIAS = 'postgres-immutable'

CONNECTION_BACKEND_ALIASES: dict[str, str] = {
    ICEBERG_ALIAS: 'amsdal_data.connections.implementations.iceberg_history.IcebergHistoricalConnection',
    SQLITE_ALIAS: 'amsdal_data.connections.implementations.sqlite_state.SqliteStateConnection',
    SQLITE_STATE_ALIAS: 'amsdal_data.connections.implementations.sqlite_state.SqliteStateConnection',
    SQLITE_HISTORICAL_ALIAS: 'amsdal_data.connections.implementations.sqlite_history.SqliteHistoricalConnection',
    SQLITE_IMMUTABLE_ALIAS: ('amsdal_data.connections.implementations.sqlite_immutable.SqliteImmutableConnection'),
    POSTGRES_HISTORICAL_ALIAS: (
        'amsdal_data.connections.implementations.postgresql_history.PostgresHistoricalConnection'
    ),
    POSTGRES_STATE_ALIAS: ('amsdal_data.connections.implementations.postgresql_state.PostgresStateConnection'),
    POSTGRES_IMMUTABLE_ALIAS: (
        'amsdal_data.connections.implementations.postgresql_immutable.PostgresImmutableConnection'
    ),
}
