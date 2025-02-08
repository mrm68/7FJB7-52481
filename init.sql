DO $$
BEGIN
   IF EXISTS (SELECT 1 FROM pg_database WHERE datname = 'example_db') THEN
      PERFORM pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'example_db';
      DROP DATABASE example_db;
   END IF;
   CREATE DATABASE example_db;
END
$$;
