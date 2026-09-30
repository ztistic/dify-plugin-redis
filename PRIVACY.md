# Privacy Policy for Redis Plugin

**Last Updated: October 4, 2026**

## Overview

This privacy policy explains how the Redis Plugin for Dify ("the Plugin") handles
data when you use it to cache and retrieve values in your own Redis server.

## Data Collection

The Plugin does **not** collect, store, log, or transmit any personal data.

The Plugin only processes the following data during operation, solely to perform
its function:

1. **Connection credentials** (provided by you): Redis host, port, password,
   cluster flag, and database index — used only to connect to your Redis server,
   and stored in Dify's credential system.
2. **Cached data**: the keys and values you write (SET) and read (GET) — written
   to and read from your own Redis server only.

## Data Processing

- All data processing occurs within the Plugin's execution environment.
- Credentials are used only to establish a connection with your Redis server.
- Cached data is used only to fulfill the SET/GET operation you requested.
- The Plugin keeps no copy of any data after the operation completes.

## Data Storage

- The Plugin does not maintain any persistent storage of user data.
- Credentials are stored securely in your Dify environment.
- Cached data is stored only in your own Redis server.

## Third-party Services

The Plugin interacts only with your specified Redis server. **No data is sent to
any third-party service**, and the Plugin does not call any third-party API.

## Data Transmission

The Plugin connects to Redis over a standard TCP connection. By default, data
(including the password) is transmitted unencrypted. Use a TLS-enabled Redis or a
TLS proxy if your Redis server is remote or untrusted.

## Data Retention

- The Plugin does not retain user data beyond the duration of the task execution.
- Cached data remains in your Redis server according to the TTL you set (default
  60 seconds, or permanent with `-1`).

## User Rights

As a user, you have the right to:

- Know what data the Plugin processes
- Remove your credentials at any time
- Delete cached data in your Redis server at any time

## Contact

For questions about this policy or our data practices, open an issue in the
[Redis Plugin Repository](https://github.com/ztistic/dify-plugin-redis).
