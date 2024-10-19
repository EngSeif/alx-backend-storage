-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

CREATE INDEX idx_name_first_score ON names (name(1), score);
