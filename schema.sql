DROP TABLE IF EXISTS trips;

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record TEXT NOT NULL,
    starred INTEGER,
    deptdate TEXT NOT NULL,
    arrivdate DATE NOT NULL,
    carrier TEXT NOT NULL,
    flight TEXT NOT NULL,
    deptair TEXT NOT NULL,
    arrivair TEXT NOT NULL
);
