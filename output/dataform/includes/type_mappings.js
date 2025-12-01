// Sybase to BigQuery type mappings
function mapSybaseType(sybaseType) {
  const mappings = {
    'INT': 'INT64',
    'INTEGER': 'INT64',
    'SMALLINT': 'INT64',
    'TINYINT': 'INT64',
    'BIGINT': 'INT64',
    'DECIMAL': 'NUMERIC',
    'NUMERIC': 'NUMERIC',
    'MONEY': 'NUMERIC(19,4)',
    'SMALLMONEY': 'NUMERIC(10,4)',
    'FLOAT': 'FLOAT64',
    'REAL': 'FLOAT64',
    'CHAR': 'STRING',
    'VARCHAR': 'STRING',
    'TEXT': 'STRING',
    'NCHAR': 'STRING',
    'NVARCHAR': 'STRING',
    'NTEXT': 'STRING',
    'DATETIME': 'TIMESTAMP',
    'SMALLDATETIME': 'TIMESTAMP',
    'DATE': 'DATE',
    'TIME': 'TIME',
    'BIT': 'BOOL',
    'BINARY': 'BYTES',
    'VARBINARY': 'BYTES',
    'IMAGE': 'BYTES'
  };
  
  return mappings[sybaseType.toUpperCase()] || 'STRING';
}

module.exports = { mapSybaseType };
