// Provisioning only: keep all measured API client limits unchanged.
import { pool } from '../src/infrastructure/db.js';
pool.options.statement_timeout = 60000;
await import('../scripts/seed.js');
