-- ranks country origins of bands
-- ordered by the number of (non-unique) fans

CREATE INDEX idx_name_first ON names (name(1));
