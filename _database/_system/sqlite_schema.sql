CREATE TABLE nodes (
  entity TEXT NOT NULL,
  id TEXT NOT NULL,
  typed_path TEXT NOT NULL UNIQUE,
  title TEXT,
  build_status TEXT,
  markdown_path TEXT NOT NULL,
  dateien_file_count INTEGER DEFAULT 0,
  imported_source_count INTEGER DEFAULT 0,
  PRIMARY KEY (entity, id)
);

CREATE TABLE edges (
  source_entity TEXT NOT NULL,
  source_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  target_entity TEXT NOT NULL,
  target_id TEXT NOT NULL,
  field TEXT,
  raw_label TEXT,
  confidence TEXT,
  resolution_rule TEXT,
  legacy_path TEXT,
  original_source TEXT,
  original_relation TEXT,
  original_target TEXT,
  edge_cleaning TEXT,
  FOREIGN KEY (source_entity, source_id) REFERENCES nodes(entity, id),
  FOREIGN KEY (target_entity, target_id) REFERENCES nodes(entity, id)
);

CREATE TABLE edge_review (
  source TEXT,
  relation TEXT,
  target TEXT,
  review_reason TEXT,
  suggested_source TEXT,
  suggested_relation TEXT,
  suggested_target TEXT,
  field TEXT,
  raw_label TEXT,
  confidence TEXT,
  resolution_rule TEXT,
  legacy_path TEXT
);
