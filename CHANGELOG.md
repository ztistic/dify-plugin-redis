# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-10-11

### Added

- Raw-key tools operating on the full key as-is: `set`, `get`, `del`, `exists`

### Changed

- Labels of existing tools renamed to `SET (namespaced)` / `GET (namespaced)` (identities `redis-set` / `redis-get` unchanged)
- Tool source files renamed: `set_namespaced.py` / `get_namespaced.py` / `delete.py`
- TTL parsing moved to `utils/redis_utils.parse_ttl`; falsy TTL now falls back to each tool's own policy (namespaced SET defaults to 60, raw SET means no expiry)

## [1.0.4] - 2026-10-10

### Added

- Unit tests with pytest (35 cases covering TTL parsing, connection factory, and tool logic)
- GitHub Actions workflow for manual plugin packaging (`.github/workflows/package.yml`)
- `minimum_dify_version: 1.14.2` in the manifest
- `requirements-dev.txt` for development dependencies
- Requirements and Installation sections in the README

### Changed

- Upgrade `dify_plugin` from `0.4.4` to `0.10.2`
- Upgrade `redis` from `3.5.3` to `8.1.0` (native cluster support)
- Rename tool source files to snake_case (`redis_set.py` / `redis_get.py`)
- Extract TTL parsing into a dedicated `_parse_ttl` function
- Rewrite `PRIVACY.md` to align with Dify marketplace privacy guidelines
- Use `REMOTE_INSTALL_URL` in `.env.example`
- Update README (version, requirements, key format, TLS note)
- Improve YAML descriptions (clearer `llm_description` for `name:key` composition and TTL `-1` semantics)
- Exclude `tests/` and `requirements-dev.txt` from the package via `.difyignore`

### Fixed

- `redis-get` returning an extra empty message (double yield)
- `redis-set` silently succeeding when required parameters were missing
- `redis-set` crashing on invalid TTL values
- Redis errors leaking raw exceptions in tool layer
- `TypeError` when `name`/`key` were passed as non-string values

### Removed

- Deprecated `redis-py-cluster` dependency
- Redundant `setuptools` dependency
- Unused `endpoint` and `storage` permissions in the manifest

## [1.0.3] - 2025-12-03

- Bump version

## [1.0.2] - 2025-09-07

- Add support for switching Redis databases

## [1.0.1] - 2025-06-07

- README fixes

## [1.0.0] - 2025-04-04

- Initial release: Redis SET and GET tools with single-node and cluster mode support
