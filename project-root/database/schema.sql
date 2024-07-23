-- Database schema for the Discord music bot

CREATE TABLE server_settings (
  server_id BIGINT PRIMARY KEY,
  default_prefix VARCHAR(255) NOT NULL DEFAULT '!',
  default_source VARCHAR(255) NOT NULL DEFAULT 'youtube',
  allowed_sources VARCHAR(255) NOT NULL DEFAULT 'youtube,spotify,soundcloud'
);

CREATE TABLE playlists (
  server_id BIGINT NOT NULL,
  name VARCHAR(255) NOT NULL,
  songs TEXT NOT NULL,
  PRIMARY KEY (server_id, name)
);

-- Insert default server settings for new servers
CREATE OR REPLACE FUNCTION insert_default_server_settings()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.server_id NOT IN (SELECT server_id FROM server_settings) THEN
    INSERT INTO server_settings (server_id) VALUES (NEW.server_id);
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_default_server_settings
AFTER INSERT ON playlists
FOR EACH ROW
EXECUTE PROCEDURE insert_default_server_settings();