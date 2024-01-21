-- Create organisms table
CREATE TABLE organisms (
  id INTEGER PRIMARY KEY,
  name VARCHAR,
  GCF VARCHAR
);

-- Create mi_grids table with foreign key constraint
CREATE TABLE mi_grids (
  id INTEGER PRIMARY KEY,
  mi_grid BLOB,
  organism_id INTEGER REFERENCES organisms(id),
  epsilon_size REAL
);

-- Create chr_whole_results table with foreign key constraint
CREATE TABLE chr_whole_results (
  id INTEGER PRIMARY KEY,
  organism_id INTEGER REFERENCES organisms(id),
  Dq_values REAL[],
  tau_q_values REAL[],
  DDq REAL
);

-- Create chr_region_results table with foreign key constraint
CREATE TABLE chr_region_results (
  id INTEGER PRIMARY KEY,
  regions_number INTEGER,
  organism_id INTEGER REFERENCES organisms(id),
  Dq_values REAL[],
  tau_q_values REAL[],
  DDq REAL
);
