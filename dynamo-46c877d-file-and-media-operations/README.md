# Locked Reel Recovery

This Dynamo task asks an agent to recover a short raw RGB24 inspection reel from a packetized video dump. The visible corpus contains compressed camera packets, a packet index with revision and CRC metadata, and an edit-decision log that must be reduced at a fixed lock clock.

The core challenge is point-in-time media reconstruction: the newest-looking packet or edit row is not always authoritative, corrupted packets must be ignored, same-rank packet ties have a line-number authority rule, delta-coded payloads depend on earlier reconstructed frames, inclusive 12 fps timecodes must be expanded correctly, and each sensor's stored orientation has to be converted back to display orientation.

Verification checks only the requested artifacts, `/app/recovered/reel.rgb` and `/app/recovered/manifest.json`. The verifier validates artifact type, manifest schema, dimensions, digest consistency, exact provenance sequence, and the deterministic raw-byte digest of the recovered locked reel.
