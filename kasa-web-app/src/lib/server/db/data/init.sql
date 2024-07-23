-- Create the SmartDevice table
CREATE TABLE IF NOT EXISTS SmartDevice (
  host TEXT PRIMARY KEY,
  deviceType INTEGER NOT NULL,
  deviceId TEXT NOT NULL,
  alias TEXT,
  mac TEXT NOT NULL,
  _state INTEGER NOT NULL,
  hasChildren INTEGER NOT NULL
);

-- Create the ChildDevice table
CREATE TABLE IF NOT EXISTS ChildDevice (
  parentId TEXT NOT NULL,
  mac TEXT NOT NULL,
  alias TEXT,
  _state INTEGER NOT NULL,
  FOREIGN KEY (parentId) REFERENCES SmartDevice(host) ON DELETE CASCADE
);
